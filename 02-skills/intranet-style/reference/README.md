# 인트라넷 디자인 시스템 (Lean-AX Intranet DS)

> **정본은 코드다.** 이 문서군은 `<인트라넷 레포>`(살아있는 인트라넷)에서 **값을 그대로 추출**한 것이며,
> 발명·추정한 값은 없다. 코드와 어긋나면 **코드가 이긴다** — 그때는 이 문서를 갱신한다.
>
> **목적 1.** "인트라넷 스타일로 만들어줘" 한마디에 **자 대고 맞춘 듯 동일한 화면**이 나오게 한다.
> **목적 2.** 인트라넷 도입 기업에 **디자인은 그대로, 기능만 기업 맞춤**으로 구축하는 재사용 라이브러리가 된다.

---

## 문서 인덱스

| 파일 | 담는 것 | 분량 |
|---|---|---|
| [`01-tokens.md`](01-tokens.md) | 색·radius·타이포·간격·그림자 **토큰 원값**, 테마 33종, 커스텀 CSS 규칙 66개 | 795줄 |
| [`02-primitives.md`](02-primitives.md) | UI 프리미티브 **27종 전수**(variant/size/상태/정확한 클래스), 커스터마이즈 136개, 함정 10건 | 1,784줄 |
| [`03-shell-layout.md`](03-shell-layout.md) | 앱 셸 골격(사이드바·헤더·콘텐츠·2패널·오버레이·반응형), 공통 상수 | 851줄 |
| [`04-page-templates.md`](04-page-templates.md) | 페이지 **6유형 스켈레톤** + 반복 패턴 20종 + do/don't | 2,280줄 |

정본 소스: `app/globals.css`(토큰 단일 진실) · `components/ui/*`(프리미티브) · `components/app-sidebar.tsx`·`site-header.tsx`(셸) · `app/*/page.tsx`(템플릿)

---

## 이 시스템의 정체성 (shadcn과 다른 점 — 재현에 결정적)

이 6가지를 놓치면 "비슷한데 다른" 화면이 나온다.

1. **색 값은 2층에만 있다.** `--color-*` 31개는 전부 `var()` 별칭이고, 실제 색은 `:root`(라이트)/`.dark`에만 있다. 색을 바꾸려면 이 2층만 건드린다.
2. **radius는 `--radius: 0.625rem` 하나에서 7단계가 파생**된다(sm 0.6× ~ 4xl 2.6×). Tailwind 기본 radius 스케일을 전부 덮어쓴다.
3. **표면 경계는 `border`가 아니라 `ring-1 ring-foreground/5`**(전경색 알파). 테마가 33종이라 고정 테두리색을 쓸 수 없기 때문이다.
4. **입력 필드는 "채워진" 스타일**: `rounded-2xl h-8 border-transparent bg-input/50`. shadcn의 윤곽선 필드와 정반대.
5. **컨트롤 기본 높이는 `h-8`**(shadcn은 `h-9`). Button은 size 8종.
6. **Dialog/AlertDialog는 `flex`가 아니라 `grid`** + `[&>*]:min-w-0` 안전망(긴 URL 오버플로 방지). 이 안전망을 빼면 레이아웃이 깨진다.

> `rounded-2xl`(16px)가 전역 규약이라 **높이 32px 이하 요소는 자연히 pill 형태**가 된다(Button `h-8`, Input `h-8`, Badge `h-5`). 의도된 디자인이다.

> **버튼 높이 — 컴포넌트 기본 vs 페이지 관례 (혼동 주의)**
> `Button`의 **컴포넌트 기본은 `size="default"` = `h-8`(32px)**이다(`components/ui/button.tsx:24-25`).
> 그러나 **페이지 우상단 주요 액션 버튼(예: "거래처 추가")은 `size="lg"` = `h-9`(36px)** 관례를 따른다 — 실렌더 실측으로 확인됨.
> 즉 "기본 h-8"은 컴포넌트 기본값이고, **주요 액션은 lg**다. 둘을 섞지 마라.

---

## 재현 검증 결과 (2026-07-15 실측)

**시험 방법**: 이 문서군**만** 읽고(앱 소스 열람 금지) 신규 화면(`app/ds-preview/page.tsx`, 목록/테이블형)을 만들게 한 뒤,
실제 화면(`/customers`)과 **렌더 대조**했다.

