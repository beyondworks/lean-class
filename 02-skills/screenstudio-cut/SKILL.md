---
name: screenstudio-cut
description: Cut-edit a Screen Studio (.screenstudio) project bundle non-destructively by editing project.json only. Removes long silences (>=1.8s by default), false starts, prefix repetitions, sentence-level repeats, and stutters detected from word-level Whisper transcripts. Preserves the original recording/, meta.json, recording-markers.json. Triggers on Korean phrases like "스크린스튜디오 더듬/중복/침묵 컷", "말 더듬는 부분 잘라줘", "이어붙여줘 자연스럽게", "screenstudio 컷 편집/트림", "false start 잘라줘", or explicit `/screenstudio-cut`. NEVER use for re-encoding, color grading, or any operation touching recording/.
argument-hint: "<bundle-path-or-name> [--language ko|en|auto] [--silence-min 1.8] [--whisper-model small|medium|large]"
allowed-tools: Bash, Read, Write, Edit
license: MIT
user-invocable: true
---

# screenstudio-cut — Word-level cut editor for Screen Studio bundles

Edits a `.screenstudio` project file by **rewriting `project.json` slices only**. The original `recording/` (HLS chunks, mp4, json events) is never touched. Screen Studio renders the new timeline from the same source files at open time.

This is **not** a video re-encoder. It is a JSON surgery tool guided by Whisper word timestamps.

---

## 0. When this skill applies

Trigger on any of these:

- User points at a `.screenstudio` bundle and asks to "컷 편집", "더듬 잘라줘", "trim stutters", "remove silences", "cut filler words", "말이 자연스럽게 이어지게 해줘", "false start 잘라줘"
- User says `/screenstudio-cut <path>`
- User asks to compress a Screen Studio recording's runtime by removing dead air

Do **not** trigger for: re-encoding, color grading, zoom/cursor effect tweaks, audio mixing, or anything that requires touching `recording/`. For those, edit `project.json` keys directly via the [project.json schema reference](docs/project-json-schema.md).

---

## 1. Pre-flight checklist (run silently; surface only failures)

```bash
# Required binaries
which ffmpeg ffprobe whisper >/dev/null || echo "MISSING:tools"
# Whisper model cache (avoid re-download)
ls ~/.cache/whisper/{small,medium,large}.pt 2>/dev/null
# Screen Studio app must NOT be running (auto-save would clobber edits)
pgrep -x "Screen Studio" >/dev/null && echo "WARN:app-running"
```

If `MISSING:tools` → tell the user to install:
```bash
brew install ffmpeg
pip3 install -U openai-whisper
```

If `WARN:app-running` → ask the user to **fully Quit** Screen Studio (⌘Q) before continuing. Do NOT proceed.

---

## 2. Bundle structure (what's inside)

```
<NAME>.screenstudio/
├── meta.json                 ← App version metadata. NEVER edit this.
├── project.json              ← THE ONLY FILE WE EDIT.
├── recording-markers.json    ← Usually [], leave alone.
└── recording/                ← Original recording. NEVER touch.
    ├── channel-1-system-audio-* (system audio, HLS)
    ├── channel-2-display-*      (screen capture, HLS)
    ├── channel-3-microphone-*   (microphone — primary speech source)
    ├── channel-4-webcam-*       (webcam, optional)
    ├── *.m3u8 + *.m4s           (HLS chunks)
    ├── channel-N-*.mp4          (per-channel concatenated mp4)
    ├── channel-N-*.m4a          (per-channel audio-only)
    ├── cursors/, cursors.json
    ├── mouseclicks-0.json, mousemoves-0.json, keystrokes-0.json
    ├── metadata.json (recorder config)
    └── polyrecorder.log
```

Speech-bearing channels in priority order:
1. `recording/channel-3-microphone-0.m4a` (preferred)
2. `recording/channel-3-microphone-0.mp4`
3. `recording/channel-1-system-audio-0.m4a` (fallback if no mic)

If neither exists, abort and tell the user this skill is for **voice-narrated** recordings only.

---

## 3. project.json — the only file you edit

