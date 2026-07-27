# Voicebox dual-voice interview simulation pattern

Use when the user wants interview practice audio where the interviewer/questions use one voice and the candidate/answers use the user's voice, delivered as **one combined MP3** rather than separate files.

## Pattern
1. Prepare two scripts:
   - `questions.txt`: numbered question blocks (`1번. ...`).
   - `answers.txt`: matching numbered answer blocks (`1번. ...`).
2. Use two Voicebox profiles:
   - Question/interviewer: a non-user Korean profile such as `애덕이` (`4d44088c-cb41-4896-82e1-2cb700899d39`) or another available interviewer voice.
   - Answer/user: `Leankim` (`6d6070e5-d965-43eb-8b8f-401ab9d5504e`) for {{OWNER_TITLE}}/{{OWNER_NAME}} voice.
3. Generate one WAV per block, alternating Q/A:
   - `01_q.wav` with interviewer profile.
   - `01_a.wav` with Leankim profile.
   - Repeat for all pairs.
4. Concatenate in one file:
   - Intro from interviewer voice.
   - For each pair: question → ~0.8s silence → answer → ~2.0s silence.
   - Ending from user voice if desired.
5. Export a single MP3 via ffmpeg and verify duration/counts.

## Voicebox generation settings that worked well
```json
{
  "language": "ko",
  "engine": "qwen",
  "model_size": "1.7B",
  "max_chunk_chars": 220,
  "crossfade_ms": 80,
  "normalize": true
}
```

For longer answer blocks, `max_chunk_chars: 260` is acceptable.

## Suggested instructions
- Question profile instruct: `차분하지만 또렷한 한국어 면접관 목소리. 질문을 명확히 읽고 문장 끝을 자연스럽게 마무리.`
- Answer profile instruct: `차분하고 신뢰감 있는 한국어 남성 답변 목소리. 면접 답변처럼 안정적으로 말하고 문장 끝을 급하게 끊지 말 것.`

## Verification
- Confirm generated chunks: `*_q.wav` count and `*_a.wav` count match the expected pair count.
- Confirm final file metadata:
  ```bash
  ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1:nokey=0 final.mp3
  ```
- Optionally run silencedetect for accidental long gaps:
  ```bash
  ffmpeg -v error -i final.mp3 -af silencedetect=noise=-45dB:d=3.0 -f null -
  ```

## Pitfall
If the user first asks for only questions, then asks for answers, clarify whether they want separate answer audio or a **single alternating Q/A simulation**. If they specify different voices, do not reuse the user's voice for questions.