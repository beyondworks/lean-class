---
name: create-video
description: 영상 콘텐츠 제작 파이프라인 실행. 리서치 → 대본 → 자막 → 보이스 → 씬 → 렌더링 → QA까지 전체 파이프라인을 오케스트레이션한다.
user_invocable: true
---

# Video Content Pipeline

인포그래픽 스타일 유튜브 영상 제작 전체 파이프라인.
"영상 만들어줘", "EP 제작", "콘텐츠 제작" 키워드에 트리거.

## 전체 파이프라인 (7단계)

인포그래픽/애니메이션형 영상:

```
1. 리서치 → 2. 대본 → 3. TTS 청크 → 4. 보이스 생성
    → 5. HTML 시각화 → 6. 캡처 → 7. CapCut 프로젝트
```

Shorts/Reels/TikTok footage-native 영상은 위 HTML 시각화 단계를 기본으로 쓰지 않는다.를 우선 적용해 **소스 리서치/스크랩을 먼저 수행**한다. 지식창/패션탐정냥식 작업은 해외 고조회수 롱폼·숏폼을 찾아 전체 영상을 보고, 2~3초 컷·확대·재배열·후킹 흐름을 추출한 뒤 공식/라이선스/사용자 제공/AI-realistic media를 ffmpeg/CapCut으로 편집한다. 부족한 장면은 Codex → GPT Image 2(이미지), Codex → Heygen(영상)으로 생성하고, 자막은 SRT/CapCut editable track으로 분리한다.

럭셔리 제품/웹GL/스크롤 스토리텔링 재현에서 사용자가 GPT Image 2, HeyGen, WebP/WebM 변환을 지시하면 CSS-only/문서점수 루프를 반복하지 않는다. `gpt-image-2-prompting/`를 우선 적용해 생성 이미지·영상 시도·WebP/WebM fallback·실제 페이지 반영·스크롤 캡처·레퍼런스 side-by-side 검증까지 한 번에 수행한다.

내레이션형 애니메이션에서 화면·자막·음성 맥락을 맞추고 정적 체감을 줄이는 QA 패턴은 참고. 사용자가 음성 품질을 지적한 세션에서는 최종 납품 전 `ttstudio-voice/`의 실제 청취 + 음성 커버리지 체크도 함께 수행한다.

브루탈리즘/다크 퓨처리즘/글래스모피즘/뉴모피즘처럼 스타일을 갈아끼울 수 있는 시멘틱 토큰 시스템은 참고. 장면 의미와 자막/내레이션 싱크는 유지하고 색상·표면·타입·모션만 토큰으로 교체한다. 실제 Maker Evan풍 Hermes 90초 영상에서 나온 Voicebox/맥락 QA/테마 토큰 교정 사례는 참고.

## 레퍼런스 채널 스타일 클론 / 토큰화

사용자가 특정 유튜브 채널 링크를 주고 “스타일을 학습”, “100% 클로닝”, “토크나이징”, “샘플 영상”을 요청하면 먼저 최소 10개 영상의 썸네일/내부 프레임을 수집해 스타일 토큰을 만든 뒤 샘플을 제작한다. 자세한 절차와 Pitfall은 참고.

## 레퍼런스 채널 스타일 토큰화 워크플로우

사용자가 특정 YouTube 채널/영상 스타일을 학습해서 애니메이션형 샘플 영상을 만들라고 요청하면, 단순 감상으로 끝내지 말고 최소 10개 영상 기준으로 **스타일 토큰화**를 수행한다.

- `yt-dlp`로 10개 이상 영상 메타데이터, 썸네일, 저해상도 내부 영상 샘플을 수집한다.
- 영상별 3~5개 내부 프레임을 ffmpeg로 추출하고 contact sheet를 만들어 시각 QA한다.
- 썸네일 스타일과 내부 영상 스타일을 분리해서 분석한다.
- 색상, 타이포, 자막 위치, SVG stroke, 여백, 장면 문법, 모션 타이밍을 숫자 토큰으로 정리한다.
- Remotion 또는 HTML+Playwright 캡처 템플릿으로 20~45초 샘플을 만든다.
- 생성 프레임 contact sheet를 다시 만들어 9.7/10 목표 루프를 돌린다.

자세한 절차와 명령은를 참고한다.

### 1단계: 리서치
- 병렬 에이전트 3개로 주제 리서치 (document-specialist)
- 결과를 `research/summary.md`에 종합
- 핵심 수치, "와" 포인트, 경쟁 차별점 정리

