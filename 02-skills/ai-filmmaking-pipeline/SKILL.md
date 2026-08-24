---
name: ai-filmmaking-pipeline
description: AI 영화·영상 샷을 Higgsfield Cinema Studio·Seedance·Kling으로 제작할 때 적용하는 검증된 프로덕션 파이프라인 방법론(Higgsfield Academy "The AI Filmmaking Pipeline" 수료 기반). 로케이션·캐릭터·소품 생성, 캐릭터 일관성, must-preserve 모델 선택, slop 방어, Seedance/Kling 모션 테스트, @자산 네이밍까지. 트리거 — "AI 영화", "AI 영상 파이프라인", "Higgsfield로 영상 만들어줘", "Seedance 샷", "시네마틱 영상 제작", "캐릭터 일관성 유지", "로케이션 생성", "slop 잡아줘/방어", "영화 씬 만들어줘", "Cinema Studio", "Filmmaker Grant 쇼릴", "캐릭터 시트로 영상".
---

# AI Filmmaking Pipeline

## Overview

아이디어 → 완성된 Seedance/Kling 샷을, 매번 같은 순서·같은 품질 기준으로 만드는 프로덕션 파이프라인. 핵심 신념: **Proof가 게이트다 — 모델 이름·프롬프트는 약속일 뿐, 픽셀이 증거.** 결함을 느끼기만 하지 말고 이름을 붙여라(name the flaw).

출처: Higgsfield Academy 수료 학습 로그(`references/higgsfield-academy-learning-log.md`). 전 단계 상세 규칙은 `references/pipeline-playbook.md`.

## When to Use

- Higgsfield(Cinema Studio) / Kling MCP로 이미지·영상 샷을 만들 때
- 여러 샷에서 **캐릭터·로케이션 일관성**을 유지해야 할 때
- 생성물이 어딘가 어색한데(=slop) 원인을 짚어야 할 때
- 캐릭터 시트·로케이션 플레이트·소품을 **재사용 자산(@Element)**으로 만들 때
- Filmmaker Grant 쇼릴처럼 **씬 하나를 프로젝트 구조부터 완성 샷까지** 뽑을 때

**When NOT to use**: 단발 이미지 한 장(파이프라인 불필요) → 바로 생성. 도구별 프롬프트 문구 최적화만 필요하면 하위 스킬로: 캐릭터 시트 문구는 `ductape`, Kling I2V 문구는 `kling-image-to-video`.

## 고정 4단계 (순서 불변)

**Think → Setup → Generate → Test.** 단계는 버튼이 아니라 **핸드오프의 연쇄** — 다음 단계가 신뢰할 구체적 산출물을 남겨야 그 단계가 끝난 것. 실패하면 **가장 이른(초기) 깨진 핸드오프**를 고쳐라(하류 증상만 닦지 말 것).

| 단계 | 남기는 산출물(핸드오프) |
|---|---|
| **Think** | 합의된 brief(.md): 샷·세계·캐스트·소품·제약 + decision log |
| **Setup** | 프로젝트 + locations/characters/props 폴더 + 하나의 네이밍 계약 |
| **Generate** | 검사→승인→이름 붙인 재사용 `@loc_/@char_/@prop_` Element |
| **Test** | 모션 테스트 + 진단(승인 or "어느 소스로 되돌릴지") |

**로케이션부터 만들어라** — 장소가 샷의 토대이자 캐릭터 성립 여부의 시험대.

## 핵심 원칙 (Quick Reference)

1. **Proof, not promises** — 모델 평판은 "무엇을 시도할지"만. 눈앞 픽셀이 통과/재실행을 결정. 요청 안 한 변화도 전수 점검.
2. **네이밍**: `@type_project_name` (`@loc_HG_museum_front`, `@char_HG_jaxx`, `@prop_HG_phone`). 멀티워드는 언더스코어. type+project가 검색을 신뢰성 있게 만듦.
3. **프롬프트 = 6결정 조립**: Subject·Action·Setting·Light·Camera/Motion·Constraints. 품질 단어("beautiful")보다 구체적 명사("weathered wood siding"). 결정 하나 바꾸면 전체 프롬프트 재작성(diff 금지).
4. **모델은 must-preserve로 선택** (오늘의 랭킹 이월 금지): Soul Cinema=분위기/캐릭터 생성, GPT Image 2=텍스트/소품/정밀, Nano Banana Pro=대담한 편집(생성·로케이션 금지), Seedream 4.5=텍스처 보존. → 표 상세: 플레이북.
5. **로케이션**: geography before style · 하나의 동기 광원 · 앵커 오브젝트로 블로킹 · 3/4 뷰 후 리버스.
6. **캐릭터 시트**: 포트레이트 25~30% · catchlight 필수 · off-frontal · grey(#3a3a3c) 배경 · 전신 패널 머리 크롭 · 게임 렌더 룩 금지.
7. **편집은 수술**: 바뀐 패치만 원본에 마스크. **편집 위 재편집 금지**(전체 재렌더가 slop을 복리로 누적).
8. **slop 4 tell**: 전환 없는 빛(flat black) · 그럴듯하나 깨진 오브젝트 · 국소 논리 붕괴 · 기름진 텍스처.
9. **Test가 결승선**: 한 번에 한 변수만. 실패가 **source asset**인지 **motion direction**인지 진단. %로 승인 불가.
10. **모더레이션 현실**: 사람 얼굴 포함 생성은 NSFW/IP 필터에 걸릴 수 있음 → 입력 조정(무인 로케이션+소품 등).

## MCP 도구 매핑

- **Higgsfield**: `mcp__higgsfield__generate_image` / `generate_video` / `models_explore`(모델 추천) / `media_upload`·`media_import_url`(레퍼런스) / `upscale_*`·`outpaint_image`·`remove_background`(수술적 편집) / `job_status`. 모델명 불확실하면 먼저 `models_explore(action:'recommend')`.
- **Kling**: `mcp__kling__who_am_i`(먼저 호출, 파라미터 규격 확인) → `text_to_image` / `image_to_image` / `text_to_video` / `image_to_video` / `file_upload`. **매 job이 과금** — 시험 삼기 금지, 불확실하면 먼저 질문.
- 두 백엔드 모두 위 10원칙(특히 proof-gate·slop·test-before-commit)이 동일하게 적용됨.

## Marketing Studio 운용

광고·UGC·제품 영상을 **실제로 발주**할 때의 함정(아바타가 조용히 바뀜, NSFW 오차단 어휘, 한국어 대사
훼손, 상품 URL 임포트 실패, 크레딧·시간 예산)은 **`higgsfield-mcp-ops` 스킬**에 있다. 이 스킬은
"어떻게 잘 찍나", 그쪽은 "왜 실패했고 어떻게 피하나".

## 상세 규칙

전체 레슨 정제본은 **`references/pipeline-playbook.md`** 를 읽어라 — 모델 선택 전체 표, 로케이션 6-lock, 캐릭터 시트 프롬프트 템플릿, slop 모델별 지문, Seedance 진단 트리, Leera 4-D 프롬프트법, 캡스톤 워크플로가 들어 있다.
