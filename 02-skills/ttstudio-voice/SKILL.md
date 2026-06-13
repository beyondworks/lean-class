---
name: ttstudio-voice
description: TTStudio/Voicebox 로컬 TTS 서버로 음성을 생성하는 스킬. "음성 생성", "TTS", "목소리", "보이스" 키워드에 트리거.
user_invocable: true
---

# TTStudio / Voicebox Voice Generator

Voicebox 앱의 내부 API를 통해 텍스트를 음성으로 변환한다.

## Voice import / sample creation pitfall

If the user asks whether “Import Voice” can take an MP3, check. API `/profiles/import` imports exported Voicebox profile ZIP archives. MP3/WAV samples normally require creating a profile via `/profiles`, then adding the sample via `/profiles/{profile_id}/samples` with accurate `reference_text`.

## 사전 조건
- Voicebox 앱 또는 `voicebox-server` 백엔드가 실행 중이어야 한다
- 포트는 동적 할당 가능 — ps에서 자동 탐지
- 에이전트/Telegram 세션에서 앱을 `open`으로 띄우면 에이전트 프로필 HOME 아래의 빈 데이터 디렉터리를 볼 수 있다. 사용자 실제 Voicebox 프로필을 써야 하면 백엔드를 직접 실행하며 `--data-dir '~/Library/Application Support/sh.voicebox.app'`를 명시한다.

## 사용자 opt-out 우선

사용자가 “TTStudio는 쓰지 말고”, “Voicebox 말고”, “무료 오픈소스 TTS로”처럼 명시적으로 이 경로를 제외하면 이 스킬의 생성 경로를 사용하지 않는다. 이 경우 TTStudio/Voicebox로 몰래 대체하지 말고, 요청한 TTS 계열을 먼저 시도한다. 이미 생성된 영상에 음성만 입히는 작업이면 `video-capture`의 패턴을 우선 적용한다.

## 포트 탐지 / 직접 실행

Voicebox는 실행 시마다 포트가 바뀔 수 있다. 아래 명령으로 현재 포트를 찾는다:

```bash
ps aux | grep voicebox-server | grep -oE '\-\-port [0-9]+' | awk '{print $2}'
```

에이전트 환경에서 안정적으로 실제 사용자 프로필을 읽게 하려면 직접 실행한다:

```bash
~/Projects/Voicebox.app/Contents/MacOS/voicebox-server \
  --data-dir '~/Library/Application Support/sh.voicebox.app' \
  --port 17494
```

자세한 agent/Voicebox 워크플로우는 참고.

## API 엔드포인트 (Voicebox 내부 서버)

### 헬스체크
```bash
curl -s http://localhost:{PORT}/health
```

### 프로파일 목록
```bash
curl -s http://localhost:{PORT}/profiles
```

### 음성 생성 (비동기)
```bash
# 1. 생성 요청
curl -s -X POST http://localhost:{PORT}/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "UUID",
    "text": "합성할 텍스트(...)",
    "language": "ko",
    "engine": "qwen",
    "model_size": "1.7B",
    "max_chunk_chars": 360,
    "crossfade_ms": 120,
    "normalize": true,
    "instruct": "차분하고 선명한 한국어 남성 내레이션. 문장 끝을 자르지 말고 자연스럽게 마무리."
  }'
# 응답: {"id": "generation-uuid", "status": "generating"}

# 2. 완료 대기 (SSE)
curl -s http://localhost:{PORT}/generate/{id}/status
# SSE 응답: data: {"status": "completed", "duration": 3.2}
# JSON 파싱 시 `data:` prefix를 제거한다. 여러 `data:` 라인이 오면 마지막 JSON data 라인을 사용한다.

# 3. 오디오 다운로드
curl -L http://localhost:{PORT}/audio/{id} -o output.wav

# 4. 메타데이터 확인
curl -s http://localhost:{PORT}/history/{id}
# → "audio_path": "/Users/.../generations/{id}.wav"
```

### 프로파일 현황
| ID | 이름 | 용도 |
|---|---|---|
| <YOUR_VOICE_ID> | Example Voice | 사용자/사용자 메인 보이스 |
| <YOUR_VOICE_ID_2> | 보조 보이스 | 대체 보이스 |

## 자동화 스크립트