### 2단계: 대본 작성
- 씬 구성 (9개 기준, 후킹→본문→정리)
- **비전문가용 비유** 필수 (회사 비유, 어댑터 비유 등)
- **"제 관점에서"** 기획자 시점 해석 포함
- 전문 용어 → 일상 언어 변환
- 괄호 설명 금지, 숫자 한글화, 영문 한글 발음
- **기존 대본의 러닝타임 조정/별도본 요청이면 먼저 원본 대본 파일·직전 주제·저장 폴더를 확인한다.** 최근에 처리한 다른 파일/스킬/업로드 맥락으로 주제를 임의 전환하지 않는다. 예: “영상 러닝타임 15-20분 대본도 별도로”는 현재 대본(예: UiPath Maestro)을 압축/확장하라는 뜻일 수 있으므로, 관련 파일을 검색·읽은 뒤 같은 주제로 별도 파일을 작성한다.
- 한국어 TTS 납품용 내레이션은 말끝 품질을 우선한다. 사용자가 끝처리 끊김을 지적했거나 Voicebox 보이스를 쓸 때는 `합니다/됩니다/입니다` 같은 `다` 종결을 줄이고 `해요/돼요/이에요/거예요`처럼 자연스러운 구어체로 쓴다.
- 화면형 영상은 대본 문장마다 대응되는 시각 은유/오브젝트를 같이 설계한다. 최종 QA에서 **화면·내용·자막 맥락 일치**를 확인한다.
- `script/draft.md`에 저장, 사용자 승인 필수

### 3단계: TTS 청크 분할
- **50자 이하**로 분할 (필수, 초과 시 TTS 누락 발생)
- 끝에 `(...)` 싱글 트레일링 (마지막 청크 제외)
- 마침표는 `(...)` 앞에: `합니다.(...)`
- `script/tts-chunks.md`에 저장

### 4단계: 보이스 생성
- Voicebox 앱 실행 확인 (포트 자동 탐지)
- `scripts/tts-generate.py` + `tts-config.json` 실행
- 씬별 WAV + 전체 합본 + SRT 자막 생성
- 300ms 꼬리 패딩, 씬 내 0.4초 갭, 씬 간 0.8초 갭
- ⤳ skill: ttstudio-voice

### 5단계: HTML 시각화 제작
- EP 시리즈 스타일: 1920x1080, #111111 배경, Pretendard + JetBrains Mono
- 액센트 #FFC505, 뱃지 #28C840, 경고 #FF6B6B
- fadeUp/fadeLeft/fadeRight CSS 애니메이션 + 노이즈 오버레이
- 병렬 에이전트(executor)로 씬 분산 제작 (3개씩)
- `scenes/` 또는 `scenes-v2/` 디렉토리에 seg-XX.html로 저장

### 6단계: Playwright 캡처
- `capture.mjs` 스크립트로 headless 캡처
- **duration = 오디오 파형 기준** (대본 예상치 아님)
- 최종 영상 길이와 내레이션 커버리지를 따로 확인한다. 의도한 무음 아웃트로가 아니라면 마지막 8~12초처럼 보이스가 비는 구간은 설계 실수로 보고, 내레이션 추가/영상 단축/아웃트로 자막 보강 중 하나로 수정한다.
- CSS 애니메이션: pause + currentTime 수동 제어
- 마지막 15프레임 프로그래매틱 페이드
- ffmpeg libx264 CRF 18 인코딩 + concat 합본
- ⤳ skill: video-capture

### 7단계: CapCut 프로젝트 생성
- `scripts/capcut-project-gen.py` + config.json
- 비디오 + 오디오 배치 (자막은 SRT 수동 임포트)
- CapCut 샌드박스: Resources/에 파일 복사 필수
- ⤳ skill: capcut-project

## YouTube 채널 스타일 학습 / 재현 요청

사용자가 유튜브 채널 링크를 주고 “이 채널 스타일을 학습”, “애니메이션형 영상 스타일 재현”, “최소 N개 영상 확인”, “9.7점까지 반복”처럼 요청하면 워크플로우를 따른다.

