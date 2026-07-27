# Urgent Google Docs → dual-voice Korean interview audio

Use when the user provides a Google Docs link and asks quickly for a single interview-style audio file with different interviewer/interviewee voices.

## Fast extraction pattern

For public Google Docs, skip browser interaction and export plain text directly:

```bash
DOC_ID="..."
python - <<'PY'
import requests
url=f'https://docs.google.com/document/d/{DOC_ID}/export?format=txt'
text=requests.get(url, timeout=20).text.replace('\ufeff','')
open('/tmp/source_doc.txt','w',encoding='utf-8').write(text)
print(len(text))
PY
```

Then parse from the requested starting section, e.g. `자기소개`, through the Q/A section only. Drop checklist/meta sections.

## Number pronunciation

If the user says numbers must be spoken as `1번(일번), 2번(이번), 3번(삼번)`, rewrite labels before TTS:

- `1번` → `일번`
- `2번` → `이번`
- `3번` → `삼번`
- `10번` → `십번`, `24번` → `이십사번`

Do this in the script text itself, not by hoping the TTS engine reads digits correctly.

## Voice routing

Preferred for final-quality Korean interview prep:

- Interviewer: a non-character Korean female/neutral Voicebox profile if available, instructed as `차분하고 선명한 한국어 여성 면접관 목소리, 과장하지 말 것`.
- Answerer: Leankim / {{OWNER_NAME}} profile when the user wants their own answer voice.

Fast fallback when the user prioritizes speed and did **not** explicitly require Voicebox:

- macOS `say` Korean female: `Yuna`
- macOS `say` Korean male: `Eddy` or another installed Korean male voice
- Keep this transparent if asked; do not claim it was Voicebox/GPT if a fallback was used.

## Assembly pattern

- Generate each Q/A block as its own chunk.
- Use explicit gaps rather than overlap/crossfade:
  - intro → Q1: ~1.4s
  - question → answer: ~0.9s
  - answer → next question: ~1.3s
- Normalize all chunks to `48000 Hz`, mono, `pcm_s16le`, then concat once.

Example `ffmpeg` verification before delivery:

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 final.mp3
ffmpeg -hide_banner -i final.mp3 -af silencedetect=noise=-45dB:d=2.5 -f null - 2> silence.txt
grep -c 'silence_start' silence.txt
```

Expected: no unexpected long silence and duration/size present.