Top-level shape:
```jsonc
{
  "json": {
    "id": "<10-char nanoid>",
    "name": "...",
    "createdAt": "...", "updatedAt": "...", "lastSavedAt": "...",
    "config": { ... global effects ... },
    "meta": { "recordingFlags": [] },
    "scenes": [
      {
        "id": "...",
        "name": "Default",
        "type": "recording",
        "sessionIndex": 0,
        "zoomRanges": [ /* zoom effects, source-time ms */ ],
        "slices":     [ /* THE TIMELINE — what we rewrite */ ],
        "layouts": [], "masks": [], "resolvedTypingSpeedIncreaseSuggestions": []
      }
    ]
  },
  "meta": { "values": { ... } }
}
```

**Slice shape** (each entry is a kept range from the source):
```jsonc
{
  "id": "<10-char id, alphanumeric>",
  "timeScale": 1,           // 1.0 = realtime; 0.5 = 2× slower; 2.0 = 2× faster
  "sourceStartMs": 0,       // start in source recording time (ms)
  "sourceEndMs": 956101.39, // end in source recording time (ms)
  "volume": 1, "systemAudioVolume": 1, "externalDeviceAudioVolume": 1,
  "hideCursor": false, "disableSmoothMouseMovement": false
}
```

**Cut editing = replace the single original slice with multiple slices that skip the cut regions.**

**Zoom shape** (do not move unless asked):
```jsonc
{
  "id": "...", "zoom": 1.7, "type": "follow-click-groups",
  "snapToEdgesRatio": 0.25, "manualTargetPoint": {"x":0.5,"y":0.5},
  "glideDirection": null, "glideSpeed": 0.5,
  "isDisabled": false,
  "startTime": 370210,    // SOURCE time, ms (NOT output time)
  "endTime":   373084,    // SOURCE time, ms
  "isSystem": false, "hasInstantAnimation": false
}
```

> **Time coordinate rule**: every time field in `project.json` is **source recording time in milliseconds**. Output (post-edit) time is implicit and is computed by walking `slices[]` in order. Screen Studio re-maps source time to output time at render. **You never write output time anywhere.**

---

## 4. The 7-step workflow

### Step 1. Resolve the bundle path AND classify the recording

Accept either a full path or a name (search `~/Screen Studio Projects/`). Verify directory exists, has `project.json` and `recording/`. Fail loudly otherwise.

**Then classify the recording** by inspecting `recording/mouseclicks-0.json`:

```bash
python3 -c "
import json
clicks = json.load(open('$BUNDLE/recording/mouseclicks-0.json'))
moves  = json.load(open('$BUNDLE/recording/mousemoves-0.json'))
import os
mb = os.path.getsize('$BUNDLE/recording/channel-3-microphone-0.m4a') / 1024 / 1024
print(f'clicks={len(clicks)} moves={len(moves)} mic_mb={mb:.1f}')
"
```

| Click count | Recording type | Implication for cuts |
|---|---|---|
| ≤ 10 | **Voice-led** (talking head, vlog) | Speech-driven cuts dominate. Filler/repeat detection is high-value. |
| 10–50 | **Mixed** | Both visual and verbal cuts. Watch for cuts spanning a click event (zoom auto-generated near clicks). |
| 50+ | **UI-led** (demo, tutorial) | Visual flow matters more. Be conservative on cuts near click bursts to preserve auto-zoom timing. |

If `clicks ≤ 10` AND mic file < 1 MB, audio is likely silent — abort with a message that this skill needs voice narration.

### Step 2. Pre-flight + back up

```bash
TS=$(date +%Y%m%dT%H%M%S)
SRC="<bundle>"
BAK="${SRC%.screenstudio}.backup-${TS}.screenstudio"
cp -R "$SRC" "$BAK"
echo "Backup: $BAK"
```

The backup is **mandatory**. Never edit without one. Record the path; report it to the user at the end.

### Step 3. Extract speech audio (16 kHz mono WAV)

```bash
WORK="<bundle parent>/.work-screenstudio-cut-${TS}"
mkdir -p "$WORK"
ffmpeg -hide_banner -loglevel error -y \
  -i "$SRC/recording/channel-3-microphone-0.m4a" \
  -ac 1 -ar 16000 \
  "$WORK/mic.wav"
```

Fall back to `channel-3-microphone-0.mp4` then `channel-1-system-audio-0.m4a` if the m4a is missing.