사용자가 쇼츠 채널 벤치마킹, CapCut 자동 편집, Voicebox 보이스, Whisper 싱크 검증을 함께 요청하면,,를 따른다. 사용자가 YouTube/Shorts/Reels 링크를 주고 낮은 조회수 원인, 제목/썸네일 개선, 공유 상승 포인트, 해외 콘텐츠의 국내 후킹 리터치를 요구하면를 적용해 공개 메타데이터·동채널 비교·동주제 해외/국내 비교·썸네일 시각 요소·첫 3초/중반/후반 유지 구조를 분리 진단하고, 수정 제목 5안/썸네일 콘셉트 3안/첫 3초 훅 3안을 바로 산출한다. 벤치마킹/리서치 시작 전에는에 따라 “분석 가능한 채널” 선별 패스를 먼저 수행한다. 단순 고조회수/유명 채널보다 포맷·시청자·썸네일/오프닝·공개 메타데이터·반복 편집 문법을 해석할 수 있는 채널을 우선 표본화한다. AI 인사이트/바이브코딩/클로드코드/하네스 엔지니어링/AI 영상 제작/페이스리스/버추얼 인플루언서 채널군은의 3개 category lane과 query-lane 설계를 적용한다. 사용자가 영상 생성 하네스/자동 콘텐츠 파이프라인/코드베이스 재사용을 말하면 `~/Agents/auto-contents`와를 먼저 참조한다. 사용자가 GPT Image/OpenAI Images, Kling, Gemini Flash/Image/Nano Banana/Imagen/Veo, Story-to-Video/Image-to-Video, 극사실주의/버추얼 인플루언서 기반 하네스를 함께 말하면를 적용한다. 이 경우 Remotion/Hyperframe/HTML 렌더가 아니라 `research → script → shot cards → identity-anchored images → 3~5s I2V clips → TTS/SRT → CapCut editable draft`를 기본 구조로 둔다. AI 인플루언서/릴스처럼 일관된 인물이 필요한 작업은 장면 생성보다 먼저에 따라 캐릭터 턴어라운드/컴카드/표정 시트를 만든다. 이 경우 타 채널 영상을 공개용으로 100% 복제하지 말고, 성공 구조·편집 리듬·자막/보이스 싱크를 토큰화해 저작권 안전한 자체 영상 하네스로 구현한다. 지식창/패션탐정냥식 쇼츠는 특히 **소스 리서치/스크랩이 본질**이다. 해외 고조회수 롱폼·숏폼을 찾아 컷, 확대, 재배열, 2~3초 장면 전환 문법을 분석하고, 최종 작업물은 flattened MP4보다 CapCut editable draft를 우선 산출한다. **중요:** 유튜브 Shorts/Reels/TikTok류는 HTML/Remotion/Hyperframe식 웹페이지 렌더를 기본 시각 레이어로 쓰지 않는다. 실사/공식/라이선스 footage 또는 AI realistic media를 ffmpeg/CapCut으로 컷편집하고, 자막은 SRT/CapCut editable track으로 분리한다. 또한 footage montage를 만들기 전에 **전체 영상 단위의 기승전결·궁금증·긴장감·반전 구조**를 먼저 학습해야 한다. 사용자가 특정 채널 퀄리티를 요구하면 앞부분만 보지 말고 채널별 최소 20편 전체를 수집해 Whisper/구간별 텍스트/contact sheet/컷리듬을 분석한다. 자세한 기준은 참고. 실제 우주 쇼츠 파일럿의 반복 QA/CapCut/Voicebox/Whisper 사례는 참고. 로컬 AI 영상 생성 도구 판별에는 참고.

핵심 원칙:
- 최소 10개 영상의 썸네일과 내부 프레임을 분리 분석한다.
- 내부 영상 스타일과 썸네일 스타일을 섞지 않는다.
- 산출물은 스타일 블루프린트, Remotion/HTML 템플릿, 자체 평가 루프로 남긴다.
- 저작권/상표/원본 자산을 그대로 복제한다고 표현하지 말고, 분석 기반의 유사 스타일 시스템으로 안전하게 변형한다.

## 프로젝트 디렉토리 구조

```
projects/YYYY-MM-DD-{title}/
├── research/summary.md       # 리서치 종합
├── script/
│   ├── draft.md              # 대본
│   └── tts-chunks.md         # TTS 청크
├── voice/
│   ├── chunk-001~N.wav       # 청크별 WAV
│   ├── scene-01~N.wav        # 씬별 합본
│   ├── full-voice.wav        # 전체 합본
│   └── subtitles.srt         # SRT 자막
├── scenes[-v2]/
│   └── seg-01~N.html         # HTML 시각화
├── output[-v2]/
│   ├── seg-01~N.mp4          # 씬별 MP4
│   └── ep{N}-{title}.mp4     # 합본 MP4
├── tts-config.json           # TTS 설정
├── capcut-config.json        # CapCut 설정
└── capture.mjs               # 캡처 스크립트
```

## SRT 자막 스타일 (사용자 편집 기준)

자동 생성 SRT은 청크 단위(50자)지만, 최종 SRT은 사용자가 호흡 단위로 재편집:
- 평균 15자 / 2.2초
- 최소 2자~최대 31자
- 같은 문장 내 절 분리: 갭 0초
- 문장 사이: 0.3~0.4초 갭
- TTS 청크 1개 → 평균 3개 SRT 세그먼트

## 설치

```bash
bash ~/.claude/skills/create-video/setup.sh
```

## 의존성
- Python 3 + requests
- Node.js + playwright
- ffmpeg + ffprobe
- Voicebox 앱 (macOS)
- CapCut 앱 (macOS)
