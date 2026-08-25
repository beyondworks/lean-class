# 01 — 디자인 토큰 (Design Tokens)

> **이 문서는 실제 코드에서 추출됨.** 값은 발명·추정하지 않았고, 아래 파일들을 직접 읽어 원문 그대로 옮겼다.
>
> **정본 = `app/globals.css`** (960줄). 색·radius 토큰의 단일 진실 원천이다.
> 폰트는 `app/layout.tsx`, 사용 관례(타이포·간격 빈도)는 `app/**` + `components/**` grep 집계.
>
> 값이 코드와 어긋나면 **코드가 옳다**. 이 문서를 고쳐라.

| 항목 | 값 |
|---|---|
| 추출 대상 커밋 시점 | `feat/commander-lan-gate` 브랜치 (2026-07-20 기준 작업본) |
| `app/globals.css` 총 줄 수 | 960 |
| CSS 커스텀 프로퍼티 **선언** 총 개수 | **1,064** |
| **고유** 토큰 이름 개수 | **72** |
| 테마(색 세트) 개수 | **33** (`:root` 라이트 + `.dark` + 커스텀 31종) |
| `globals.css` 커스텀 CSS 규칙(셀렉터) 개수 | **66** |

---

## 0. 토큰 계층 구조 — 3층

값을 바꾸려면 **어느 층을 만져야 하는지**가 가장 중요하다.

```
[1층] @theme inline          globals.css:8-49    Tailwind 유틸리티 ↔ CSS 변수 배선 (색 값 없음)
        --color-primary: var(--primary)          → bg-primary / text-primary 가 동작하게 함
        --radius-lg: var(--radius)               → rounded-lg 의 실제 값 결정

[2층] :root / .dark          globals.css:52-119  실제 색 값 (OKLCH)  ← 여기가 팔레트 정본
        --primary: oklch(0.205 0 0)

[3층] .tokyo-night 등 31종    globals.css:126-681 테마별 전체 재정의 (HEX)  ← 2층을 통째로 덮음
        --primary: #7aa2f7
```

- 1층은 **별칭(alias)일 뿐**이다. `--color-*`에는 색 값이 없고 전부 `var(--*)` 참조다 (`globals.css:11-41`).
- 따라서 **새 색을 넣으려면 2층(`:root`/`.dark`)에**, 새 유틸리티 이름을 열려면 1층에 추가한다.
- 3층 커스텀 테마는 2층보다 **뒤에 선언**되어 있어 항상 이긴다. 주석이 이를 명시한다 — `globals.css:121-123`.

### 1층 전체 — `@theme inline` (globals.css:8-49, 선언 40개)

| 분류 | 개수 | 내용 |
|---|---|---|
| 폰트 | 2 | `--font-heading`, `--font-sans` |
| 색 별칭 `--color-*` | 31 | 아래 2절 시맨틱 토큰과 1:1 대응 |
| radius | 7 | `--radius-sm` ~ `--radius-4xl` (3절 참조) |

```css
/* globals.css:9-10 — 폰트 배선 */
--font-heading: var(--font-sans);
--font-sans: var(--font-sans);   /* 우변은 layout.tsx의 next/font 주입 변수 (4절) */
```

> ⚠️ `--font-sans: var(--font-sans)`는 오타가 아니다. `@theme inline`의 좌변은 Tailwind 테마 네임스페이스이고,
> 우변 `var(--font-sans)`는 `<html>`에 붙는 next/font 변수를 가리킨다 (`layout.tsx:9,20`).
> `--font-heading`이 `--font-sans`를 그대로 따르므로 **현재 제목/본문 폰트는 동일**하다.

---

## 1. 컬러 팔레트

### 1.1 팔레트 출처

```css
/* globals.css:51 — 원문 주석 그대로 */
/* SnowUI Design System (ByeWind) — researched palette, sRGB→OKLCH 변환 */
```

- 출처: **SnowUI Design System (ByeWind)**
- 색 공간: **OKLCH**. 원 팔레트가 sRGB였고 이를 OKLCH로 변환해 넣은 것이라고 주석이 밝히고 있다.
- 표기법: `oklch(L C H)` — L=명도 0~1, C=채도, H=색상각(deg). 무채색은 `C=0 H=0`.

### 1.2 라이트(`:root`) / 다크(`.dark`) 전체 대조표

- `:root` — `globals.css:52-85`, 선언 **32개** (색 31 + `--radius` 1)
- `.dark` — `globals.css:87-119`, 선언 **31개** (`--radius`는 재정의하지 않음 → 라이트 값 상속)

**HEX는 근사값이다.** OKLCH → OKLab → 선형 sRGB → 감마보정 변환을 직접 계산해 얻었다.
브라우저 렌더링 결과와 마지막 자리가 다를 수 있으므로 **참고용이며, 복붙은 OKLCH 원값으로 하라.**