**Optional**: extract preview frames at 60s intervals so you can read screen content while reviewing the transcript. Useful for cuts that depend on what's on screen at the moment.
```bash
mkdir -p "$WORK/frames"
ffmpeg -hide_banner -loglevel error -y \
  -i "$SRC/recording/channel-2-display-0.mp4" \
  -vf "fps=1/60,scale=320:-1" -qscale:v 5 \
  "$WORK/frames/t%03d.jpg"
```

### Step 4. Run Whisper with word-level timestamps

**Default to `small` for any language.** It is dramatically faster than `medium` (~3-5× on M-series CPU) and handles Korean/English/Japanese reliably. Only escalate if the user reports transcription errors. Confirmed empirically: `medium` on a 16-min Korean recording took ~12 min CPU; `small` took ~8-10 min and produced equally usable word boundaries for cut decisions.

| Situation | Model |
|---|---|
| **Default** (any language) | `small` |
| User reports words missing or wrong language ID | `medium` |
| Heavy accent or domain-specific terms | `medium` |
| User explicitly asks for highest quality and accepts the wait | `large` |
| Pure clean English narration only | `base` (faster) |

```bash
whisper "$WORK/mic.wav" \
  --model small \
  --language Korean \
  --task transcribe \
  --output_format json \
  --word_timestamps True \
  --output_dir "$WORK" \
  --verbose False
```

**Important**: launch this with the Bash tool's `run_in_background: true`. Do **not** wrap in `nohup ... &` inside a foreground Bash call — the process group dies with the Bash invocation. (Confirmed failure mode 2026-05.)

A 16-minute Korean recording takes ~8-12 min on M-series CPU with `small`.

**Waiting strategy**:
- The Bash `run_in_background` task posts a `<task-notification>` when complete. Prefer waiting on that notification — it requires zero polling.
- If you must schedule active work for later, use `ScheduleWakeup` with `delaySeconds <= 270` to stay inside the 5-minute prompt cache window. Going past 300s makes the wake-up reload the conversation cold.
- While waiting, you may pre-compute `mouseclicks` distribution, extract preview frames, and study the existing `zoomRanges` so you know which cut regions to avoid.

Output: `$WORK/mic.json` with `segments[].words[].{start,end,word}`.

### Step 5. Analyze and propose cuts

Run [`scripts/analyze.py`](scripts/analyze.py):

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/analyze.py" \
  --whisper-json "$WORK/mic.json" \
  --silence-min 1.8 \
  --silence-keep-breath 0.4 \
  --prefix-min-words 2 \
  --output "$WORK/cuts_candidates.json" \
  --report "$WORK/analysis_report.txt"
```

The report contains four sections:
1. **Long silences** (gap ≥ `silence-min`)
2. **Standalone fillers** ("어", "음", "그", "근데", "막", "뭐", "이제", "약간")
3. **Prefix repetitions** (≥ N consecutive words repeating with a 0.4–8.0s break)
4. **Full transcript** (segment-by-segment, with timestamps)

**Critical: prefix repetition candidates have many false positives.** In a real Korean run we saw 11 candidates, only 4 were true false starts. The rest were legitimate phrase reuse across different sentences (e.g. `'젠스파크 클로를'` mentioned twice in successive paragraphs about the same topic). **Always inspect each candidate's `ctx_first` and `ctx_second`** before cutting. Heuristics for "true false start":
- The first instance ends with `...` or trails off (incomplete sentence)
- A silence ≥ 1.0s separates the two instances
- The second instance restarts with the same opening word (not just a shared phrase)

Whisper alone misses some patterns. **Read the full transcript top-to-bottom** and add cuts for:
- **Sentence-level repetition** ("이게 무료 티어를 쓸 때였는데 ... 이게 무료 티어를 쓸 때였는데" — same sentence twice across a pause). The analyzer's prefix detector won't catch this if the prefix is only 2 words and the sentence is much longer.
- **Mid-word stutters that read as two distinct words** ("사용...", "또 이...")
- **Word-pair stutters where a partial cut would leave the first instance audible** — see § 6 Mistake A.

Build the final cut list as `[(start_ms, end_ms, reason), ...]`.

### Step 6. Validate cuts BEFORE applying

For each candidate `(start, end)`:

| Check | Pass criterion |
|---|---|
| Range sanity | `0 ≤ start < end ≤ sourceEndMs` of original slice |
| Word boundaries | `start` ≤ end of last word kept; `end` ≥ start of first word resumed. Print the surrounding words. |
| Zoom overlap | No `zoomRange` such that `[zoom.startTime, zoom.endTime]` ∩ `[start, end]` ≠ ∅. If overlap → ask user whether to drop the zoom or shift it. |
| Stutter completeness | If cutting a false-start prefix, the **second occurrence's first word must start exactly at or after `end`**. If the first occurrence's words end before `end`, the cut covers the entire false start. |
| Breath margin | For pure silences, leave `silence-keep-breath` (default 0.4s) before the cut start. For false starts, leave 0s — cut to the resumed-word boundary. |

Print the resulting kept ranges with output-time mapping. Confirm with user **unless** the user explicitly told you to apply automatically.

### Step 7. Apply via [`scripts/apply_cuts.py`](scripts/apply_cuts.py)

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/apply_cuts.py" \
  --bundle "$SRC" \
  --cuts "$WORK/cuts_final.json"
```

