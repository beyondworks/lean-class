# claude-watch

**Turn any tutorial or lecture video into structured study notes.** Paste a URL, walk away, come back to a markdown file with embedded screenshots, timestamped transcript, and Claude's synthesis — saved to a persistent library.

```
/claude-watch https://youtu.be/<lecture> backprop intuition
```

## Install

| Surface | Command |
|---|---|
| **Claude Code** | `/plugin marketplace add devinilabs/claude-watch` then `/plugin install claude-watch@claude-watch` |
| **claude.ai** (web) | Download `claude-watch.skill` from the latest release → Settings → Capabilities → Skills → `+` |
| **Codex** | `git clone https://github.com/devinilabs/claude-watch ~/.codex/skills/claude-watch` |

## What it does

1. Downloads via `yt-dlp` (or accepts a local file).
2. Detects scene changes with `ffmpeg`. Inserts coverage-floor frames every 45s across long static gaps so a lecture with one slide for 5 minutes still gets ~7 frames, not 1.
3. Pulls a timestamped transcript — captions first (free), Whisper API (Groq preferred, OpenAI alt) only when missing.
4. Hands frames + transcript to Claude. Claude `Read`s every frame as an image and writes `notes.md` to a strict template:
   - `## TLDR` — 3-4 sentence synthesis
   - `## Key Concepts` — bulleted with timestamps
   - `## Notes` — one section per scene with embedded screenshot, on-screen text, what was said, Claude's synthesis
   - `## Code & Commands` — every code-on-screen frame transcribed into a runnable fenced block
   - `## Diagrams Referenced`, `## Open Questions`
5. Saves everything to `~/claude-watch/library/<slug>/` — re-running the same URL is a cache hit.

## Why this exists

`claude-video`'s uniform frame sampling spends the budget poorly on long lectures with slow-changing slides. And answers live in chat, so you can't go back to "the notes from that video." `claude-watch` is opinionated for the tutorial workflow: scene-aware frames, persistent library, structured notes file.

## Usage

```
/claude-watch <url-or-path> [topic]
/claude-watch ~/Lectures/cs231n.mp4 backpropagation derivation
/claude-watch https://youtu.be/<long> --start 5:00 --end 25:00
/claude-watch <url> --resolution 1024            # for slides with tiny code text
```

Flags: `--start/--end`, `--max-frames`, `--resolution`, `--scene-threshold`, `--max-gap`, `--whisper groq|openai`, `--no-whisper`, `--out-dir`.

## Bring your own keys

Captions cover the majority of public videos for free. Whisper only kicks in when a video has no caption track.

| Need | Cost |
|---|---|
| Download + native captions | free (`yt-dlp` + `ffmpeg`) |
| Whisper fallback (preferred) | Groq `whisper-large-v3` — cheap, fast |
| Whisper fallback (alt) | OpenAI `whisper-1` |
| Disable Whisper | `--no-whisper` (frames-only when no captions) |

Keys go in `~/.config/claude-watch/.env` (mode 0600).

## Re-running the same video

The library is keyed on `slug = YYYY-MM-DD-<title>-<short-hash>` where the short hash is `sha1(source + focus_range)[:4]`. Re-running the same URL with the same focus range hits the cache — no re-download, no re-transcribe, only frames + notes regenerate. Different focus range = different slug = a separate notes file.

To force a fresh run, delete the `meta.json` in the library dir.

## Limits

- **Best accuracy: under ~30 minutes** for a single notes pass. Past that, use `--start`/`--end` to focus.
- **Hard frame cap: 80** by default. Bump with `--max-frames` (token cost grows linearly).
- **Whisper upload limit: 25 MB** (~50 min mono 16 kHz). Longer videos need captions.
- **No private platforms.** Public URLs and local files only.

## Develop

```bash
git clone https://github.com/devinilabs/claude-watch
cd claude-watch
python3 -m pytest                         # full suite
bash scripts/build-skill.sh               # → dist/claude-watch.skill (claude.ai bundle)
```

Releasing: tag `vX.Y.Z`, push the tag — CI builds and attaches `claude-watch.skill`.

## License

MIT. Built on `yt-dlp`, `ffmpeg`, and Claude's multimodal `Read` tool. Whisper transcription via [Groq](https://groq.com) or [OpenAI](https://openai.com).