`scripts/tts-generate.py` — tts-chunks.md에서 청크를 읽어 Voicebox API로 배치 생성.

```bash
python3 scripts/tts-generate.py config.json
```

config.json:
```json
{
  "chunks_file": "script/tts-chunks.md",
  "output_dir": "voice",
  "profile_id": "<YOUR_VOICE_ID>",
  "language": "ko",
  "padding_ms": 300,
  "gap_within_scene_ms": 400,
  "gap_between_scene_ms": 800
}
```

## TTS 품질 규칙

### Voicebox-only / 다중 보이스 인터뷰 파일

사용자가 “Voicebox 사용”, “질문은 다른 목소리, 답변은 내 목소리”, “말이 겹치지 않게”, “끝음절이 짤리지 않게”, “10분 이후 무음 해결”을 요구하면

긴급 면접/리허설 오디오에서 사용자가 Voicebox를 명시하지 않고 “빨리”, “시간 없다”, “한국어 자연스러운 여성/남성 음성”을 요구하면 macOS `say`의 한국어 보이스를 빠른 납품 경로로 사용할 수 있다. 예: 면접관 여성 `Yuna`, 답변자 남성 `Eddy` 또는 사용 가능한 ko_KR 남성 보이스. 단, 사용자가 Voicebox 또는 본인 목소리를 지정한 경우에는 이 fallback을 쓰지 않는다.

핵심 원칙:
- 사용자가 Voicebox를 지정하면 macOS `say`, ttstudio, 외부 TTS로 대체하지 않는다. 특히 사용자가 “TTStudio 아니고 voicebox”라고 정정하면 Voicebox 서버/API 경로로만 진행한다.
- 질문/답변 또는 영상 씬 나레이션을 문장 단위로 생성하고 `crossfade_ms: 0` + 명시적 무음 파일로 연결한다.
- 모든 Voicebox chunk와 silence를 `48kHz mono pcm_s16le`로 변환한 뒤 concat한다. 긴 MP3에서 10분 이후 무음이 생기는 것을 방지한다.
- 문장 끝 `다/까/요` 잘림 방지를 위해 각 chunk에 `apad=pad_dur=0.35~0.45`를 적용하고, instruct에 “마지막 음절을 자르지 말라”고 명시한다.
- 납품 전 `silencedetect`와 10분 이후 구간 `volumedetect`를 확인한다.

1. **청크 50자 이하** — 짧은 수동 청크 방식에서는 길면 TTS가 중간 내용 누락
2. **사용자가 “급하다/겹친다/직접 들으며 수정”을 지적하면 장문 자동 청크를 버리고 문장별 생성** — Voicebox `/generate`를 한 문장씩 호출하고, ffmpeg concat에서 0.45~0.65초 무음 갭을 명시해 겹침을 줄인다. 한 번에 긴 대본을 넣고 `crossfade_ms`에 맡기면 일부 문장이 붙거나 반복될 수 있다.
3. **장문 자동 청크 방식** — 빠른 초안에는 Voicebox `/generate`에 `max_chunk_chars` 300~400, `crossfade_ms` 80~120, `normalize: true`를 넣어 자연 연결을 우선한다. 최종 납품/사용자 지적 후에는 문장별 생성으로 전환한다.
4. **끝에 `(...)` 싱글 트레일링** — 수동 청크 방식의 끝음 끊김 방지. 마지막 청크만 제외
5. **마침표는 `(...)` 앞에** — `합니다.(...)` (억양 자연스러움)
6. **숫자 한글화** — "50개" → "오십 개"
7. **영문 한글 발음 변환** — "CLAUDE.md" → "클로드엠디"
8. **300ms 꼬리 패딩 / 짧은 crossfade** — ffmpeg `apad` 또는 Voicebox `crossfade_ms` 사용. 문장별 concat에서는 crossfade보다 무음 갭이 안전하다.
9. **블록 간 무음 갭** — 같은 씬 0.4초, 씬 경계 0.8초. 빠르게 들리면 0.55초 기본으로 재조립한다.
10. **Whisper로 싱크 검증** — 최종 wav/mp4를 Whisper로 전사해 segment timing을 자막/씬 타이밍에 반영한다. 표시 자막은 Whisper 오인식만 교정한다. trailing silence/reverb에서 Whisper가 가짜 마지막 문장을 hallucinate할 수 있으므로 마지막 유효 발화 이후는 trim하거나 suspicious final segment를 제외한다.
11. **silencedetect로 연결 확인** — `ffmpeg -af silencedetect=noise=-45dB:d=0.25~0.35`로 긴 무음/비정상 끊김을 확인한다. 문장별 갭이 0.45~0.65초로 반복되는 것은 정상 호흡으로 본다.
12. **반복/오인식 문장은 대본을 바꿔 재생성** — 같은 문장이 반복되거나 고유명사(사용자 등)가 깨지면 seed만 바꾸지 말고 문장을 더 단순하게 고쳐 재생성한다.
13. **결과 듣고 끊기면 재생성** — 자동 검수는 한계, 수동 확인이 최선
14. **한국어 `다` 종성 급끊김 대응** — 사용자가 “`다`가 `ㄷ`로 끊긴다”거나 말끝이 부자연스럽다고 지적하면, 단순 tail padding만으로 해결하려 하지 말고 대본 자체를 더 구어체로 바꾼다. 영상 내레이션에서는 `합니다/됩니다/맞습니다`를 `해요/돼요/맞아요`, `입니다`를 `이에요/예요`, 마지막 문장은 `거예요/가까워요`처럼 열린 말끝으로 재작성한 뒤 문장별 재생성한다. 필요하면 Voicebox instruct에 “문장 끝의 요/예요/거예요를 급하게 끊지 말고 숨을 살짝 남긴다”를 명시한다.

