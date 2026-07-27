# Voicebox dual-voice interview Q&A recipe

Use when the user wants an interview simulation where questions and answers are in different voices, delivered as one MP3.

## Key user preference from BAT CMO prep session

- If the user says "Voicebox", do **not** substitute macOS `say`, ttstudio, or another TTS path unless explicitly allowed.
- Avoid character voices for serious interview prep. If only Voicebox profiles are available, use a non-character profile with a strong `instruct` such as "평범하고 차분한 한국어 면접관 목소리, 캐릭터처럼 과장하지 말 것".
- For the user's own answers, use the Leankim / {{OWNER_NAME}} Voicebox profile: `6d6070e5-d965-43eb-8b8f-401ab9d5504e`.

## Durable implementation pattern

1. Build a compact Q/A script first.
   - Long answer scripts make generation slow and increase overlap/cutoff risk.
   - Prefer 2–5 short sentences per answer.
2. Generate with Voicebox `/generate` only.
   - `crossfade_ms: 0`
   - `max_chunk_chars`: 120–180 for sentence-level generation
   - `normalize: true`
   - Instruct both voices not to cut final syllables: `문장 끝의 다, 까, 요를 절대 자르지 말고 숨을 살짝 남겨 마무리`.
3. Split into sentence-level chunks.
   - Generate each sentence separately, not a whole 10–20 minute script.
   - Insert explicit silence, not crossfade:
     - sentence gap: ~0.55s
     - question → answer gap: ~0.95s
     - answer → next question gap: ~1.5s
4. Convert every generated WAV chunk before concat.
   - Use the same format for all chunks: `48000 Hz`, `mono`, `pcm_s16le`.
   - Add tail padding per chunk to prevent clipped endings:
     - `apad=pad_dur=0.35~0.45`
   - Example filter: `apad=pad_dur=0.45,loudnorm=I=-18:TP=-2:LRA=11`.
5. Final concat and export.
   - `ffmpeg -f concat -safe 0 -i concat.txt -af "alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -ac 1 -c:a pcm_s16le final.wav`
   - MP3 for Telegram: `libmp3lame`, `128k`, `48000`, `mono`.

## Verification checklist

Run before delivery:

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 final.mp3
ffmpeg -hide_banner -i final.mp3 -af silencedetect=noise=-45dB:d=2.5 -f null - 2> silence.txt
grep -c 'silence_start' silence.txt
for SS in 600 720 800; do
  ffmpeg -hide_banner -ss $SS -t 20 -i final.mp3 -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume'
done
```

Expected:
- No unexpected long silence over 2.5s.
- 10-minute and later segments have non-`-inf` mean/max volume.
- Total duration matches expected Q/A length.

## Pitfalls

- A previous MP3 had no sound after ~10 minutes. Avoid this by converting every chunk and every silence file to the same 48k mono PCM format before concat, then exporting once.
- If the user complains of overlap, do not reduce gaps or use crossfade. Regenerate sentence-level chunks with `crossfade_ms: 0` and explicit silence files.
- If final syllables like `다`, `까?`, `요` are clipped, do not rely only on final-file padding. Add per-chunk tail padding and rewrite very abrupt formal endings into slightly more natural spoken Korean where appropriate.
