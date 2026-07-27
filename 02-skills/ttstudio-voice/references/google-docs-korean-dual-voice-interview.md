# Google Docs interview Q&A → Korean dual-voice MP3 fallback workflow

Use when the user provides a Google Docs link and asks to extract interview/self-introduction Q&A into a Korean audio file with separate interviewer/respondent voices.

## Durable workflow

1. Export Google Doc text via `/export?format=txt` when the doc is public or accessible in the environment.
2. Extract only the requested scope. For interview practice, keep self-introduction and question/answer pairs; remove unrelated notes, headings, duplicate prompts, and meta commentary.
3. Normalize spoken numbering before TTS:
   - `1번` → `일번`
   - `2번` → `이번`
   - `3번` → `삼번`
   - Continue with Korean pronunciations for all question numbers.
4. Split the script into chunks by speaker:
   - Interviewer: female Korean voice.
   - Respondent: male Korean voice.
5. Preferred path: use Voicebox/TTStudio dual-voice flow if the server is healthy.
6. Fast fallback path on macOS: use `say` with Korean-capable voices for chunk-level AIFF/WAV generation, then concatenate with `ffmpeg` into one MP3.
7. Verify before delivery:
   - `ffprobe` duration and stream metadata.
   - Spot-check middle sections with `ffmpeg`/volumedetect or by sampling to ensure no huge silence gaps.
   - Confirm output file exists and is non-empty.
8. Deliver via Telegram as `MEDIA:/absolute/path/to/file`.

## Practical prompt/normalization notes

- The user may say “자기소개부터 질문과 답변만” — do not include earlier document setup, instructions, or non-QA material.
- If time pressure is explicit, prefer a robust local fallback over spending time debugging a stuck TTS server.
- Preserve Korean readability for TTS: expand abbreviations and symbol-heavy numbering into natural Korean speech.
- Use a single final MP3 unless the user asks for separate clips.

## Pitfalls

- Do not claim a Voicebox server is unavailable forever just because one health/profile request timed out. Treat it as a transient setup/runtime issue and use the fallback path if speed matters.
- Browser access is usually unnecessary for Google Docs text export; use direct text export when possible.
- Avoid leaving long unexplained pauses between chunks; insert only short intentional speaker pauses.
