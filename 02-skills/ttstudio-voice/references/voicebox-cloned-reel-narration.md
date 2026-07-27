# Voicebox cloned narration for image-to-video reel packages

Use this when a user asks for Voicebox voice cloning from a sample MP3 and narration files for Kling/Runway/HeyGen image-to-video scenes. Do not substitute TTStudio, macOS `say`, or another TTS when the user explicitly says Voicebox.

## Proven workflow

1. Start Voicebox backend with the real user data dir when Hermes cannot see the app profile:

```bash
$HOME/Projects/Voicebox.app/Contents/MacOS/voicebox-server \
  --data-dir '$HOME/Library/Application Support/sh.voicebox.app' \
  --port 17494
```

2. Wait for health before API calls. Model load/download can make early requests fail or hang briefly.

```bash
curl -s http://localhost:17494/health
```

3. If the sample reference text is unknown, transcribe the sample locally first. Voicebox `/transcribe` may trigger Whisper model download and can be unstable during first use; local `whisper` is a reliable fallback.

```bash
whisper sample.mp3 --language Korean --model base --output_dir transcribe --output_format txt --fp16 False
```

4. Create or reuse a profile, then upload the sample:

```bash
curl -s -X POST http://localhost:17494/profiles \
  -H 'Content-Type: application/json' \
  -d '{"name":"Seo-Ian Voice Clone","description":"Cloned from sample MP3","language":"ko"}'

curl -s -X POST http://localhost:17494/profiles/$PROFILE_ID/samples \
  -F "file=@sample.mp3" \
  -F "reference_text=$REFERENCE_TEXT"
```

5. Generate short scene-by-scene lines, not one long reel script. Recommended payload:

```json
{
  "profile_id": "PROFILE_ID",
  "text": "씬별 한 문장 나레이션",
  "language": "ko",
  "engine": "qwen",
  "model_size": "1.7B",
  "max_chunk_chars": 120,
  "crossfade_ms": 0,
  "normalize": true,
  "instruct": "차분하고 선명한 한국어 여성 내레이션. 노션은 노-션으로 또렷하게 발음하고, 노쎤처럼 된소리로 발음하지 말 것. 에이아이는 에이아이로 읽기. 문장 끝의 요/게요를 급하게 자르지 말고 숨을 살짝 남긴다."
}
```

6. Download generated audio and convert for editing:

```bash
curl -L -s http://localhost:17494/audio/$GENERATION_ID -o scene.wav
ffmpeg -y -i scene.wav \
  -af 'apad=pad_dur=0.35,loudnorm=I=-16:TP=-1.5:LRA=11' \
  -ar 48000 -ac 1 -codec:a libmp3lame -b:a 192k scene.mp3
```

7. QA with Whisper transcript before delivery:

```bash
whisper all_narration.mp3 --language Korean --model base --output_dir qa_transcript --output_format txt --fp16 False
```

## Content rules for reel narration

- Every scene should have a narration/dialogue line, even when the image-to-video provider's sound-video sync is OFF. OFF scenes get external Voicebox narration in edit.
- Preserve story continuity across locations. Example pattern: meeting room → cafe review → street transition → office human review → CTA.
- If moving from meeting room to cafe, explicitly bridge it: “회의실을 나와서도 흐름은 이어져요. 방금 정리된 내용을 카페에서 바로 확인해요.”
- Closing CTA can be explicit and two-part: “댓글에 회의록 남겨주시면, 회의 자동화 정리본 보내드릴게요.”
- For Korean pronunciation stability, rewrite hard lines into simpler spoken Korean instead of only adding padding. Example fixes:
  - “말은 빠르게 오가고” → “말이 빠르게 오가고”
  - “구조화돼요” → “차분히 정리돼요” or “정리돼요”
  - “자동화는 초안을 만들고, 판단은 사람이 해요” → “마지막에는 사람이 한 번 더 확인해요. 에이아이는 초안만 만들어요.”
- If Whisper hears a key term incorrectly, regenerate that one scene with simpler wording and stronger instruct; do not regenerate the whole batch unless needed.

## Delivery package shape

Recommended folder for final handoff:

```text
Kling_Voicebox_Final/
  images/
  kling3_prompts/
  voicebox_narration/
    00_all_narration_script.md
    voicebox_generation_plan.json
    generated_audio/
      01_*.mp3
      ...
      all_narration_voicebox.mp3
      qa_transcript/
  scene_map_v2.csv
  README_KLING3_VOICEBOX_V2.md
```

Include both individual MP3 files and a combined preview MP3. State any remaining QA caveat explicitly, e.g. Whisper heard “차분히” as “차분이” but key terms and CTA passed.