| 항목 | 실제 `/customers` | 스펙만 보고 만든 `/ds-preview` | 판정 |
|---|---|---|---|
| 주요 액션 버튼 높이 | 36px | 36px | ✅ 일치 |
| 카드 radius | 24px | 24px | ✅ 일치 |
| 입력 필드 | — | 36px · radius 18px · 배경 알파 0.5(채워진 스타일) | ✅ 규약 준수 |
| 셸 배치(`@container/main` 배선) | — | 사이드바 셸 아래 정상 렌더 | ✅ 확인 |

**결론: 스펙만으로 동일 외형 재현이 성립한다.** 다만 아래 구멍을 메우면 더 정확해진다.

### 스펙 보강 백로그 (재현 시험이 찾아낸 구멍 14건) — **전건 반영 완료 (2026-07-20)**

재현 시험 중 "스펙에 없어 추정해야 했던" 지점들. 아래 값은 전부 **앱 소스에서 확인해 원문 그대로** 옮겼다.

**A. API 계약 누락 (경로만 있고 시그니처 없음)**

- [x] 1. `toneBadgeClass()` / `statusBadgeClass()` → **[`02-primitives.md` 부록 D-1·D-2](02-primitives.md)** (신설). export 이름·인자·톤 키 8종·반환값·`TaskStatus` 4값·짝 함수 `statusDotClass`. 근거 `lib/badge-tone.ts:4-33`, `lib/task-ui.ts:8-35`, `lib/constants.ts:4-10`
- [x] 2. `useT()` → **[부록 D-5](02-primitives.md)**. named export, `t: (ko: string) => string`, **보간 인자 없음**, **사전에 없는 키는 한국어 원문 그대로 반환**(`?? ko`). 근거 `lib/i18n.tsx:492-495`, `:503`
- [x] 3. `StatCard` / `Stat` → **[부록 D-3·D-4](02-primitives.md)**. `Stat` **export 됨**, props는 `{ stat: Stat }` 객체 1개. **톤 키 집합은 `toneBadgeClass`와 다르다**(`info`/`success`/… vs `blue`/`green`/…) — 동명 타입이지만 별개. 근거 `components/stat-card.tsx:14-20`, `:33-41`

**B. 값 누락 (다른 유형에서 이식해야 했음)**

- [x] 4. 표 셀 우측 정렬 → **04 § 3-2a**. `className="text-right"`를 **`TableHead`·`TableCell` 양쪽에 짝으로**. 근거 `app/usage/page.tsx:197`·`:209`
- [x] 5. 탭+검색+주액션 한 줄 툴바 → **04 § 3-7**(신설). 유형 3에 **선례 없음을 전수 확인**하고 "유형 2 원문을 이식한다"로 명시 규정 + 이식 시 지킬 값·바뀔 값. 근거 `app/mail/page.tsx:741-810`
- [x] 6. 목록 행 우측 끝 메타 → **04 § 7-1a**. 4가지 조합(A 아이콘+시각 / B 시각+카운트배지 / C 고정폭+액션 / D 표 행). 근거 `app/mail/page.tsx:843-857`, `components/chat-panel.tsx:904-923`, `app/drive/page.tsx:641-658`
- [x] 7. 생성 폼 다이얼로그 푸터 → **04 § 5-4a**. `취소(outline)` → `저장(default)`, **높이 미지정 = `h-8`**(헤더의 `h-9`와 다름), 삭제는 이 푸터에 안 옴. 3개 페이지 동일. 근거 `app/customers/page.tsx:678-685`
- [x] 8. 스탯 카드 개수별 열 수 → **04 § 1-2a**. 3개/4개/5개 전수 + 3개 정본 확정. 근거 `app/usage/page.tsx:163-164`, `components/stat-card.tsx:108`, `app/page.tsx:269`
- [x] 9. 이니셜 아바타 글자 수 → **04 § 7-1b**. **A=1자+대문자화(사람 아바타) / B=2자(한글 이름 칩)** 2규칙. 한글은 BMP 1유닛이라 `slice(0,2)` 절단 문제 없음. 근거 `app/mail/page.tsx:139`, `app/page.tsx:439`
- [x] 10. 빈 상태 독립 배치 래퍼 → **04 § 7-7a**. **`space-y-4` > `Card shadow-xs` > `CardContent`** 로 확정(5:2 다수결). 근거 `app/customers/page.tsx:325-334` 외 4곳

