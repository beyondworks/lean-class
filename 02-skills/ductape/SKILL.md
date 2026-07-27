---
name: ductape
description: GPT Image 2(덕테이프) 캐릭터 시트·인물 이미지 프롬프트 최적화. AI 인플루언서/버추얼 모델의 얼굴·의상·표정·각도 일관성을 단일 프롬프트로 강제. 트리거 — "캐릭터 시트", "GPT Image 2 프롬프트", "AI 인플루언서 캐릭터 만들어줘", "AI 모델 생성", "덕테이프", "ducktape", "character sheet", "동일 캐릭터 다른 의상/표정/포즈", "버추얼 모델 이미지", "ChatGPT 이미지 캐릭터", "Nano Banana 캐릭터" (대안 도구도 매핑).
---

# Ducktape Character Sheet — GPT Image 2 캐릭터 시트 프롬프트 최적화

## Session-specific reference pointers

- `references/2026-07-04-real-beauty-not-conceptual.md` — **⚠️ 최우선 교정 ({{OWNER_NAME}} 2026-07-04): "컨셉 ≠ 미모".** 역할·의상·소품·배경 같은 conceptual/persona 설정은 얼굴을 예쁘게 만들지 않는다. 실제 예쁨/잘생김은 오직 ①얼굴 이목구비 DNA(6축) ②미모 명시적 강지정(idol/actor급) ③비-프로 카메라+imperfection ④미모 다이얼 상단값에서만 온다. "다 비슷하다"=평균수렴 슬롭 → 6축 distinct DNA 필수. 인물 생성 전 반드시 이 파일의 게이트를 통과시켜라. 근거: 레벨10 마스터 `$HOME/Agents/Image-gen/research/10-vi-2026/00-MASTER-vi-gpt-image2-level10.md`.
- `references/seoian-lean-company-agent-anchor-lessons.md` — Seo-Ian/lean-company recurring office-worker anchor correction: preserve clean v1-like Korean startup casting, avoid abstract worldbuilding terms in generation prompts, and separate agent characters with visible styling/props/context rather than harsh anti-slop face edits.
- `references/2026-05-28-lean-company-agent-v1-beautified-direction.md` — follow-up correction for 효일·효리·효삼·효나·효정: keep v1 personas, upgrade to attractive Korean startup-coworker casting, and differentiate via hair/wardrobe/expression/props rather than rough anti-beauty face edits.

> **🚦 인물/캐릭터 생성 전 강제 게이트 (2026-07-04):** ①프롬프트에 **얼굴 이목구비 DNA(6축: 얼굴형·눈·코·입·턱·피부)**가 있나 — 없으면 slop. ②**미모를 명시적으로(K-idol/actor급) 지정**했나 — 컨셉·의상만으로 안 예뻐진다. ③같은 성별 세트면 **6축 값이 인물마다 다른가** — 아니면 평균수렴. ④**비-프로 카메라+imperfection**으로 진짜 사람인가. ⑤실측 커뮤니티 verbatim(BubbleBrain 35mm film / WolfRiccardo RAW)을 이식했나. 상세: 위 real-beauty 파일 + 레벨10 마스터 §4·§7.

## 0. 이 스킬은 언제 발동되나

사용자가 "AI 인플루언서를 만들고 싶다", "캐릭터 시트가 필요하다", "같은 사람을 여러 씬에 쓰고 싶다" 종류의 요청을 하면 즉시 이 스킬을 호출하라.

**대상 모델**: GPT Image 2 (=ChatGPT Images 2.0, 별명 "덕테이프"). ChatGPT Plus/Pro에 내장. API는 `gpt-image-2`.
**왜 GPT Image 2인가**: ① 한글 텍스트 99% 정확 ② 1-shot multi-panel 픽셀 일관성 ③ Thinking 모드로 18 패널 단일 출력. 한글 라벨·자막을 캐릭터와 함께 한 컷에 박을 수 있는 유일한 옵션. ([상세]($HOME/Agents/Image-gen/research/01-gpt-image-ducktape.md))

대안 도구 결정 룰:
- **한글 텍스트 노출 필수 + 캐릭터 1-shot 시트** → GPT Image 2 (덕테이프)
- **단일 인물 사진의 재맥락화·합성 (몇 초)** → Nano Banana 2 (Gemini 2.5 Flash Image)
- **로컬 정밀 편집·텍스트 in-place 수정** → FLUX Kontext [pro/max]
- **무한 재현 + 영구 캐릭터** → SDXL/SD3 + LoRA 학습 (30-50장, 1-2h)

