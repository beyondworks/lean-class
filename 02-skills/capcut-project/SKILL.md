---
name: capcut-project
description: CapCut 프로젝트를 코드로 자동 생성. "캡컷", "CapCut", "프로젝트 생성", "타임라인" 키워드에 트리거.
user_invocable: true
---

# CapCut Project Generator

MP4 비디오 + WAV 오디오 → CapCut 프로젝트 자동 생성.
CapCut을 열면 프로젝트 목록에 바로 표시됨.

쇼츠/릴스/틱톡의 source-scrap 편집에서는 CapCut을 최종 편집 중심으로 둔다. ffmpeg는 원본에서 2~3초 클립을 자르고 9:16 프록시/preview를 만드는 보조 도구이며, 최종 산출은 가능한 한 CapCut editable draft + SRT + source manifest로 남긴다.

## 사용법

우선순위:
1. 프로젝트/레포에 검증된 CapCut generator가 있으면 그것을 먼저 사용한다. 사용자 영상 생성 하네스는 `~/Agents/auto-contents`를 참조하고, 그 repo context의 CapCut 지침/기존 generator를 우선 확인한다.
2. 현재 skill의 간단 generator는 fallback으로 사용한다.
3. `draft_info.json`을 완전 수동 작성하는 방식은 마지막 수단이며, 반드시 CapCut에서 실제 목록 노출/열림을 검증한다.

```bash
python3 scripts/capcut-project-gen.py config.json
```

config.json:
```json
{
  "name": "프로젝트명",
  "fps": 30,
  "canvas": { "width": 1920, "height": 1080 },
  "video": [
    "/abs/path/seg-01.mp4",
    "/abs/path/seg-02.mp4"
  ],
  "audio": [
    { "path": "/abs/path/voice-01.wav", "start": 0 },
    "/abs/path/voice-02.wav"
  ]
}
```

- **video**: 경로 배열 → 타임라인에 순차 배치 (duration ffprobe 자동 감지)
- **audio**: 경로 또는 {path, start(초)} → start 생략 시 이전 오디오 뒤에 순차 배치
- 자막(SRT)은 CapCut에서 직접 임포트 (text material 외부 생성 불가)

## 핵심 규칙

### 샌드박스 파일 복사 필수
CapCut은 macOS 샌드박스 앱 (`com.lemon.lvoverseas`). `~/Movies/CapCut/` 외부 파일에 접근 불가.
스크립트가 자동으로 프로젝트 `Resources/` 폴더에 복사한다.

### Whisper 기반 싱크 우선
쇼츠/내레이션 프로젝트는 대본 예상 시간이 아니라 실제 음성 파형과 Whisper 전사 타이밍을 기준으로 타임라인을 만든다.
1. Voicebox/TTS로 `full.wav` 생성
2. `whisper --language ko --word_timestamps True`로 segment timing 추출
3. Whisper segment 기준으로 SRT와 씬 duration 생성
4. 최종 MP4를 다시 Whisper로 전사해 자막/보이스/컷 싱크를 검증

### CapCut schema는 버전 검증 필요
CapCut draft JSON은 앱 버전에 따라 필드가 바뀐다. 새 generator를 만들 때는 최소 draft를 생성한 뒤 CapCut에서 실제로 열리는지 확인하고, 안 열리면 같은 버전에서 만든 정상 프로젝트의 `draft_info.json`/`draft_meta_info.json`과 diff해서 필드를 보정한다. `root_meta_info.json`은 전역 인덱스라 파괴적으로 덮어쓰지 말고 백업/병합한다.

생성 후 검증은 체크리스트를 따른다. 특히 SRT가 `Resources/`에 복사되지 않았더라도 `draft_info.json`에 text track/materials로 변환되어 있으면 정상일 수 있으므로, 파일 존재만으로 실패 처리하지 말고 track/material counts와 `draft_meta_info.json` SRT 참조를 함께 확인한다.

### 자막은 SRT/CapCut editable track 우선
text material의 content JSON을 외부에서 생성하면 CapCut이 파싱하지 못하는 경우가 많다.
SRT 파일을 CapCut에서 직접 임포트하거나, 현재 CapCut 버전의 정상 text material schema를 먼저 추출해 검증한다.