**C. 문서 내부 충돌**

- [x] 11. 페이지 설명 `<p>`의 `mt-1` → **04 § 8-6a**(전수 집계 신설) + § 3-1 스켈레톤을 `mt-1`로 갱신(원문과 다름을 해당 위치에 명시) + § 8-6 표 갱신 + **아래 정규화 표에 행 추가**. 정본 **`mt-1`**(8:4)
- [x] 12. `[&>*]:min-w-0` 적용 깊이 → **[`02-primitives.md` 부록 C-1a](02-primitives.md)**(신설) + 04 § 5-4에 판정 기준 주석 추가 + **아래 정규화 표에 행 추가**. 정본 = **깊이가 아니라 "와이드 콘텐츠를 담는가"**. 근거 커밋 `32b9b99`, `app/mail/page.tsx:1041-1042`

**D. 미검증(해소됨/남음)**

- [x] 13. ~~셸 `@container/main` 배선~~ → **실렌더로 해소**(정상 동작 확인)
- [x] 14. ~~시각 검증 미수행~~ → **위 렌더 대조로 해소**

> **이번 패스에서 확인하지 못해 남긴 것 (미확인)**
> - 유형 3에서 **탭+검색+주액션을 실제로 렌더한 화면이 앱에 없다.** § 3-7은 "유형 2 원문 이식"이라는 **규정**이며 실렌더 검증본이 아니다.
> - 3개 스탯 그리드는 **코드가 갈려 있다**(3열 오버라이드 2곳 / 기본 유지 3곳). 정본은 주석이 달린 쪽(`app/usage/page.tsx:163`)을 근거로 정했을 뿐 코드 다수결은 아니다.
> - 위 두 건과 이번 패스에서 추가된 모든 항목은 **소스 대조 기반이며, 브라우저 실렌더 대조는 하지 않았다.**

---

## 정규화 결정 (혼재 → 정본 확정)

추출 과정에서 **코드베이스 자체의 불일치**가 발견됐다. 디자인 시스템은 답이 하나여야 하므로 아래로 **확정**한다.
기존 코드는 아직 혼재하지만 **신규 화면·신규 기업 배포는 반드시 "정본" 열을 따른다.**

