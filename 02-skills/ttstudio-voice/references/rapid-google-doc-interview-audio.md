# Rapid Google Docs interview Q&A audio recipe

Use when the user provides a Google Docs URL and asks urgently for one Korean interview audio file with different voices for interviewer and answerer, without explicitly requiring Voicebox.

## Flow

1. Extract the public/shared Google Doc as plain text:

```bash
DOC_ID="..."
curl -L "https://docs.google.com/document/d/${DOC_ID}/export?format=txt" -o /tmp/source.txt
```

If this returns a permission/login page, use the authenticated Google Workspace Docs path instead.

2. Keep only the requested interview region.
   - For BAT-style prep docs, keep the compressed self-introduction plus Q/A section only.
   - Drop checklists, “do not say” sections, and meta notes unless the user asked for them.

3. Normalize pronunciation before TTS.
   - Replace `Q1` labels with spoken labels: `일번 질문입니다`, `이번 질문입니다`, `삼번 질문입니다`, etc.
   - Convert common acronyms and symbols to Korean pronunciation: `BAT→비에이티`, `PB→피비`, `MCN→엠씨엔`, `P&L→피앤엘`, `D2C→디투씨`, `KPI→케이피아이`, `→→에서`, `0→1→제로에서 원`.
   - Remove formatting markers, stars, separators, and metadata labels like `핵심 1문장`.

4. Generate chunks.
   - If Voicebox is required, follow the Voicebox dual-voice recipe.
   - If speed is more important and Voicebox is not specified, macOS `say` can produce a quick draft:
     - interviewer female: `Yuna`
     - answerer male: `Eddy` or another available ko_KR male voice
     - example: `say -v Yuna -r 188 -o q01.aiff "일번 질문입니다. ..."`

5. Convert and concat with explicit gaps.

```bash
ffmpeg -y -i chunk.aiff -af "apad=pad_dur=0.25,loudnorm=I=-18:TP=-2:LRA=11" -ar 48000 -ac 1 -c:a pcm_s16le chunk.wav
ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=mono -t 0.9 -c:a pcm_s16le silence_q_to_a.wav
ffmpeg -y -f concat -safe 0 -i concat.txt -af "alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -ac 1 -c:a libmp3lame -b:a 128k final.mp3
```

Suggested gaps:
- self-introduction → Q1: 1.4s
- question → answer: 0.9s
- answer → next question: 1.35s

## Verification

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 final.mp3
ffmpeg -hide_banner -i final.mp3 -af silencedetect=noise=-45dB:d=2.5 -f null - 2> silence.txt
grep -c 'silence_start' silence.txt
ffmpeg -hide_banner -ss 120 -t 10 -i final.mp3 -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume'
```

Expect no unexpected long silence and non-`-inf` volume in later segments.
