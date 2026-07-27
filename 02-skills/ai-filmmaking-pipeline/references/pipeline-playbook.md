# AI Filmmaking Pipeline — 상세 플레이북

> Higgsfield Academy "The AI Filmmaking Pipeline"(22 레슨) 정제본. SKILL.md의 10원칙을 실제로 적용할 때 이 파일을 규칙 소스로 쓴다.
> 원본 학습 로그: `higgsfield-academy-learning-log.md` (같은 폴더).

---

## 0. The bar (기준)

모든 규칙은 의견 기반(opinionated)이다. 반대해도 되지만 **왜 그 룰이 존재하는지 설명할 수 있어야** 한다. 핵심 교훈: **결함을 느끼기만 하지 말고 이름을 붙여라(name the flaw)** — 이름 붙은 결함만 고칠 수 있다.

---

## 1. 4단계 파이프라인 + 핸드오프

| 핸드오프 | 넘겨가는 것 | 이유 |
|---|---|---|
| Brief → Setup | 합의된 brief(샷, 세계, 캐스트, 소품, 제약) | Setup이 추측 없이 올바른 폴더 구조를 만듦 |
| Setup → Generation | 프로젝트 + 폴더 + 하나의 네이밍 계약 | 모든 후보가 주소를 갖고, 승인된 것이 재사용 @Element가 됨 |
| Generation → Seedance/Kling | 검증·명명된 로케이션·캐릭터·소품 Element | 모션 엔진은 실제 소스 픽셀을 결합 — 넘어간 결함은 모션에서 증폭 |
| Test → Review | 모션 테스트 + 진단 | 샷 승인 또는 특정 소스만 수정하러 되돌림 |

- **Setup은 주소를 정의하고, generation이 그 주소를 벌어들인다.** 파일이 존재한다고 프로덕션 입력이 되지 않음 → 검사→승인→이름→Element 저장.
- **로케이션부터.** 장소는 토대이자 캐릭터가 진짜 성립하는지 보는 시험대.
- **Review는 루프를 닫는다.** 테스트는 pass/fail이 아니라 "어디로 돌아갈지". 지오메트리 붕괴→로케이션, 정체성 흐림→캐릭터 시트, 액션 오류→모션 연출. **가장 이른 깨진 핸드오프**를 고쳐라.

---

## 2. 네이밍 계약

패턴: **`@type_project_name`**

| 접두사 | 대상 | 예시 |
|---|---|---|
| `@loc_` | 로케이션 | `@loc_HG_museum_front` |
| `@char_` | 캐릭터 | `@char_HG_jaxx` |
| `@prop_` | 소품 | `@prop_HG_leather_briefcase` |