| 항목 | 코드 현황(혼재) | **정본 (신규는 이것)** | 근거 |
|---|---|---|---|
| 페이지 루트 컨테이너 | `<>` / `space-y-4` / `space-y-6` / `flex flex-col gap-3` | **`<div className="space-y-4">`** | 다수결(6개 페이지) |
| focus 링 | `ring-3 ring-ring/30` vs `ring-[3px] ring-ring/50` | **`ring-3 ring-ring/30`** | 다수파(Button·Input·Textarea·Select·Checkbox·Toggle) |
| 알림/카운트 뱃지 | 알림벨 `h-4 min-w-4 text-[10px]` vs 챗 `h-5 min-w-5 text-[11px]` (색은 양쪽 다 `bg-destructive`로 정규화 완료 — `components/chat-panel.tsx:921`) | **`h-4 min-w-4 text-[10px] bg-destructive`** | 색 정규화는 코드 반영됨. **형상만 아직 2벌** |
| 다이얼로그 최대 높이 | `max-h-[88vh]` vs `max-h-[90vh]` | **`max-h-[88vh]`** | 다수결 |
| 말줄임표 | `…` vs `...` | **`…`**(U+2026) | 다수결·타이포 정합 |
| 속성 행 라벨 폭 | `w-28` vs `w-24` | **`w-28`** | 다수결 |
| 페이지 설명 `<p>` 상단 여백 | `mt-1`(8) vs 없음(4) vs `mt-0.5`(1) vs `mb-3`(1) | **`mt-1 text-sm text-muted-foreground`** | 다수결 8:4 — 전수 집계는 [04 § 8-6a](04-page-templates.md) |
| `[&>*]:min-w-0` 적용 깊이 | 부록 C-1 "중첩에도 붙여라" vs § 5-4 원문 미적용 | **직계 자식은 안전망이 커버(명시 불필요). 2단계 이상 중첩 + 와이드 콘텐츠(긴 URL·에디터·표)를 담는 컨테이너는 깊이 무관 직접 명시** | 커밋 `32b9b99`가 안전망과 명시적 `min-w-0`(`app/mail/page.tsx:1042`)을 **함께** 넣었다 — 상세 [02 부록 C-1a](02-primitives.md) |
| 스탯 카드 3개 그리드 | 3열 오버라이드(2) vs 기본 4열 유지(3) | **`<StatGrid stats={stats} className="grid-cols-1 @xl/main:grid-cols-3" />`** | 코드는 소수지만 의도 주석이 달린 쪽(`app/usage/page.tsx:163`). 상세 [04 § 1-2a](04-page-templates.md) |
| 독립 배치 빈 상태 래퍼 | `Card > CardContent`(5) vs `rounded-lg border` div(2) | **`space-y-4` > `Card shadow-xs` > `CardContent`** | 다수결 5:2 + 표면 규약(`ring-1`이지 `border` 아님). 상세 [04 § 7-7a](04-page-templates.md) |
| 슬림 스크롤바 | ~~`SLIM` / `SLIM_SCROLL` 2벌~~ → **공용화 완료** | **`SCROLL_SLIM`** (기본) / **`SCROLL_SLIM_STABLE`** (거터 고정이 필요한 곳) — `lib/ui-constants.ts` | 기능이 달라 통합 대신 베이스+합성. 문자열 중복 제거로 재분기 불가 |
| 전체높이 스크롤 차감 | ~~메일 9rem / 지식망·워크보드 7rem 인라인~~ → **공용화 완료** | **`CONTENT_H_TOOLBAR`**(9rem, 상단 행 있는 화면) / **`CONTENT_H`**(7rem, 표준) — `lib/ui-constants.ts` | 값은 유지(회귀 0). ⚠️ 차감량 근거는 실측 미검증 — 값 통일은 별건 |

### 정규화 백로그 — **전건 코드 반영 완료 (2026-07-20)**

- [x] 1. `SLIM` / `SLIM_SCROLL` 2벌 정의 → **`lib/ui-constants.ts`로 공용화**.
      두 정의는 기능이 달랐다(메일=Firefox `scrollbar-color`+hover / 대시보드=`scrollbar-gutter:stable`).
      억지 통합 대신 **베이스 1개 + 합성 변형 1개**로 정리: `SCROLL_SLIM`, `SCROLL_SLIM_STABLE = SCROLL_SLIM + 거터고정`.
      문자열 중복이 사라져 값이 다시 갈릴 수 없다. 소비처: `app/mail/page.tsx`, `app/page.tsx`.
- [x] 2. 전체높이 차감값 → **`lib/ui-constants.ts`의 `CONTENT_H_TOOLBAR`(9rem, 메일) / `CONTENT_H`(7rem, 지식망·워크보드)**로 공용화.
      소비처에서 인라인 `h-[calc(100svh-7rem)]` 제거. **값은 그대로 유지**(시각 회귀 0).
      ⚠️ 차감량의 산출 근거는 **여전히 실측 미검증**(9rem이 주석의 6rem과 불일치) — 값 통일은 실측 후 별건.
      드라이브(`min-h-[calc(100vh-3.5rem)]`)는 패턴 자체가 달라 이번 범위에서 제외.
- [x] 3. 챗 뱃지 `bg-red-500 … text-white` → **`bg-destructive … text-destructive-foreground`** (3곳: `chat-panel.tsx:269,921,1052`).
      **기업별 테마 교체 시 이 뱃지만 안 바뀌던 문제 해소.**
      (범위 밖으로 남긴 것: `app/agents/page.tsx:220` 진행바 경고색, `components/stat-card.tsx:26` `danger` 톤 팔레트 — 둘 다 의도된 별개 팔레트라 판단)
- [x] 4. `components/nav-documents.tsx` **제거**(89줄). 동적 참조 포함 전수 검사로 호출부 0 확정 후 `git rm` — 이력에 남아 복구 가능.
- [x] 5. `NavUser` 드롭다운 라벨 **i18n 적용** — 하드코딩 영어 4개 → `t("계정")·t("결제")·t("알림")·t("로그아웃")`.
      사전(`lib/i18n-dict.ts`)에 없던 3개(계정·결제·로그아웃) **en/ja 등재**.