| 토큰 | `:root` (라이트) OKLCH | ≈HEX | `.dark` OKLCH | ≈HEX |
|---|---|---|---|---|
| `--background` | `oklch(1 0 0)` | `#ffffff` | `oklch(0.226 0 0)` | `#1c1c1c` |
| `--foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--card` | `oklch(1 0 0)` | `#ffffff` | `oklch(0.285 0 0)` | `#2a2a2a` |
| `--card-foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--popover` | `oklch(1 0 0)` | `#ffffff` | `oklch(0.285 0 0)` | `#2a2a2a` |
| `--popover-foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--primary` | `oklch(0.205 0 0)` | `#171717` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` |
| `--primary-foreground` | `oklch(0.985 0 0)` | `#fafafa` | `oklch(0.226 0 0)` | `#1c1c1c` |
| `--secondary` | `oklch(0.982 0 0)` | `#f9f9f9` | `oklch(0.321 0 0)` | `#333333` |
| `--secondary-foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--muted` | `oklch(0.982 0 0)` | `#f9f9f9` | `oklch(0.305 0 0)` | `#2f2f2f` |
| `--muted-foreground` | `oklch(0.542 0 0)` | `#6f6f6f` | `oklch(0.715 0 0)` | `#a3a3a3` |
| `--accent` | `oklch(0.952 0.019 282.8)` | `#edeefc` | `oklch(0.321 0 0)` | `#333333` |
| `--accent-foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--destructive` | `oklch(0.667 0.220 25.5)` | `#ff4747` | `oklch(0.667 0.220 25.5)` | `#ff4747` |
| `--border` | `oklch(0.940 0 0)` | `#ebebeb` | `oklch(1 0 0 / 10%)` | 흰색 10% 알파 |
| `--input` | `oklch(0.940 0 0)` | `#ebebeb` | `oklch(1 0 0 / 15%)` | 흰색 15% 알파 |
| `--ring` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` |
| `--chart-1` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` | 〃 (동일) | `#9f9ff8` |
| `--chart-2` | `oklch(0.797 0.103 257.2)` | `#92bfff` | 〃 (동일) | `#92bfff` |
| `--chart-3` | `oklch(0.824 0.060 258.7)` | `#aec7ed` | 〃 (동일) | `#aec7ed` |
| `--chart-4` | `oklch(0.860 0.077 183.5)` | `#96e2d6` | 〃 (동일) | `#96e2d6` |
| `--chart-5` | `oklch(0.805 0.084 301.9)` | `#c9b3ed` | 〃 (동일) | `#c9b3ed` |
| `--sidebar` | `oklch(0.982 0 0)` | `#f9f9f9` | `oklch(0.226 0 0)` | `#1c1c1c` |
| `--sidebar-foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--sidebar-primary` | `oklch(0.205 0 0)` | `#171717` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` |
| `--sidebar-primary-foreground` | `oklch(0.985 0 0)` | `#fafafa` | `oklch(0.226 0 0)` | `#1c1c1c` |
| `--sidebar-accent` | `oklch(0.952 0.019 282.8)` | `#edeefc` | `oklch(0.321 0 0)` | `#333333` |
| `--sidebar-accent-foreground` | `oklch(0.226 0 0)` | `#1c1c1c` | `oklch(0.985 0 0)` | `#fafafa` |
| `--sidebar-border` | `oklch(0.940 0 0)` | `#ebebeb` | `oklch(1 0 0 / 10%)` | 흰색 10% 알파 |
| `--sidebar-ring` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` |

#### 이 팔레트에서 읽히는 규칙 (코드가 실제로 그렇게 되어 있음)

1. **회색이 진짜 회색이다.** `--background`/`--foreground`/`--card`/`--muted`/`--border` 전부 `C=0 H=0` — 색조가 섞이지 않은 순수 무채색.
2. **유일한 유채색 앵커는 hue 282.8 (보라)** — `--ring`, `--chart-1`, 라이트의 `--accent`, 다크의 `--primary`가 모두 이 색상각을 쓴다. 브랜드 액센트가 사실상 `oklch(0.738 0.127 282.8)` 하나다.
3. **라이트/다크에서 `--primary`가 뒤집힌다.** 라이트는 거의 검정(`0.205`), 다크는 보라(`0.738 0.127 282.8`). 즉 라이트에서 primary 버튼은 **검정 배경 + 흰 글자**, 다크에서는 **보라 배경 + 어두운 글자**다.
4. **차트 5색과 `--destructive`는 라이트/다크가 완전히 동일하다.** 테마 전환 시 그래프 색이 바뀌지 않는다.
5. **다크의 `--border`/`--input`만 알파 값**(`oklch(1 0 0 / 10%)`, `/ 15%`)이다. 불투명 회색이 아니라 배경 위에 흰색을 얹는 방식 → 카드 위/배경 위에서 자동으로 다르게 보인다.
6. `--secondary`와 `--muted`는 라이트에서 **값이 같다**(`0.982`). 다크에서만 갈라진다(`0.321` vs `0.305`).

### 1.3 커스텀 테마 31종 (globals.css:126-681)

`:root`/`.dark` 뒤에 선언되어 **덮어쓰는** 방식. 각 테마는 예외 없이 **31개 선언 전부**를 재정의한다
(`--radius`는 어느 테마도 건드리지 않음 → 전 테마 radius 동일).
계산: 31 테마 × 31 선언 = 961, + `@theme` 40 + `:root` 32 + `.dark` 31 = **1,064** ✓

값은 전부 **HEX**(OKLCH 아님)로 적혀 있다.

| # | 클래스 | 이름 (`components/theme-select.tsx`) | 명암 | `--background` | `--primary` | globals.css |
|---|---|---|---|---|---|---|
| 1 | `.tokyo-night` | Tokyo Night | dark | `#1a1b26` | `#7aa2f7` | 126 |
| 2 | `.nord` | Obsidian Nord | dark | `#2e3440` | `#88c0d0` | 144 |
| 3 | `.everforest` | Obsidian Everforest | dark | `#2d353b` | `#a7c080` | 162 |
| 4 | `.claude` | Claude | light | `#f5f4ee` | `#d97757` | 180 |
| 5 | `.monokai-sun` | Monokai Pro Light (Sun) | light | `#f8efe7` | `#cc6a3a` | 198 |
| 6 | `.solarized-dark` | Solarized Dark | dark | `#002b36` | `#268bd2` | 216 |
| 7 | `.dracula-soft` | Dracula Soft | dark | `#282a36` | `#bd93f9` | 234 |
| 8 | `.material-hc` | Material High Contrast | dark | `#0f111a` | `#82aaff` | 252 |
| 9 | `.monokai-pro` | Monokai Pro | dark | `#2d2a2e` | `#ffd866` | 270 |
| 10 | `.slack` | Slack | dark | `#1a1d21` | `#36c5f0` | 288 |
| 11 | `.rose-pine` | Rosé Pine | dark | `#191724` | `#c4a7e7` | 306 |
| 12 | `.quiet-light` | Quiet Light | light | `#f5f5f5` | `#7a3e9d` | 324 |
| 13 | `.earthbound` | EarthBound | dark | `#2b2438` | `#ff8c42` | 342 |
| 14 | `.base16-grayscale` | Base16 Grayscale | dark | `#101010` | `#cdcdcd` | 360 |
| 15 | `.solarized-autumn` | Solarized Autumn | dark | `#232017` | `#cb4b16` | 378 |
| 16 | `.turtle` | Turtle | dark | `#0e1a14` | `#4caf7d` | 396 |
| 17 | `.semantic-colors` | Semantic Colors | dark | `#1e1e1e` | `#569cd6` | 414 |
| 18 | `.natural` | Natural | light | `#f4ecd8` | `#7d9b56` | 432 |
| 19 | `.thanatos` | Thanatos | dark | `#16161d` | `#7b6ce6` | 450 |
| 20 | `.mossy-forest` | Mossy Forest Light Green | light | `#eef2e6` | `#5a8f3c` | 468 |
| 21 | `.codex` | Codex Theme Collection | dark | `#0d1117` | `#10a37f` | 486 |
| 22 | `.anthropic-inspired` | Anthropic Inspired | dark | `#1f1d1a` | `#cc785c` | 504 |
| 23 | `.retro-keyboard` | Retro Keyboard | dark | `#1a1410` | `#ffb000` | 522 |
| 24 | `.savanna-dusk` | Claude Kenya — Savanna Dusk | dark | `#241a14` | `#e0985a` | 540 |
| 25 | `.savanna-dawn` | Claude Kenya — Savanna Dawn | light | `#f7ece0` | `#d98a4f` | 558 |
| 26 | `.mocaccino-light` | Mocaccino Light | light | `#f3ece2` | `#8b5e3c` | 576 |
| 27 | `.claude-warm-light` | Claude Warm Light | light | `#faf4ec` | `#d97757` | 594 |
| 28 | `.claude-vscode` | Claude Theme for VS Code | dark | `#1f1e1c` | `#d97757` | 612 |
| 29 | `.paper-notebook` | Paper Notebook Light | light | `#faf7ef` | `#2d5fa3` | 630 |
| 30 | `.sociedade-pinguim` | SociedadePinguim | dark | `#1e1e2e` | `#a78bfa` | 648 |
| 31 | `.orange-flavor` | Orange Flavor | dark | `#1a1614` | `#ff8c1a` | 666 |

**다크 22종 + 라이트 9종 = 31.** 이 분류는 두 곳에서 일관되게 유지된다:
- `@custom-variant dark (...)` — `globals.css:6` (다크 22종 + `.dark`)
- `color-scheme: dark` 셀렉터 목록 — `globals.css:698-720` (동일 23개)
- `color-scheme: light` 셀렉터 목록 — `globals.css:721-729` (라이트 9종)

> **새 테마를 추가할 때 3곳을 모두 고쳐야 한다.** ① 테마 클래스 블록 ② `@custom-variant dark` 목록(다크일 때)
> ③ `color-scheme` 목록. ②를 빼먹으면 `dark:` 유틸리티가 안 먹고, ③을 빼먹으면 날짜/시간 네이티브 피커
> 아이콘이 반대 명암으로 렌더된다 (`globals.css:695-696` 주석에 이유가 적혀 있다).