문장별 Voicebox 재생성/concat/QA 예시는 참고.

이미지→영상 릴스 패키지에서 Voicebox 클론 보이스로 씬별 나레이션을 생성하고, Kling/Runway 등 영상 생성 프롬프트와 함께 납품해야 하는 경우는 참고. 핵심: 사용자가 Voicebox를 명시하면 TTStudio/`say`로 대체하지 말고, 모든 씬에 나레이션을 부여하며, sound-video sync OFF 씬은 외부 Voicebox MP3를 편집에서 붙인다. 한국어 발음 QA는 Whisper 전사로 확인하고 `노션→노쎤`, `AI`, 어려운 한자어 발음이 깨지면 해당 씬만 구어체로 단순화해 재생성한다.

면접/리허설 질문처럼 여러 질문을 **하나의 MP3**로 전달해야 하는 경우는 참고. 질문별 개별 파일을 전달하지 말고, 질문 단위 WAV 청크를 생성한 뒤 명시적 무음 갭으로 concat한다. 긴 배치가 도구 timeout으로 끊겨도 이미 생성된 청크는 살리고, idempotent 스크립트를 재실행해 누락 청크와 최종 MP3 export만 이어서 처리한다.

Google Docs 링크에서 자기소개+Q/A만 빠르게 추출해 여성 면접관/남성 답변자 단일 MP3를 만들어야 하는 긴급 작업은를 참고한다. 공개 Docs는 `/export?format=txt`로 직접 추출하고, `1번/2번/3번` 같은 번호는 `일번/이번/삼번`으로 대본에서 선변환한다.

Google Docs 링크에서 자기소개+Q/A를 빠르게 추출해 여성 면접관/남성 답변자 단일 MP3로 만드는 긴급 워크플로우는 참고.

## 듀얼 보이스 인터뷰 시뮬레이션

사용자가 면접 연습/인터뷰 시뮬레이션을 요청하면서 "질문은 다른 목소리, 답변은 내 목소리" 또는 "하나의 파일"을 요구하면 패턴을 따른다. 질문과 답변을 같은 번호 블록으로 맞춘 뒤, 질문은 비사용자 한국어 프로필(예: 애덕이), 답변은 Example Voice/사용자 프로필로 생성하고 `질문 → 짧은 무음 → 답변 → 긴 무음` 순서로 하나의 MP3로 concat한다. 질문만/답변만 별도 생성하지 말고, 사용자가 명시한 최종 청취 형태(단일 Q/A 파일)를 우선한다.

## Voicebox 정리

```bash
vb-clean  # alias: DB 정리 + WAV 삭제 + 캐시 삭제 + 앱 재시작
```