## 1. 워크플로 (사용자 요청 → 최종 프롬프트)

```
1. 페르소나 정보 수집 (없으면 5질문)
2. 5-튜플 DNA 잠금
3. 작업 유형 결정 (시트 vs 씬)
4. 템플릿 선택 + 프롬프트 합성
5. 사용자에게 출력 (그대로 ChatGPT에 붙여넣기 가능한 형태)
```

### 1.1 페르소나 수집 (정보 부족 시 한 번에 묻기)

```
다음 5가지만 빠르게 알려주세요:
1. 나이/성별/인종 (예: 24세 한국 여성)
2. 니치 (먹방/뷰티/패션/피트니스/ASMR/라이프스타일)
3. 시그니처 (예: 핑크 트랙수트 + 갈색 긴 머리)
4. 사용처 (Reels 9:16 / 포트레이트 4:5 / 캐러셀 1:1)
5. 한글 텍스트 노출 필요 여부 (있으면 verbatim 텍스트도)
```

## 2. 캐릭터 일관성의 5대 메커니즘 (반드시 적용)

이 5개가 빠지면 face drift·outfit drift 발생.

1. **5-튜플 캐릭터 DNA**: `age + ethnicity + hairstyle + iconic features + clothing` — 매 프롬프트마다 동일하게 prefix로 박는다
2. **5-부 구조 (fal.ai 공식)**: `Scene / Subject / Important details / Use case / Constraints`
3. **Anchor verbatim 반복**: "EXACT same face, EXACT same hair, EXACT identity from reference image. No identity change." — 매 컷에 한 번 더 적는다
4. **이미지 역할 라벨링**: `Image 1: base scene to preserve. Image 2: jacket reference. Image 3: pose reference.` (최대 16장 첨부 가능)
5. **자연어 negative**: GPT는 SD식 negative token이 없으므로 본문에 자연어로 `no plastic skin, no airbrushing, no watermark, no extra limbs, no identity change`

### 시드 (API만 가능)
Web ChatGPT에서는 시드 노출 X. OpenAI Images API 호출 시 `extra_body={"seed": 20260421}` 로 lighting·composition 재현. 사용자가 ChatGPT Plus만 쓴다면 시드 안내 생략하고 reference image 재첨부 전략으로 우회.

## 3. 6가지 시트 템플릿 (작업 유형별)

선택 가이드:
- **첫 캐릭터 만들 때** → A. 베이스 포트레이트 1장
- **여러 의상 필요** → B. 2x3 의상 시트
- **표정 리액션 컷 대량** → C. 3x3 표정 시트
- **풀바디 다각도** → D. 8-view 턴어라운드
- **씬별 스토리보드** → E. 2x2 / 1x4 스토리보드
- **광고/협찬 (브랜드 로고 픽셀 락)** → F. 덕테이프 verbatim 패턴

각 템플릿은 `references/templates.md`에 상세 (실제 프롬프트 + 출력 예시 + 평점). 처음에는 SKILL.md 안의 압축 버전만 보여주고, 사용자가 깊이 원하면 references를 Read하라.

### A. 베이스 포트레이트 (모든 후속 작업의 anchor)

```
Photorealistic medium close-up portrait of a [AGE]-year-old [ETHNICITY] 
[GENDER] with [HAIR] and [DISTINCTIVE FEATURE]. Wearing [CLOTHING], 
seated in [LOCATION]. Shot on [CAMERA] with [LENS], shallow depth of 
field, [LIGHTING] from camera [DIRECTION], [COLOR TEMP] color temperature. 
Photoreal skin texture with visible pores. NO airbrushing, NO plastic skin, 
NO watermark, NO text.
Aspect ratio: 4:5.
```

### B. 의상 시트 2x3 (베이스 attach 필수)

```
Using this reference image EXACTLY for face, body proportions, age, 
ethnicity and hairstyle: generate a character outfit sheet, 6 full-body 
looks in a 2x3 grid, identical face and lighting. Outfits, labeled below 
each panel:
(1) [outfit 1 description]
(2) [outfit 2 description]
... (6 개)
White seamless background, soft butterfly lighting, no shadows on face, 
keep EXACT same face, EXACT same hair color and length across all 6.
Aspect ratio: 4:5.
ATTACH: [base portrait reference].
```

### C. 표정 시트 3x3 (9-표정)

```
Reference attached. Generate a 3x3 expression sheet of the same 
[ETHNICITY] [GENDER], identical lighting and crop (chest-up), white 
background:
neutral / soft smile / laugh teeth showing / wink / pout / surprised / 
focused thinking / shy looking down / confident smirk
EXACT same face, hair, makeup across all 9. Label each below.
Aspect ratio: 1:1.
```