#### `@custom-variant dark` 원문 (globals.css:6)

```css
@custom-variant dark (&:is(.dark *, .tokyo-night *, .nord *, .everforest *, .solarized-dark *, .dracula-soft *, .material-hc *, .monokai-pro *, .slack *, .rose-pine *, .earthbound *, .base16-grayscale *, .solarized-autumn *, .turtle *, .semantic-colors *, .thanatos *, .codex *, .anthropic-inspired *, .retro-keyboard *, .savanna-dusk *, .claude-vscode *, .sociedade-pinguim *, .orange-flavor *));
```

### 1.4 팔레트 밖에서 쓰는 원색 (Tailwind 기본 색)

시맨틱 토큰으로 커버되지 않는 상태 표현에는 Tailwind 기본 팔레트를 직접 쓴다. 실측 빈도:

| 클래스 | 빈도 | 용도 (실제 코드) |
|---|---|---|
| `bg-red-500` | 5 | 안읽음 배지 — `components/chat-panel.tsx:269,921,1052` |
| `border-emerald-500/30` | 7 | 성공/정상 상태 테두리 |
| `border-amber-500/30` | 6 | 경고 상태 테두리 |

> 이건 **관례가 아니라 예외**다. 새 코드에서는 가능하면 `--destructive` 등 시맨틱 토큰을 쓰라.
> (`bg-red-500` 배지가 `bg-destructive`를 쓰지 않는 이유는 코드 주석에 없음 → **미확인**)

---

## 2. Radius 스케일

기준값 하나(`--radius`)에 **배수**를 곱해 파생시키는 방식. Tailwind v4 기본 스케일을 **전부 덮어쓴다.**

```css
/* globals.css:76 — 기준값 (:root 안, .dark 및 31개 커스텀 테마 어디서도 재정의 안 함) */
--radius: 0.625rem;   /* = 10px */

/* globals.css:42-48 — @theme inline 안의 파생 */
--radius-sm:  calc(var(--radius) * 0.6);
--radius-md:  calc(var(--radius) * 0.8);
--radius-lg:  var(--radius);
--radius-xl:  calc(var(--radius) * 1.4);
--radius-2xl: calc(var(--radius) * 1.8);
--radius-3xl: calc(var(--radius) * 2.2);
--radius-4xl: calc(var(--radius) * 2.6);
```

| 유틸리티 | 계산식 | rem | **px** | Tailwind v4 기본값 | 덮어씀? |
|---|---|---|---|---|---|
| `rounded-sm` | `0.625 × 0.6` | `0.375rem` | **6px** | `0.25rem` (4px) | ✅ |
| `rounded-md` | `0.625 × 0.8` | `0.5rem` | **8px** | `0.375rem` (6px) | ✅ |
| `rounded-lg` | `0.625 × 1` | `0.625rem` | **10px** | `0.5rem` (8px) | ✅ |
| `rounded-xl` | `0.625 × 1.4` | `0.875rem` | **14px** | `0.75rem` (12px) | ✅ |
| `rounded-2xl` | `0.625 × 1.8` | `1.125rem` | **18px** | `1rem` (16px) | ✅ |
| `rounded-3xl` | `0.625 × 2.2` | `1.375rem` | **22px** | `1.5rem` (24px) | ✅ |
| `rounded-4xl` | `0.625 × 2.6` | `1.625rem` | **26px** | `2rem` (32px) | ✅ |
| `rounded-xs` | — | — | `0.125rem` (2px) | `0.125rem` | ❌ 기본값 그대로 |
| `rounded` (무접미사) | — | — | `0.25rem` (4px) | 하드코딩 | ❌ 스케일 무관 |
| `rounded-full` | — | — | `9999px` | 하드코딩 | ❌ 스케일 무관 |

> Tailwind 기본값 출처: `node_modules/.pnpm/tailwindcss@4.3.1/node_modules/tailwindcss/theme.css:397-404`
> **`--radius` 하나만 바꾸면 sm~4xl 7단계가 비례해서 전부 움직인다.** 이것이 이 스케일의 설계 의도다.
> 단, `rounded`(무접미사)와 `rounded-full`은 스케일 밖이라 따라오지 않는다.

### 실측 사용 빈도 (`app/**` + `components/**`)

| 유틸리티 | 빈도 | 실제 px | 주 용도 |
|---|---|---|---|
| `rounded-md` | 70 | 8px | 가장 흔한 기본 — 입력·작은 카드·메뉴 항목 |
| `rounded-full` | 53 | 9999px | 아바타, 배지, 스크롤바 thumb, pill 버튼 |
| `rounded` | 40 | 4px | 인라인 코드, 작은 태그 |
| `rounded-lg` | 25 | 10px | 중간 컨테이너 |
| `rounded-2xl` | 17 | 18px | **Button 기본** (`components/ui/button.tsx:8`) |
| `rounded-xl` | 15 | 14px | — |
| `rounded-sm` | 3 | 6px | — |
| `rounded-none` | 2 | 0 | — |

#### 특수 케이스 — Card는 상한이 걸린 radius를 쓴다

```css
/* components/ui/card.tsx:15 */
rounded-[min(var(--radius-4xl),24px)]
```
`--radius-4xl`(26px)과 24px 중 **작은 쪽** → 현재 값 기준 **24px**. `--radius`를 키워도 카드 모서리는 24px에서 멈춘다.
`CardHeader:28`, `CardFooter:84`, 카드 내부 첫/마지막 `img`도 동일 식을 쓴다.

---

## 3. 타이포그래피

### 3.1 폰트 패밀리 — 로드되는 실제 폰트는 **Inter 하나**

