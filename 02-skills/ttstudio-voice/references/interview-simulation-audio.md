# Voicebox + OpenAI Realtime interview audio generation notes

Use when creating one-file interview simulation audio with questions/answers, multiple voices, or OpenAI Realtime fallback.

## User-facing preferences observed

- If the user asks for a simulation audio file, prefer **one combined file** unless they explicitly ask for per-question files.
- If the user asks for question/answer simulation, include both **questions and answers** in order when requested; do not only generate the questions.
- Use different voices for interviewer and answerer when requested.
- If the user explicitly says “Voicebox”, do not switch to macOS TTS or TTStudio as the main generation path.
- Avoid “애덕이” voice when the user requests a plain/ordinary interviewer voice.
- Prevent speech overlap; avoid crossfades in Q/A concatenation.
- Add padding after sentence ends to reduce clipped final syllables like “다”, “까?”, “요”.
- Verify long files past the 10-minute mark; earlier failures can appear only after long concatenation.

## Voicebox-only generation checklist

1. Confirm Voicebox server and available profiles.
2. Split long answer text by sentence or short chunks rather than one huge request.
3. Generate each chunk as PCM/WAV consistently.
4. Normalize all chunks to the same sample rate and channels, e.g. 48kHz mono.
5. Concatenate with explicit silence gaps and `crossfade_ms = 0`.
6. Export final MP3.
7. Verify:
   - duration and size with `ffprobe`
   - no unexpected long silence with `silencedetect=noise=-45dB:d=2.5`
   - volume after 10 minutes with `volumedetect` at offsets such as 600s, 720s, and near tail.

## OpenAI Realtime TTS notes

OpenAI Realtime preset voices are not user voice clones. Tell the user plainly if they asked for their own cloned voice.

Known-good GA WebSocket shape:

- URL: `wss://api.openai.com/v1/realtime?model=gpt-realtime-2`
- Do **not** use the old beta header/shape when GA is required; `OpenAI-Beta: realtime=v1` can produce `beta_api_shape_disabled`.
- `session.update` should use GA schema with `type: realtime`, output modalities, and audio output format.
- Include `session.audio.output.format.rate`, e.g. `24000`; missing it can produce `Missing required parameter: 'session.audio.output.format.rate'`.
- Receive `response.output_audio.delta` chunks, decode base64 PCM, and convert with ffmpeg.

Recommended validation for final Realtime MP3:

```bash
FILE=/tmp/final.mp3
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1:nokey=0 "$FILE"
ffmpeg -hide_banner -i "$FILE" -af silencedetect=noise=-45dB:d=2.5 -f null -
ffmpeg -hide_banner -ss 600 -t 30 -i "$FILE" -af volumedetect -f null -
```

## Text preservation

When generating Korean technical scripts, apply pronunciation substitutions for acronyms to improve speech:

- BAT → 비에이티
- CMO → 씨엠오
- MCN → 엠씨엔
- PB → 피비
- IP → 아이피
- GTM → 지티엠
- P&L → 피앤엘
- CRM → 씨알엠
- CAC → 씨에이씨
- LTV → 엘티비
- D2C → 디투씨
- AI → 에이아이
- OpenAI → 오픈에이아이
