---
name: video-content-visuals
description: Use when producing the full set of visual sources for a video from a script — insert/B-roll keyframes, character art, diagrams, motion clips — that must all share one consistent mood, in ANY style (illustration, manga, photoreal, graph, infographic). 영상 콘텐츠 비주얼 소스 제작, 이미지·영상 소스 일관 생산, 캐릭터/다이어그램/인서트, 무드 잡고 씬별 제작. Style-agnostic master workflow.
---

# Video Content Visual Sources (범용 마스터)

## Overview
영상 한 편에 들어갈 **모든 비주얼 소스**(인서트 키프레임 · 캐릭터 · 다이어그램 · 모션 클립)를 **하나의 통일된 무드로 일관 생산**한다. 스타일 무관 — 만화·컬러 웹툰·초실사·그래프 글로우·인포그래픽 어떤 톤이든.
**최종 goal**: 사용자가 채널/대본/무드만 정하면, 바로 영상에 넣을 수 있는 **톤이 일관된 비주얼 세트**를 받는다.
ima2(이미지) · Kling/Veo(영상) · HTML(텍스트)을 조합해 달성. ima2 CLI 세부·Kling 모션 형식은 **REQUIRED SUB-SKILL: video-insert-keyframes-ima2** 참조.

## 도구 맵 (무엇을 무엇으로)
| 산출물 | 도구 | 자동화 |
|---|---|---|
| 정지 이미지 (키프레임·캐릭터·씬) | **ima2-gen** (GPT Image 2, 127.0.0.1:3333) | 자동 (CLI) |
| 영상 클립 (이미지→영상) | **Kling I2V** | 수동 (프롬프트 전달, 사용자가 생성) |
| 영상 클립 (대안, 자동) | **Veo3** (`scripts/produce.py`) | 자동 |
| 텍스트 다이어그램·인포그래픽 | **HTML/CSS + 렌더** | 자동 |
| 합성·자막·오버레이 | CapCut | 수동 |

## 워크플로 (순서 고정)
1. **대본 → 비주얼 구간 분할** — 각 구간이 "무엇을 보여주나" 한 줄로.
2. **무드 결정 + 샘플 1컷 먼저 확정** — 전체 생산 전 대표 1컷으로 톤·색·그림체 확정받기. (무드가 자주 바뀐다 — 전량 재생산 방지의 핵심)
3. **무드 통일 + 내용 구체화** — 톤은 고정, 소재는 발화 내용이 보이게(인물·오브젝트·UI·메타포). 추상 일변도 금지.
4. **스타일별 제작 경로** — 이미지=ima2 / 영상=Kling·Veo / 텍스트=HTML / 캐릭터=ref 고정.
5. **검증** — 생성본을 Read로 시각 확인. 자기 보고만으로 완료 선언 금지.
6. **산출 정리** — 키프레임 + Kling 모션 프롬프트(`video-prompts.md`) + 다이어그램.

## 무드 라이브러리 (검증된 톤 — 프롬프트 키)
각 무드는 **모든 컷에 동일 DNA**를 내장해 통일. (전부 `no readable text, no letters, no watermark, no logos` 포함; 16:9 영상 / 캐릭터 세로 1024x1536)
- **흑백 잉크 망가** — `high-contrast black-and-white ink, 1980s manga line-art, bold black fills, white background`
- **검정 배경 흰 선 만화** — `pure black background, clean white ink linework, cinematic manga line-art (inverted)` (디테일은 별도 만화 무드 적용)
- **컬러 웹툰/애니** — `clean modern Korean webtoon, soft cell shading, appealing colors`
- **초실사 사진** — `real photograph, shot on Sony Alpha 7 + 85mm f/1.4, natural skin texture with pores, lifelike, shallow DOF; NOT illustration / NOT 3D / NOT CG, no plastic skin`
- **그래프 글로우** — `dark navy void, glowing nodes + links (Obsidian graph), purple+cyan glow` (단 추상 노드만 반복하면 내용 전달 실패 — 구체 소재와 섞을 것)
- **8비트 픽셀** — `retro 8-bit pixel art, blocky, limited warm palette`
- **밝은 인포그래픽** — HTML/CSS로 제작 (아래 텍스트 규칙)