```tsx
// app/layout.tsx:5,9 — next/font/google
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

// app/layout.tsx:20
<html lang="ko" className={cn("font-sans", inter.variable)} suppressHydrationWarning>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 폰트 | **Inter** (Google Fonts, next/font 셀프호스팅) | `layout.tsx:5,9` |
| subsets | `['latin']` | `layout.tsx:9` |
| CSS 변수 | `--font-sans` | `layout.tsx:9` |
| weight 지정 | **없음** → next/font 기본 = **가변 폰트(variable font) 전 weight** | `layout.tsx:9` |
| 적용 지점 | `<html>` 에 `font-sans` + 변수 클래스 동시 부착 | `layout.tsx:20` |
| 전역 강제 | `html { @apply font-sans; }` | `globals.css:690-692` |
| `--font-heading` | `var(--font-sans)` → **Inter와 동일** | `globals.css:9` |

> **한글 폰트는 지정되지 않았다.** `subsets`가 `['latin']`뿐이고 `lang="ko"`인데 Inter에는 한글 글리프가 없으므로,
> 한글은 **OS 기본 sans-serif 폴백**(macOS: Apple SD Gothic Neo / Windows: 맑은 고딕)으로 렌더된다.
> 이는 코드에서 확인된 사실이며, 의도적인지 여부는 코드에 근거 없음 → **미확인**.

`font-mono`는 6회 사용되나 별도 폰트를 로드하지 않는다 → Tailwind 기본 mono 스택(OS 폴백).
사용처 예: `components/chat-thread.tsx:183` (타임스탬프/메타 줄).

### 3.2 텍스트 크기 계층 — 실측 빈도순

`app/**` + `components/**` 전수 grep 집계 (총 **497건**).

| 클래스 | 빈도 | 실제 크기 | line-height | 용도 (코드에서 확인된 것만) |
|---|---:|---|---|---|
| `text-sm` | **248** | `0.875rem` = **14px** | 1.25rem | **본문 기본값.** Card 전체가 `text-sm` (`ui/card.tsx:15`), Button 전체가 `text-sm` (`ui/button.tsx:8`), CardDescription (`ui/card.tsx:50`) |
| `text-xs` | **177** | `0.75rem` = **12px** | 1rem | 보조 라벨, 배지, 툴바 버튼 (`globals.css:944`), tiptap 인라인 코드·코드블록 (`globals.css:786,789`), Button `size=xs` (`ui/button.tsx:29`) |
| `text-base` | 15 | `1rem` = **16px** | 1.5rem | **제목용.** CardTitle (`ui/card.tsx:40`), DialogTitle (`ui/dialog.tsx:134`), SheetTitle (`ui/sheet.tsx:117`), DrawerTitle (`ui/drawer.tsx:102`) — 모두 `font-heading text-base font-medium` |
| `text-[11px]` | 15 | **11px** | 기본 | 타임스탬프 (`app/page.tsx:442`, `components/agent-working-indicator.tsx:80`), 아바타 이니셜 (`app/page.tsx:437`), 채팅 메타줄 (`chat-thread.tsx:183`), 섹션 헤더 대문자 라벨 (`chat-panel.tsx:1164`), 캘린더 셀 (`app/calendar/popout/page.tsx:186,193,203`) |
| `text-lg` | 14 | `1.125rem` = **18px** | 1.75rem | AlertDialogTitle (`ui/alert-dialog.tsx:126`), tiptap h3 (`globals.css:770`), 큰 숫자 (`chart-tokens.tsx:64`) |
| `text-[10px]` | 10 | **10px** | 기본 | 최소 크기. 알림 배지 (`notification-bell.tsx:128`), 마이크로 Badge (`org-chart.tsx:73`, `app/tools/page.tsx:92,97`), 인라인 코드 칩 (`org-chart.tsx:95`) |
| `text-[13px]` | 5 | **13px** | 기본 | `text-sm`(14)과 `text-xs`(12) 사이 미세조정. 요약문 (`app/page.tsx:473`), 메일 목록 제목 (`app/mail/page.tsx:862`), 캘린더 날짜 숫자 (`app/calendar/page.tsx:206`) |
| `text-[12px]` | 4 | **12px** | 기본 | `text-xs`와 **동일 크기** — 캘린더 페이지에서만 사용 (`app/calendar/page.tsx:213,220,228`, `popout/page.tsx:179`) |
| `text-2xl` | 4 | `1.5rem` = **24px** | 2rem | tiptap h1 (`globals.css:765`) |
| `text-3xl` | 3 | `1.875rem` = **30px** | 2.25rem | 대시보드 큰 수치 — `sm:` 반응형에서만 (`chart-tokens.tsx:64`) |
| `text-xl` | 2 | `1.25rem` = **20px** | 1.75rem | tiptap h2 (`globals.css:768`) |

> Tailwind 기본 크기 출처: `tailwindcss/theme.css:347-360`

**읽히는 규칙:**
1. **14px(`text-sm`)가 본문, 12px(`text-xs`)가 보조** — 이 둘만으로 **425건 / 497건 = 85.5%**. 나머지 9개 크기를 다 합쳐도 72건뿐이다. 즉 크기 선택지는 사실상 **2개**이고 나머지는 예외적 미세조정이다.
2. **제목은 크기가 아니라 `font-heading text-base font-medium` 조합으로 만든다.** 16px + medium(500)이 이 앱의 "제목"이다. 큰 글씨로 제목을 만들지 않는다.
3. **11px 이하는 "메타 정보" 전용** — 시각, 카운트, 배지 숫자. 본문에 쓰이지 않는다.
4. `text-[12px]`는 `text-xs`와 값이 같은 **중복**이다 (캘린더 4곳). 정리 대상.

### 3.3 Font weight — 실측 빈도

| 클래스 | 빈도 | 값 | 용도 |
|---|---:|---|---|
| `font-medium` | **113** | 500 | **강조 기본값.** 모든 제목 컴포넌트, Button 전체 (`ui/button.tsx:8`), 표 헤더 (`globals.css:922`), 읽지 않은 메일 (`app/mail/page.tsx:862`) |
| `font-semibold` | 35 | 600 | tiptap h1/h2/h3 (`globals.css:765,768,771`), 알림 배지 숫자 (`notification-bell.tsx:128`) |
| `font-normal` | 29 | 400 | 상속된 굵기를 **되돌릴 때** (`org-chart.tsx:60`) |
| `font-bold` | 8 | 700 | 최상위 수치 (`chart-tokens.tsx:64`), 안읽음 카운트 배지 (`chat-panel.tsx:269,921,1052`) |

**규칙: 굵기는 500(medium)이 기본 강조다.** 600은 tiptap 에디터 본문 제목에 한정, 700은 숫자 강조에만.
`font-sans`(8회)·`font-mono`(6회)는 weight가 아니라 패밀리 지정.

### 3.4 Line-height / 자간 — 실측

| 클래스 | 빈도 | 용도 |
|---|---:|---|
| `leading-relaxed` | 11 | 긴 본문 문단 |
| `leading-none` | 8 | 배지·숫자 — 높이를 글자에 딱 맞춤 (`chat-panel.tsx:910,1049`, `notification-bell.tsx:128`) |
| `leading-snug` | 4 | 요약문 (`app/page.tsx:473`) |
| `leading-tight` | 2 | — |
| `leading-6` / `leading-5` / `leading-4` | 1 / 2 / 2 | 픽셀 정렬이 필요한 곳 (`globals.css:826` 콜아웃 아이콘) |
| `tracking-wide` | 1 | 대문자 섹션 라벨 (`chat-panel.tsx:1164`) |
| `tracking-widest` | 1 | — |

**자간은 사실상 조정하지 않는다** (전체 2건). 줄간격도 대부분 Tailwind 크기별 기본값에 맡긴다.

### 3.5 텍스트 넘침 처리

| 클래스 | 빈도 | 비고 |
|---|---:|---|
| `truncate` | **54** | 압도적 기본 — 한 줄 말줄임 |
| `line-clamp-2` | 3 | 2줄 말줄임 |
| `line-clamp-1` | 2 | — |

> `truncate`는 부모에 `min-w-0`이 없으면 flex 안에서 동작하지 않는다. 코드에서 `flex min-w-0 flex-1` 조합이
> 반복 등장한다 (`chat-panel.tsx:650`, `employees/page.tsx:173`, `globals.css:815,838,896`). **이 조합이 관례다.**

---

## 4. 간격(Spacing) 관례

### 4.1 기준 단위

```
--spacing: 0.25rem  (= 4px)   ← Tailwind v4 기본값, 프로젝트에서 재정의하지 않음
```
출처: `tailwindcss/theme.css:325`. `globals.css`에 `--spacing` 선언 없음(확인함) → 기본값 사용.
따라서 `gap-2` = 2 × 4px = **8px**, `gap-1.5` = 1.5 × 4px = **6px**.

### 4.2 Gap — 실측 빈도

| 클래스 | 빈도 | px | 맥락 (코드에서 확인) |
|---|---:|---|---|
| `gap-2` | **103** | 8px | **기본 간격.** 아이콘+라벨 나열, 버튼 그룹, 리스트 항목 내부 (`chat-thread.tsx:794,807`, `employees/page.tsx:106,173`) |
| `gap-3` | 61 | 12px | 한 단계 넓은 그룹 — 컬럼 리스트 (`globals.css:893`) |
| `gap-1.5` | **61** | 6px | **밀집 UI 기본.** Button 기본/lg 사이즈 내부 (`ui/button.tsx:26,32`), CardHeader (`ui/card.tsx:28`), 칩·태그 나열 (`chat-thread.tsx:205,229`), 메타 줄 (`chat-thread.tsx:183`) |
| `gap-1` | 58 | 4px | 최밀집 — Button `xs`/`sm` (`ui/button.tsx:29,31`), 툴바 (`globals.css:940`) |
| `gap-4` | 17 | 16px | 섹션 간 |
| `gap-2.5` | 10 | 10px | 콜아웃 아이콘↔본문 (`globals.css:822`) |
| `gap-0.5` | 10 | 2px | 아이콘 피커 그리드 (`globals.css:832`) |
| `gap-6` | 3 | 24px | 최상위 레이아웃 |

**계층: 2px(0.5) → 4px(1) → 6px(1.5) → 8px(2) → 12px(3) → 16px(4) → 24px(6).**
`gap-5`(20px)는 **한 번도 쓰이지 않는다**. 8px에서 12px로 건너뛴다.

### 4.3 Padding — 실측 빈도 (상위)

| 클래스 | 빈도 | px | 맥락 |
|---|---:|---|---|
| `py-2` | 53 | 8px | 리스트 행 세로 |
| `px-2` | 49 | 8px | 밀집 가로 |
| `px-3` | 41 | 12px | Button 기본/sm 가로 (`ui/button.tsx:26,31`), 채팅 버블 (`chat-thread.tsx:701`), tiptap 콜아웃 (`globals.css:822`) |
| `py-1` | 28 | 4px | 최밀집 세로 |
| `py-1.5` | 25 | 6px | 메뉴 항목 (`chat-thread.tsx:807`), 툴바 (`globals.css:940`) |
| `p-3` | 24 | 12px | **정사각 패딩 기본** — tiptap 코드블록 (`globals.css:789`), 메일 본문 영역 (`app/mail/page.tsx:987`) |
| `px-1` | 23 | 4px | 배지 내부 (`chat-panel.tsx:269`) |
| `px-4` | 17 | 16px | Button `lg` (`ui/button.tsx:32`) |
| `p-6` / `px-6` / `pt-6` | 8 / 6 / 8 | 24px | 카드·페이지 여백 |
| `p-1.5` | 8 | 6px | 아이콘 피커 컨테이너 (`globals.css:832`) |

### 4.4 가로+세로 패딩 **조합** — 실측 (이게 진짜 관례다)

| 조합 | 빈도 | px | 용도 |
|---|---:|---|---|
| `px-2 py-1` | **23** | 8 / 4 | 칩·태그·작은 셀 (`chat-thread.tsx:229`, `globals.css:918` 표 셀) |
| `px-3 py-2` | 17 | 12 / 8 | 리스트 행, 채팅 버블 (`chat-thread.tsx:701`) |
| `px-3 py-2.5` | 7 | 12 / 10 | tiptap 콜아웃 (`globals.css:822`) |
| `px-1 py-0.5` | 6 | 4 / 2 | 최소 배지 — tiptap 인라인 코드 (`globals.css:786`), 캘린더 항목 (`app/calendar/page.tsx:220`) |
| `px-2.5 py-1` | 5 | 10 / 4 | 툴바 버튼 (`globals.css:943`) |
| `px-4 py-2` | 4 | 16 / 8 | 넓은 버튼 |

**규칙: 가로 패딩이 세로의 약 1.5~2배.** 예외 없이 이 비율을 지킨다.

### 4.5 세로 스택 — `space-y-*` 실측

| 클래스 | 빈도 | px | 맥락 |
|---|---:|---|---|
| `space-y-1.5` | **46** | 6px | **폼 필드 내부** — 라벨↔입력 |
| `space-y-1` | 37 | 4px | 리스트 항목 사이 (`globals.css:778,781,805` tiptap 목록) |
| `space-y-4` | 33 | 16px | **섹션 사이** |
| `space-y-3` | 13 | 12px | 중간 그룹 |
| `space-y-0.5` | 10 | 2px | 최밀집 |
| `space-y-2` | 5 | 8px | — |

> `space-y-1.5`(46)가 `space-y-2`(5)보다 9배 많다. **세로 밀집 간격의 기본은 8px이 아니라 6px이다.**
> 가로(`gap-2`=8px 기본)와 세로(`space-y-1.5`=6px 기본)의 기본값이 다르다는 점에 주의.

### 4.6 컴포넌트 내부 spacing 토큰 — `--card-spacing`

Card만 **자체 spacing 변수**를 갖는다. `globals.css`가 아니라 **컴포넌트에 인라인 선언**되어 있다.

```tsx
// components/ui/card.tsx:15
[--card-spacing:--spacing(5)]                      // 5 × 4px = 20px  (기본)
data-[size=sm]:[--card-spacing:--spacing(4)]       // 4 × 4px = 16px  (size="sm")
```

소비 지점 — `gap-(--card-spacing)`, `py-(--card-spacing)` (`card.tsx:15`), `px-(--card-spacing)`
(`card.tsx:28,73,84`), `[.border-b]:pb-(--card-spacing)` (`card.tsx:28`), `[.border-t]:pt-(--card-spacing)` (`card.tsx:84`).

> **Card 안쪽 여백을 바꾸려면 `card.tsx:15`의 이 값 하나만 바꾸면 된다.** header/content/footer가 전부 따라온다.

### 4.7 아이콘 크기 관례

| 컨텍스트 | 크기 | 출처 |
|---|---|---|
| Button 기본/sm/lg 내부 아이콘 | `size-4` (16px) | `ui/button.tsx:8` — `[&_svg:not([class*='size-'])]:size-4` |
| Button `xs` / `icon-xs` 내부 | `size-3` (12px) | `ui/button.tsx:29,35` |
| tiptap 콜아웃 아이콘 버튼 | `size-6` (24px) | `globals.css:828` |
| tiptap 아이콘 피커 항목 | `size-7` (28px) | `globals.css:835` |
| 워크보드 거터 버튼 | `size-6` (24px) | `globals.css:864` |

### 4.8 Button 높이 스케일 (`components/ui/button.tsx:26-36`)

| size | 높이 | 가로 패딩 | gap |
|---|---|---|---|
| `xs` | `h-6` (24px) | `px-2.5` | `gap-1` |
| `sm` | `h-7` (28px) | `px-3` | `gap-1` |
| `default` | `h-8` (32px) | `px-3` | `gap-1.5` |
| `lg` | `h-9` (36px) | `px-4` | `gap-1.5` |
| `icon-xs` / `icon-sm` / `icon` / `icon-lg` | `size-6` / `size-7` / `size-8` / `size-9` | — | — |

**4px 간격의 조밀한 스케일**(24/28/32/36px). shadcn 기본(36/32/40px)보다 전반적으로 작다.

---

## 5. 그림자 · 보더 · 링

### 5.1 Shadow — 실측 빈도

| 클래스 | 빈도 | 값 (Tailwind v4 기본) | 맥락 |
|---|---:|---|---|
| `shadow-xs` | **56** | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | **압도적 기본.** 거의 모든 표면 (`chart-tokens.tsx:43`) |
| `shadow` | 11 | — | (bare) |
| `shadow-none` | 10 | `none` | 그림자 제거 |
| `shadow-lg` | 9 | `0 10px 15px -3px …, 0 4px 6px -4px …` | 떠 있는 표면 — 표 컨트롤 툴바 (`globals.css:940`) |
| `shadow-sm` | 6 | `0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px …` | **Card** (`ui/card.tsx:15`) |
| `shadow-md` | 4 | — | 아이콘 피커 팝오버 (`globals.css:832`) |
| `shadow-xl` | 4 | — | — |
| `shadow-2xl` | 1 | — | — |

> Tailwind 기본 그림자 값 출처: `tailwindcss/theme.css:406-412`
> **깊이 위계: `shadow-xs`(평면) → `shadow-sm`(카드) → `shadow-md`(팝오버) → `shadow-lg`(플로팅 툴바).**
> 이 앱은 그림자를 거의 쓰지 않고 **테두리(ring/border)로 표면을 구분한다** — 아래 5.3 참조.

### 5.2 Border

전역 기본이 `globals.css`에 박혀 있다:

```css
/* globals.css:684-686 */
* {
  @apply border-border outline-ring/50;
}
```
→ **모든 요소의 기본 테두리 색이 `--border`, 기본 아웃라인이 `--ring` 50%.**
그래서 코드에서는 색 없이 `border`/`border-b`만 쓰면 자동으로 테마 색이 붙는다.

| 클래스 | 빈도 | 비고 |
|---|---:|---|
| `border` | 105 | 색 미지정 → 위 전역 규칙으로 `--border` |
| `border-b` | 21 | 구분선 |
| `border-0` | 16 | 제거 |
| `border-border` | 12 | 명시 (전역 규칙과 동일 결과) |
| `border-t` | 11 | |
| `border-primary` | 9 | 선택 상태 |
| `border-ring` | 8 | 포커스 (`ui/button.tsx:8` — `focus-visible:border-ring`) |
| `border-transparent` | 8 | 레이아웃 유지용 (`ui/button.tsx:8` 기본) |
| `border-destructive` | 8 | 에러 |
| `border-l` / `border-r` | 8 / 5 | |
| `border-destructive/50` | 5 | 다크모드 에러 (`ui/button.tsx:8`) |

기타 확인된 보더 관례:
- 점선 — `border-dashed border-transparent` → hover 시 `border-border/60`으로 드러남 (tiptap 컬럼 경계, `globals.css:896,906`)
- 인용문 — `border-l-2 border-border` (`globals.css:783`)
- 표 셀 — `border border-border` (`globals.css:918`)

### 5.3 Ring — **이 앱의 표면 구분 주력 수단**

| 클래스 | 빈도 | 맥락 |
|---|---:|---|
| `ring` (bare/조합 포함) | 78 | — |
| `ring-3` | 15 | **포커스 링 표준 두께** — `focus-visible:ring-3 focus-visible:ring-ring/30` (`ui/button.tsx:8`) |
| `ring-1` | 15 | **표면 경계** — Card `ring-1 ring-foreground/5` (`ui/card.tsx:15`) |
| `ring-foreground/10` | 9 | 다크모드 Card 경계 (`ui/card.tsx:15` — `dark:ring-foreground/10`) |
| `ring-destructive/40` | 9 | 다크 에러 (`ui/button.tsx:8`) |
| `ring-destructive/20` | 9 | 라이트 에러 (`ui/button.tsx:8`) |
| `ring-foreground/5` | 8 | 라이트모드 Card 경계 |
| `ring-2` | 7 | 배지 외곽 (`chat-panel.tsx:269` — `ring-2 ring-background`) |
| `ring-ring/30` | 6 | 포커스 링 색 |
| `ring-sidebar-ring` | 5 | 사이드바 포커스 |
| `ring-background` | 5 | 배경색 링 = 겹침 분리용 |
| `ring-[3px]` | 4 | — |
| `ring-ring/50` | 3 | — |

**핵심 패턴 — Card 표면 (`components/ui/card.tsx:15`):**
```
shadow-sm ring-1 ring-foreground/5 dark:ring-foreground/10
```
> `border`가 아니라 **`ring-1` + 전경색 5%(다크 10%) 알파**로 카드 경계를 그린다.
> 테마가 31종이라 고정 테두리색을 쓸 수 없기 때문 — 전경색 알파는 어느 테마에서도 자동으로 맞는다.
> **새 표면 컴포넌트를 만들 때 이 패턴을 그대로 쓰라.**

**핵심 패턴 — 포커스 (`components/ui/button.tsx:8`):**
```
outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30
```
에러 상태: `aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20`
+ `dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40`

`outline-none` 18회, `outline-hidden` 13회 — 네이티브 아웃라인을 끄고 ring으로 대체하는 것이 일관된 관례다.

### 5.4 알파 합성 — `color-mix`

테마 무관 반투명 처리에 `color-mix(in oklab, ...)`를 쓴다.

```css
/* globals.css:876 — 텍스트 선택 영역 */
background-color: color-mix(in oklab, var(--primary) 22%, transparent);

