# Voicebox sentence-chunk QA pattern

Use this when a generated narration feels rushed, overlaps, repeats a phrase, or the user asks to “listen directly and fix it.”

## Durable pattern

1. Split the script into sentence-level chunks.
   - Prefer one natural sentence per Voicebox `/generate` call.
   - Avoid complex appositions and repeated labels that can cause the model to repeat phrases.
2. Generate each chunk separately with `crossfade_ms: 0`.
   - Keep `normalize: true`.
   - Instruct: clear Korean narration, no repetition, do not cut sentence endings.
3. Convert all chunks to a shared format before concat.
   - Example: `ffmpeg -i chunk.wav -ar 48000 -ac 1 -c:a pcm_s16le chunk_48k.wav`
   - If sample rates differ, ffmpeg concat can silently produce wrong total durations.
4. Insert explicit silence files between chunks.
   - Default user-facing narration fix: `0.55s` between sentences.
   - Increase to `0.7~0.8s` at scene boundaries if needed.
5. Concat, normalize, and apply limiter.
   - Avoid crossfade for overlap complaints; use silence gaps instead.
6. Run Whisper on the final WAV/MP4.
   - Use it to identify repeats, dropped phrases, and subtitle timing.
   - Do not treat every Whisper typo as TTS failure; Korean terms like “로컬/네온/챗봇” may be misrecognized.
7. Run `silencedetect` and check the voice coverage against the video duration.
   - Expected: repeated 0.45~0.65s pauses between chunks.
   - Problem: unexpected long mid-speech silence, missing final tail, speech after intended outro, or a long unvoiced video tail.
   - If the video continues more than ~2–3s after the final intended speech, either add a spoken outro or shorten the visual tail; do not present a silent 10s+ QA/outro as intentional unless the user explicitly requested silence.
8. Do a quick real-listen pass on the final WAV/MP4 before delivery when the user has complained about pacing, overlap, or clipped endings. Automated Whisper/silencedetect checks are supporting evidence, not a substitute for listening.
9. If a chunk repeats or mangles a key term, rewrite that sentence and regenerate only that chunk.
   - Rewrite examples: “마지막 원칙은 검증입니다” → “검증 단계에서는...”
   - “{{OWNER_TITLE}}의” may be simplified if TTS or Whisper repeatedly mangles it.

## Minimal concat recipe

```bash
# convert chunks first
for f in audio_chunks/chunk_*.wav; do
  ffmpeg -y -i "$f" -ar 48000 -ac 1 -c:a pcm_s16le "audio_chunks/48k/$(basename "$f")"
done

# silence gap
ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=mono -t 0.55 -c:a pcm_s16le audio_chunks/48k/silence_055.wav

# concat.txt alternates chunks and silence
ffmpeg -y -f concat -safe 0 -i audio_chunks/48k/concat.txt \
  -af "alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:90" \
  -c:a pcm_s16le narration_final.wav

whisper narration_final.wav --language Korean --model small --output_format txt --fp16 False
ffmpeg -hide_banner -i narration_final.wav -af silencedetect=noise=-45dB:d=0.25 -f null - 2> silencedetect.txt
```

## Pitfalls

- Launching Voicebox with Hermes HOME can show an empty profile list. Use the real data dir for {{OWNER_TITLE}}’s profiles.
- Long single `/generate` calls can sound efficient but may create overlap, rushed pacing, missing text, or phrase repetition.
- Re-encoding AAC without specifying sample rate can produce unusual sample rates; normalize final deliverables to 48kHz.
