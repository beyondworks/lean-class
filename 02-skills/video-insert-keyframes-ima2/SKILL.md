---
name: video-insert-keyframes-ima2
description: Use when turning a video script into insert/B-roll keyframe images with the local ima2-gen CLI (GPT Image 2) and then writing Kling image-to-video motion prompts. Triggers — 영상 인서트 이미지/키프레임 만들기, 대본 기반 B-roll, ima2-gen 이미지 생성, 발화 내용 시각화, Kling 영상 프롬프트, 무드 잡고 씬별 이미지.
---

# Video Insert Keyframes via ima2-gen

## Overview
대본의 각 발화 구간을, 토킹헤드 영상 중간에 끼울 **인서트 B-roll 키프레임**으로 만든다. 로컬 `ima2-gen` CLI(GPT Image 2)로 이미지 생성 → Kling I2V 모션 프롬프트로 마감.
핵심 원칙: **무드는 통일, 소재는 발화 내용을 알아볼 수 있게 구체화.**

## Workflow (순서 고정)
1. **대본 → 씬 분할** — 발화를 12~16개 인서트 구간으로. 각 구간이 "무엇을 시각화하나"를 한 줄로.
2. **무드 샘플 먼저** — 전체 생성 전, 대표 1컷으로 톤·색·그림체 샘플 생성 → **사용자 확정**. 확정 전 전체 생성 금지.
3. **구체화 기획** — 각 씬을 발화 내용이 보이는 구체적 장면/오브젝트/UI/메타포로. 추상 일변도(노드·그래프만) 금지.
4. **배치 생성** — ima2로 8컷씩 병렬, 16:9.
5. **검증** — 생성본을 Read로 시각 확인 (톤 일관·내용 전달·글자 깨짐). 자기 보고만으로 완료 선언 금지.
6. **모션 프롬프트** — `video-prompts.md`에 컷별 Kling I2V (넣을 이미지 + 풀 프롬프트).

## ima2-gen CLI 핵심
```bash
ima2 ping                    # 서버(127.0.0.1:3333) 헬스
ima2 capabilities --json     # 지원 모델·quality 확인 (추측 금지)
# 생성: 16:9, 고품질, 타임아웃 넉넉히, 출력 지정
ima2 gen "<프롬프트>" --size 1536x1024 -q high --timeout 300 -o keyframes/sNN.png
# 캐릭터 일관성: 참조 이미지 최대 5장
ima2 gen "<모션/장면만>" --ref char.png --size 1536x1024 -q high -o out.png
# 형태 보존(색만 변경): gen 대신 edit (gen은 형태를 재해석함)
ima2 edit in.png --prompt "recolor only, keep exact shape/silhouette" --quality high -o out.png
```
- **배치 병렬**: 여러 `ima2 gen ... &` 뒤 `wait` (서버 동시 ~8).
- **CLI 타임아웃**: 기본 180s. ref 다수·고품질은 초과 → `--timeout 300`. 초과해도 **서버는 계속 생성**하므로 `ima2 ps`로 확인 후 `~/.ima2/generated/`의 최신 파일을 복사.
- **사이즈**: 임의 픽셀(예 1920x1080) OpenAI가 거부. gpt-image 가로 최대 `1536x1024`. 옵션은 `ima2 gen --help`로 확인 — **docs만 보고 단정 금지**.

## 핵심 규칙
- **무드 샘플 먼저, 확정 후 전체.** 16컷 다 만들고 무드가 틀리면 전량 재생성된다.
- **구체화 > 추상.** 같은 추상 모티프(노드/그래프)만 16컷이면 발화 내용이 안 보인다. 인물·오브젝트·UI·메타포로 "무슨 말인지" 보이게.
- **한글 텍스트는 ima2로 못 만든다** (영어도 불완전, 한글 다량은 깨짐). 텍스트 인포그래픽/다이어그램은 **HTML/CSS로 만들어 렌더**(텍스트=진짜 폰트), 또는 글자는 **CapCut 오버레이**로만. 모든 프롬프트에 `no readable text, no letters, no numbers` 내장.
- **캐릭터 일관성**: 채팅 첨부는 직접 파일화 불가 → 사용자에게 `references/`에 저장 요청 → `--ref`로 고정. **베이스 1장 먼저 확정** 후 그걸 ref로 씬 확장. 형태 보존이 핵심이면 `gen`이 아니라 `edit`.
- **비율 우선**: 사용자가 지정한 비율(16:9 등)을 추정으로 바꾸지 않는다.

## 모션 프롬프트 형식 (이 사용자 선호 — 고정)
컷별 자체완결. **공통/네거티브 섹션을 따로 만들지 말 것** — 각 풀 프롬프트에 전부 내장.
```
### S01 · "한국어 제목"
- 넣을 이미지 (Start Frame): keyframes/sNN.png
- 길이 / 비율: 4s / 16:9
- 풀 프롬프트:
[모션만 · 1 액션 + 1 카메라무브 · 약한 동사(slow/gently/gradually) · "keep the ... style and identity unchanged" · no added text, no letters, no warping, no identity drift, no flicker 까지 내장]
```
외형은 start frame이 가지므로 **모션만** 쓴다. Kling은 미세 모션에 강하고 격한 동작·다중 캐릭터 일관성에 약하다.

## 폴더 규칙
`projects/{프로젝트}/{날짜}/` (기획·video-prompts) · `projects/{프로젝트}/references/` (레퍼런스·베이스) · `.../keyframes/` (생성본). 폐기 버전은 사용자 확인 후 정리.

## Common Mistakes (실전 실패 기반)
| 실수 | 방지 |
|---|---|
| 무드 확정 전 전체 생성 | 샘플 1컷 먼저 확정받기 |
| 추상 노드/그래프만 반복 → 내용 안 보임 | 발화 내용 구체화(인물·UI·오브젝트·메타포) |
| 한글 텍스트를 ima2로 시도 → 깨짐 | HTML/CSS 렌더 또는 CapCut 오버레이 |
| ima2 사이즈/옵션을 docs만 보고 단정 | `--help`·`capabilities --json` 확인 |
| CLI 타임아웃을 생성 실패로 오인 | 서버는 계속 생성 → generated/에서 복사, `--timeout` 상향 |
| 캐릭터가 매 컷 변형 | `--ref` 고정, 베이스 먼저 확정, 색만이면 `edit` |
| HTML 렌더 시 `file://` 차단 | `python3 -m http.server` 띄우고 `http://localhost`로 navigate |
| 생성본 안 보고 "완료" 선언 | Read로 시각 검증 후 보고 |