/* globals.css:880 — 블록 선택 하이라이트 */
background-color: color-mix(in oklab, var(--primary) 16%, transparent);
```
```tsx
/* components/ui/button.tsx:16 — secondary hover */
hover:bg-[color-mix(in_oklch,var(--secondary),var(--foreground)_5%)]
```
> 색 공간이 `oklab`(CSS)과 `oklch`(버튼)로 **혼용**되어 있다. 의도적 구분인지는 코드에 근거 없음 → **미확인**.

---

## 6. 커스텀 유틸 · 레이어 · 전역 규칙

`globals.css:683-960`에 **66개 CSS 규칙**이 정의되어 있다. 전수 목록:

### 6.1 `@layer base` (globals.css:683-693)

```css
@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground; }
  html { @apply font-sans; }
}
```

### 6.2 `color-scheme` — 네이티브 컨트롤 명암 (globals.css:695-729)

```css
:root { color-scheme: light; }
.dark, .tokyo-night, … (23개) { color-scheme: dark; }
.claude, .monokai-sun, … (9개) { color-scheme: light; }
```
> 원문 주석(`globals.css:695-696`): 날짜/시간 선택 아이콘·네이티브 컨트롤이 테마에 맞게 렌더되도록.

### 6.3 전역 슬림 스크롤바 (globals.css:731-742)

```css
* {
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}
*::-webkit-scrollbar { width: 8px; height: 8px; }
*::-webkit-scrollbar-track { background: transparent; }
*::-webkit-scrollbar-thumb { background: var(--border); border-radius: 9999px; }
*::-webkit-scrollbar-thumb:hover { background: var(--muted-foreground); }
```

**관련 — `SLIM` 상수** (`app/mail/page.tsx:60-61`). 전역 규칙보다 **더 얇은**(6px) 스크롤바가 필요한 곳에서
Tailwind arbitrary variant로 구현한 지역 상수다. `globals.css`에는 없다.

```ts
// app/mail/page.tsx:60-61
// 가드레일(트랙/거터) 없이 테마색 슬라이더만 — 슬림하게.
const SLIM =
  "[scrollbar-width:thin] [scrollbar-color:var(--border)_transparent] [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar]:bg-transparent [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-border hover:[&::-webkit-scrollbar-thumb]:bg-muted-foreground/40"