The script:
1. Refuses to run if Screen Studio is open
2. Loads `project.json` (validates schema)
3. Sorts + merges overlapping cut ranges
4. Splits the original slice into kept ranges → new slices
5. Generates fresh 10-char alphanumeric IDs
6. Preserves all common slice fields (timeScale, volumes, hideCursor, etc.)
7. Writes back, then re-loads to verify JSON validity
8. Reports source/output durations, slice count, zoom-overlap status

Tell the user the backup path and the new output duration. Ask them to reopen the bundle in Screen Studio (⌘Q first, then double-click) and verify.

### Step 8. Iterate on user feedback (the most important step)

A single pass rarely catches every issue. Plan for **at least one revision round**.

When the user reports a residual issue:

1. **Disambiguate the timestamp**: ask once whether they're reading from the Screen Studio playback (output time) or the original recording (source time) — see § 7. If it's output time, convert.
2. **Restore from backup before re-applying**: do not stack cuts on top of partially-cut slices. Run `cp <backup>/project.json <bundle>/project.json` first, then re-build the entire cut list and re-apply. This prevents accumulated rounding errors and slice ID confusion.
3. **Re-load the saved `words.json`** (in `$WORK`) — do NOT re-run Whisper. The transcript is deterministic for the same audio.
4. **Check word boundaries explicitly** for the reported region: print every word in `[reported_t-3, reported_t+5]` so the cut is anchored to real word starts/ends.
5. **Show the cut delta to the user** before applying: "I'll replace cut #N `[A→B]` with `[A'→B']` because…"
6. **Re-run all cuts together**, never piecewise. Apply produces a fresh `slices[]` from scratch; partial application creates inconsistent state.