- [x] 6. 미사용 프리미티브 6종 → **유지 결정**(제거하지 않음).
      이제 이 라이브러리는 **기업 배포 자산**이므로, 인트라넷이 안 쓴다고 버리면 납품처에서 필요할 때 없다.
      `toggle·toggle-group·skeleton·sheet·drawer·breadcrumb` = **"라이브러리 자산(현 인트라넷 미사용)"**으로 분류.
      (`skeleton`·`sheet`는 `sidebar.tsx` 내부 의존이라 애초에 제거 불가)

**검증**: `tsc --noEmit` 실제 출력 확인 → **에러 0**. 메일·대시보드·지식망 **렌더 회귀 없음**(에러 오버레이 0, 높이 계산 정상).

---

## 기업 배포 절차 (디자인 동일 · 기능 커스텀)

인트라넷은 **테마 33종**을 이미 지원한다 → 골격을 그대로 두고 **브랜드 테마만 갈아끼우는** 방식이 구조적으로 가능하다.

1. **골격 이식** — `app/globals.css`(토큰 정본) + `components/ui/*`(프리미티브 27종) + 셸(`app-sidebar`·`site-header`) 복사.
   상세 절차는 [`03-shell-layout.md` 부록 A(신규 앱 이식 체크리스트)](03-shell-layout.md) 참조.
2. **브랜드 테마 주입** — `:root`/`.dark` 2층의 색 토큰만 기업 브랜드로 교체(다른 층은 손대지 않는다). radius를 바꾸려면 `--radius` **하나만** 조정하면 7단계가 함께 움직인다.
3. **화면 구성** — 필요한 화면을 [`04-page-templates.md`](04-page-templates.md)의 6유형에서 고르고 스켈레톤을 복붙 → **기능만** 기업 요구에 맞게 교체.
4. **검수** — 아래 "재현 체크리스트"로 자기검수.

> shadcn 철학대로 **npm 의존이 아니라 복사**한다. 정본(AI-Native)이 갱신되면 이 문서군을 갱신하고, 기업 프로젝트는 필요한 시점에 선택적으로 재복사한다.

---

## 신규 화면 만드는 순서 (요약)

1. 화면 유형 결정 → [`04-page-templates.md`](04-page-templates.md)에서 해당 유형 스켈레톤 복사
2. 루트 컨테이너 = **`space-y-4`** (정본)
3. 프리미티브는 반드시 [`02-primitives.md`](02-primitives.md)의 **정확한 클래스**로 (임의 높이·radius 금지)
4. 색·간격은 **토큰만** 사용 — 하드코딩 색(`bg-red-500` 등) 금지, 테마가 깨진다
5. 완료 후 아래 체크리스트로 자기검수

### 재현 체크리스트 (자 대고 맞췄는지)

- [ ] 컨트롤 높이가 `h-8` 기본인가 (버튼·입력)
- [ ] 입력 필드가 **채워진** 스타일(`bg-input/50 border-transparent rounded-2xl`)인가
- [ ] 표면 경계가 `border`가 아니라 **`ring-1 ring-foreground/5`**인가
- [ ] 색이 전부 **토큰**인가 (하드코딩 색 0개)
- [ ] radius를 임의값이 아니라 **스케일**(`rounded-2xl` 등)로 썼는가
- [ ] 다이얼로그를 썼다면 `[&>*]:min-w-0`가 살아있는가 (긴 URL 오버플로)
- [ ] focus 링이 `ring-3 ring-ring/30`인가
- [ ] 아이콘 크기가 관례(`size-3.5`/`size-4`)를 따르는가
- [ ] 빈 상태·로딩·에러 화면을 템플릿대로 넣었는가

---

## 유지 규칙

- 이 문서군은 **추출물**이다. 코드를 바꾸면 해당 섹션을 같이 갱신한다(드리프트 방지).
- 각 문서의 값에는 **출처 `파일:라인`**이 붙어 있다 — 의심되면 원본을 열어 대조한다.
- 코드에서 확인 못 한 것은 **"미확인"**으로 표기돼 있다. 미확인을 사실로 승격시키지 않는다.