```
| 항목 | 전역 (`globals.css:736`) | `SLIM` (`mail/page.tsx:61`) |
|---|---|---|
| 두께 | 8px | `w-1.5` = **6px** |
| thumb 기본 | `var(--border)` | `bg-border` (동일) |
| thumb hover | `var(--muted-foreground)` (불투명) | `muted-foreground/40` (40% 알파) |

사용처 3곳: `app/mail/page.tsx:817, 987, 1076`.

**같은 파일의 또 다른 레이아웃 상수** (`app/mail/page.tsx:63-64`):
```ts
// 전역 프레임: SiteHeader(3rem) + 콘텐츠 py-6(상하 1.5rem씩) → 본문 가용 높이.
const FULL_H = "h-[calc(100svh-9rem)]";
```
> ⚠️ 주석의 계산(3rem + 1.5rem×2 = 6rem)과 실제 값(`9rem`)이 맞지 않는다. 왜 9rem인지 코드에 근거 없음 → **미확인**.

### 6.4 리스트뷰 표 여백 축소 (globals.css:744-758)

Tailwind 유틸리티를 이기기 위해 `data-slot` 속성 선택자로 특이도를 올린 규칙 3개. 원문 주석이 이유를 명시한다.

```css
table thead th[data-slot="table-head"]                  { height: 2rem; }
table tbody tr:first-child > td[data-slot="table-cell"]  { padding-top: 0.375rem; }
table tbody tr:last-child  > td[data-slot="table-cell"]  { padding-bottom: 0.375rem; }
```

### 6.5 tiptap 워크보드 에디터 (globals.css:760-960)

`.tiptap` 스코프 안의 WYSIWYG 스타일. **전체 목록:**

| 구역 | 셀렉터 | 라인 | 핵심 토큰 |
|---|---|---|---|
| 기본 블록 | `.tiptap :first-child` | 761 | `margin-top: 0` |
| 제목 | `.tiptap h1` / `h2` / `h3` | 764/767/770 | `text-2xl` / `text-xl` / `text-lg` + `font-semibold` |
| 문단 | `.tiptap p` | 773 | `mb-2` |
| 목록 | `.tiptap ul` / `ol` | 776/779 | `mb-2 ml-5 list-disc|decimal space-y-1` |
| 인용 | `.tiptap blockquote` | 782 | `border-l-2 border-border pl-3 text-muted-foreground` |
| 인라인 코드 | `.tiptap code` | 785 | `rounded bg-muted px-1 py-0.5 text-xs` |
| 코드블록 | `.tiptap pre` / `pre code` | 788/791 | `rounded-md bg-muted p-3 text-xs` |
| 링크 | `.tiptap a` | 794 | `text-primary underline` |
| 구분선 | `.tiptap hr` | 797 | `my-3 border-border` |
| 이미지 | `.tiptap img` | 800 | `my-2 max-w-full rounded` |
| 체크박스 목록 | `.tiptap ul[data-type="taskList"]` (+ li / label / div / 중첩) | 804·807·810·813·817 | `flex items-start gap-2` |
| 콜아웃 | `.tiptap div[data-type="callout"]` (+ icon / icon-btn / picker / picker-item / body / first / last) | 821·824·827·831·834·837·840·843 | `gap-2.5 rounded-lg border border-border bg-muted/50 px-3 py-2.5` |
| 토글 | `.tiptap div[data-type="toggle"]` (+ marker / 닫힘 규칙) | 847·850·855 | `relative my-1 pl-6` |
| 거터 핸들 | `.wb-gutter` / `.wb-gutter-btn` / `.wb-drag-grip` | 860·863·866 | `size-6 rounded text-muted-foreground/70` |
| 블록 선택 | `.tiptap .ProseMirror-selectednode` | 871 | `rounded-sm bg-primary/10 outline-2 outline-primary/20` |
| 텍스트 선택 | `.tiptap ::selection` | 875 | `color-mix(in oklab, var(--primary) 22%, transparent)` |
| 다중 블록 선택 | `.tiptap .wb-block-selected` | 879 | `color-mix(… 16% …)` + `border-radius: 0.25rem` |
| 선택 숨김 | `.tiptap.wb-block-selecting ::selection` / `.ProseMirror-hideselection ::selection` | 884·887 | `background: transparent` |
| 컬럼 | `.tiptap div[data-type="column-list"]` / `column` (+ first / last / hover) | 892·895·898·901·905 | `flex flex-col gap-3 sm:flex-row sm:gap-4` |
| 표 | `.tiptap .tableWrapper` / `table` / `td,th` / `th` / `td>p,th>p` / `.selectedCell::after` | 910·913·916·920·923·927 | `text-sm`, `min-w-24 border border-border px-2 py-1`, `bg-muted font-medium` |
| 컬럼 리사이즈 | `.tiptap table .column-resize-handle` (+ hover) | 932·935 | `w-1 bg-primary/30` → hover `bg-primary/70` |
| 표 툴바 | `.wb-table-controls` (+ button / danger / sep) | 939·942·945·948 | `rounded-full border bg-card/95 px-2 py-1.5 shadow-lg backdrop-blur` |
| 리사이즈 커서 | `.tiptap .resize-cursor` | 951 | `cursor: col-resize / ew-resize` |
| placeholder | `.tiptap p.is-editor-empty:first-child::before` | 957 | `content: attr(data-placeholder)` + `text-muted-foreground` |

**워크보드 전용 클래스 네임스페이스 = `wb-`** (`wb-gutter`, `wb-callout-*`, `wb-toggle-*`, `wb-block-selected`, `wb-block-selecting`, `wb-table-controls`, `wb-drag-grip`).

### 6.6 import 3개 (globals.css:1-3)

```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";
```

| import | 실체 | 토큰 제공? |
|---|---|---|
| `tailwindcss` | `tailwindcss@4.3.1` | ✅ `--spacing`, `--text-*`, `--shadow-*`, `--font-weight-*` 기본값 |
| `tw-animate-css` | 애니메이션 유틸리티 | 이 문서 범위 밖 — **미확인** |
| `shadcn/tailwind.css` | `shadcn@4.11.0` → `dist/tailwind.css` (95줄) | ❌ **색·간격·타이포 토큰 전무.** 확인함 |

`shadcn/tailwind.css`가 실제로 제공하는 것 (전수 — 파일 95줄 직접 읽음):
- `@keyframes accordion-down` / `accordion-up` (1-25행)
- `@custom-variant` 9개: `data-open`, `data-closed`, `data-checked`, `data-unchecked`, `data-selected`, `data-disabled`, `data-active`, `data-horizontal`, `data-vertical` (28-86행)
- `@utility no-scrollbar` (88-95행)

> **따라서 색/간격/타이포의 유일한 정본은 `app/globals.css` + Tailwind 기본값이다.** 서드파티가 끼어들지 않는다.

---

## 7. 차트 토큰

`--chart-1` ~ `--chart-5`는 라이트/다크 **동일 값**이며, 커스텀 테마 31종은 각자 5색을 재정의한다.

소비 방식 (`components/chart-tokens.tsx:24-28`):
```tsx
const chartConfig = {
  tokens: { label: "토큰" },
  input:  { label: "입력", color: "var(--chart-1)" },
  output: { label: "출력", color: "var(--chart-2)" },
} satisfies ChartConfig;
```
실제 렌더 (`components/chart-tokens.tsx:116`):

```tsx
<Bar dataKey={active} fill={`var(--color-${active})`} />
```

→ shadcn `ChartContainer`가 `chartConfig`의 `color`를 `--color-input` / `--color-output`으로 승격시킨다.
즉 차트에서 쓰는 색 변수 이름은 `--chart-N`이 아니라 **`chartConfig`의 키 이름**(`--color-input`)이 된다.

| 토큰 | 기본 팔레트 OKLCH | ≈HEX | 계열 |
|---|---|---|---|
| `--chart-1` | `oklch(0.738 0.127 282.8)` | `#9f9ff8` | 보라 (= `--ring`, 브랜드 앵커) |
| `--chart-2` | `oklch(0.797 0.103 257.2)` | `#92bfff` | 파랑 |
| `--chart-3` | `oklch(0.824 0.060 258.7)` | `#aec7ed` | 연한 파랑 (저채도) |
| `--chart-4` | `oklch(0.860 0.077 183.5)` | `#96e2d6` | 청록 |
| `--chart-5` | `oklch(0.805 0.084 301.9)` | `#c9b3ed` | 연보라 |

