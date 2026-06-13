# screenstudio-cut

Word-level cut editor for **Screen Studio** (.screenstudio) project bundles.

Removes silences, false starts, and stutters by **rewriting `project.json` slices only** — the original `recording/` folder is never touched (non-destructive editing).

## What it does

1. Backs up the bundle
2. Extracts microphone audio (16 kHz mono WAV via ffmpeg)
3. Transcribes with **OpenAI Whisper** locally, with `--word_timestamps True`
4. Detects long silences (≥1.8s default), standalone fillers, and prefix repetitions
5. Lets the agent (Claude) read the full transcript and add sentence-level repetition cuts the analyzer can't catch
6. Validates each cut against word boundaries and zoom overlaps
7. Splits the original timeline slice into multiple slices that exclude the cut regions
8. Writes back, JSON-validated

## Usage

In Claude Code (any session with this skill installed):

- `/screenstudio-cut <bundle-path-or-name>`
- Or just describe in natural language: "이 스크린스튜디오 프로젝트 더듬는 부분 컷 편집해줘"

## Requirements

- macOS with `ffmpeg`, `ffprobe` (`brew install ffmpeg`)
- `whisper` CLI (`pip3 install -U openai-whisper`)
- Python 3.10+
- Screen Studio app must be **closed** during edits (auto-save would clobber)

## Files

```
screenstudio-cut/
├── SKILL.md                          ← Main skill instructions for Claude
├── README.md                         ← This file
├── commands/
│   └── screenstudio-cut.md           ← Slash-command trigger
├── scripts/
│   ├── analyze.py                    ← Whisper JSON → cut candidates
│   └── apply_cuts.py                 ← Cuts → project.json mutation
└── docs/
    └── project-json-schema.md        ← Reverse-engineered schema reference
```

## Guardrails baked in

- `apply_cuts.py` refuses to run if Screen Studio is open
- All edits are JSON-validated by reload after write
- Backups always taken before mutation
- Zoom overlap detection (configurable: abort / drop / keep)
- Word-boundary precision required for cuts
- Output-time vs source-time conversion helpers documented

See `SKILL.md` § 5 (Guardrails) and § 6 (Common mistakes) for the full list.

## Recommended workflow (iteration is the norm)

1. **First pass — conservative.** Apply only cuts you're 100% sure of (long silences, clear false starts the user told you about, sentence-level repeats you can read in the transcript). Show result to the user.
2. **User reviews in Screen Studio.** They report residual issues with playback timestamps.
3. **Convert output time → source time** (see SKILL.md § 7). Disambiguate once if unclear.
4. **Restore from backup, rebuild the FULL cut list** (old + new), re-apply. Never stack cuts on already-cut slices.
5. **Reuse `mic.json` / `words.json`** from the work directory — do not re-run Whisper between iterations.

Plan for at least one iteration. The first pass exists to surface edge cases the analyzer can't detect (sentence-level repeats, false starts where the partial cut would leave the first instance audible).

## Development

The skill was extracted from a real editing session on a 16-minute Korean recording. The lessons in `SKILL.md` § 6 (Common mistakes A through J) come from concrete failures during that session:

- **Mistake A** — partial cut left `개발한 서버에 개발한 서버에` repetition audible
- **Mistake B** — confused user-reported `12:43` (output time) with source time
- **Mistake F** — `nohup whisper … &` died silently when the parent Bash exited
- **Mistake G** — analyzer flagged 11 prefix repetitions, only 4 were real stutters
- **Mistake H** — accumulated drift when stacking cuts on a partially-cut project
- **Mistake J** — picked `medium` model first; `small` would have been faster with no quality loss

Every common mistake in the SKILL.md list is something that actually happened during development.