### D. 8-view 턴어라운드 (게임/애니 스타일)

```
Generate 8 orthographic character views in a 4x2 grid: 
(1) front straight, (2) 3/4 front-left, (3) profile left, (4) 3/4 back-left, 
(5) back straight, (6) 3/4 back-right, (7) profile right, (8) 3/4 front-right.
Subject: same person from reference. Neutral A-pose, arms slightly away 
from body. Wearing [WARDROBE]. White seamless background. Even diffused 
lighting from 4 directions. Each view labeled below. Maintain EXACT same 
face, body proportions, age, ethnicity from reference image. No identity 
changes.
Aspect ratio: 16:9.
```

### E. 4-패널 스토리보드 (Kling I2V에 바로 투입)

```
4-panel storyboard sheet for a [DURATION]-second [GENRE] reel, same 
person (reference attached), labeled [TIME RANGES]:
panel 1 — [shot description, action]
panel 2 — [shot description, action]
panel 3 — [shot description, action]
panel 4 — [shot description, action]
Same lighting ([COLOR TEMP] from camera-[DIRECTION]), same outfit, 
[LOCATION] background. EXACT face across all 4.
Aspect ratio: 9:16 each, 4 panels in 2x2 grid.
```

### F. 덕테이프 verbatim — 브랜드 로고/한글 텍스트 픽셀 락 (광고 필수)

```
ATTACH: [character reference] + [brand logo PNG / target text image].
Generate a [SHOT TYPE] of the same person [ACTION], holding/showing 
[BRAND ASSET] with the attached [logo/text] printed verbatim, no 
distortion, no color shift. [SCENE DETAILS]. EXACT face, EXACT [logo/text] 
pixels. [CAMERA LOOK].
Aspect ratio: 9:16.
```

한글 텍스트는 반드시 ① 따옴표 ② `verbatim` ③ `no extra words, no duplicate text` 3종 세트:
```
The poster shows the Korean text "오늘도 든든하게" verbatim, in bold round 
Hangul typography, white text on red background. No extra words.
```

## 4. 출력 시 체크리스트 (사용자에게 프롬프트 주기 전)

**I2V 릴스/숏폼용 씬 스틸을 만들 때:** 한 장짜리 깨끗한 9:16 스틸을 씬별로 생성하고, 내부 텍스트/자막은 기본적으로 넣지 않는다. 실제 장소 기반 크리에이터 컷이면 먼저 장소 카드(뷰포인트·시간대 빛·주변 건물/가게·방문객 스타일)를 정리한다. 세부 패턴은 `references/scene-stills-for-i2v.md`를 확인한다.

- [ ] **[미모 게이트 · 2026-07-04]** 프롬프트에 **얼굴 이목구비 DNA(6축: 얼굴형·눈·코·입·턱·피부)**가 실제로 들어갔는가? generic `beautiful woman`은 슬롭 트리거일 뿐 미모 지정이 아니다. 없으면 다시 써라. See `references/2026-07-04-real-beauty-not-conceptual.md`.
- [ ] **[미모 게이트]** 예쁨/잘생김을 **명시적으로(K-idol/actor급)** 지정했는가? 역할·의상·소품·배경(conceptual/persona)은 얼굴을 예쁘게 만들지 않는다 — 컨셉을 미모로 착각 금지.
- [ ] **[미모 게이트]** 실측 커뮤니티 verbatim(BubbleBrain `35mm film + visible skin texture`, WolfRiccardo `RAW iPhone`)을 이식했는가? 스킬 자작 문장보다 실제 창작자 프롬프트가 강하다.
- [ ] For a team of recurring characters, especially same-gender characters, did you avoid AI-slop average faces by locking distinct face DNA first? See `references/anti-slop-distinct-agent-anchors.md`.
- [ ] For lean-company / Seo-Ian office-vlog characters, did you keep abstract lore out of the image prompt? Do not write `Seo-Ian's lean company universe`, `humanized AI agent`, or `AI employee` as visual instructions. Translate the persona into visible Korean office-worker details: hair, wardrobe, expression, props, posture, camera, and workspace.
- [ ] If the user wants the characters “예쁘고 잘생긴 수준,” did you preserve the v1 clean attractive coworker casting and avoid rough/tired anti-beauty overcorrection? See `references/2026-05-28-lean-company-agent-v1-beautified-direction.md`.
- [ ] 5-튜플 DNA가 prompt 맨 앞에 prefix로 박혔는가
- [ ] "EXACT same face/proportions/identity from reference" 자연어가 들어갔는가
- [ ] aspect ratio가 사용처에 맞는가 (Reels 9:16 / 포트레이트 4:5 / 캐러셀 1:1 / 시트 16:9)
- [ ] negative ("no plastic skin, no watermark, no text, no identity change")가 들어갔는가
- [ ] 한글 텍스트는 따옴표 + verbatim + no extra words 3종 세트인가
- [ ] reference image 첨부 안내가 있는가 (ATTACH: 표시)
- [ ] ChatGPT 시스템 메시지 권장 ("Always treat the first attached image as identity anchor")