**5색 모두 L 0.738~0.860의 좁은 명도대 + C 0.060~0.127의 낮은 채도.** 파스텔 계열로 균일하게 묶여 있어
어느 색이 도드라지지 않는다 (범주형 차트에 적합, 강조가 필요하면 별도 처리 필요).

---

## 8. 재현 체크리스트

다른 프로젝트에서 이 디자인을 "자 대고 맞춘 듯" 재현하려면:

1. **색** — `globals.css:52-119`의 `:root` + `.dark` 블록을 **OKLCH 원값 그대로** 복사. HEX로 변환하지 말 것 (알파 토큰 `oklch(1 0 0 / 10%)`이 깨진다).
2. **배선** — `globals.css:8-49`의 `@theme inline` 블록을 그대로 복사. 이게 없으면 `bg-primary` 같은 유틸리티가 동작하지 않는다.
3. **radius** — `--radius: 0.625rem` + 7개 `calc()` 파생 (`globals.css:42-48,76`).
4. **폰트** — `Inter({ subsets: ['latin'], variable: '--font-sans' })` + `<html className="font-sans {inter.variable}">` (`layout.tsx:9,20`). 한글이 필요하면 **여기서 한글 폰트를 추가해야 한다** (현재 없음).
5. **전역 base** — `globals.css:683-693`의 3줄. 특히 `* { @apply border-border outline-ring/50 }`이 빠지면 모든 테두리가 무색이 된다.
6. **표면 패턴** — 카드류는 `shadow-sm ring-1 ring-foreground/5 dark:ring-foreground/10` (`ui/card.tsx:15`).
7. **포커스 패턴** — `outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30` (`ui/button.tsx:8`).
8. **간격 기본값** — 가로 `gap-2`(8px), 세로 `space-y-1.5`(6px), 패딩 조합 `px-2 py-1` / `px-3 py-2`.
9. **타이포 기본값** — 본문 `text-sm`(14px), 보조 `text-xs`(12px), 제목 `font-heading text-base font-medium`(16px/500).
10. **스크롤바** — `globals.css:731-742` (전역 8px). 더 얇게는 `SLIM` 패턴 (`mail/page.tsx:61`).