- 가운데는 **프로젝트 접두사**(예: HG=Hell's Grind, RR=Rooftop Reckoning) — 킥오프에서 짧은 코드 합의 → 영화 간 자산 충돌 없음.
- 멀티워드 설명은 **언더스코어**(`museum_front`), 공백·하이픈 금지.
- **로컬 파일 ≠ Element.** 파일 업로드 후 재사용 Element를 만들어야 프롬프트가 `@이름`으로 호출.
- type+project 세그먼트가 검색·@피커 선택을 신뢰성 있게 만든다.

---

## 3. Think — 프롬프트 만들기 (6결정 + Leera 4-D)

**만능 문장 공식은 없다. 신뢰할 결정 패스가 있다.** 6슬롯에 답하고 한 문단으로 조립:

1. **Subject** 2. **Action** 3. **Setting** 4. **Light** 5. **Camera/Motion** 6. **Constraints**

- 각 절이 임무를 가짐: 주체 식별 · 액션 블로킹 · 배경을 그릴 수 있게 · 조명 일관 · 프레임/모션 연출 · 알려진 실패 방지.
- "hot summer day" 같은 미해결 슬롯 금지(조명 방향·그림자를 안 정함).
- **품질 단어보다 구체적 명사**: "weathered wood siding" O, "beautiful" X.
- **반복(iteration) 규칙**: 결정 하나만 바꾸고 전체 프롬프트를 **다시 쓰게** 한다. diff/조각 편집 금지 — 모든 슬롯이 여전히 일치하도록.
- Claude가 선택 안 된 소품/스타일/날씨/카메라 무빙을 조용히 추가하면 → "무슨 모호함을 해결하나?" 물어 승인/교체/제거. **나는 감독, Claude는 조립.**

**Leera 4-D 방법**(로케이션 프롬프트용, decision log 필수):
1. **DECONSTRUCT** — brief 단어를 6슬롯에 매핑, 각 슬롯 explicit/implied/missing 표시.
2. **DIAGNOSE** — 명확성·논리 감사(태양 하나, 그럴듯한 문·창, 반대로 지는 그림자). 결함마다 질문 or default 라벨. 날씨/소품/스타일/카메라 조용한 추가 금지.
3. **DEVELOP** — 승인된 결정으로 구축: 명확한 주체+액션, 배경, 나중 캐릭터 배치용 **named anchor object**(소파·출입구·배너), 명시적 조명(실내는 소프트; 하드 가시광선은 대개 slop), 부드러운 falloff 팔레트(크러시 그림자 없이), 카메라 앵글(없으면 3/4-view 기본). 비디오만 모션 추가.
4. **DELIVER** — 영어 한 문단 + decision log(추가/재구성마다 어떤 모호함·실패를 해결하는지).

운영 모드: **DETAIL**(새 로케이션 기본 — 2~3 질문 후 딥패스) / **BASIC**(빠른 수정 — 질문 생략).

---

## 4. 모델 선택 — must-preserve 요구로 결정

**영원한 "최고" 모델 없음.** 매 패스 전 **하나의 must-preserve 요구를 명명** → 의도한 크롭에서 출력 검사 → must-preserve를 증명하고 **재실행/마스크 수리로 감당 가능한 실패만** 남기는 모델 선택. 로스터 바뀌면 매번 증거 테스트 반복, 오늘 랭킹 이월 금지.

| 모델 | 성격 | 강점 | 배제 요인 | 용도 |
|---|---|---|---|---|
| **Soul Cinema** | from-scratch | 시네마틱 질감·분위기, raking side light, haze 깊이감, 사실적 피부/의상 | 정확한 구도는 여러 번, 특정 소품/크리처 약함, 다중 레퍼런스·완성 편집 불가 | 분위기·재질·인간 사실성이 가장 고치기 어려울 때. **캐릭터 생성 1순위** |
| **GPT Image 2** | control | 읽히는 텍스트, 소품 지오메트리, 미세 디테일, 리버스 앵글, 레퍼런스 가이드 편집 | 조명 변형 미검증, 매크로 클로즈업 없음, 콜라주 소프트, 인간 피부엔 오버샤픈 slop | 텍스트·제어된 지오메트리·소품. **크리처**(인간 아님)에도 |
| **Nano Banana Pro** | edit | 완성 이미지에 대담한 의상/얼굴/오브젝트 변경, 크리처 적합 | after-only는 정체성 보존 증명 불가, 톤 tint·gradient 손상 위험, 얼굴이 대칭·생기 없어질 수 있음 | 변경 안착이 톤/얼굴보다 중요할 때. **로케이션·히어로 캐릭터 from-scratch 금지, 시트 생성 금지** |
| **Seedream 4.5** | texture edit | 피부/의상 텍스처 보존(주근깨·모공·눈 생존), oversharpen 회피, 병렬 배치 | after-only는 포즈/비율 lock 증명 불가, 편집이 포즈/앵글 이동 가능 | 깨끗한 캐릭터 텍스처가 고치기 어려울 때 |

- **Cinematic Cameras**: 무료 크레딧 로케이션 생성에 실전 사용된 모델(캡스톤 로케이션).
- **AI Cast (Cinema Studio)**: 캐스팅 탐색 툴.
- **Seedance 2.0 / Kling**: 모션(영상) 엔진 — 소스 Element를 real reference로 첨부해 샷 생성.

---

## 5. 로케이션 규칙

유용한 로케이션 = 예쁜 프레임이 아니라 **배우를 블로킹할 수 있고, 조명 논리가 하나, 카메라가 깊이를 보고, 나중 뷰가 같은 지오메트리를 반복**. 모든 샷이 이 결정을 상속하므로 천천히.

**6 lock (인과적 결정 체인)**:
1. **Geography before style** — 입구·플레이 경로·3개 깊이 평면 먼저 명명.
2. **One motivated light** — 하나의 동기 광원·방향·falloff(모순 광원=충돌 그림자).
3. **3/4, then reverse** — 3/4 마스터가 측면 지오메트리 노출. 리버스는 anchor·openings·light·depth·materials 일치 시만 승인.
4. **Anchor the blocking** — 모든 액션을 하나의 고정 오브젝트 기준으로("소파 홀쪽 팔걸이와 창문 사이"). "왼쪽에 선다" 금지(카메라 돌면 drift).
5. **Qualify one wide** — 오프프레임 발명이 나중 컷/연속성을 안 깰 때만 마스터 와이드 하나로 충분.
6. **Approve by locks** — 모든 명명 lock이 마스터·리버스에 보일 때만 진행, 첫 실패 lock에서 hold.

**3/4 뷰 이유**: 측면 지오메트리 + 전/중/배경 분리 → 나중 캐릭터 배치 단서. 정면(head-on)은 로케이션을 배경판으로 평평하게, 숨은 측면을 무제약으로 남겨 모델이 문·벽 위치를 발명.

---

## 6. 캐릭터 시트 규칙

캐릭터의 생사는 **시트**에 달림. Seedance/Kling은 시트를 **문자 그대로** 읽으므로 시트의 모든 결함 = 모든 샷의 결함.

**시트 파이프라인(항상 이 순서)**: Generate → Inspect → Edit(masked onto original) → Test.

**프롬프트 템플릿 불변 2요소**: **deep neutral grey 배경(#3a3a3c)** + **지배적 포트레이트가 있는 컬럼 분할**.
- COLUMN 1(가장 큼, 좌): chest-up 정면 포트레이트, 눈 샤프+catchlight.
- COLUMN 2: 전신 정면 A-pose.
- COLUMN 3: 전신 후면(같은 포즈 미러).

**Seedance-proof 규칙**:
- 포트레이트 = 시트의 **25~30%**(얼굴 디테일이 나오는 픽셀).
- 포트레이트 앵글 **off-frontal**(정면보다 머리 볼륨 읽힘).
- **눈은 절대 검정 아님**(홍채 색 명확). **catchlight 없으면 죽은 눈.**
- **대칭 깨기**(완벽한 미러=AI).
- **3D 게임 렌더 룩 금지**(모션 엔진이 게임 무드로 애니메이트).
- **Grey가 황금 중간**(흰색=washout, 검정=디테일 삼킴).
- **전신 패널 머리는 크롭** → 얼굴 텍스처를 포트레이트 패널에서만 가져오게 강제.

**SLOP 시트 3종(전부 reject)**: dirty sheet(재생성 때 축적+전신 얼굴 불일치=두 정체성) / game render(플라스틱+baked rim light+포트레이트 과소) / Nano Banana slop(미러 대칭+비누 피부+지배 포트레이트 없음).

---

## 7. 편집 = 수술 (로케이션·캐릭터 공통)

- **Edit the original** — 바뀐 패치만 원본에 합성(마스크). 편집을 쌓지 말 것.
- **Run models in parallel** — GPT Image 2(텍스트/정밀), Nano Banana Pro(대부분), Seedream 4.5(병렬 배치); 변경마다 최선 결과 채택.
- **Never re-edit an edit** — 두 번째 패스는 전체 프레임 재렌더 → grime·drift **복리 누적**. 항상 마스터에 마스크.
- **함정**: 편집 모델은 요청한 것만 건드리지 않고 **전체를 조용히 재렌더**. 그래서 추가/제거 디테일을 원본에 마스크(바뀐 패치만).

---

## 8. Slop 탐지

**보편 4 tell**:
1. **Light with no transitions** — 부드러운 램프 대신 납작한 검은 웅덩이(flat black crush).
2. **Broken-but-plausible objects** — 거의 읽히는 크레이트/난간이 모션에서 뭉개지고 증식.
3. **Local logic breaks** — 프레임 일부에만 있는 효과(한 구석만 긁는 비).
4. **Oily textures** — 비누 표면이 재질감 상실, 반사가 모션에서 기어다님.

**모델별 지문**:
- **Banana slop(Nano Banana Pro)**: 자로 잰 대칭, 평행·직각, 대비 없는 평평한 빛/색 → stock photo. 모든 편집을 **과장**("더 시네마틱"→쓰레기·먼지 도배).
- **GPT slop(GPT Image 2)**: 샤프니스·마이크로컨트라스트 최대, 하드 halo, 깊이 없음(전부 초점), warm 화이트밸런스, 플라스틱 재질. **최악 tell: 하나의 병든 텍스처(film-wrap)가 프레임 전체에 동일하게 덮임.**

**규칙**: 가시적 스틸 프레임 결함은 이미 stop. 크롭이 스틸 스캔을 통과하고 불확실한 엣지/반사만 남을 때 Seedance/Kling으로 확인.

---

## 9. Test (Seedance/Kling) — 결승선

스틸은 가설. 샷에 실제 필요한 모션을 돌리고 **한 번에 한 변수만** 바꿔 좁힌다.

- **진단 가능한 baseline에서 시작**: 캐릭터가 질문이면 로케이션을 변수에서 제외(이미 잡힌 플레이트 사용). 깨진 플레이트는 두 번째 그럴듯한 원인을 준다.
- **%로 승인 불가** — 명명된 소스 자산, 필요한 모션, 가시적 결과가 증거.
- **실패 입력 진단**(첫 실패를 소스 스틸과 비교):
  - **Source asset** — 결함이 소스에 존재하거나, 방향 바꿔도 같은 feature에 묶임.
  - **Motion direction** — 소스는 깨끗한데 의심 모션 절만 바꿨을 때 결함이 변함.
  - **Inconclusive** — 컨트롤 충돌/어느 변수도 안 따름 → 테스트를 더 좁힘.
- 이 진단은 **테스트한 자산·방향에 한정**. 재실행 한 번이 다음 결과를 보장하지 않음.

---

## 10. 모더레이션 현실 (실전 교훈)

사람 **얼굴이 포함된** 생성은 콘텐츠 모더레이션(NSFW/IP)에 걸려 거부·크레딧 환불될 수 있다. 캡스톤 실전에서 탐정 얼굴 포함 샷이 거부됨 → **사람 없는 로케이션+소품 버전**으로 재생성해 통과. 얼굴 포함 샷이 막히면 입력을 조정(무인 구도, 캐릭터 프레임 밖 등)하고 사용자에게 알린다.

---

## 11. 캡스톤 워크플로 (씬 하나 → 완성 샷, 5단계)

1. **Set up** — 씬 이름 프로젝트 + locations/characters/props 폴더 3개.
2. **Cast character** — Soul Cinema로 시트 생성 → Create Element `char_XX_name`(Category: Character).
3. **Build location** — 로케이션 6-lock 적용 생성 → Create Element `loc_XX_name`(Category: Location).
4. **Dress scene** — GPT Image 2로 스토리 핵심 소품(구체적 명사·재질 wear) → Create Element `prop_XX_name`(Category: Prop).
5. **Shoot** — Video 탭 → Seedance 2.0(또는 Kling) → 3개 @Element를 real reference 첨부(Face/IP eligibility 체크) → Generate → job 완료 대기(영상 렌더 15분+ 가능).

**실전 예(Rooftop Reckoning)**: `@char_RR_detective`(Soul Cinema) + `@loc_RR_rooftop_dusk`(Cinematic Cameras) + `@prop_RR_briefcase`(GPT Image 2) → Seedance 2.0 720p 8s 샷. 결과물 = `filmmaker-grant-showreel.mp4`(1280×720, h264, 8s) — 이 스킬의 워크드 예시.

---

## 12. MCP 실행 매핑

파이프라인 단계를 실제 도구 호출로:

| 파이프라인 행위 | Higgsfield MCP | Kling MCP |
|---|---|---|
| 모델 추천 | `models_explore(action:'recommend')` | `who_am_i`(규격 확인 먼저) |
| 레퍼런스 업로드 | `media_upload` / `media_import_url` → media_id | `file_upload` |
| 이미지 생성(로케이션/시트/소품) | `generate_image(model, prompt, medias)` | `text_to_image` / `image_to_image` |
| 수술적 편집 | `outpaint_image`·`remove_background`·`upscale_image` | `image_to_image` |
| 모션 테스트(샷) | `generate_video(model, prompt, medias)` | `text_to_video` / `image_to_video` |
| 상태 확인 | `job_status` / `show_generations` | `query_tasks` |

**과금 주의**: 모든 job이 크레딧 차감. 시험 삼기 금지, 파라미터/의도 불확실하면 **먼저 질문**(Kling MCP 규칙). 타임아웃·실패 시 자동 재제출 금지 — 사용자에게 알리고 재시도/변경 확인.