Rule of thumb: **the first pass should be conservative** (only cuts you're 100% sure are stutters/silences). Use the user's feedback to add aggressive cuts in pass 2+.

---

## 5. Guardrails (NEVER violate)

1. **Never edit `recording/` or any file in it.** It is the immutable source.
2. **Never edit `meta.json`.** Especially never raise `requiredVersion`.
3. **Never edit `recording-markers.json`** unless the user explicitly asks.
4. **Always back up the bundle directory** before mutating `project.json`. Backup name = `<basename>.backup-<UTC-timestamp>.screenstudio` next to the original.
5. **Always quit Screen Studio first.** If `pgrep -x "Screen Studio"` returns a PID, refuse and tell the user.
6. **All time fields are sourceMs**. Never inject output-time values.
7. **Cuts must be at word boundaries**, not in the middle of a word. Use `words[].start` / `words[].end` from Whisper.
8. **Empty slice list is forbidden.** If cuts cover the entire recording, abort.
9. **Zoom (`zoomRanges`) entries are sourceMs too.** Cuts that overlap a zoom break the zoom. Either skip the cut, drop the zoom (ask user), or shift the zoom.
10. **Do not change `id` of existing scenes/zoomRanges.** Only generate new IDs for newly created slices.
11. **Do not run `whisper` with `nohup … &` inside a foreground Bash call.** Use the Bash tool's own `run_in_background: true`.
12. **Do not delete the `.work-…/` directory** until the user confirms the result is correct. The `mic.json`, `words.json`, and `analysis_report.txt` are needed if cuts must be revised.
13. **JSON round-trip validation is mandatory** after every write (`json.load(open(SRC))`).
14. **Time accounting** must reconcile: `original_duration - sum(cut_lengths) == final_duration` (within float epsilon).
15. **Always restore from backup before re-applying** in iteration rounds. Stacking cuts on already-cut slices accumulates rounding errors and creates ID drift.
16. **Never trust prefix-repetition candidates without manual context inspection.** ~60% of automatic prefix matches in Korean speech are false positives (legitimate phrase reuse). Read both occurrences' surrounding context before deciding.
17. **Never re-run Whisper on the same audio**. The first run's `mic.json` and `words.json` are deterministic and cached in the work directory. Re-running burns ~10 minutes and changes nothing useful.

---

## 6. Common mistakes (learned the hard way)

### Mistake A — partial cut leaves first false-start audible

User said `"개발한 서버에 ▮ 개발한 서버에 오류가..."`. We cut only the 0.58s gap between the two utterances. Result: viewer hears `"개발한 서버에 개발한 서버에 오류가"` — duplicated.

**Fix**: when cutting a prefix repetition, the cut must start at **the first word of the false start** (or before the silence preceding it) and end at **the first word of the resumed utterance**. Verify with word timestamps.

```
Before:  ...메일이 온다든지 [개발한 서버에] [break] [개발한 서버에 오류가...]
Wrong cut:                              └──┘   (only the gap)
Right cut:                  └──────────────────┘   (first instance + gap)
```

### Mistake B — confusing output time and source time

User says "edit at 12:43". After your cuts, Screen Studio plays a 14:58 video. **12:43 is OUTPUT time**, not source. You must convert:

```python
def output_to_source(out_ms, slices):
    out_cursor = 0
    for sl in slices:
        sl_len = sl["sourceEndMs"] - sl["sourceStartMs"]
        if out_ms <= out_cursor + sl_len:
            return sl["sourceStartMs"] + (out_ms - out_cursor)
        out_cursor += sl_len
    return slices[-1]["sourceEndMs"]
```

Always echo the converted source time back to the user before cutting.

### Mistake C — segment-only analysis misses sentence repeats

Whisper gives you both `segments[]` and `segments[].words[]`. Filler analysis on segments alone misses cases like "이게 무료 티어를 쓸 때였는데" appearing twice across a 3.4s silence. **Always also run a manual scan of the full transcript text** for repeated sentences within 30 seconds.

### Mistake D — too aggressive on natural breathing

Pauses of 1.0–1.7s are usually intentional rhetorical breaths. Cutting them flat makes speech feel rushed and unnatural. **Default `silence-min = 1.8s`** and **leave 0.4s of breath** at the cut boundary. Only go below 1.8s if the user explicitly requests it.

### Mistake E — touching zoom timing while cutting

`zoomRanges[].startTime/endTime` are source-ms and remain valid after cuts iff the cut never overlaps the zoom. Always check overlap. If overlap is unavoidable, ask the user whether to delete the zoom or move it.

### Mistake F — Whisper subprocess dies under nohup

`nohup whisper … &` inside the Bash tool returns instantly because the parent shell exits and the process group is reaped. **Always use the Bash tool's `run_in_background: true`** instead, or block in the foreground with a generous timeout.

### Mistake G — Treating prefix-repeat candidates as true positives

The analyzer flags any 2+ word sequence that repeats within 8 seconds. Many of those are not stutters; they're a speaker naturally circling back to the same topic with the same vocabulary. In one real Korean session: 11 candidates → only 4 were stutters. **Read both occurrences' context (`ctx_first`, `ctx_second`)**. If the second one is a complete sentence with new content following the shared prefix, it's not a false start — leave it alone.

### Mistake H — Stacking cuts on a partially-cut bundle during iteration

When the user reports a residual issue and you re-run cuts, **always restore `project.json` from the backup first**. Re-applying additional cuts on top of an already-cut `slices[]` causes:
- Cut coordinates measured against source time to fall in unexpected slices
- Slice IDs to be regenerated when they didn't need to be
- Float drift between source/output time accounting

Always: `cp <backup>/project.json <bundle>/project.json` → then re-apply the full cut list (old + new together).

### Mistake I — Re-running Whisper between iterations

Whisper transcription on the same audio is deterministic. Re-running it consumes 8-12 minutes and produces the same `mic.json`. Always reuse the existing `mic.json`/`words.json` in `$WORK` between iteration rounds.

### Mistake J — Choosing model `medium` first by default

`medium` is ~3× slower than `small` on CPU and produces almost identical word boundaries for Korean and clean English. Default to `small`. Escalate only on user-reported transcription errors. (Confirmed: 16-min Korean recording, `medium` 12 min, `small` 8 min, identical cut decisions in our session.)

---

## 7. Time coordinate map

```
SOURCE TIME (project.json)        OUTPUT TIME (what user sees)
─────────────────────────         ────────────────────────────
       0  ───────┐
                 │  slice 1  ─────►       0
   src_a  ───────┘                   out_a = src_a
   src_b  ───────┐
                 │  slice 2  ─────►   out_a
   src_c  ───────┘                   out_a + (src_c - src_b)
       …                                       …
```

Conversion helpers live in [`scripts/apply_cuts.py`](scripts/apply_cuts.py) (`_output_time_at(...)`).

When the user reports a problem time:
- "I see a stutter at MM:SS in the playback" → that's **output** time → convert to source time → analyze.
- "Cut from 798s to 808s of the original" → that's **source** time → use directly.

If ambiguous, ask once: "Are you reading that timestamp from the Screen Studio playback (post-cut) or from the original recording?"

---

## 8. Filler vocabulary (Korean)

Standalone fillers worth cutting only when isolated by ≥0.2s gap on at least one side:

```
어, 음, 그, 그.., 어.., 음.., 이제, 막, 뭐, 근데, 약간, 하여튼, 자, 아
```

Do **not** cut these when they appear inline (no gap), e.g. "그런데", "근데요", "이제는". Whisper word boundaries are noisy on these — verify gaps before cutting.

---

## 9. Reverting

```bash
# Single project.json revert
cp "<bundle>.backup-<TS>.screenstudio/project.json" "<bundle>.screenstudio/project.json"

# Full bundle revert
rm -rf "<bundle>.screenstudio"
mv "<bundle>.backup-<TS>.screenstudio" "<bundle>.screenstudio"
```

Always offer this as a one-liner in the final report.

---

## 10. Reporting template

End every run with this structure:

```markdown
## ScreenStudio cut-edit complete

- Bundle:   <path>
- Backup:   <backup path>
- Workdir:  <work path>           # contains mic.json, words.json, analysis_report.txt
- Original: M:SS  (XXX.XXs)
- Final:    M:SS  (YYY.YYs)
- Cuts:     N (false starts: A, silences: B)
- Slices:   K (was 1)
- Zoom overlaps: 0
- JSON valid: ✓

### Cut breakdown
| # | source range | length | reason |
| 1 | 79.14 → 88.56 | 9.42s | FS: '...' |
...

### Verify
1. Quit Screen Studio (⌘Q) if open
2. Open the bundle: `open "<path>"`
3. Listen for stutters or unnatural seams
4. Report timestamps as MM:SS from the playback (output time); I'll re-map.

### Revert
`cp "<backup>/project.json" "<bundle>/project.json"`
```

---

## 11. Out of scope (not handled by this skill)

- Trimming `recording/` files (re-encoding) — would defeat non-destructive editing
- Adding zooms / cursor effects / device mockups — edit `config.*` and `zoomRanges` directly
- Speech-to-text in languages without robust Whisper support
- Auto-mixing background music — see `config.backgroundAudioFileName`
- Recordings without microphone narration

If asked, redirect: "This skill only does cut editing. For X, edit `project.json` keys: …"

## 12. Relationship to other skills / tools

- **`claude-watch`**: a separate skill that produces study notes from videos. It uses Groq/OpenAI Whisper APIs (requires API keys) and outputs markdown notes, not cut decisions. It is **not used by this skill** — we run `whisper` locally with word timestamps directly because (a) cut editing needs raw word boundaries, not narrative summaries, and (b) the user may not have Groq/OpenAI keys. Do not invoke `claude-watch` from inside this workflow.
- **`ffmpeg`/`ffprobe`**: hard dependency. Used for audio extraction and metadata only — never to produce a cut output video. The cut output is the original `recording/` rendered through the new `slices[]` by Screen Studio at open time.
- **`whisper` (openai-whisper, local CLI)**: hard dependency. Run locally, model cached in `~/.cache/whisper/`.
- **`pgrep`**: used to detect a running Screen Studio app. Required by `apply_cuts.py`.
- **Bash tool's `run_in_background`**: required for Whisper invocation. Do not substitute with shell `nohup &`.