## 5. 실패 모드 즉시 대응표

| 사용자 호소 | 원인 | 즉시 줄 답 |
|---|---|---|
| "얼굴이 자꾸 바뀌어요" | 2~3장 반복 후 latent 표류 | 매번 원본 reference 재첨부 + "EXACT same face from reference image" 자연어 강제 |
| "너는 인물 일관성이 안 맞다" | 기존 버추얼 인물을 텍스트-only로 씬별 독립 생성함 | 즉시 인정하고 reference-anchored workflow로 전환. 기존 인물 reference를 첫 입력으로 고정하고, 배경/의상/소품만 바꾸는 방식으로 재생성한다. |
| "의상이 다르게 나와요" | 색상·디테일 누락 | 의상을 5-튜플 DNA에 포함, 색상 hex/팔레트 첨부 |
| "한글 텍스트가 깨져요" | verbatim 명시 누락 | 따옴표 + `verbatim` + `no extra words` 3종 세트 |
| "8 패널 이상이 깨져요" | 토큰 과부하 | Thinking 모드로 전환, 또는 3x3 → 2x2로 줄이고 시트끼리 stitch |
| "측면/후면에서 인종 특성 변화" | ethnicity drift | "[ETHNICITY], [구체적 특징]" 명시 + 배경 제거 후 단순 의상으로 시트 재제작 |
| "동안/노안 편향" | 표정·각도가 어려질수록 동안 | "[AGE]-year-old" 매 컷에 verbatim 반복 |

### Existing virtual-influencer rule: no text-only scene generation

For an already-established AI persona (e.g. a local library of reference images), do **not** generate multi-scene stills from text alone and claim identity consistency. Text-only prompts produce "similar person" drift across face, age, jawline, hair, and body proportions.

Use this sequence instead:

1. Pick one approved identity anchor image and label it explicitly: `Image 1: identity anchor — preserve exact face, age, hair, proportions, and mood`.
2. Attach the anchor to every generation/edit request, or create a 2x2/1x4 storyboard sheet first so the face DNA is solved in one latent pass.
3. Keep the DNA prefix identical across all cuts: age, ethnicity, hairstyle, face features, signature mood, outfit, and camera/prop lock.
4. Add the anchor phrase verbatim in every prompt: `EXACT same face, EXACT same identity from Image 1. No identity change. Do not invent a new person.`
5. For local `ima2` workflows, prefer reference generation/editing: `HOME=$HOME ima2 gen "PROMPT" --ref /absolute/path/identity.png --quality high`; use edit/inpainting when the face should be preserved and only the scene changes.
6. For Seo-Ian-style 출사/Reels stills, the desired look is often not polished GPT fashion photography but low-quality candid iPhone photos shot by a friend: imperfect framing, mild motion blur/noise, auto-exposure, natural situational expression, and no camera-conscious posing. See `references/seo-ian-candid-reels.md`.
7. QC identity before moving to image-to-video: compare face, hair, age, body proportions, outfit continuity, and prop shape. If any cut reads as "another similar model," regenerate before Kling/Grok.

## 6. 더 깊이 — references/