쇼츠 footage montage에서는 ffmpeg `drawtext`로 한국어 자막을 바로 burn-in하지 않는다. 폰트/필터 파싱이 깨지거나 영상 비율·가독성을 망칠 수 있고, 사용자는 CapCut에서 수정 가능한 자막 트랙을 선호한다. 먼저 clean footage + voice + SRT/CapCut track으로 draft를 만들고, 스타일 확정 후 최종 export에서만 burn-in을 고려한다.

### Source-scrap Shorts는 CapCut draft가 source of truth
지식창/패션탐정냥식 쇼츠처럼 해외 고조회수 영상의 문법을 분석해 2~3초 컷·확대·재배열로 만드는 작업은 flattened preview MP4를 최종물로 보지 않는다.
- `clips/`: 원본/공식/라이선스/AI 생성 asset에서 잘라낸 9:16 편집 클립
- `draft_info.json`/`draft_meta_info.json`: CapCut editable timeline
- `*.srt`: CapCut import용 자막
- `edit_manifest.json`: URL, source policy, start time, duration, scene purpose, model/prompt, QA status
- `contact-sheet.jpg` 또는 `contact-sheet.pdf`: preview에서 추출한 얼굴/손/텍스트/물리/조명/카메라 리듬 QA 시트
- `qa/`: Whisper 재전사, sync drift, slop report 등 검수 산출물
- `preview.mp4`: 검토용 proxy

CapCut이 열렸는지는 `open -a CapCut <project-dir>` 후 `pgrep -fl "CapCut|lveditor|com.lemon"`와 프로젝트 `Resources` 파일 수로 확인한다. 그러나 앱 프로세스와 draft 파일 존재만으로 홈 프로젝트 목록 노출을 보장하지 않는다. 사용자가 스크린샷을 보내면 실제 목록에 프로젝트가 보이는지 확인하고, 안 보이면 root/index 메타 등록 문제로 판단해 “앱은 열렸지만 목록에는 아직 안 보인다”고 명확히 말한 뒤 CapCut 재실행/목록 새로고침/프로젝트 폴더 import/root_meta 병합을 시도한다.

### AI 영상 생성 QA bundle
Kling/Seedance/Veo/Runway/Pika/Hailuo/Luma/Higgsfield/Nano Banana/GPT Image 같은 모델을 쓸 때도 최종 운영 단위는 CapCut draft다. 모델별 output은 소재일 뿐이며, `edit_manifest.json`에 source URL/권리 상태/model/prompt/timeline start/scene purpose/QA status를 남긴다. preview export 후 contact sheet를 만들고 얼굴·손·텍스트·물리·조명·카메라·편집 리듬을 검사한다. voice/SRT 싱크는 가능하면 Whisper 재전사로 확인하고 0.25초 이상 drift는 수정 대상으로 표시한다. 세부 예시는를 참고한다.

## draft_info.json 구조

```
tracks[] → segments[] → material_id → materials.videos[]/audios[]
                    └→ extra_material_refs[] → speeds/canvases/...
```

- 시간 단위: 마이크로초 (1초 = 1,000,000)
- Video segment refs: speeds, placeholder_infos, canvases, sound_channel_mappings, material_colors, vocal_separations (6개)
- Audio segment refs: speeds, placeholder_infos, beats, sound_channel_mappings, vocal_separations (5개)

### 필요 파일 3개
1. `draft_info.json` — 타임라인 전체 데이터
2. `draft_meta_info.json` — 프로젝트 메타 + 소재 임포트 목록
3. `root_meta_info.json` — 프로젝트 인덱스 (CAPCUT_DRAFTS 루트, 업데이트)

### 프로젝트 경로
`~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`

## CapCut 앱 정보
- Bundle ID: `com.lemon.lvoverseas`
- 스택: Qt/QML(UI) + CEF(웹패널) + C++ 엔진 + FFmpeg + ByteDance AI
- 버전: 8.3.0

## 의존성
- Python 3, ffmpeg, ffprobe