## 캐릭터 일관성
- **ref 고정**: 첨부 이미지를 `references/`에 저장(채팅 첨부는 직접 파일화 불가 → 사용자에게 저장 요청) → `--ref`(최대 5장).
- **베이스 먼저 확정** → 그 베이스를 ref로 다양한 씬/포즈 확장.
- **스타일 변환**(웹툰↔실사 등): 원본 + 직전 버전을 **둘 다 ref**로 넣어 정체성 유지하며 톤만 전환.
- **형태 보존(색만 변경)**: `gen`이 아니라 `edit` (gen은 형태를 재해석함).

## 초실사 리얼리즘 (CG티 제거)
일반 "photorealistic"는 CG·일러스트티가 남는다. 진짜 사진엔 카메라/렌즈/질감을 명시:
`shot on a Sony Alpha 7 full-frame camera with an 85mm f/1.4 lens, natural realistic lighting, true-to-life skin texture with natural pores and subtle imperfections, lifelike eyes, shallow depth of field, soft bokeh — a genuine real human photograph, NOT an illustration, NOT a 3D render, NOT CG, no skin smoothing, no plastic skin.`

## 한글 텍스트 (절대 규칙)
ima2(GPT Image)는 **한글 다량 텍스트를 못 만든다**(거의 깨짐, 영어도 불완전). 텍스트 인포그래픽/다이어그램은:
- **HTML/CSS로 제작 → 렌더**(텍스트=진짜 폰트, 100% 정확). 무드도 CSS로 맞춤(예: 검정배경+흰선+손글씨 `Gaegu` = 만화 톤; 밝은 파스텔 = 깔끔 톤).
- 렌더: `python3 -m http.server <port>` 띄우고 playwright로 `http://localhost`로 navigate(폰트 `document.fonts.ready` 대기) → fullPage screenshot. (`file://`는 차단됨)
- 또는 글자는 Kling/ima2 빼고 **CapCut 오버레이**로만.

## Kling 모션 프롬프트 (이 사용자 선호 — 고정)
이미지별 자체완결. **공통/네거티브 섹션 분리 금지** — 각 풀 프롬프트에 모션·"keep style/identity unchanged"·네거티브 전부 내장. 외형은 start frame이 가지므로 **모션만**(1 액션 + 1 카메라무브, 약한 동사). 상세 형식·예시는 video-insert-keyframes-ima2 참조.

## 폴더 규칙
`projects/{프로젝트}/{날짜}/` (기획·video-prompts) · `projects/{프로젝트}/references/` (레퍼런스·베이스) · `.../keyframes/` 또는 `.../characters/` (생성본) · `.../diagrams/` (HTML 다이어그램). 무드/버전 폐기본은 사용자 확인 후 정리.

## 다른 에이전트를 위한 핵심
- **무드 샘플 먼저 확정**(전량 재생산 방지) · **내용 구체화**(추상 일변도 금지) · **Read로 시각 검증 후 보고**.
- 비율은 사용자 지정 우선(추정 금지). ima2 가로 최대 `1536x1024`.
- CLI 타임아웃은 실패 아님(서버는 계속 생성 → `~/.ima2/generated/`에서 복사).

## Common Mistakes (실전 실패 기반)
| 실수 | 방지 |
|---|---|
| 무드 확정 전 전량 생성 | 샘플 1컷 먼저 확정 |
| 추상 노드/그래프만 반복 → 내용 안 보임 | 발화 내용 구체화 |
| 한글 텍스트를 ima2로 | HTML 렌더 / CapCut 오버레이 |
| "photorealistic"인데 CG·일러스트티 | Sony A7+렌즈+피부질감+NOT CG 명시 |
| 캐릭터가 변형 | ref 고정, 베이스 먼저, 변환은 dual-ref, 색만은 edit |
| ima2 사이즈/옵션 docs만 보고 단정 | `--help`·`capabilities --json` 확인 |
| 경로 검증을 프로젝트 루트 기준만 | 참조 파일(md) 위치 기준 상대경로로 확인 |
| 생성본 안 보고 "완료" | Read 시각 검증 후 보고 |
