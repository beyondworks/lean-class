# Voicebox from Hermes: durable workflow notes

Use these notes when a Telegram/Hermes session needs local Voicebox TTS output, especially with {{OWNER_TITLE}}/Leankim voice.

## Launch and discovery

Voicebox may launch its backend with Hermes' profile HOME when started via `open`, which can create an empty data directory and hide the user's real profiles. Prefer launching the backend directly with the real user data directory:

```bash
$HOME/Projects/Voicebox.app/Contents/MacOS/voicebox-server \
  --data-dir '$HOME/Library/Application Support/sh.voicebox.app' \
  --port 17494
```

If the UI is already running, discover the dynamic port:

```bash
ps aux | grep voicebox-server | grep -oE '\-\-port [0-9]+' | awk '{print $2}'
```

Health/profile checks:

```bash
curl -s http://127.0.0.1:${PORT}/health
curl -s http://127.0.0.1:${PORT}/profiles
curl -s http://127.0.0.1:${PORT}/models/status
```

## {{OWNER_TITLE}} voice profile

Voicebox profile used as the {{OWNER_NAME}} voice in this environment:

- name: `Leankim`
- id: `6d6070e5-d965-43eb-8b8f-401ab9d5504e`

## Long-form generation pattern

For narration longer than a sentence, generate asynchronously and poll the status endpoint. Useful request fields:

```json
{
  "profile_id": "6d6070e5-d965-43eb-8b8f-401ab9d5504e",
  "text": "...",
  "language": "ko",
  "engine": "qwen",
  "model_size": "1.7B",
  "seed": 20260517,
  "max_chunk_chars": 360,
  "crossfade_ms": 120,
  "normalize": true,
  "instruct": "차분하고 선명한 한국어 남성 내레이션. 문장 끝을 자르지 말고 자연스럽게 마무리."
}
```

Status responses are often Server-Sent-Event shaped:

```text
data: {"id":"...","status":"completed","duration":90.0,"error":null}
```

Strip the `data:` prefix before JSON parsing.

Download audio directly:

```bash
curl -L http://127.0.0.1:${PORT}/audio/${GENERATION_ID} -o narration.wav
```

Or inspect metadata:

```bash
curl -s http://127.0.0.1:${PORT}/history/${GENERATION_ID}
```

## Post-processing and QA

For exact target length and natural ending:

```bash
ffmpeg -y -i main.wav -i extra.wav \
  -filter_complex "[0:a]apad=pad_dur=0.25[a0];[a0][1:a]concat=n=2:v=0:a=1,alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11,atempo=1.0112,apad,atrim=0:90.0,afade=t=out:st=89.65:d=0.35,aresample=48000" \
  -c:a pcm_s16le narration_90s.wav
```

Verify:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 narration_90s.wav
ffmpeg -hide_banner -i narration_90s.wav -af silencedetect=noise=-45dB:d=0.35 -f null - 2> silencedetect.txt
whisper narration_90s.wav --language Korean --model small --output_format json --fp16 False
```

Use Whisper segments for subtitle timing. Correct obvious display-text transcription errors in subtitles only; do not assume Whisper text is the script of record.