- `references/anti-slop-distinct-agent-anchors.md` — Seo-Ian/lean company의 효일·효리·효삼·효나·효정처럼 반복 등장하는 AI 에이전트 의인화 캐릭터를 만들 때, 같은 성별끼리 평균 얼굴로 수렴하는 AI slop을 막는 distinct face DNA와 contact-sheet QA. Do not overcorrect into rough documentary faces; preserve clean attractive Korean startup casting when the v1 direction was approved.
- `references/2026-05-28-lean-company-agent-v1-beautified-direction.md` — v1 persona-preserving beautification recipe: use each v1 portrait as reference, make characters attractive/polished, and separate them through visible role cues rather than harsh facial quirks.
- `references/session-multi-model-image-video-tips.md` — **세션에서 검증한 멀티모델 이미지/영상 꿀팁**: GPT Image 2 `n=숫자` 다중 출력 시 콜라주 방지 문구, Grok `n/aspect_ratio/reference_images/image-to-video`, Gemini/Nano Banana 다중 레퍼런스와 텍스트/인포그래픽, Kling start-frame/contact-sheet 금지 및 motion-only prompt, Veo first/last-frame planning. 사용자가 "숨은 꿀팁", "여러 장 따로", "GPT/Grok/Gemini/Kling 비교", "이미지→영상"을 요구하면 우선 확인.
- `references/photoreal-mastery.md` — **실물 구분 불가 수준 인물 사진 (요약)**: 5대 원칙, 6 마스터 템플릿 시그니처, 7대 tell-tale 체크리스트, imperfection 5요소 verbatim, multi-ref 8축. 사용자가 "더 사실적으로", "실사 퀄리티", "광고처럼 안 보이게", "AI 같지 않게"를 요구하면 우선 호출.
- `references/ima2-photoreal-cli.md` — **로컬 ima2 CLI 즉시 실행 레시피** (v1.1.11, gpt-5.5/high, 127.0.0.1:3333 launchd 자동 실행). 사용자가 "ima2로", "CLI로", "터미널로", "로컬 서버로" photoreal을 요청하면 우선 호출. 단일 씬 1-ref, 광고 3-ref, 8-view multimode, edit, 검증 명령 모두 포함.
- `references/templates.md` — 6대 템플릿 각각의 풀 예시 + 평점
- `references/ima2-reference-anchored-personas.md` — local ima2 + reference image workflow for established personas; prevents text-only multi-scene identity drift before Kling/Grok.
- `references/seo-ian-candid-reels.md` — Seo-Ian-specific reference-anchored candid iPhone friend-shot workflow for Reels/Shorts stills.
- `references/seoian-friend-shot-reels.md` — expanded Seo-Ian friend-shot workflow: 24F AI-builder/snap-photographer story contract, low-quality iPhone style rules, B-roll/talking cut shot list, and local ima2 reference command pattern.
- `references/seoian-lean-company-agent-character-system.md` — photoreal recurring-character system for Seo-Ian/lean-company office vlogs: {{OWNER_NAME}} and 서이안 as identity-anchored references, 효일/효리/효삼/효나/효정 as personified AI-agent employees, with role DNA, props, satire failure modes, and anchor-first production sequence.
- `references/case-studies.md` — 한국 11 크리에이터 실제 프롬프트 verbatim
- `references/anti-patterns.md` — 8개 자주 하는 실수와 수정 패턴

상세 리서치 원본:
- 기본: [$HOME/Agents/Image-gen/research/01-gpt-image-ducktape.md]($HOME/Agents/Image-gen/research/01-gpt-image-ducktape.md)
- **포토리얼 마스터 (Level 10 통합 가이드)**: [$HOME/Agents/Image-gen/research/09-ducktape-photoreal-mastery.md]($HOME/Agents/Image-gen/research/09-ducktape-photoreal-mastery.md)
- **ima2 CLI 실행 레시피** (로컬 server 통합): [$HOME/Agents/Image-gen/research/09-ducktape-photoreal-cli-recipes.md]($HOME/Agents/Image-gen/research/09-ducktape-photoreal-cli-recipes.md)
- 4개 도메인 상세: [09-A · API/기술]($HOME/Agents/Image-gen/research/09-photoreal-research-A-gpt-image-tech.md) · [09-B · 커뮤니티]($HOME/Agents/Image-gen/research/09-photoreal-research-B-community-prompts.md) · [09-C · 사진 학술]($HOME/Agents/Image-gen/research/09-photoreal-research-C-photography-methodology.md) · [09-D · Identity 보존]($HOME/Agents/Image-gen/research/09-photoreal-research-D-identity-preservation.md)

## 6.1 Seo-Ian lean-company agent personas

When creating recurring images for {{OWNER_TITLE}}'s Seo-Ian office-vlog universe, use `references/2026-05-27-lean-company-agent-personas.md` before generating the humanized AI employees 효일/효리/효삼/효나/효정. The required pattern is: create one photoreal anchor portrait per agent first, get approval, then reuse that anchor for outfit sheets, expression sheets, and episode scenes. Keep them as realistic Korean startup employees, not robots/cyberpunk characters.

## 7. 자매 스킬

- 시트가 완성되면 → `kling-image-to-video` 스킬 호출 (정지 → 영상)
- 시나리오가 먼저면 → `virtual-influencer-script` 스킬 호출 (스토리 → 시트 → 영상)
