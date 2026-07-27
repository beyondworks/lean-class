# Voicebox interview question pack workflow

Use when the user asks for many interview/practice questions as **one audio file** rather than one file per question.

## Pattern
1. Write a plain-text script with:
   - short intro
   - numbered questions
   - short outro
2. Generate audio **per block/question**, not as one long prompt. This improves reliability and lets retries resume from completed chunks.
3. Store chunks in a deterministic directory, e.g. `/tmp/<topic>_voice_chunks/01.wav`.
4. Make the generation script idempotent: if `NN.wav` exists and has non-trivial size, skip regeneration.
5. Concatenate with FFmpeg and explicit silence gaps:
   - intro → first question: ~1.0s
   - between questions: ~2.0s for mental answer time
   - outro: no extra requirement unless requested
6. Convert final WAV to MP3 and deliver only the final combined file.

## Reliability pitfall
Long Voicebox jobs can exceed the foreground tool timeout even though many chunks were already generated successfully. Do **not** discard the output. Re-run the same idempotent script so it skips existing chunks and finishes concat/export.

## Minimal concat commands
```bash
ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 2.0 /tmp/silence_2s.wav
ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -ar 44100 -ac 2 /tmp/final.wav
ffmpeg -y -i /tmp/final.wav -codec:a libmp3lame -b:a 192k /tmp/final.mp3
```

## Verification
```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 /tmp/final.mp3
ffmpeg -v error -i /tmp/final.mp3 -af silencedetect=noise=-45dB:d=2.5 -f null -
```
No `silencedetect` output for very long silences is generally acceptable when intentional gaps are shorter than the threshold.