---

## 9. 미확인 항목 (코드에서 확인 못 한 것 — 추측하지 않음)

| # | 항목 | 상태 |
|---|---|---|
| 1 | **HEX 근사값 전부** | OKLCH→OKLab→sRGB 변환을 직접 계산한 **근사값**이다. 코드에 HEX로 적혀 있지 않다(커스텀 테마 31종 제외). 브라우저 실제 렌더값과 최하위 자리가 다를 수 있다. `--destructive: oklch(0.667 0.220 25.5)`는 sRGB 색역 경계에 있어 클리핑 가능성이 있다 → 실측 필요. **복붙은 OKLCH로.** |
| 2 | **한글 폰트 미지정이 의도인지** | `subsets: ['latin']` + `lang="ko"` 조합이 코드에 있는 사실은 확인. 의도 여부는 주석·문서 근거 없음. |
| 3 | **`--font-heading`을 `--font-sans`와 분리할 계획이 있는지** | `globals.css:9`에서 동일하게 배선된 사실만 확인. 분리 의도 근거 없음. |
| 4 | **`bg-red-500` 배지가 `bg-destructive`를 안 쓰는 이유** | `chat-panel.tsx:269,921,1052`에 존재하는 사실만 확인. 근거 주석 없음. |
| 5 | **`FULL_H = "h-[calc(100svh-9rem)]"`의 9rem 산출 근거** | 바로 위 주석의 계산(3rem+1.5rem×2=6rem)과 불일치. `mail/page.tsx:63-64`. |
| 6 | **`color-mix` 색공간 혼용** (`oklab` vs `oklch`) | `globals.css:876,880`은 `oklab`, `ui/button.tsx:16`은 `oklch`. 의도적 구분인지 근거 없음. |
| 7 | **`text-[12px]`와 `text-xs`가 같은 값인데 병존하는 이유** | 캘린더 4곳(`app/calendar/**`)에서만 `text-[12px]` 사용. 근거 없음. |
| 8 | **`tw-animate-css`가 정의하는 토큰** | 이 문서 범위(색·타이포·radius·간격) 밖이라 조사하지 않음. 애니메이션 토큰이 필요하면 별도 조사 필요. |
| 9 | **다크모드 전환 메커니즘** | `app/providers.tsx`가 테마 클래스를 붙인다는 것만 grep으로 확인. 구현 상세는 미조사(이 문서 범위 밖). |
| 10 | **접근성 대비비(WCAG) 검증** | 어떤 조합도 대비비를 실측하지 않았다. 특히 `--muted-foreground` 계열은 검증 필요. |

---

## 부록 A — 추출 방법 (재현 가능)

```bash
cd <인트라넷 레포>

# 토큰 선언 총 개수
rg -o -- '--[a-z0-9-]+\s*:' app/globals.css | wc -l          # → 1064
rg -o -- '--[a-z0-9-]+\s*:' app/globals.css | sed 's/[: ]//g' | sort -u | wc -l   # → 72

# 커스텀 테마 개수
sed -n '121,681p' app/globals.css | rg -c '^\.[a-z0-9-]+ \{'  # → 31

# 텍스트 크기 빈도
rg -o --no-filename 'text-\[[0-9]+px\]|text-(xs|sm|base|lg|xl|2xl|3xl)\b' app components | sort | uniq -c | sort -rn

# 간격 빈도
rg -o --no-filename 'gap-[0-9.]+' app components | sort | uniq -c | sort -rn
rg -o --no-filename 'space-y-[0-9.]+' app components | sort | uniq -c | sort -rn

# 패딩 조합 빈도
rg -o --no-filename 'px-3 py-2\.5|px-2 py-1|px-3 py-2|px-2\.5 py-1|px-4 py-2|px-1 py-0\.5' app components | sort | uniq -c | sort -rn

# Tailwind 기본값 대조
rg -n '^\s*--(spacing|radius-|text-|shadow-|font-weight-)' \
  node_modules/.pnpm/tailwindcss@4.3.1/node_modules/tailwindcss/theme.css
```

---

## 부록 B — 관련 문서

| 파일 | 역할 |
|---|---|
| `app/globals.css` | **정본** — 색·radius 토큰, 전역 base, 커스텀 레이어 |
| `app/layout.tsx` | 폰트 로딩 (`Inter`, `--font-sans`) |
| `components/theme-select.tsx` | 테마 선택 UI + 34개 항목 레지스트리(light/dark/system + 31) |
| `components/ui/card.tsx` | 표면 패턴 정본 (`ring-1 ring-foreground/5`, `--card-spacing`) |
| `components/ui/button.tsx` | 포커스·크기 스케일 정본 |
| `components/chart-tokens.tsx` | 차트 색 소비 예시 |
