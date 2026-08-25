# 02. UI 프리미티브 레퍼런스 (27종)

원본 인트라넷 `components/ui/` 전체 27개 컴포넌트의 **실측 스펙**. 모든 클래스 문자열은
소스 파일에서 그대로 복사한 원문이며, 각 값에 `파일:라인` 출처를 달았다. 이 문서만 보고 동일한
외형(높이·패딩·radius·글자크기·상태)을 재현할 수 있어야 한다.

- 추출 기준: 저장소 `components/ui/*.tsx` 27개 파일 (읽은 시점 기준 HEAD)
- 스택: React 19 + Next.js(App Router) + Tailwind CSS v4 + `radix-ui`(통합 패키지) + `cva`
- 이 문서는 **디자인 토큰 자체**(색/타이포/spacing 변수)는 다루지 않는다 — 토큰은 `app/globals.css` 참조.

---

## 0. 이 라이브러리의 공통 규약 (shadcn 대비 전역 커스터마이즈)

27개 전부에 걸쳐 적용되는 프로젝트 고유 규칙이다. **개별 컴포넌트보다 먼저 읽어야 한다.**

| 규약 | 내용 | 근거 |
|---|---|---|
| **통합 radix import** | `import { Dialog as DialogPrimitive } from "radix-ui"` — 개별 `@radix-ui/react-*` 패키지를 쓰지 않고 단일 `radix-ui` 패키지에서 네임스페이스로 가져온다 | `components/ui/dialog.tsx:4`, `select.tsx:4`, `avatar.tsx:4` 등 전 파일 |
| **`Slot.Root`** | `asChild` 구현이 `Slot`이 아니라 `Slot.Root` | `button.tsx:52`, `badge.tsx:37`, `breadcrumb.tsx:48` |
| **`data-slot` 전면 부착** | 모든 요소에 `data-slot="<이름>"`. CSS에서 `*:data-[slot=...]`로 자식을 선택하는 패턴이 라이브러리 전반에 쓰인다 | `avatar.tsx:81`, `select.tsx:47`, `usage/page.tsx:262` |
| **`data-variant` / `data-size` 부착** | variant·size를 클래스뿐 아니라 DOM 속성으로도 노출 → 부모가 `group-data-[size=lg]/avatar:` 식으로 자식 스타일을 제어 | `button.tsx:57-58`, `badge.tsx:42`, `avatar.tsx:18` |
| **`group/<이름>` 네이밍** | 컨테이너마다 named group (`group/button`, `group/card`, `group/avatar`, `group/toggle-group`) → 중첩 group 충돌 방지 | `button.tsx:8`, `card.tsx:15`, `avatar.tsx:20` |
| **radius 기본값 = `rounded-2xl`** | shadcn 기본(`rounded-md`)이 아니라 **`rounded-2xl`**이 기본. 큰 표면(Card/Dialog)은 `rounded-[min(var(--radius-4xl),24px)]` | `button.tsx:8`, `input.tsx:11`, `card.tsx:15` |
| **radius 토큰** | `--radius: 0.625rem`(10px), `--radius-xl: calc(var(--radius) * 1.4)`(0.875rem=14px), `--radius-4xl: calc(var(--radius) * 2.6)`(1.625rem=26px → `min(…,24px)`으로 **24px 캡**) | `app/globals.css:45,48,76` |
| **focus 링 = `ring-3` + `ring-ring/30`** | shadcn 기본 `ring-[3px] ring-ring/50` 대신 대부분 `focus-visible:ring-3 focus-visible:ring-ring/30`로 통일. (Badge/Toggle/Tabs 일부는 `ring-[3px]`·`/50` 잔존) | `button.tsx:8`, `input.tsx:11`, `textarea.tsx:10` |
| **입력 배경 = `bg-input/50` + 투명 보더** | shadcn의 `border-input bg-transparent` 대신 **`border border-transparent bg-input/50`** (채워진 필드 룩) | `input.tsx:11`, `textarea.tsx:10`, `select.tsx:47` |
| **테두리 대신 `ring-1 ring-foreground/5`** | 떠 있는 표면(Card/Dialog/Popover/Select/Dropdown)은 border가 아니라 ring. 다크모드는 `dark:ring-foreground/10` | `card.tsx:15`, `dialog.tsx:65`, `select.tsx:72` |
| **`data-open` / `data-closed` / `data-active` 축약** | `data-[state=open]` 대신 Tailwind v4 축약형 `data-open:` 사용이 지배적 | `dialog.tsx:42`, `tabs.tsx:68`, `dropdown-menu.tsx:46` |
| **`has-data-[icon=inline-start|end]`** | 아이콘이 앞/뒤에 붙으면 해당 방향 패딩을 자동으로 줄이는 광학 정렬 규칙 — Button/Badge/Toggle 공통 | `button.tsx:25-28`, `badge.tsx:8`, `toggle.tsx:19-21` |
| **`font-heading`** | 제목류(CardTitle/DialogTitle/SheetTitle/DrawerTitle/AlertDialogTitle)는 본문 폰트와 분리된 `font-heading` | `card.tsx:40`, `dialog.tsx:134`, `alert-dialog.tsx:126` |

---

## 1. Button

버튼 — 앱 전역에서 가장 많이 쓰이는 프리미티브(26개 파일). `components/ui/button.tsx`

### 베이스 클래스 (`button.tsx:8`)

```
group/button inline-flex shrink-0 items-center justify-center rounded-2xl border border-transparent bg-clip-padding text-sm font-medium whitespace-nowrap transition-all outline-none select-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30 active:not-aria-[haspopup]:translate-y-px disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4
```

### variant (`button.tsx:11-22`)

| variant | 클래스 원문 |
|---|---|
| `default` | `bg-primary text-primary-foreground hover:bg-primary/80` |
| `outline` | `border-border bg-background hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground dark:bg-transparent dark:hover:bg-input/30` |
| `secondary` | `bg-secondary text-secondary-foreground hover:bg-[color-mix(in_oklch,var(--secondary),var(--foreground)_5%)] aria-expanded:bg-secondary aria-expanded:text-secondary-foreground` |
| `ghost` | `hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground dark:hover:bg-muted/50` |
| `destructive` | `bg-destructive/10 text-destructive hover:bg-destructive/20 focus-visible:border-destructive/40 focus-visible:ring-destructive/20 dark:bg-destructive/20 dark:hover:bg-destructive/30 dark:focus-visible:ring-destructive/40` |
| `link` | `text-primary underline-offset-4 hover:underline` |

### size (`button.tsx:23-33`)

| size | 클래스 원문 | 높이 |
|---|---|---|
| `default` | `h-8 gap-1.5 px-3 has-data-[icon=inline-end]:pr-2.5 has-data-[icon=inline-start]:pl-2.5` | 32px |
| `xs` | `h-6 gap-1 px-2.5 text-xs has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2 [&_svg:not([class*='size-'])]:size-3` | 24px |
| `sm` | `h-7 gap-1 px-3 has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2` | 28px |
| `lg` | `h-9 gap-1.5 px-4 has-data-[icon=inline-end]:pr-3 has-data-[icon=inline-start]:pl-3` | 36px |
| `icon` | `size-8` | 32×32 |
| `icon-xs` | `size-6 [&_svg:not([class*='size-'])]:size-3` | 24×24 |
| `icon-sm` | `size-7` | 28×28 |
| `icon-lg` | `size-9` | 36×36 |

기본값: `variant: "default"`, `size: "default"` (`button.tsx:35-38`)

### 기본 외형 값

- 높이 32px(`h-8`) / 패딩 `px-3` / radius `rounded-2xl` / 글자 `text-sm font-medium`
- 보더: `border border-transparent` + `bg-clip-padding` (배경이 보더 영역으로 새지 않게)
- 아이콘 기본 크기: `size-4`(=16px), 단 `xs`/`icon-xs`는 `size-3`

### 상태 스타일

- **hover**: variant별로 다름(위 표)
- **focus-visible**: `border-ring` + `ring-3 ring-ring/30`
- **active**: `active:not-aria-[haspopup]:translate-y-px` — 눌리면 1px 내려감. **단 `aria-haspopup` 요소(드롭다운 트리거)는 제외**
- **aria-expanded**: `outline`/`secondary`/`ghost`는 열린 상태에서 hover와 동일한 배경 유지
- **disabled**: `pointer-events-none opacity-50`
- **aria-invalid**: `border-destructive ring-3 ring-destructive/20`(다크 `/40`)

### shadcn 기본과 다른 커스터마이즈 포인트

> - **size 8종** (shadcn은 4종: default/sm/lg/icon). `xs`, `icon-xs`, `icon-sm`, `icon-lg` 추가.
> - **`default` 높이가 `h-8`(32px)** — shadcn `h-9`(36px)보다 낮다. shadcn의 `h-9`는 여기서 `lg`.
> - **`rounded-2xl`** (shadcn `rounded-md`).
> - **`destructive`가 채움이 아니라 톤다운** — `bg-destructive/10 text-destructive` (shadcn은 `bg-destructive text-white`).
> - **`active:translate-y-px` 눌림 모션** + `aria-haspopup` 예외.
> - **`has-data-[icon=inline-*]` 광학 패딩 보정**.
> - **`aria-expanded` 스타일** — 팝오버 트리거가 열려 있는 동안 강조 유지.
> - `bg-clip-padding`, `select-none` 추가.

### 사용 예시 (`app/calendar/page.tsx:157`)

```tsx
<Button variant="outline" onClick={() => load(true)} disabled={syncing} className="h-9 py-2">
```

---

## 2. Input

단일 행 텍스트 입력. `components/ui/input.tsx`

### 클래스 원문 (`input.tsx:11`)

```
h-8 w-full min-w-0 rounded-2xl border border-transparent bg-input/50 px-2.5 py-1 text-base transition-[color,box-shadow] duration-200 outline-none file:inline-flex file:h-6 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30 disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 md:text-sm dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40
```

### 기본 외형 값

| 항목 | 값 |
|---|---|
| 높이 | `h-8` (32px) |
| 패딩 | `px-2.5 py-1` |
| radius | `rounded-2xl` |
| 글자 | `text-base` → `md:text-sm` (모바일 16px, 데스크톱 14px) |
| 보더 | `border border-transparent` |
| 배경 | `bg-input/50` |
| 전환 | `transition-[color,box-shadow] duration-200` |

variant/size 없음 — 단일 형태. 크기 변경은 `className` 오버라이드로.

### 상태 스타일

- **focus-visible**: `border-ring ring-3 ring-ring/30`
- **disabled**: `pointer-events-none cursor-not-allowed opacity-50`
- **aria-invalid**: `border-destructive ring-3 ring-destructive/20`(다크 `/40` + `border-destructive/50`)
- **placeholder**: `text-muted-foreground`
- **file 입력**: `file:inline-flex file:h-6 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`h-8`(32px)** — shadcn `h-9`.
> - **`rounded-2xl`** — shadcn `rounded-md`.
> - **`border-transparent` + `bg-input/50`** — shadcn은 `border-input bg-transparent`(윤곽선 필드). 여기는 **채워진 필드**.
> - `shadow-xs` 없음(그림자 제거).
> - `duration-200` 명시.
> - `disabled:pointer-events-none` 추가.

### 사용 예시 (`app/employees/page.tsx:109`)

```tsx
<Input value={name} onChange={(e) => setName(e.target.value)} placeholder={t("직원 이름")} />
```

---

## 3. Textarea

여러 줄 입력. `components/ui/textarea.tsx`

### 클래스 원문 (`textarea.tsx:10`)

```
flex field-sizing-content min-h-16 w-full resize-none rounded-2xl border border-transparent bg-input/50 px-2.5 py-2 text-base transition-[color,box-shadow] duration-200 outline-none placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30 disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 md:text-sm dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40
```

### 기본 외형 값

| 항목 | 값 |
|---|---|
| 최소 높이 | `min-h-16` (64px) |
| 패딩 | `px-2.5 py-2` (Input의 `py-1`보다 큼) |
| radius | `rounded-2xl` |
| 글자 | `text-base` → `md:text-sm` |
| 리사이즈 | `resize-none` + `field-sizing-content` (내용 길이에 따라 자동 증가) |

### 상태 스타일
Input과 동일 (`focus-visible:border-ring ring-3 ring-ring/30`, `disabled:cursor-not-allowed opacity-50`, `aria-invalid:*`).

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`resize-none` 강제** — 사용자가 드래그로 크기 조절 불가. 대신 **`field-sizing-content`**로 자동 성장.
> - `rounded-2xl`, `border-transparent bg-input/50` (Input과 동일 철학).
> - `min-h-16` (shadcn `min-h-16`과 동일하나 `shadow-xs` 제거).

### 사용 예시 (`app/quote-contract/page.tsx:116`)

```tsx
<Textarea rows={3} value={terms} onChange={(e) => setTerms(e.target.value)} placeholder={t("계약 체결 후 착수\n현장 방문 교육은 이틀 기준")} />
```

---

## 4. Label

폼 라벨. `components/ui/label.tsx`

### 클래스 원문 (`label.tsx:16`)

```
flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50
```

### 기본 외형 값
글자 `text-sm font-medium leading-none` / 레이아웃 `flex items-center gap-2` / `select-none`. 높이·패딩·radius 없음.

### 상태 스타일
- 부모 `group[data-disabled=true]` → `pointer-events-none opacity-50`
- 형제 `peer:disabled` → `cursor-not-allowed opacity-50`

### shadcn 기본과 다른 커스터마이즈 포인트
> shadcn 기본과 실질적으로 동일. `gap-2`(shadcn과 같음), 별도 커스터마이즈 없음.

### 사용 예시 (`app/company/page.tsx:417`)

```tsx
<Label htmlFor="item">{t("항목명 *")}</Label>
```

---

## 5. Badge

상태·태그 칩. `components/ui/badge.tsx`

### 베이스 클래스 (`badge.tsx:8`)

```
group/badge inline-flex h-5 w-fit shrink-0 items-center justify-center gap-1 overflow-hidden rounded-2xl border border-transparent px-2 py-0.5 text-xs font-medium whitespace-nowrap transition-all focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 aria-invalid:border-destructive aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 [&>svg]:pointer-events-none [&>svg]:size-3!
```

### variant (`badge.tsx:11-22`)

| variant | 클래스 원문 |
|---|---|
| `default` | `bg-primary text-primary-foreground [a]:hover:bg-primary/80` |
| `secondary` | `bg-secondary text-secondary-foreground [a]:hover:bg-secondary/80` |
| `destructive` | `bg-destructive/10 text-destructive focus-visible:ring-destructive/20 dark:bg-destructive/20 dark:focus-visible:ring-destructive/40 [a]:hover:bg-destructive/20` |
| `outline` | `border-border text-foreground [a]:hover:bg-muted [a]:hover:text-muted-foreground` |
| `ghost` | `hover:bg-muted hover:text-muted-foreground dark:hover:bg-muted/50` |
| `link` | `text-primary underline-offset-4 hover:underline` |

기본값: `variant: "default"` (`badge.tsx:24-26`). size 축 없음.

### 기본 외형 값
높이 `h-5`(20px) / 패딩 `px-2 py-0.5` / radius `rounded-2xl` / 글자 `text-xs font-medium` / 아이콘 `size-3!`(강제 12px)

### 상태 스타일
- **hover는 `<a>`일 때만** — `[a]:hover:*` 선택자. 링크가 아닌 배지는 hover 반응 없음(`ghost`/`link` 제외)
- **focus-visible**: `border-ring ring-[3px] ring-ring/50`
- **aria-invalid**: `border-destructive ring-destructive/20`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **variant 6종** (shadcn 4종). `ghost`, `link` 추가.
> - **높이 고정 `h-5`(20px)** — shadcn은 높이 미지정.
> - **`rounded-2xl`** — shadcn은 `rounded-md`.
> - **`[a]:hover:` 게이팅** — 앵커일 때만 hover. shadcn은 `[a&]:hover:`.
> - `destructive`가 톤다운 채움(`bg-destructive/10`).
> - **focus 링이 `ring-[3px] ring-ring/50`** — Button(`ring-3 ring-ring/30`)과 값이 다르다. 라이브러리 내부 비일관 지점.

### 사용 예시 (`app/employees/page.tsx:176`)

```tsx
<Badge variant="outline" className="font-normal">
  {e.role}
</Badge>
```

---

## 6. Card

카드 표면 + 7개 하위 슬롯. `components/ui/card.tsx`

### Card 루트 (`card.tsx:15`)

```
group/card flex flex-col gap-(--card-spacing) overflow-hidden rounded-[min(var(--radius-4xl),24px)] bg-card py-(--card-spacing) text-sm text-card-foreground shadow-sm ring-1 ring-foreground/5 [--card-spacing:--spacing(5)] has-[>img:first-child]:pt-0 data-[size=sm]:[--card-spacing:--spacing(4)] dark:ring-foreground/10 *:[img:first-child]:rounded-t-[min(var(--radius-4xl),24px)] *:[img:last-child]:rounded-b-[min(var(--radius-4xl),24px)]
```

### size (props 기반, cva 아님 — `card.tsx:5-9`)

| size | 효과 |
|---|---|
| `default` | `[--card-spacing:--spacing(5)]` → 20px |
| `sm` | `data-[size=sm]:[--card-spacing:--spacing(4)]` → 16px |

### 하위 슬롯 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `CardHeader` | `group/card-header @container/card-header grid auto-rows-min items-start gap-1.5 rounded-t-[min(var(--radius-4xl),24px)] px-(--card-spacing) has-data-[slot=card-action]:grid-cols-[1fr_auto] has-data-[slot=card-description]:grid-rows-[auto_auto] [.border-b]:pb-(--card-spacing)` | `card.tsx:28` |
| `CardTitle` | `font-heading text-base font-medium` | `card.tsx:40` |
| `CardDescription` | `text-sm text-muted-foreground` | `card.tsx:50` |
| `CardAction` | `col-start-2 row-span-2 row-start-1 self-start justify-self-end` | `card.tsx:61` |
| `CardContent` | `px-(--card-spacing)` | `card.tsx:73` |
| `CardFooter` | `flex items-center rounded-b-[min(var(--radius-4xl),24px)] px-(--card-spacing) [.border-t]:pt-(--card-spacing)` | `card.tsx:84` |

### 기본 외형 값
radius 24px 캡(`min(var(--radius-4xl),24px)`) / 배경 `bg-card` / 그림자 `shadow-sm` / 테두리 = `ring-1 ring-foreground/5`(다크 `/10`) / 글자 `text-sm` / 내부 여백 = CSS 변수 `--card-spacing` 단일 소스

### 상태 스타일
상태 없음(정적 표면). 조건부 스타일만:
- 첫 자식이 `<img>`면 상단 패딩 제거(`has-[>img:first-child]:pt-0`)하고 이미지 모서리를 카드 radius에 맞춤
- `CardHeader`에 `CardAction`이 있으면 자동 2열 그리드
- `CardHeader`/`CardFooter`에 `.border-b`/`.border-t` 클래스를 붙이면 해당 방향 패딩이 자동 추가

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`--card-spacing` CSS 변수로 패딩 단일화** — shadcn은 `px-6`/`py-6` 하드코딩. 여기는 `size="sm"` 하나로 전체 여백이 20px→16px로 바뀐다.
> - **`size` prop 존재** (shadcn Card에는 없음).
> - **테두리가 `border`가 아니라 `ring-1 ring-foreground/5`**.
> - **radius `min(var(--radius-4xl),24px)`** — shadcn `rounded-xl`.
> - **`overflow-hidden` + 이미지 모서리 자동 처리** (`*:[img:first-child]:rounded-t-*`).
> - `CardTitle`이 `font-heading text-base font-medium` (shadcn은 `leading-none font-semibold`).
> - 루트에 `text-sm` 기본 지정.

### 사용 예시 (`app/employees/page.tsx:105-106`)

```tsx
<Card className="shadow-xs">
  <CardContent className="flex flex-wrap items-end gap-2 py-4">
```

---

## 7. Dialog

모달 다이얼로그. `components/ui/dialog.tsx`

### DialogContent 클래스 원문 (`dialog.tsx:65`)

```
fixed top-1/2 left-1/2 z-50 grid [&>*]:min-w-0 w-full max-w-[calc(100%-2rem)] -translate-x-1/2 -translate-y-1/2 gap-6 rounded-[min(var(--radius-4xl),24px)] bg-popover p-6 text-sm text-popover-foreground shadow-xl ring-1 ring-foreground/5 duration-100 outline-none sm:max-w-md dark:ring-foreground/10 data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95
```

### DialogOverlay (`dialog.tsx:42`)

```
fixed inset-0 isolate z-50 bg-black/30 duration-100 supports-backdrop-filter:backdrop-blur-sm data-open:animate-in data-open:fade-in-0 data-closed:animate-out data-closed:fade-out-0
```

### 하위 슬롯

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `DialogHeader` | `flex flex-col gap-1.5` | `dialog.tsx:93` |
| `DialogFooter` | `flex flex-col-reverse gap-2 sm:flex-row sm:justify-end` | `dialog.tsx:111` |
| `DialogTitle` | `font-heading text-base leading-none font-medium` | `dialog.tsx:134` |
| `DialogDescription` | `text-sm text-muted-foreground *:[a]:underline *:[a]:underline-offset-3 *:[a]:hover:text-foreground` | `dialog.tsx:150` |

### 기본 외형 값
패딩 `p-6` / 자식 간격 `gap-6` / radius 24px 캡 / 배경 `bg-popover` / 그림자 `shadow-xl` / 테두리 `ring-1 ring-foreground/5` / 최대폭 `max-w-[calc(100%-2rem)]` → `sm:max-w-md` / 애니메이션 `duration-100`

### 상태 스타일
- **열림**: `data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95`
- **닫힘**: `data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95`
- 오버레이: `bg-black/30` + `supports-backdrop-filter:backdrop-blur-sm`(지원 브라우저만 블러)

### 닫기 버튼 (`dialog.tsx:71-83`)
`showCloseButton` 기본 `true`. 실제 `Button` 컴포넌트를 `asChild`로 사용:

```tsx
<Button variant="ghost" className="absolute top-4 right-4 bg-secondary" size="icon-sm">
```

`DialogFooter`도 `showCloseButton` prop(기본 `false`)을 받아 `<Button variant="outline">Close</Button>`를 렌더한다 (`dialog.tsx:117-121`).

### shadcn 기본과 다른 커스터마이즈 포인트 ⚠️ 핵심

> - **`grid` 레이아웃** — shadcn은 `flex flex-col`. 이 프로젝트는 `grid`.
> - **`[&>*]:min-w-0` 전역 안전망** (최근 추가, `dialog.tsx:64-65`). 소스 주석 원문:
>   > `[&>*]:min-w-0 — grid 자식이 축소 가능해야 긴 URL·와이드 콘텐츠가 다이얼로그를 넘치지 않음(전역 안전망)`
>   grid 아이템의 기본 `min-width:auto` 때문에 긴 URL이 다이얼로그를 밀어내는 오버플로 버그의 근본 수정.
> - **radius `min(var(--radius-4xl),24px)`** — shadcn `rounded-lg`.
> - **`ring-1 ring-foreground/5`** (border 아님) + **`shadow-xl`**.
> - **`gap-6`** (shadcn `gap-4`), 루트에 `text-sm`.
> - **닫기 버튼이 `Button variant="ghost" size="icon-sm" bg-secondary`** — shadcn은 raw `<button>` + `rounded-xs opacity-70`.
> - **`DialogFooter`에 `showCloseButton` prop 존재** (shadcn에 없음).
> - 오버레이에 `isolate`, `duration-100`, `supports-backdrop-filter:backdrop-blur-sm` 추가.
> - `DialogDescription` 안의 `<a>` 자동 밑줄 스타일.

### 사용 예시 (`app/company/page.tsx:411-413`)

```tsx
<DialogContent className="sm:max-w-lg">
  <DialogHeader>
    <DialogTitle>{editTarget ? t("항목 수정") : t("항목 추가")}</DialogTitle>
```

---

## 8. AlertDialog

파괴적 행위 확인 모달. `components/ui/alert-dialog.tsx`

### AlertDialogContent 클래스 원문 (`alert-dialog.tsx:61`)

```
group/alert-dialog-content fixed top-1/2 left-1/2 z-50 grid [&>*]:min-w-0 w-full -translate-x-1/2 -translate-y-1/2 gap-6 rounded-[min(var(--radius-4xl),24px)] bg-popover p-6 text-popover-foreground shadow-xl ring-1 ring-foreground/5 duration-100 outline-none data-[size=default]:max-w-xs data-[size=sm]:max-w-xs data-[size=default]:sm:max-w-md dark:ring-foreground/10 data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95
```

### size (props — `alert-dialog.tsx:47-53`)

| size | 최대폭 |
|---|---|
| `default` | `max-w-xs` → `sm:max-w-md` (모바일 좁게, 데스크톱 448px) |
| `sm` | `max-w-xs` 고정 (반응형 확대 없음) |

### 하위 슬롯

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `AlertDialogOverlay` | `fixed inset-0 z-50 bg-black/30 duration-100 supports-backdrop-filter:backdrop-blur-sm data-open:animate-in data-open:fade-in-0 data-closed:animate-out data-closed:fade-out-0` | `alert-dialog.tsx:39` |
| `AlertDialogHeader` | `grid grid-rows-[auto_1fr] place-items-center gap-1.5 text-center has-data-[slot=alert-dialog-media]:grid-rows-[auto_auto_1fr] has-data-[slot=alert-dialog-media]:gap-x-6 sm:group-data-[size=default]/alert-dialog-content:place-items-start sm:group-data-[size=default]/alert-dialog-content:text-left sm:group-data-[size=default]/alert-dialog-content:has-data-[slot=alert-dialog-media]:grid-rows-[auto_1fr]` | `alert-dialog.tsx:78` |
| `AlertDialogFooter` | `flex flex-col-reverse gap-2 group-data-[size=sm]/alert-dialog-content:grid group-data-[size=sm]/alert-dialog-content:grid-cols-2 sm:flex-row sm:justify-end` | `alert-dialog.tsx:94` |
| `AlertDialogMedia` | `mb-2 inline-flex size-16 items-center justify-center rounded-full bg-muted sm:group-data-[size=default]/alert-dialog-content:row-span-2 *:[svg:not([class*='size-'])]:size-8` | `alert-dialog.tsx:110` |
| `AlertDialogTitle` | `font-heading text-lg font-medium sm:group-data-[size=default]/alert-dialog-content:group-has-data-[slot=alert-dialog-media]/alert-dialog-content:col-start-2` | `alert-dialog.tsx:126` |
| `AlertDialogDescription` | `text-sm text-balance text-muted-foreground md:text-pretty *:[a]:underline *:[a]:underline-offset-3 *:[a]:hover:text-foreground` | `alert-dialog.tsx:142` |

### Action / Cancel
둘 다 **`Button`을 `asChild`로 감싼다** — 자체 클래스 없음. 기본 variant:
- `AlertDialogAction`: `variant="default"`, `size="default"` (`alert-dialog.tsx:150-158`)
- `AlertDialogCancel`: `variant="outline"`, `size="default"` (`alert-dialog.tsx:168-176`)

### 기본 외형 값
Dialog와 동일(패딩 `p-6`, `gap-6`, radius 24px 캡, `shadow-xl`, `ring-1`). 다만 **루트에 `text-sm` 없음**(Dialog와 차이), **닫기(X) 버튼 없음**.

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`AlertDialogMedia` 슬롯 신설** (shadcn에 없음) — 64px 원형 아이콘 컨테이너, 내부 SVG는 `size-8`.
> - **모바일 중앙정렬 → 데스크톱 좌측정렬** (`place-items-center text-center` → `sm:…place-items-start sm:…text-left`, `default` 사이즈 한정).
> - **`size="sm"`이면 Footer가 2열 그리드** (버튼 반반).
> - **`[&>*]:min-w-0`** — Dialog와 같은 grid 오버플로 안전망.
> - **Action/Cancel이 `Button` 래핑 + variant/size prop 전달 가능** (shadcn은 `buttonVariants()` 클래스만 적용).
> - `AlertDialogTitle`이 `text-lg`(Dialog는 `text-base`).
> - Description에 `text-balance` + `md:text-pretty`.

### 사용 예시 (`app/tasks/page.tsx:1179-1187`)

```tsx
<AlertDialogContent>
  <AlertDialogHeader>
    <AlertDialogTitle>{t("업무를 삭제할까요?")}</AlertDialogTitle>
    <AlertDialogDescription>{t("되돌릴 수 없습니다.")}</AlertDialogDescription>
  </AlertDialogHeader>
  <AlertDialogFooter>
    <AlertDialogCancel>{t("취소")}</AlertDialogCancel>
    <AlertDialogAction onClick={doDelete}>{t("삭제")}</AlertDialogAction>
  </AlertDialogFooter>
</AlertDialogContent>
```

---

## 9. Sheet

측면 슬라이드 패널. `components/ui/sheet.tsx` (radix `Dialog` 기반)

### SheetContent 클래스 원문 (`sheet.tsx:65`)

```
fixed z-50 flex flex-col bg-popover bg-clip-padding text-sm text-popover-foreground shadow-xl transition duration-200 ease-in-out data-[side=bottom]:inset-x-0 data-[side=bottom]:bottom-0 data-[side=bottom]:h-auto data-[side=bottom]:border-t data-[side=left]:inset-y-0 data-[side=left]:left-0 data-[side=left]:h-full data-[side=left]:w-3/4 data-[side=left]:border-r data-[side=right]:inset-y-0 data-[side=right]:right-0 data-[side=right]:h-full data-[side=right]:w-3/4 data-[side=right]:border-l data-[side=top]:inset-x-0 data-[side=top]:top-0 data-[side=top]:h-auto data-[side=top]:border-b data-[side=left]:sm:max-w-sm data-[side=right]:sm:max-w-sm data-open:animate-in data-open:fade-in-0 data-[side=bottom]:data-open:slide-in-from-bottom-10 data-[side=left]:data-open:slide-in-from-left-10 data-[side=right]:data-open:slide-in-from-right-10 data-[side=top]:data-open:slide-in-from-top-10 data-closed:animate-out data-closed:fade-out-0 data-[side=bottom]:data-closed:slide-out-to-bottom-10 data-[side=left]:data-closed:slide-out-to-left-10 data-[side=right]:data-closed:slide-out-to-right-10 data-[side=top]:data-closed:slide-out-to-top-10
```

### side (props — `sheet.tsx:51,55`)

| side | 위치/크기 |
|---|---|
| `right` (기본) | `inset-y-0 right-0 h-full w-3/4` + `sm:max-w-sm` + `border-l` |
| `left` | `inset-y-0 left-0 h-full w-3/4` + `sm:max-w-sm` + `border-r` |
| `top` | `inset-x-0 top-0 h-auto` + `border-b` |
| `bottom` | `inset-x-0 bottom-0 h-auto` + `border-t` |

### 하위 슬롯

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `SheetOverlay` | `fixed inset-0 z-50 bg-black/30 duration-100 supports-backdrop-filter:backdrop-blur-sm data-open:animate-in data-open:fade-in-0 data-closed:animate-out data-closed:fade-out-0` | `sheet.tsx:40` |
| `SheetHeader` | `flex flex-col gap-1.5 p-6` | `sheet.tsx:93` |
| `SheetFooter` | `mt-auto flex flex-col gap-2 p-6` | `sheet.tsx:103` |
| `SheetTitle` | `font-heading text-base font-medium text-foreground` | `sheet.tsx:117` |
| `SheetDescription` | `text-sm text-muted-foreground` | `sheet.tsx:132` |

### 상태 스타일
- 방향별 슬라이드: `slide-in-from-{side}-10` / `slide-out-to-{side}-10` (10 = 2.5rem)
- 전환: `transition duration-200 ease-in-out`
- 닫기 버튼: Dialog와 동일한 `Button variant="ghost" size="icon-sm" className="absolute top-4 right-4 bg-secondary"` (`sheet.tsx:72-82`), `showCloseButton` 기본 `true`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **radius 없음** — 모서리 직각(화면 가장자리에 붙음).
> - **슬라이드 거리 `-10`** — shadcn은 `slide-in-from-right`(전체 폭). 여기는 40px만 이동 + 페이드.
> - **`bg-popover` + `shadow-xl` + `bg-clip-padding`** (shadcn은 `bg-background`).
> - 닫기 버튼이 `Button` 컴포넌트.
> - 루트에 `text-sm`.

### 사용 예시 (`components/ui/sidebar.tsx:184-196`) — 모바일 사이드바 컨테이너

```tsx
<SheetContent
  dir={dir}
  data-sidebar="sidebar"
  data-slot="sidebar"
  data-mobile="true"
  className="w-(--sidebar-width) bg-sidebar p-0 text-sidebar-foreground [&>button]:hidden"
  style={{ "--sidebar-width": SIDEBAR_WIDTH_MOBILE } as React.CSSProperties}
  side={side}
>
```

> 앱 페이지 코드에서의 직접 사용처는 없음 — 현재 Sidebar 모바일 모드에서만 소비된다.

---

## 10. Drawer

바닥/측면 드래그 시트 (vaul 기반). `components/ui/drawer.tsx`

### DrawerContent 클래스 원문 (`drawer.tsx:59`)

```
group/drawer-content fixed z-50 flex h-auto flex-col bg-transparent p-4 text-sm before:absolute before:inset-2 before:-z-10 before:rounded-[min(var(--radius-4xl),24px)] before:border before:border-border before:bg-popover before:shadow-xl data-[vaul-drawer-direction=bottom]:inset-x-0 data-[vaul-drawer-direction=bottom]:bottom-0 data-[vaul-drawer-direction=bottom]:mt-24 data-[vaul-drawer-direction=bottom]:max-h-[80vh] data-[vaul-drawer-direction=left]:inset-y-0 data-[vaul-drawer-direction=left]:left-0 data-[vaul-drawer-direction=left]:w-3/4 data-[vaul-drawer-direction=right]:inset-y-0 data-[vaul-drawer-direction=right]:right-0 data-[vaul-drawer-direction=right]:w-3/4 data-[vaul-drawer-direction=top]:inset-x-0 data-[vaul-drawer-direction=top]:top-0 data-[vaul-drawer-direction=top]:mb-24 data-[vaul-drawer-direction=top]:max-h-[80vh] data-[vaul-drawer-direction=left]:sm:max-w-sm data-[vaul-drawer-direction=right]:sm:max-w-sm
```

### 방향별 값 (`data-[vaul-drawer-direction=*]`)

| 방향 | 값 |
|---|---|
| `bottom` | `inset-x-0 bottom-0 mt-24 max-h-[80vh]` |
| `top` | `inset-x-0 top-0 mb-24 max-h-[80vh]` |
| `left` | `inset-y-0 left-0 w-3/4` + `sm:max-w-sm` |
| `right` | `inset-y-0 right-0 w-3/4` + `sm:max-w-sm` |

### 하위 슬롯

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `DrawerOverlay` | `fixed inset-0 z-50 bg-black/30 supports-backdrop-filter:backdrop-blur-sm data-open:animate-in data-open:fade-in-0 data-closed:animate-out data-closed:fade-out-0` | `drawer.tsx:40` |
| 드래그 핸들 | `mx-auto mt-4 hidden h-1.5 w-[100px] shrink-0 rounded-full bg-muted group-data-[vaul-drawer-direction=bottom]/drawer-content:block` | `drawer.tsx:64` |
| `DrawerHeader` | `flex flex-col gap-0.5 p-4 group-data-[vaul-drawer-direction=bottom]/drawer-content:text-center group-data-[vaul-drawer-direction=top]/drawer-content:text-center md:gap-1.5 md:text-left` | `drawer.tsx:76` |
| `DrawerFooter` | `mt-auto flex flex-col gap-2 p-4` | `drawer.tsx:88` |
| `DrawerTitle` | `font-heading text-base font-medium text-foreground` | `drawer.tsx:102` |
| `DrawerDescription` | `text-sm text-muted-foreground` | `drawer.tsx:117` |

### shadcn 기본과 다른 커스터마이즈 포인트 ⚠️

> - **콘텐츠 자체가 `bg-transparent`이고, 실제 시트 표면은 `::before` 의사요소**로 그린다 —
>   `before:absolute before:inset-2 before:-z-10 before:rounded-[min(var(--radius-4xl),24px)] before:border before:border-border before:bg-popover before:shadow-xl`.
>   결과: 화면 가장자리에서 **8px 띄운 플로팅 시트**(iOS 스타일). shadcn은 `bg-background` + 방향별 `rounded-t-lg`.
> - **드래그 핸들이 `bottom` 방향에서만 표시** (`group-data-[vaul-drawer-direction=bottom]/…:block`). shadcn은 항상 표시.
> - 핸들 크기 `h-1.5 w-[100px]` (shadcn `h-2 w-[100px]`).
> - `DrawerHeader` 정렬이 방향별 자동(bottom/top은 가운데, md 이상 좌측).
> - 루트 패딩 `p-4`, 루트 `text-sm`.

### 사용 예시
> **미확인** — 앱 코드(`app/`, `components/` 중 `components/ui/` 제외)에 `Drawer` import·사용처가 없다. 라이브러리에만 존재.

---

## 11. Select

드롭다운 선택. `components/ui/select.tsx`

### SelectTrigger 클래스 원문 (`select.tsx:47`)

```
flex w-fit items-center justify-between gap-1.5 rounded-2xl border border-transparent bg-input/50 px-3 py-2 text-sm whitespace-nowrap transition-[color,box-shadow] duration-200 outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30 disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 data-placeholder:text-muted-foreground data-[size=default]:h-8 data-[size=sm]:h-7 *:data-[slot=select-value]:line-clamp-1 *:data-[slot=select-value]:flex *:data-[slot=select-value]:items-center *:data-[slot=select-value]:gap-1.5 dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4
```

### size (props — `select.tsx:36,40`)

| size | 높이 |
|---|---|
| `default` | `data-[size=default]:h-8` (32px) |
| `sm` | `data-[size=sm]:h-7` (28px) |

### 하위 슬롯

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `SelectContent` | `relative z-50 max-h-(--radix-select-content-available-height) min-w-36 origin-(--radix-select-content-transform-origin) overflow-x-hidden overflow-y-auto rounded-2xl bg-popover p-1.5 text-popover-foreground shadow-lg ring-1 ring-foreground/5 duration-100 data-[align-trigger=true]:animate-none data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 dark:ring-foreground/10 data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95` | `select.tsx:72` |
| `SelectContent` (popper일 때 추가) | `data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1` | `select.tsx:72` |
| `SelectViewport` | `space-y-0.5 data-[position=popper]:h-(--radix-select-trigger-height) data-[position=popper]:w-full data-[position=popper]:min-w-(--radix-select-trigger-width)` | `select.tsx:81` |
| `SelectGroup` | `scroll-my-1.5 p-1` | `select.tsx:22` |
| `SelectLabel` | `px-2 py-1 text-xs text-muted-foreground` | `select.tsx:100` |
| `SelectItem` | `relative flex min-h-7 w-full cursor-default items-center gap-2 rounded-xl py-1.5 pr-8 pl-2 text-sm outline-hidden select-none focus:bg-accent focus:text-accent-foreground not-data-[variant=destructive]:focus:**:text-accent-foreground data-disabled:pointer-events-none data-disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 *:[span]:last:flex *:[span]:last:items-center *:[span]:last:gap-2` | `select.tsx:115` |
| `SelectSeparator` | `pointer-events-none -mx-1 my-1 h-px bg-border` | `select.tsx:137` |
| `SelectScrollUpButton` / `SelectScrollDownButton` | `z-10 flex cursor-default items-center justify-center bg-popover py-1 [&_svg:not([class*='size-'])]:size-4` | `select.tsx:151`, `select.tsx:170` |

### 기본 외형 값
트리거: 높이 32px, 패딩 `px-3 py-2`, radius `rounded-2xl`, 배경 `bg-input/50`, 글자 `text-sm`, 너비 `w-fit`(내용 맞춤)
콘텐츠: radius `rounded-2xl`, 패딩 `p-1.5`, 최소 너비 `min-w-36`(144px), `shadow-lg` + `ring-1 ring-foreground/5`
아이템: 최소 높이 `min-h-7`(28px), radius `rounded-xl`, 패딩 `py-1.5 pr-8 pl-2`

### 상태 스타일
- **placeholder**: `data-placeholder:text-muted-foreground`
- **focus-visible(트리거)**: `border-ring ring-3 ring-ring/30`
- **disabled(트리거)**: `cursor-not-allowed opacity-50`
- **아이템 focus**: `bg-accent text-accent-foreground` + 자식 텍스트도 `**:text-accent-foreground`
- **아이템 disabled**: `data-disabled:pointer-events-none data-disabled:opacity-50`
- **열림/닫힘**: `data-open:animate-in fade-in-0 zoom-in-95` / `data-closed:animate-out fade-out-0 zoom-out-95`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`position` 기본값이 `"item-aligned"`** (shadcn은 `"popper"`) — 선택된 항목이 트리거 위에 정렬되는 네이티브 셀렉트 동작. 이때 `data-[align-trigger=true]:animate-none`으로 **애니메이션을 끈다**.
> - **`align` 기본값 `"center"`** (`select.tsx:64`).
> - **체크 표시가 오른쪽** — `pr-8` + `absolute right-2` 인디케이터 (shadcn은 왼쪽 `pl-8`/`right-2`… 위치가 프로젝트마다 다름; 여기는 오른쪽 고정).
> - `w-fit` 기본 (shadcn과 동일하나 앱에서는 `<SelectTrigger>`를 폭 지정 없이 써서 내용 폭으로 렌더).
> - `rounded-2xl` 트리거 / `rounded-xl` 아이템.
> - `bg-input/50` + `border-transparent`.
> - `shadow-lg ring-1 ring-foreground/5`(border 아님).

### 사용 예시 (`app/employees/page.tsx:117-124`)

```tsx
<Select value={agent} onValueChange={setAgent}>
  <SelectTrigger>
    <SelectValue />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="claude">Claude Code</SelectItem>
```

---

## 12. DropdownMenu

컨텍스트/액션 메뉴. `components/ui/dropdown-menu.tsx`

### DropdownMenuContent 클래스 원문 (`dropdown-menu.tsx:46`)

```
z-50 max-h-(--radix-dropdown-menu-content-available-height) w-(--radix-dropdown-menu-trigger-width) min-w-32 origin-(--radix-dropdown-menu-content-transform-origin) overflow-x-hidden overflow-y-auto rounded-2xl bg-popover p-1.5 space-y-0.5 text-popover-foreground shadow-lg ring-1 ring-foreground/5 duration-100 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 data-[state=closed]:overflow-hidden dark:ring-foreground/10 data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95
```

기본 props: `align = "start"`, `sideOffset = 4` (`dropdown-menu.tsx:36-37`)

### DropdownMenuItem variant (props — `dropdown-menu.tsx:64,68`)

| variant | 효과 (`dropdown-menu.tsx:76`) |
|---|---|
| `default` | `not-data-[variant=destructive]:focus:**:text-accent-foreground` |
| `destructive` | `data-[variant=destructive]:text-destructive data-[variant=destructive]:focus:bg-destructive/10 data-[variant=destructive]:focus:text-destructive dark:data-[variant=destructive]:focus:bg-destructive/20 data-[variant=destructive]:*:[svg]:text-destructive` |

`inset` prop → `data-inset:pl-7`

### 하위 슬롯 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `DropdownMenuItem` | `group/dropdown-menu-item relative flex min-h-7 cursor-default items-center gap-2 rounded-xl px-2 py-1.5 text-sm outline-hidden select-none focus:bg-accent focus:text-accent-foreground not-data-[variant=destructive]:focus:**:text-accent-foreground data-inset:pl-7 data-[variant=destructive]:text-destructive data-[variant=destructive]:focus:bg-destructive/10 data-[variant=destructive]:focus:text-destructive dark:data-[variant=destructive]:focus:bg-destructive/20 data-disabled:pointer-events-none data-disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 data-[variant=destructive]:*:[svg]:text-destructive` | `dropdown-menu.tsx:76` |
| `DropdownMenuCheckboxItem` | `relative flex min-h-7 cursor-default items-center gap-2 rounded-xl py-1.5 pr-8 pl-2 text-sm outline-hidden select-none focus:bg-accent focus:text-accent-foreground focus:**:text-accent-foreground data-inset:pl-7 data-disabled:pointer-events-none data-disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4` | `dropdown-menu.tsx:98` |
| `DropdownMenuRadioItem` | (CheckboxItem과 동일 문자열) | `dropdown-menu.tsx:142` |
| `DropdownMenuLabel` | `px-2 py-1 text-xs text-muted-foreground data-inset:pl-7` | `dropdown-menu.tsx:173` |
| `DropdownMenuSeparator` | `-mx-1 my-1 h-px bg-border/50` | `dropdown-menu.tsx:188` |
| `DropdownMenuShortcut` | `ml-auto text-xs tracking-widest text-muted-foreground group-focus/dropdown-menu-item:text-accent-foreground` | `dropdown-menu.tsx:202` |
| `DropdownMenuSubTrigger` | `flex min-h-7 cursor-default items-center gap-2 rounded-xl px-2 py-1.5 text-sm outline-hidden select-none focus:bg-accent focus:text-accent-foreground not-data-[variant=destructive]:focus:**:text-accent-foreground data-inset:pl-7 data-open:bg-accent data-open:text-accent-foreground [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4` | `dropdown-menu.tsx:229` |
| `DropdownMenuSubContent` | `z-50 min-w-[96px] origin-(--radix-dropdown-menu-content-transform-origin) overflow-hidden rounded-2xl bg-popover p-1.5 space-y-0.5 text-popover-foreground shadow-lg ring-1 ring-foreground/5 duration-100 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 dark:ring-foreground/10 data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95` | `dropdown-menu.tsx:247` |

### 기본 외형 값
콘텐츠: radius `rounded-2xl`, 패딩 `p-1.5`, 아이템 간격 `space-y-0.5`, 최소 너비 `min-w-32`(128px), **너비 = 트리거 너비**(`w-(--radix-dropdown-menu-trigger-width)`)
아이템: 최소 높이 `min-h-7`(28px), radius `rounded-xl`, 패딩 `px-2 py-1.5`, 글자 `text-sm`

### 상태 스타일
- **focus**: `bg-accent text-accent-foreground` (+ 자식 텍스트 `**:text-accent-foreground`)
- **disabled**: `data-disabled:pointer-events-none data-disabled:opacity-50`
- **SubTrigger 열림**: `data-open:bg-accent data-open:text-accent-foreground`
- **닫히는 중**: `data-[state=closed]:overflow-hidden` (스크롤바 깜빡임 방지)

### shadcn 기본과 다른 커스터마이즈 포인트

> - **콘텐츠 너비가 트리거 폭을 따라간다** (`w-(--radix-dropdown-menu-trigger-width)`) — shadcn은 `min-w-[8rem]`만. 앱에서 `className="w-72"` 등으로 오버라이드하는 패턴이 흔하다.
> - **`space-y-0.5` 아이템 간격** (shadcn은 간격 없음).
> - **패딩 `p-1.5`** (shadcn `p-1`), **아이템 `rounded-xl`** (shadcn `rounded-sm`).
> - **`min-h-7`** 명시(아이콘 유무에 관계없이 높이 일정).
> - **Separator가 `bg-border/50`** (반투명).
> - **Label이 `text-xs text-muted-foreground`** (shadcn `text-sm font-medium`).
> - `data-[state=closed]:overflow-hidden` 추가.
> - `destructive`가 `bg-destructive/10` 톤다운.

### 사용 예시 (`components/nav-user.tsx:58-60`)

```tsx
<DropdownMenuContent
  className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
  side={isMobile ? "bottom" : "right"}
```

---

## 13. Tabs

탭 네비게이션. `components/ui/tabs.tsx`

### Tabs 루트 (`tabs.tsx:19`)

```
group/tabs flex gap-2 data-horizontal:flex-col
```

`orientation` 기본 `"horizontal"` (`tabs.tsx:11`)

### TabsList variant (cva — `tabs.tsx:27-40`)

베이스:
```
group/tabs-list inline-flex w-fit items-center justify-center gap-1 rounded-2xl p-1 text-muted-foreground group-data-horizontal/tabs:h-9 group-data-vertical/tabs:h-fit group-data-vertical/tabs:flex-col group-data-vertical/tabs:p-1 data-[variant=line]:rounded-none
```

| variant | 클래스 원문 |
|---|---|
| `default` | `bg-foreground/[0.06] dark:bg-foreground/10` |
| `line` | `gap-1 bg-transparent` |

기본값: `variant: "default"`

### TabsTrigger (4개 문자열 결합 — `tabs.tsx:66-69`)

```
relative inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-2xl border border-transparent! px-4 py-1 text-sm font-medium whitespace-nowrap text-foreground/60 transition-all group-data-vertical/tabs:w-full group-data-vertical/tabs:justify-start group-data-vertical/tabs:px-3 group-data-vertical/tabs:py-0.5 hover:text-foreground focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-1 focus-visible:outline-ring disabled:pointer-events-none disabled:opacity-50 dark:text-muted-foreground dark:hover:text-foreground [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4
```
```
group-data-[variant=line]/tabs-list:bg-transparent group-data-[variant=line]/tabs-list:data-active:bg-transparent dark:group-data-[variant=line]/tabs-list:data-active:border-transparent dark:group-data-[variant=line]/tabs-list:data-active:bg-transparent
```
```
data-active:bg-background data-active:text-foreground data-active:shadow-sm data-active:ring-1 data-active:ring-black/5 dark:data-active:border-input dark:data-active:bg-input/40 dark:data-active:text-foreground dark:data-active:ring-0
```
```
after:absolute after:bg-foreground after:opacity-0 after:transition-opacity group-data-horizontal/tabs:after:inset-x-0 group-data-horizontal/tabs:after:bottom-[-5px] group-data-horizontal/tabs:after:h-0.5 group-data-vertical/tabs:after:inset-y-0 group-data-vertical/tabs:after:-right-1 group-data-vertical/tabs:after:w-0.5 group-data-[variant=line]/tabs-list:data-active:after:opacity-100
```

### TabsContent (`tabs.tsx:84`)

```
flex-1 text-sm outline-none
```

### 기본 외형 값
List: 높이 `h-9`(36px, 가로 방향), radius `rounded-2xl`, 패딩 `p-1`, 배경 `bg-foreground/[0.06]`(다크 `/10`)
Trigger: 높이 `h-[calc(100%-1px)]`, 패딩 `px-4 py-1`, radius `rounded-2xl`, 글자 `text-sm font-medium`, 비활성 색 `text-foreground/60`

### 상태 스타일
- **hover**: `text-foreground`
- **active(default variant)**: `bg-background text-foreground shadow-sm ring-1 ring-black/5` / 다크는 `bg-input/40 border-input ring-0`
- **active(line variant)**: 배경 없이 **`::after` 밑줄**(`h-0.5`, 가로면 `bottom-[-5px]`; 세로면 `-right-1` 세로선) 이 `opacity-100`
- **focus-visible**: `border-ring ring-[3px] ring-ring/50 outline-1 outline-ring`
- **disabled**: `pointer-events-none opacity-50`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`line` variant 신설** — 밑줄형 탭. shadcn 기본에는 pill 하나뿐.
> - **`orientation="vertical"` 완전 지원** — List가 세로 스택, Trigger는 좌측 정렬(`justify-start px-3 py-0.5`), 인디케이터는 오른쪽 세로선.
> - **`border-transparent!`** — `!` 강제로 다른 보더가 새어 들어오는 것 차단.
> - **비활성 글자색이 `text-foreground/60`** (다크는 `text-muted-foreground`) — shadcn은 `text-foreground`.
> - `rounded-2xl`(List·Trigger 둘 다), List 배경이 `bg-foreground/[0.06]`(shadcn `bg-muted`).
> - active 그림자가 `shadow-sm + ring-1 ring-black/5`.

### 사용 예시 (`app/reports/page.tsx:213-215`)

```tsx
<TabsList>
  <TabsTrigger value="all">{t("전체")}</TabsTrigger>
```

---

## 14. Table

데이터 테이블. `components/ui/table.tsx`

### 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| 컨테이너(`table-container`) | `relative w-full overflow-x-auto` | `table.tsx:11` |
| `Table` (`<table>`) | `w-full caption-bottom text-sm` | `table.tsx:15` |
| `TableHeader` | `[&_tr]:border-b` | `table.tsx:26` |
| `TableBody` | `[&_tr:last-child]:border-0` | `table.tsx:36` |
| `TableFooter` | `border-t bg-muted/50 font-medium [&>tr]:last:border-b-0` | `table.tsx:47` |
| `TableRow` | `border-b transition-colors hover:bg-muted/50 has-aria-expanded:bg-muted/50 data-[state=selected]:bg-muted` | `table.tsx:60` |
| `TableHead` | `h-10 px-2 text-left align-middle font-medium whitespace-nowrap text-foreground [&:has([role=checkbox])]:pr-0` | `table.tsx:73` |
| `TableCell` | `p-2 align-middle whitespace-nowrap [&:has([role=checkbox])]:pr-0` | `table.tsx:86` |
| `TableCaption` | `mt-4 text-sm text-muted-foreground` | `table.tsx:101` |

### 기본 외형 값
헤더 셀 높이 `h-10`(40px), 패딩 `px-2` / 데이터 셀 패딩 `p-2` / 전체 글자 `text-sm` / 줄바꿈 없음(`whitespace-nowrap`)

### 상태 스타일
- **행 hover**: `bg-muted/50`
- **행 선택**: `data-[state=selected]:bg-muted`
- **행에 펼침 상태 자식이 있으면**: `has-aria-expanded:bg-muted/50`
- 컨테이너에 `overflow-x-auto` — 가로 스크롤 자체 처리

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`has-aria-expanded:bg-muted/50`** 추가 — 행 안의 트리거가 열려 있으면 행이 강조 유지.
> - **`TableHead`가 `text-foreground`** (shadcn은 `text-muted-foreground`) — 헤더가 본문과 같은 진한 색.
> - **셀 패딩 `p-2`** (shadcn `p-2`와 동일), 헤더 `h-10`(shadcn `h-10`) — 여기는 일치.
> - `TableFooter`에 `border-t bg-muted/50` (shadcn과 유사).

### 사용 예시 (`app/page.tsx:299-306`)

```tsx
<TableHeader>
  <TableRow>
    <TableHead>{t("제목")}</TableHead>
    <TableHead className="w-36 text-center">{t("상태")}</TableHead>
    <TableHead className="w-28 text-center">{t("날짜")}</TableHead>
  </TableRow>
</TableHeader>
```

---

## 15. Checkbox

체크박스. `components/ui/checkbox.tsx`

### 클래스 원문 (`checkbox.tsx:17`)

```
peer relative flex size-4 shrink-0 items-center justify-center rounded-[5px] border border-transparent bg-input/90 transition-shadow outline-none group-has-disabled/field:opacity-50 after:absolute after:-inset-x-3 after:-inset-y-2 focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30 disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 aria-invalid:aria-checked:border-primary dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 data-checked:border-primary data-checked:bg-primary data-checked:text-primary-foreground dark:data-checked:bg-primary
```

### Indicator (`checkbox.tsx:24`)

```
grid place-content-center text-current transition-none [&>svg]:size-3.5
```

### 기본 외형 값
크기 `size-4`(16×16) / **radius `rounded-[5px]`**(임의값) / 배경 `bg-input/90` / 보더 `border-transparent` / 체크 아이콘 `size-3.5`(14px)

### 상태 스타일
- **checked**: `data-checked:border-primary data-checked:bg-primary data-checked:text-primary-foreground` (다크도 `bg-primary` 유지)
- **focus-visible**: `border-ring ring-3 ring-ring/30`
- **disabled**: `cursor-not-allowed opacity-50` / 필드 그룹 비활성 시 `group-has-disabled/field:opacity-50`
- **aria-invalid**: `border-destructive ring-3 ring-destructive/20`, 단 **체크되어 있으면 `aria-invalid:aria-checked:border-primary`로 primary 보더로 되돌림**

### shadcn 기본과 다른 커스터마이즈 포인트 ⚠️

> - **터치 히트 영역 확장** — `after:absolute after:-inset-x-3 after:-inset-y-2`. 시각적으로는 16px지만 실제 클릭 가능 영역은 좌우 +12px, 상하 +8px. shadcn에는 없음.
> - **`rounded-[5px]` 임의값** — 라이브러리 전역 `rounded-2xl` 규칙의 예외(16px 사각형에 2xl은 원이 되므로).
> - **`bg-input/90` + `border-transparent`** (shadcn `border-input bg-input/30` 계열과 다름).
> - **`aria-invalid:aria-checked:border-primary`** — 오류 상태여도 체크되면 정상 색으로 복귀하는 세밀 규칙.
> - `transition-shadow`만(색 전환 없음), Indicator는 `transition-none`(즉시).

### 사용 예시 (`app/employees/page.tsx:168-172`)

```tsx
<Checkbox
  checked={bulk.has(e.id)}
  onCheckedChange={() => bulk.toggle(e.id)}
  aria-label={`${e.name} ${t("선택")}`}
/>
```

---

## 16. Toggle

단일 토글 버튼. `components/ui/toggle.tsx`

### 베이스 클래스 (`toggle.tsx:10`)

```
group/toggle inline-flex items-center justify-center gap-1 rounded-2xl text-sm font-medium whitespace-nowrap transition-colors outline-none hover:bg-muted hover:text-foreground focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/30 disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-destructive/20 aria-pressed:bg-muted dark:aria-invalid:ring-destructive/40 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4
```

### variant (`toggle.tsx:13-16`)

| variant | 클래스 원문 |
|---|---|
| `default` | `bg-transparent` |
| `outline` | `border border-input bg-transparent hover:bg-muted` |

### size (`toggle.tsx:17-22`)

| size | 클래스 원문 | 높이 |
|---|---|---|
| `default` | `h-8 min-w-8 px-2.5 has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2` | 32px |
| `sm` | `h-7 min-w-7 px-2.5 has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5` | 28px |
| `lg` | `h-9 min-w-9 px-2.5 has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2` | 36px |

기본값: `variant: "default"`, `size: "default"`

### 기본 외형 값
높이 32px / 최소 너비 32px / 패딩 `px-2.5` / radius `rounded-2xl` / 글자 `text-sm font-medium` / 아이콘 `size-4`

### 상태 스타일
- **hover**: `bg-muted text-foreground`
- **pressed(on)**: `aria-pressed:bg-muted`
- **focus-visible**: `border-ring ring-[3px] ring-ring/30`
- **disabled**: `pointer-events-none opacity-50`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **on 상태를 `aria-pressed:`로 처리** (shadcn은 `data-[state=on]:`). ToggleGroupItem은 별도로 `data-[state=on]:bg-muted`도 붙인다.
> - **`min-w-*` 지정** — 아이콘만 있는 토글이 정사각형 유지.
> - `rounded-2xl`, `has-data-[icon=inline-*]` 광학 패딩.
> - 모든 size의 좌우 패딩이 `px-2.5`로 통일(shadcn은 size별로 다름).

### 사용 예시
> **미확인** — 앱 코드에 `<Toggle>` 직접 사용처 없음. `toggleVariants`가 `toggle-group.tsx:8`에서 소비될 뿐.

---

## 17. ToggleGroup

토글 그룹(세그먼티드 컨트롤). `components/ui/toggle-group.tsx`

### ToggleGroup 루트 (`toggle-group.tsx:44`)

```
group/toggle-group flex w-fit flex-row items-center gap-[--spacing(var(--gap))] data-[spacing=0]:data-[variant=outline]:rounded-2xl data-vertical:flex-col data-vertical:items-stretch
```

인라인 스타일: `style={{ "--gap": spacing }}` (`toggle-group.tsx:42`)

### props (`toggle-group.tsx:22-34`)

| prop | 기본값 | 효과 |
|---|---|---|
| `variant` | (컨텍스트 전파) | `toggleVariants`의 variant |
| `size` | (컨텍스트 전파) | `toggleVariants`의 size |
| `spacing` | `2` | 아이템 간격. **`0`이면 세그먼티드(붙은) 모드** |
| `orientation` | `"horizontal"` | `data-vertical:flex-col` |

### ToggleGroupItem (`toggle-group.tsx:75`)

```
shrink-0 group-data-[spacing=0]/toggle-group:rounded-none group-data-[spacing=0]/toggle-group:px-2 group-data-[spacing=0]/toggle-group:shadow-none focus:z-10 focus-visible:z-10 group-data-[spacing=0]/toggle-group:has-data-[icon=inline-end]:pr-1.5 group-data-[spacing=0]/toggle-group:has-data-[icon=inline-start]:pl-1.5 group-data-horizontal/toggle-group:data-[spacing=0]:first:rounded-l-2xl group-data-vertical/toggle-group:data-[spacing=0]:first:rounded-t-2xl group-data-horizontal/toggle-group:data-[spacing=0]:last:rounded-r-2xl group-data-vertical/toggle-group:data-[spacing=0]:last:rounded-b-2xl data-[state=on]:bg-muted group-data-horizontal/toggle-group:data-[spacing=0]:data-[variant=outline]:border-l-0 group-data-vertical/toggle-group:data-[spacing=0]:data-[variant=outline]:border-t-0 group-data-horizontal/toggle-group:data-[spacing=0]:data-[variant=outline]:first:border-l group-data-vertical/toggle-group:data-[spacing=0]:data-[variant=outline]:first:border-t
```

(위 문자열 + `toggleVariants({ variant, size })` 결합 — `toggle-group.tsx:76-79`)

### 기본 외형 값
너비 `w-fit`, 간격 `gap-[--spacing(2)]`(8px), 아이템 외형은 Toggle과 동일. `spacing=0`이면 아이템 radius가 사라지고 **첫/마지막만 바깥쪽 모서리 `rounded-{l|r|t|b}-2xl`**, outline variant는 인접 보더가 겹치지 않게 `border-l-0`/`border-t-0`.

### 상태 스타일
- **on**: `data-[state=on]:bg-muted` (+ Toggle의 `aria-pressed:bg-muted`)
- **focus**: `focus:z-10 focus-visible:z-10` — 붙은 모드에서 포커스 링이 이웃에 가리지 않게

### shadcn 기본과 다른 커스터마이즈 포인트 ⚠️

> - **`spacing` prop 신설** — 숫자로 간격 제어. `spacing={0}`이면 세그먼티드 컨트롤, `>0`이면 떨어진 버튼들. shadcn은 항상 붙은 형태.
> - **`orientation` 세로 지원** — 세로일 때 모서리·보더 규칙이 상하로 전환.
> - **간격이 CSS 변수 경유** — `style={{ "--gap": spacing }}` + `gap-[--spacing(var(--gap))]`.
> - Context로 variant/size 전파(`toggle-group.tsx:10-20`), 기본 컨텍스트 값은 `{size:"default", variant:"default", spacing:2, orientation:"horizontal"}`.

### 사용 예시
> **미확인** — 앱 코드에 `<ToggleGroup>` 사용처 없음.

---

## 18. Avatar

아바타 + 그룹/배지. `components/ui/avatar.tsx`

### Avatar 루트 (`avatar.tsx:20`)

```
group/avatar relative flex size-8 shrink-0 rounded-full select-none after:absolute after:inset-0 after:rounded-full after:border after:border-border after:mix-blend-darken data-[size=lg]:size-10 data-[size=sm]:size-6 dark:after:mix-blend-lighten
```

### size (props — `avatar.tsx:10,13`)

| size | 크기 |
|---|---|
| `default` | `size-8` (32px) |
| `sm` | `data-[size=sm]:size-6` (24px) |
| `lg` | `data-[size=lg]:size-10` (40px) |

### 하위 슬롯

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `AvatarImage` | `aspect-square size-full rounded-full object-cover` | `avatar.tsx:36` |
| `AvatarFallback` | `flex size-full items-center justify-center rounded-full bg-muted text-sm text-muted-foreground group-data-[size=sm]/avatar:text-xs` | `avatar.tsx:52` |
| `AvatarBadge` | `absolute right-0 bottom-0 z-10 inline-flex items-center justify-center rounded-full bg-primary text-primary-foreground bg-blend-color ring-2 ring-background select-none` + `group-data-[size=sm]/avatar:size-2 group-data-[size=sm]/avatar:[&>svg]:hidden` + `group-data-[size=default]/avatar:size-2.5 group-data-[size=default]/avatar:[&>svg]:size-2` + `group-data-[size=lg]/avatar:size-3 group-data-[size=lg]/avatar:[&>svg]:size-2` | `avatar.tsx:65-68` |
| `AvatarGroup` | `group/avatar-group flex -space-x-2 *:data-[slot=avatar]:ring-2 *:data-[slot=avatar]:ring-background` | `avatar.tsx:81` |
| `AvatarGroupCount` | `relative flex size-8 shrink-0 items-center justify-center rounded-full bg-muted text-sm text-muted-foreground ring-2 ring-background group-has-data-[size=lg]/avatar-group:size-10 group-has-data-[size=sm]/avatar-group:size-6 [&>svg]:size-4 group-has-data-[size=lg]/avatar-group:[&>svg]:size-5 group-has-data-[size=sm]/avatar-group:[&>svg]:size-3` | `avatar.tsx:97` |

### 기본 외형 값
32px 원형 / 이미지 `object-cover` / fallback 배경 `bg-muted`, 글자 `text-sm`(sm이면 `text-xs`)

### 상태 스타일
상태 없음. 다만 **`::after` 오버레이 링**이 항상 존재:
`after:inset-0 after:rounded-full after:border after:border-border after:mix-blend-darken`(다크 `mix-blend-lighten`)

### shadcn 기본과 다른 커스터마이즈 포인트 ⚠️

> - **`::after` + `mix-blend-darken/lighten` 테두리** — 이미지 위에 블렌드 모드로 얇은 링을 얹어, 밝은 이미지에서도 경계가 보이게 한다. shadcn에는 없는 기법.
> - **`size` prop 3단계** (shadcn Avatar에는 size 축 없음, `size-8` 고정).
> - **`AvatarBadge` 신설** — 우하단 상태 점. 아바타 size에 따라 8/10/12px, `sm`일 땐 내부 아이콘 숨김.
> - **`AvatarGroup` / `AvatarGroupCount` 신설** — 겹침(`-space-x-2`) + `ring-2 ring-background`, 카운트 칩은 그룹의 size를 `group-has-data-[size=*]`로 상속.
> - `overflow-hidden` 대신 각 자식에 `rounded-full`을 개별 부여.

### 사용 예시 (`components/nav-user.tsx:45-48`)

```tsx
<Avatar className="h-8 w-8 rounded-lg grayscale">
  <AvatarImage src={user.avatar} alt={user.name} />
  <AvatarFallback className="rounded-lg">CN</AvatarFallback>
</Avatar>
```

> 주의: `app/mail/page.tsx:833`의 `<Avatar name= email= size={9} />`는 **이 컴포넌트가 아니다**(동명의 로컬 컴포넌트). `@/components/ui/avatar`를 import하는 파일은 `components/nav-user.tsx` 하나뿐.

---

## 19. Breadcrumb

경로 표시. `components/ui/breadcrumb.tsx`

### 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `Breadcrumb` (`<nav aria-label="breadcrumb">`) | `cn(className)` — 자체 클래스 없음 | `breadcrumb.tsx:12` |
| `BreadcrumbList` | `flex flex-wrap items-center gap-1.5 text-sm wrap-break-word text-muted-foreground sm:gap-2.5` | `breadcrumb.tsx:23` |
| `BreadcrumbItem` | `inline-flex items-center gap-1.5` | `breadcrumb.tsx:35` |
| `BreadcrumbLink` | `transition-colors hover:text-foreground` | `breadcrumb.tsx:53` |
| `BreadcrumbPage` | `font-normal text-foreground` | `breadcrumb.tsx:66` |
| `BreadcrumbSeparator` | `[&>svg]:size-3.5` (기본 children = `<ChevronRightIcon />`) | `breadcrumb.tsx:82,86` |
| `BreadcrumbEllipsis` | `flex size-5 items-center justify-center [&>svg]:size-4` | `breadcrumb.tsx:102` |

### 기본 외형 값
글자 `text-sm text-muted-foreground` / 항목 간격 `gap-1.5` → `sm:gap-2.5` / 구분자 아이콘 `size-3.5`(14px) / 생략 표시 `size-5` 박스에 `size-4` 아이콘

### 상태 스타일
- 링크 hover: `text-foreground`
- 현재 페이지(`BreadcrumbPage`): `role="link" aria-disabled="true" aria-current="page"` + `font-normal text-foreground`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`BreadcrumbPage`가 `font-normal`** (shadcn `font-normal`과 동일하나, 여기선 굵기 강조를 아예 쓰지 않음).
> - `wrap-break-word` 사용(Tailwind v4 표기).
> - `BreadcrumbEllipsis`가 `size-5`(shadcn `size-9`)로 훨씬 작다.
> - 그 외 shadcn 기본과 거의 동일.

### 사용 예시
> **미확인** — 앱 코드에 `Breadcrumb` import·사용처 없음.

---

## 20. ScrollArea

커스텀 스크롤 영역. `components/ui/scroll-area.tsx`

### 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `ScrollArea` 루트 | `relative` | `scroll-area.tsx:16` |
| Viewport | `size-full overscroll-contain rounded-[inherit] transition-[color,box-shadow] outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50 focus-visible:outline-1` | `scroll-area.tsx:21` |
| `ScrollBar` | `flex touch-none p-px transition-colors select-none data-horizontal:h-2.5 data-horizontal:flex-col data-horizontal:border-t data-horizontal:border-t-transparent data-vertical:h-full data-vertical:w-2.5 data-vertical:border-l data-vertical:border-l-transparent` | `scroll-area.tsx:42` |
| Thumb | `relative flex-1 rounded-full bg-border` | `scroll-area.tsx:49` |

`ScrollBar`의 `orientation` 기본값: `"vertical"` (`scroll-area.tsx:33`)

### 기본 외형 값
스크롤바 두께 10px(`w-2.5`/`h-2.5`), 내부 패딩 `p-px`, 썸 `rounded-full bg-border`. 루트는 `relative`만 — **높이는 소비자가 지정**.

### 상태 스타일
- Viewport focus-visible: `ring-[3px] ring-ring/50 outline-1`
- **`overscroll-contain`** — 끝까지 스크롤해도 부모/페이지로 전파되지 않음

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`overscroll-contain` 추가** (shadcn에 없음) — 채팅 패널 등 중첩 스크롤에서 페이지가 같이 밀리는 문제 방지.
> - `ScrollBar`에 `data-orientation` 속성을 직접 부착하고 `data-horizontal:`/`data-vertical:` 변형 사용(shadcn은 `data-[orientation=…]`).
> - 썸 색이 `bg-border` (shadcn `bg-border` 동일).

### 사용 예시 (`components/chat-panel.tsx:843`)

```tsx
<ScrollArea className="min-h-0 flex-1">
```

---

## 21. Separator

구분선. `components/ui/separator.tsx`

### 클래스 원문 (`separator.tsx:20`)

```
shrink-0 bg-border data-horizontal:h-px data-horizontal:w-full data-vertical:w-px data-vertical:self-stretch
```

기본 props: `orientation = "horizontal"`, `decorative = true` (`separator.tsx:10-11`)

### 기본 외형 값
두께 1px, 색 `bg-border`. 가로: `h-px w-full` / 세로: `w-px self-stretch`

### 상태 스타일
없음.

### shadcn 기본과 다른 커스터마이즈 포인트

> - **세로 방향이 `h-full`이 아니라 `self-stretch`** — flex 부모 안에서 형제 높이에 자동으로 맞춰진다(부모 높이를 몰라도 됨). shadcn은 `data-[orientation=vertical]:h-full`.
> - `data-horizontal:`/`data-vertical:` 축약 변형 사용.

### 사용 예시 (`app/tools/page.tsx:129`)

```tsx
<Separator />
```

---

## 22. Skeleton

로딩 플레이스홀더. `components/ui/skeleton.tsx`

### 클래스 원문 (`skeleton.tsx:7`)

```
animate-pulse rounded-2xl bg-muted
```

### 기본 외형 값
radius `rounded-2xl`, 배경 `bg-muted`, 애니메이션 `animate-pulse`. **크기는 소비자가 지정**.

### 상태 스타일
없음(항상 pulse).

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`rounded-2xl`** — shadcn `rounded-md`. 라이브러리 전역 radius 규칙을 따른다.
> - `bg-muted` (shadcn `bg-accent`).

### 사용 예시 (`components/ui/sidebar.tsx:606-619`) — SidebarMenuSkeleton 내부

```tsx
<Skeleton className="size-4 rounded-xl" data-sidebar="menu-skeleton-icon" />
<Skeleton
  className="h-4 max-w-(--skeleton-width) flex-1"
  data-sidebar="menu-skeleton-text"
  style={{ "--skeleton-width": width } as React.CSSProperties}
/>
```

> 앱 페이지 코드에서의 직접 사용처는 없음.

---

## 23. Progress

진행률 바. `components/ui/progress.tsx`

### 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| Root | `relative flex h-2 w-full items-center overflow-x-hidden rounded-2xl bg-muted` | `progress.tsx:17` |
| Indicator | `size-full flex-1 bg-primary transition-all` | `progress.tsx:24` |

Indicator 위치는 인라인 스타일: `style={{ transform: 'translateX(-${100 - (value || 0)}%)' }}` (`progress.tsx:25`)

### 기본 외형 값
높이 `h-2`(8px), radius `rounded-2xl`, 트랙 `bg-muted`, 인디케이터 `bg-primary`

### 상태 스타일
`transition-all` (값 변경 시 부드럽게 이동). 별도 상태 없음.

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`rounded-2xl`** (shadcn `rounded-full`) — 8px 높이에서는 실질 차이가 거의 없으나 토큰 일관성을 위해 2xl.
> - **`overflow-x-hidden`** (shadcn `overflow-hidden`) — 세로 클리핑 없음.
> - `flex items-center` 추가.

### 사용 예시 (`app/usage/page.tsx:259-262`)

```tsx
<Progress
  value={Math.round(((tok.input + tok.output) / maxToken) * 100)}
  className="h-1.5 bg-muted [&_[data-slot=progress-indicator]]:bg-chart-1"
/>
```

> 인디케이터 색 변경은 `[&_[data-slot=progress-indicator]]:bg-*` 로 한다(`data-slot` 규약의 실사용 예). `app/agents/page.tsx:220`에서는 `[&>*]:bg-red-500` 방식도 쓰인다.

---

## 24. Tooltip

툴팁. `components/ui/tooltip.tsx`

### TooltipContent 클래스 원문 (`tooltip.tsx:45`)

```
z-50 inline-flex w-fit max-w-xs origin-(--radix-tooltip-content-transform-origin) items-center gap-1.5 rounded-xl bg-foreground px-3 py-1.5 text-xs text-background has-data-[slot=kbd]:pr-1.5 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 **:data-[slot=kbd]:relative **:data-[slot=kbd]:isolate **:data-[slot=kbd]:z-50 **:data-[slot=kbd]:rounded-lg data-[state=delayed-open]:animate-in data-[state=delayed-open]:fade-in-0 data-[state=delayed-open]:zoom-in-95 data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95
```

### Arrow (`tooltip.tsx:51`)

```
z-50 size-2.5 translate-y-[calc(-50%_-_2px)] rotate-45 rounded-[2px] bg-foreground fill-foreground data-[side=left]:translate-x-[-1.5px] data-[side=right]:translate-x-[1.5px]
```

### 기본 props
- `TooltipProvider`: `delayDuration = 0` (`tooltip.tsx:9`) — **즉시 표시**
- `TooltipContent`: `sideOffset = 0` (`tooltip.tsx:35`)

### 기본 외형 값
배경 `bg-foreground`(반전) / 글자 `text-xs text-background` / 패딩 `px-3 py-1.5` / radius `rounded-xl` / 최대폭 `max-w-xs`

### 상태 스타일
- 열림: `data-open:animate-in fade-in-0 zoom-in-95`, 지연 열림도 동일(`data-[state=delayed-open]:*`)
- 닫힘: `data-closed:animate-out fade-out-0 zoom-out-95`
- 방향별 슬라이드 `slide-in-from-*-2`

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`delayDuration = 0`** (shadcn 기본 `0`이지만 Provider 레벨에서 명시), **`sideOffset = 0`** (shadcn `4`) — 트리거에 딱 붙는다.
> - **`rounded-xl` + `px-3 py-1.5`** (shadcn `rounded-md px-3 py-1.5`).
> - **`bg-foreground` / `text-background`** (shadcn `bg-primary text-primary-foreground`) — primary 색이 아니라 순수 반전색.
> - **`kbd` 슬롯 특별 처리** — `has-data-[slot=kbd]:pr-1.5` + `**:data-[slot=kbd]:{relative,isolate,z-50,rounded-lg}`. 툴팁 안에 단축키 칩을 넣는 용도.
> - **화살표가 커스텀** — `size-2.5 rotate-45 rounded-[2px]` 회전 사각형 + 좌우 side에서 1.5px 보정.

### 사용 예시 (`app/providers.tsx:12`, 전역 Provider로만 소비)

```tsx
import { TooltipProvider } from "@/components/ui/tooltip";
```

`TooltipContent`의 앱 코드 직접 사용처는 **미확인**(0건). 실제 렌더는 `components/ui/sidebar.tsx:533-538`의 `SidebarMenuButton` 툴팁에서 일어난다.

---

## 25. Sonner (Toaster)

토스트. `components/ui/sonner.tsx`

### 설정 원문

| 항목 | 값 | 출처 |
|---|---|---|
| 루트 클래스 | `toaster group` | `sonner.tsx:24` |
| CSS 변수 | `"--normal-bg": "var(--popover)"`, `"--normal-text": "var(--popover-foreground)"`, `"--normal-border": "var(--border)"`, `"--border-radius": "var(--radius)"` | `sonner.tsx:44-49` |
| toast 클래스 | `cn-toast cursor-pointer` | `sonner.tsx:53` |
| 테마 | `next-themes`의 `theme` (기본 `"system"`) | `sonner.tsx:9,24` |

### 아이콘 (`sonner.tsx:26-42`)

| 종류 | 아이콘 | 클래스 |
|---|---|---|
| success | `CircleCheckIcon` | `size-4` |
| info | `InfoIcon` | `size-4` |
| warning | `TriangleAlertIcon` | `size-4` |
| error | `OctagonXIcon` | `size-4` |
| loading | `Loader2Icon` | `size-4 animate-spin` |

### shadcn 기본과 다른 커스터마이즈 포인트 ⚠️

> - **클릭하면 닫히는 동작을 직접 구현** (`sonner.tsx:11-20`). 소스 주석 원문:
>   > `토스트 본문 아무 곳이나 클릭하면 즉시 닫힘. Sonner는 클릭-닫힘 빌트인이 없어(타이머·스와이프·닫기버튼만) 문서 위임으로 처리(포털 안전). 현재 보이는 토스트를 닫는다.`
>   `document.addEventListener("click", …)` → `e.target.closest("[data-sonner-toast]")`면 `toast.dismiss()`.
> - **`cursor-pointer`** 부여 — 클릭 가능함을 시각적으로 알림.
> - **lucide 아이콘 5종 전면 교체** (Sonner 기본 SVG 대신).
> - **`--border-radius: var(--radius)`** 추가 — 토스트 모서리를 앱 토큰에 맞춤.
> - 커스텀 클래스 `cn-toast` 부여(전역 CSS에서 추가 스타일링 훅).

### 사용 예시 (`app/providers.tsx:112`)

```tsx
<Toaster />
```

---

## 26. Chart

Recharts 래퍼. `components/ui/chart.tsx`

### ChartContainer 클래스 원문 (`chart.tsx:68`)

```
flex aspect-video justify-center text-xs [&_.recharts-cartesian-axis-tick_text]:fill-muted-foreground [&_.recharts-cartesian-grid_line[stroke='#ccc']]:stroke-border/50 [&_.recharts-curve.recharts-tooltip-cursor]:stroke-border [&_.recharts-dot[stroke='#fff']]:stroke-transparent [&_.recharts-layer]:outline-hidden [&_.recharts-polar-grid_[stroke='#ccc']]:stroke-border [&_.recharts-radial-bar-background-sector]:fill-muted [&_.recharts-rectangle.recharts-tooltip-cursor]:fill-muted [&_.recharts-reference-line_[stroke='#ccc']]:stroke-border [&_.recharts-sector]:outline-hidden [&_.recharts-sector[stroke='#fff']]:stroke-transparent [&_.recharts-surface]:outline-hidden
```

### ChartTooltipContent (`chart.tsx:194`)

```
grid min-w-32 items-start gap-1.5 rounded-xl bg-popover px-2.5 py-1.5 text-xs text-popover-foreground shadow-lg ring-1 ring-foreground/5 dark:ring-foreground/10
```

인디케이터 (`chart.tsx:225-232`):
- 베이스: `shrink-0 rounded-[2px] border-(--color-border) bg-(--color-bg)`
- `indicator="dot"` (기본): `h-2.5 w-2.5`
- `indicator="line"`: `w-1`
- `indicator="dashed"`: `w-0 border-[1.5px] border-dashed bg-transparent`
- dashed + nestLabel: `my-0.5`

값 텍스트: `font-mono font-medium text-foreground tabular-nums` (`chart.tsx:256`)

### ChartLegendContent (`chart.tsx:294-295`, `309`, `316`)

- 컨테이너: `flex items-center justify-center gap-4` + (`verticalAlign === "top"` ? `pb-3` : `pt-3`)
- 항목: `flex items-center gap-1.5 [&>svg]:h-3 [&>svg]:w-3 [&>svg]:text-muted-foreground`
- 색 점: `h-2 w-2 shrink-0 rounded-[2px]`

### 기본 외형 값
컨테이너 `aspect-video` 기본 비율, 글자 `text-xs`. 초기 치수 `INITIAL_DIMENSION = { width: 320, height: 200 }` (`chart.tsx:12`)

### 테마 색 주입 (`chart.tsx:10`, `84-115`)
`THEMES = { light: "", dark: ".dark" }`. `ChartStyle`이 `config`를 읽어 `[data-chart=<id>] { --color-<key>: <color> }` 를 `<style>`로 주입.

### shadcn 기본과 다른 커스터마이즈 포인트

> - **`initialDimension` prop 신설** (`chart.tsx:47`, 기본 `{width:320,height:200}`) — SSR/최초 렌더 시 0×0 깜빡임 방지. shadcn에는 없음.
> - **툴팁이 `bg-popover` + `ring-1 ring-foreground/5` + `rounded-xl`** (shadcn `border-border/50 bg-background rounded-lg`) — 라이브러리 표면 규약 적용.
> - **`type !== "none"` payload 필터링** (`chart.tsx:201`, `300`) — 숨김 시리즈가 툴팁·범례에 안 뜨게.
> - 값 포맷이 `toLocaleString()` 기본 적용 (`chart.tsx:257-259`).
> - `min-w-32` 툴팁 최소폭.

### 사용 예시 (`app/reports/page.tsx:112`)

```tsx
<ChartContainer config={radarChartConfig} className="h-[260px] w-full min-w-0">
```

`components/chart-tokens.tsx:79-81`:

```tsx
<ChartContainer
  config={chartConfig}
  className="aspect-auto h-[250px] w-full"
>
```

---

## 27. Sidebar

앱 셸 사이드바 — 23개 서브컴포넌트 + `useSidebar` 훅. `components/ui/sidebar.tsx` (705줄, 최대 규모)

### 상수 (`sidebar.tsx:27-32`)

| 상수 | 값 |
|---|---|
| `SIDEBAR_COOKIE_NAME` | `"sidebar_state"` |
| `SIDEBAR_COOKIE_MAX_AGE` | `60 * 60 * 24 * 7` (7일) |
| `SIDEBAR_WIDTH` | `"16rem"` (256px) |
| `SIDEBAR_WIDTH_MOBILE` | `"18rem"` (288px) |
| `SIDEBAR_WIDTH_ICON` | `"3rem"` (48px) |
| `SIDEBAR_KEYBOARD_SHORTCUT` | `"b"` (⌘B / Ctrl+B) |

### Sidebar props (`sidebar.tsx:151-163`)

| prop | 기본값 | 값 |
|---|---|---|
| `side` | `"left"` | `left` \| `right` |
| `variant` | `"sidebar"` | `sidebar` \| `floating` \| `inset` |
| `collapsible` | `"offcanvas"` | `offcanvas` \| `icon` \| `none` |

### 주요 클래스 원문

| 슬롯 | 클래스 | 출처 |
|---|---|---|
| `SidebarProvider` | `group/sidebar-wrapper flex min-h-svh w-full has-data-[variant=inset]:bg-sidebar` | `sidebar.tsx:140` |
| `Sidebar` (`collapsible="none"`) | `flex h-full w-(--sidebar-width) flex-col bg-sidebar text-sidebar-foreground` | `sidebar.tsx:171` |
| `Sidebar` (모바일 Sheet) | `w-(--sidebar-width) bg-sidebar p-0 text-sidebar-foreground [&>button]:hidden` | `sidebar.tsx:189` |
| `sidebar-gap` | `relative w-(--sidebar-width) bg-transparent transition-[width] duration-200 ease-linear` + `group-data-[collapsible=offcanvas]:w-0` + `group-data-[side=right]:rotate-180` | `sidebar.tsx:220-222` |
| `sidebar-gap` (floating/inset) | `group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)+(--spacing(4)))]` | `sidebar.tsx:224` |
| `sidebar-gap` (기타) | `group-data-[collapsible=icon]:w-(--sidebar-width-icon)` | `sidebar.tsx:225` |
| `sidebar-container` | `fixed inset-y-0 z-10 hidden h-svh w-(--sidebar-width) transition-[left,right,width] duration-200 ease-linear data-[side=left]:left-0 data-[side=left]:group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)] data-[side=right]:right-0 data-[side=right]:group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)] md:flex` | `sidebar.tsx:232` |
| `sidebar-container` (floating/inset) | `p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)+(--spacing(4))+2px)]` | `sidebar.tsx:235` |
| `sidebar-container` (기타) | `group-data-[collapsible=icon]:w-(--sidebar-width-icon) group-data-[side=left]:border-r group-data-[side=right]:border-l` | `sidebar.tsx:236` |
| `sidebar-inner` | `flex size-full flex-col bg-sidebar group-data-[variant=floating]:rounded-2xl group-data-[variant=floating]:shadow-sm group-data-[variant=floating]:ring-1 group-data-[variant=floating]:ring-sidebar-border` | `sidebar.tsx:244` |
| `SidebarRail` | `absolute inset-y-0 z-20 hidden w-4 transition-all ease-linear group-data-[side=left]:-right-4 group-data-[side=right]:left-0 after:absolute after:inset-y-0 after:start-1/2 after:w-[2px] hover:after:bg-sidebar-border sm:flex ltr:-translate-x-1/2 rtl:-translate-x-1/2` (+ 커서/오프캔버스 규칙 4줄) | `sidebar.tsx:291-296` |
| `SidebarInset` | `relative flex w-full flex-1 flex-col bg-background md:peer-data-[variant=inset]:m-2 md:peer-data-[variant=inset]:ml-0 md:peer-data-[variant=inset]:rounded-2xl md:peer-data-[variant=inset]:shadow-sm md:peer-data-[variant=inset]:peer-data-[state=collapsed]:ml-2` | `sidebar.tsx:309` |
| `SidebarInput` | `h-8 w-full bg-input/50 shadow-none` | `sidebar.tsx:325` |
| `SidebarHeader` | `flex flex-col gap-2 p-2 [--radius:var(--radius-xl)]` | `sidebar.tsx:337` |
| `SidebarFooter` | `flex flex-col gap-2 p-2` | `sidebar.tsx:350` |
| `SidebarSeparator` | `mx-2 w-auto bg-sidebar-border` | `sidebar.tsx:364` |
| `SidebarContent` | `no-scrollbar flex min-h-0 flex-1 flex-col gap-2 overflow-auto overscroll-contain [--radius:var(--radius-xl)] group-data-[collapsible=icon]:overflow-hidden` | `sidebar.tsx:376` |
| `SidebarGroup` | `relative flex w-full min-w-0 flex-col p-2` | `sidebar.tsx:389` |
| `SidebarGroupLabel` | `flex h-8 shrink-0 items-center rounded-xl px-3 text-xs font-medium text-sidebar-foreground/70 ring-sidebar-ring outline-hidden transition-[margin,opacity] duration-200 ease-linear group-data-[collapsible=icon]:-mt-8 group-data-[collapsible=icon]:opacity-0 focus-visible:ring-3 [&>svg]:size-4 [&>svg]:shrink-0` | `sidebar.tsx:407` |
| `SidebarGroupAction` | `absolute top-3.5 right-3 flex aspect-square w-5 items-center justify-center rounded-xl p-0 text-sidebar-foreground ring-sidebar-ring outline-hidden transition-transform group-data-[collapsible=icon]:hidden after:absolute after:-inset-2 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-3 md:after:hidden [&>svg]:size-4 [&>svg]:shrink-0` | `sidebar.tsx:427` |
| `SidebarGroupContent` | `w-full text-sm` | `sidebar.tsx:443` |
| `SidebarMenu` | `flex w-full min-w-0 flex-col gap-0.5` | `sidebar.tsx:454` |
| `SidebarMenuItem` | `group/menu-item relative` | `sidebar.tsx:465` |
| `SidebarMenuAction` | `absolute top-1.5 right-1 flex aspect-square w-5 items-center justify-center rounded-xl p-0 text-sidebar-foreground ring-sidebar-ring outline-hidden transition-transform group-data-[collapsible=icon]:hidden peer-hover/menu-button:text-sidebar-accent-foreground peer-data-[size=default]/menu-button:top-1.5 peer-data-[size=lg]/menu-button:top-2.5 peer-data-[size=sm]/menu-button:top-1 after:absolute after:-inset-2 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-3 md:after:hidden [&>svg]:size-4 [&>svg]:shrink-0` | `sidebar.tsx:559` |
| `SidebarMenuAction` (`showOnHover`) | `group-focus-within/menu-item:opacity-100 group-hover/menu-item:opacity-100 peer-data-active/menu-button:text-sidebar-accent-foreground aria-expanded:opacity-100 md:opacity-0` | `sidebar.tsx:561` |
| `SidebarMenuBadge` | `pointer-events-none absolute right-1 flex h-5 min-w-5 items-center justify-center rounded-xl px-1 text-xs font-medium text-sidebar-foreground tabular-nums select-none group-data-[collapsible=icon]:hidden peer-hover/menu-button:text-sidebar-accent-foreground peer-data-[size=default]/menu-button:top-1.5 peer-data-[size=lg]/menu-button:top-2.5 peer-data-[size=sm]/menu-button:top-1 peer-data-active/menu-button:text-sidebar-accent-foreground` | `sidebar.tsx:578` |
| `SidebarMenuSkeleton` | `flex h-8 items-center gap-2 rounded-xl px-2` | `sidebar.tsx:602` |
| `SidebarMenuSub` | `mx-3.5 flex min-w-0 translate-x-px flex-col gap-1 border-l border-sidebar-border px-2.5 py-0.5 group-data-[collapsible=icon]:hidden` | `sidebar.tsx:630` |
| `SidebarMenuSubItem` | `group/menu-sub-item relative` | `sidebar.tsx:646` |
| `SidebarMenuSubButton` | `flex h-7 min-w-0 -translate-x-px items-center gap-2 overflow-hidden rounded-xl px-3 text-sidebar-foreground ring-sidebar-ring outline-hidden group-data-[collapsible=icon]:hidden hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-3 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[size=md]:text-sm data-[size=sm]:text-xs data-active:bg-sidebar-accent data-active:text-sidebar-accent-foreground [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 [&>svg]:text-sidebar-accent-foreground` | `sidebar.tsx:672` |

### SidebarMenuButton (cva — `sidebar.tsx:471-491`)

베이스:
```
peer/menu-button group/menu-button flex w-full items-center gap-2 overflow-hidden rounded-xl px-3 py-2 text-left text-sm whitespace-nowrap ring-sidebar-ring outline-hidden transition-[width,height,padding] duration-200 group-has-data-[sidebar=menu-action]/menu-item:pr-8 group-data-[collapsible=icon]:size-8! group-data-[collapsible=icon]:p-2! hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-3 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 has-[>svg:first-child]:pl-2.5 has-[>svg:last-child]:pr-2.5 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-open:hover:bg-sidebar-accent data-open:hover:text-sidebar-accent-foreground data-active:bg-sidebar-accent data-active:font-medium data-active:text-sidebar-accent-foreground [&_svg]:size-4 [&_svg]:shrink-0 [&>span:last-child]:truncate
```

| variant | 클래스 원문 |
|---|---|
| `default` | `hover:bg-sidebar-accent hover:text-sidebar-accent-foreground` |
| `outline` | `bg-background shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]` |

| size | 클래스 원문 |
|---|---|
| `default` | `h-8 text-sm` |
| `sm` | `h-7 text-xs` |
| `lg` | `h-12 px-3 text-sm group-data-[collapsible=icon]:p-0!` |

기본값: `variant: "default"`, `size: "default"`

`SidebarTrigger`는 `Button variant="ghost" size="icon-sm"` + `PanelLeftIcon` (`sidebar.tsx:261-275`).
`SidebarMenuSubButton`의 `size` 기본값은 `"md"` (`sidebar.tsx:654`, 값은 `sm` \| `md`).

### 상태 스타일
- **active**: `data-active:bg-sidebar-accent data-active:font-medium data-active:text-sidebar-accent-foreground`
- **hover/active(press)**: `bg-sidebar-accent text-sidebar-accent-foreground`
- **focus-visible**: `ring-3` (+ `ring-sidebar-ring`)
- **disabled / aria-disabled**: `pointer-events-none opacity-50`
- **collapsible=icon일 때**: 버튼이 `size-8! p-2!` 정사각형, 라벨은 `-mt-8 opacity-0`으로 접힘, action/badge/sub는 `hidden`
- **collapsible=offcanvas일 때**: 컨테이너가 `left-[calc(var(--sidebar-width)*-1)]`로 화면 밖 이동

### shadcn 기본과 다른 커스터마이즈 포인트

> - **메뉴 버튼 radius가 `rounded-xl`**, Header/Content가 `[--radius:var(--radius-xl)]`로 **지역 radius 토큰을 재정의** — 사이드바 안의 모든 컴포넌트가 자동으로 더 작은 radius를 쓴다. shadcn에 없는 기법.
> - **메뉴 버튼 패딩 `px-3 py-2`** + **`has-[>svg:first-child]:pl-2.5` / `has-[>svg:last-child]:pr-2.5`** 광학 보정.
> - **메뉴 간격 `gap-0.5`** (shadcn `gap-1`), 아이콘 폭 `3rem`(shadcn `3rem` 동일).
> - **`SidebarContent`에 `no-scrollbar` + `overscroll-contain`**.
> - **floating variant가 `rounded-2xl shadow-sm ring-1 ring-sidebar-border`** (shadcn `rounded-lg border`).
> - **`SidebarInset` inset variant가 `rounded-2xl shadow-sm`** (shadcn `rounded-xl shadow-sm`).
> - `SidebarRail`에 `ltr:`/`rtl:` 및 `in-data-[side=*]` 커서 규칙 다수.
> - `SidebarMenuSub`의 `mx-3.5 px-2.5` (shadcn `mx-3.5 px-2.5` 동일), `translate-x-px` 보더 정렬 보정.

### 사용 예시 (`components/app-sidebar.tsx:95-101`)

```tsx
<SidebarHeader>
  <SidebarMenu>
    <SidebarMenuItem>
      <SidebarMenuButton
        asChild
        className="data-[slot=sidebar-menu-button]:p-1.5!"
      >
```

---

## 부록 A. 사용 빈도 (앱 코드 기준)

`components/ui/` 를 제외한 `app/`·`components/`·`lib/` 에서 각 컴포넌트를 import 하는 **파일 수**.
측정 명령: `rg -l "@/components/ui/<name>\"" -g '!components/ui/**' app components lib`

| 순위 | 컴포넌트 | 파일 수 |
|---|---|---|
| 1 | button | 26 |
| 2 | card | 22 |
| 3 | badge | 20 |
| 4 | input | 15 |
| 5 | dialog | 13 |
| 6 | select | 10 |
| 6 | alert-dialog | 10 |
| 8 | textarea | 7 |
| 8 | tabs | 7 |
| 8 | sidebar | 7 |
| 8 | checkbox | 7 |
| 12 | table | 6 |
| 12 | label | 6 |
| 14 | dropdown-menu | 5 |
| 15 | scroll-area | 3 |
| 16 | separator | 2 |
| 16 | progress | 2 |
| 16 | chart | 2 |
| 19 | tooltip | 1 (Provider만) |
| 19 | sonner | 1 (Toaster 전역 1회) |
| 19 | avatar | 1 (`components/nav-user.tsx`) |
| 22 | **toggle-group** | **0** |
| 22 | **toggle** | **0** (toggle-group이 `toggleVariants`만 소비) |
| 22 | **skeleton** | **0** (sidebar 내부에서만) |
| 22 | **sheet** | **0** (sidebar 모바일 모드에서만) |
| 22 | **drawer** | **0** |
| 22 | **breadcrumb** | **0** |

> 기업 배포 라이브러리로 잘라낼 때: 하위 6종(toggle/toggle-group/skeleton/sheet/drawer/breadcrumb)은 앱 미사용이지만 **skeleton·sheet은 sidebar가 의존**하므로 함께 유지해야 한다.

---

## 부록 B. 조합 관례 (앱 페이지에서 실제로 반복되는 패턴)

### B-1. 폼 카드 — `Card > CardContent > (label + Input|Select)`
`app/employees/page.tsx:105-124`

```tsx
<Card className="shadow-xs">
  <CardContent className="flex flex-wrap items-end gap-2 py-4">
    <div className="flex-1 min-w-32">
      <label className="mb-1 block text-xs text-muted-foreground">{t("이름")}</label>
      <Input value={name} onChange={(e) => setName(e.target.value)} placeholder={t("직원 이름")} />
    </div>
```
- **관례**: `Card className="shadow-xs"`로 그림자를 기본(`shadow-sm`)보다 약하게 낮춘다 — 앱 전역에서 반복(`app/company/page.tsx:208,257` 등).
- 필드 라벨은 `Label` 컴포넌트가 아니라 **raw `<label className="mb-1 block text-xs text-muted-foreground">`** 를 쓰는 곳도 많다. `Label`은 주로 Dialog 폼에서 사용(`app/company/page.tsx:417`).
- 필드 최소폭 `min-w-32` + `flex-1`로 반응형 줄바꿈.

### B-2. 목록 행 — `Checkbox + 이름 + Badge들 + 우측 액션`
`app/employees/page.tsx:167-185`

```tsx
<div key={e.id} className="flex items-center gap-3 py-3">
  <Checkbox checked={bulk.has(e.id)} onCheckedChange={() => bulk.toggle(e.id)} aria-label={...} />
  <div className="flex min-w-0 flex-1 items-center gap-2">
    <span className="font-medium">{e.name}</span>
    <Badge variant="outline" className="font-normal">{e.role}</Badge>
```
- **관례**: `Badge variant="outline" className="font-normal"` — 메타 정보 칩은 거의 항상 `outline` + `font-normal`(기본 `font-medium` 해제).
- 텍스트 영역은 `min-w-0 flex-1`로 감싸 말줄임을 보장. (Dialog의 `[&>*]:min-w-0`과 같은 원리)
- 행 컨테이너는 `flex items-center gap-3 py-3`.

### B-3. 사이드바 사용자 행 — `SidebarMenuButton size="lg" > Avatar + 2줄 텍스트 + 아이콘`
`components/nav-user.tsx:41-57`

```tsx
<SidebarMenuButton size="lg" className="data-[state=open]:bg-sidebar-accent …">
  <Avatar className="h-8 w-8 rounded-lg grayscale">
    <AvatarImage src={user.avatar} alt={user.name} />
    <AvatarFallback className="rounded-lg">CN</AvatarFallback>
  </Avatar>
  <div className="grid flex-1 text-left text-sm leading-tight">
    <span className="truncate font-medium">{user.name}</span>
    <span className="truncate text-xs text-muted-foreground">{user.email}</span>
  </div>
  <EllipsisVerticalIcon className="ml-auto size-4" />
</SidebarMenuButton>
```
- **관례**: 아바타 + 주텍스트(`text-sm font-medium`) + 부텍스트(`text-xs text-muted-foreground`) + 우측 아이콘(`ml-auto size-4`). 둘 다 `truncate`.
- Avatar를 `rounded-lg`로 오버라이드해 원형이 아닌 라운드 사각형으로 쓰는 경우가 있다.

### B-4. 확인 모달 — `AlertDialog` 4슬롯 고정형
`app/tasks/page.tsx:1179-1188`
- 항상 `Header(Title + Description)` + `Footer(Cancel + Action)` 구성. `AlertDialogCancel`이 자동으로 `outline`, `AlertDialogAction`이 `default`이므로 **variant를 따로 지정하지 않는다.**
- 삭제 확인 문구는 Title에 질문형, Description에 결과 설명("되돌릴 수 없습니다.").

### B-5. 폼 다이얼로그 — `DialogContent className="sm:max-w-{lg|2xl|6xl}"`
`app/company/page.tsx:411`, `app/reports/page.tsx:315`, `app/documents/page.tsx:512`
- 기본 `sm:max-w-md`를 거의 항상 오버라이드한다: `sm:max-w-lg`(폼) / `sm:max-w-2xl`(상세) / `sm:max-w-6xl`(문서 뷰어).
- 본문은 `<div className="space-y-4 py-2">` + 필드마다 `<div className="space-y-1.5"><Label/><Input/></div>`.

### B-6. 탭 필터 — `Tabs > TabsList > TabsTrigger(반복)`
`app/reports/page.tsx:213-218`, `app/agents/page.tsx:486`
- 모바일 대응이 필요한 곳은 `<TabsList className="w-full sm:w-fit">`.
- 항목은 배열 `.map()`으로 생성, `value`가 필터 키.

### B-7. 스크롤 패널 — `ScrollArea className="min-h-0 flex-1"`
`components/chat-panel.tsx:843,1113`, `app/wiki/page.tsx:115`
- **관례 고정**: flex 부모 안에서 `min-h-0 flex-1` 조합. `min-h-0` 없으면 flex 아이템이 축소되지 않아 스크롤이 생기지 않는다.

### B-8. Progress 색 오버라이드
`app/usage/page.tsx:259-262` / `app/agents/page.tsx:220`
```tsx
className="h-1.5 bg-muted [&_[data-slot=progress-indicator]]:bg-chart-1"
className={over80 ? "[&>*]:bg-red-500" : undefined}
```
- 두 가지 방식이 공존한다. **`data-slot` 셀렉터 방식이 정석**(구조 변경에 안전), `[&>*]`는 축약형.

---

## 부록 C. 주의 · 함정 (소스 주석 및 실측 기반)

### C-1. Dialog / AlertDialog의 grid 오버플로 — `[&>*]:min-w-0`
`components/ui/dialog.tsx:64` 주석 원문:

> `[&>*]:min-w-0 — grid 자식이 축소 가능해야 긴 URL·와이드 콘텐츠가 다이얼로그를 넘치지 않음(전역 안전망)`

**이유**: 이 라이브러리의 DialogContent는 `flex flex-col`이 아니라 **`grid`**다. CSS grid/flex 아이템의 기본 `min-width`는 `auto`라서 자식의 최소 내용 크기(긴 URL 한 덩어리 등)보다 작아질 수 없다. 그래서 `max-w-md`를 줘도 다이얼로그가 가로로 터진다. `[&>*]:min-w-0`이 직계 자식 전부를 축소 가능하게 만들어 근본 차단한다.
`AlertDialogContent`(`alert-dialog.tsx:61`)에도 동일하게 적용되어 있다.

**따라야 할 규칙**: Dialog 안에 **새 중첩 컨테이너**를 만들 때는 그 안쪽에도 `min-w-0`을 직접 붙여야 한다(안전망은 직계 자식 1단계만 커버). 목록 행 패턴(B-2)의 `min-w-0 flex-1`이 같은 이유.

#### C-1a. 적용 깊이 — 정본 (2026-07-20 확정)

`[&>*]`는 **자식 결합자**라 `DialogContent`의 **직계 자식 1단계에만** 적용된다. 손자 이하에는 상속되지 않는다. 이 사실 위에서 정본은 이렇다:

| 위치 | 안전망 적용? | 직접 `min-w-0` | 근거 |
|---|---|---|---|
| DialogContent **직계 자식** (`DialogHeader`, 폼 래퍼, `DialogFooter`) | ✅ 자동 | 불필요(붙여도 무해) | `components/ui/dialog.tsx:64-65` |
| **2단계 이상 중첩** 컨테이너 중 flex/grid 부모 | ❌ 미적용 | **필수** | CSS 자식 결합자 |
| 긴 URL·와이드 콘텐츠(에디터·표·코드)를 담는 컨테이너 | 깊이 무관 | **붙인다** | 아래 실사례 |

**실사례 — 메일 작성창은 직계 자식인데도 명시적으로 붙였다.**

```tsx
// app/mail/page.tsx:1041-1042 (원문) — DialogHeader의 형제 = DialogContent 직계 자식
{/* min-w-0: DialogContent가 grid라 본문의 긴 URL이 트랙을 넓혀 필드가 넘치는 것 방지 */}
<div className="min-w-0 space-y-3">
```

전역 안전망과 이 명시적 `min-w-0`은 **같은 커밋에서 함께** 들어갔다(`32b9b99` "fix(ui): 다이얼로그 grid 자식 min-w-0 — 긴 URL·와이드 콘텐츠 오버플로 해소"). 즉 저자는 안전망을 깔고도 **와이드 콘텐츠를 담는 컨테이너에는 직접 명시**하는 쪽을 택했다. 같은 커밋이 에디터 본문에 `[&_.ProseMirror]:break-words [&_.ProseMirror_a]:[overflow-wrap:anywhere]`(`app/mail/page.tsx:1074`)도 함께 넣었다 — `min-w-0`은 트랙이 넓어지는 것을 막을 뿐, **긴 URL 자체를 줄바꿈하지는 않는다.** 둘은 짝이다.

**04 §5-4 원문(거래처 폼)에 `min-w-0`이 없는 것은 모순이 아니다** — 그 폼의 컨테이너는 직계 자식이고 담는 것이 짧은 라벨·입력뿐이라 안전망만으로 충분하다. 신규 화면 판단 기준은 **깊이가 아니라 "와이드 콘텐츠를 담는가"**다.

### C-2. Sonner 클릭-닫힘은 직접 구현
`components/ui/sonner.tsx:11-12` 주석 원문:

> `토스트 본문 아무 곳이나 클릭하면 즉시 닫힘. Sonner는 클릭-닫힘 빌트인이 없어(타이머·스와이프·닫기버튼만) 문서 위임으로 처리(포털 안전). 현재 보이는 토스트를 닫는다.`

**함정**: `document` 레벨 클릭 위임이라 `toast.dismiss()`가 **인자 없이 호출** — 즉 특정 토스트가 아니라 표시 중인 것을 닫는다. 토스트 안에 액션 버튼을 넣으면 클릭 시 토스트가 함께 닫힌다는 점을 감안해야 한다.

### C-3. Select의 `position="item-aligned"` 기본값
`select.tsx:63` — shadcn 기본(`popper`)과 다르다. `item-aligned`에서는 `data-[align-trigger=true]:animate-none`으로 **열림 애니메이션이 꺼진다**(`select.tsx:72`). 애니메이션이 필요하면 `position="popper"`를 명시해야 하고, 그때만 `translate-y-1` 계열 오프셋이 적용된다.

### C-4. focus 링 값 비일관
같은 라이브러리 안에 두 계열이 섞여 있다:
- `focus-visible:ring-3 focus-visible:ring-ring/30` — Button(`button.tsx:8`), Input(`input.tsx:11`), Textarea, Select, Checkbox, Toggle
- `focus-visible:ring-[3px] focus-visible:ring-ring/50` — Badge(`badge.tsx:8`), Tabs(`tabs.tsx:66`), ScrollArea(`scroll-area.tsx:21`)

두께는 같지만 **불투명도가 30% vs 50%로 다르다.** 새 컴포넌트를 만들 땐 다수파인 `ring-3 ring-ring/30`을 따르는 것이 안전하다.

### C-5. Button의 `active:not-aria-[haspopup]:translate-y-px`
`button.tsx:8` — 눌림 모션이 **`aria-haspopup` 속성이 없는 버튼에만** 적용된다. DropdownMenu/Select 트리거로 쓰면 자동으로 제외되어 팝오버가 열릴 때 트리거가 흔들리지 않는다. `asChild`로 커스텀 트리거를 만들 때 이 속성이 붙는지 확인할 것.

### C-6. Checkbox의 확장 히트 영역
`checkbox.tsx:17`의 `after:absolute after:-inset-x-3 after:-inset-y-2` 때문에 **시각 크기(16px)보다 실제 클릭 영역이 훨씬 크다**(좌우 +12px, 상하 +8px). 체크박스를 다른 클릭 가능 요소 바로 옆에 두면 히트 영역이 겹쳐 오작동할 수 있다. 간격을 최소 `gap-3` 이상 둘 것(B-2 패턴이 `gap-3`인 이유).

### C-7. Sidebar의 지역 radius 재정의
`SidebarHeader`(`sidebar.tsx:337`)와 `SidebarContent`(`sidebar.tsx:376`)에 `[--radius:var(--radius-xl)]`가 붙어 있다. 사이드바 **내부에 넣은 모든 컴포넌트의 radius가 자동으로 작아진다**(전역 `--radius: 0.625rem` → `--radius-xl` = `calc(0.625rem * 1.4)`). 사이드바 안에서 카드나 다이얼로그를 렌더하면 바깥과 모서리가 달라 보이는데, 버그가 아니라 의도된 동작이다.

### C-8. `rounded-2xl`는 크기에 따라 원이 된다
전역 radius 규약이 `rounded-2xl`(=1rem, 16px)이므로 **높이 32px 이하 요소는 사실상 pill 형태**가 된다(Button `h-8`, Badge `h-5`, Input `h-8`). 이는 의도된 디자인이다. 사각형이 필요한 소형 요소는 Checkbox처럼 임의값(`rounded-[5px]`)을 쓴다.

### C-9. `data-slot` 은 스타일링 계약이다
`data-slot`은 디버깅용 마커가 아니라 **외부에서 내부 요소를 겨냥하는 공식 훅**이다. 예: `[&_[data-slot=progress-indicator]]:bg-chart-1`(`app/usage/page.tsx:261`), `*:data-[slot=avatar]:ring-2`(`avatar.tsx:81`), `has-data-[slot=card-action]:grid-cols-[1fr_auto]`(`card.tsx:28`). **컴포넌트를 수정할 때 `data-slot` 값을 바꾸면 앱 곳곳의 스타일이 조용히 깨진다.**

### C-10. Toggle의 on 상태 선택자가 두 갈래
`Toggle`은 `aria-pressed:bg-muted`(`toggle.tsx:10`), `ToggleGroupItem`은 추가로 `data-[state=on]:bg-muted`(`toggle-group.tsx:75`)를 쓴다. 커스텀 on 스타일을 얹을 때 **둘 다 오버라이드**해야 한다.

---

## 부록 D. 헬퍼·유틸 계약 (API 시그니처 — 페이지가 호출하는 것들)

> 재현 시험에서 "경로는 있는데 시그니처가 없어 추정해야 했던" 3종. 아래는 **실제 export 원문**이다.

### D-1. `toneBadgeClass(tone)` — 범용 톤 배지

```ts
// lib/badge-tone.ts:4-33 (원문)
export type BadgeTone =
  | "gray" | "blue" | "green" | "amber" | "yellow" | "purple" | "violet" | "red";

export function toneBadgeClass(tone: BadgeTone): string
```

| 항목 | 값 |
|---|---|
| import | `import { toneBadgeClass, type BadgeTone } from "@/lib/badge-tone";` |
| export 형태 | **named** (default export 없음) |
| 인자 | **1개, 필수**. `BadgeTone` 유니언 (선택적 아님 — 생략 시 타입 에러) |
| 반환 | `string` — Tailwind 클래스 문자열. `<Badge variant="outline" className={…}>`에 그대로 넣는다 |
| 톤 키 전체 (8) | `gray` · `blue` · `green` · `amber` · `yellow` · `purple` · `violet` · `red` |
| 별칭 | `amber`와 `yellow`는 **같은 case로 폴스루** — 반환값 동일 (`badge-tone.ts:20-22`) |
| 기본/폴백 | `gray`가 `default` case와 합쳐져 있어 미지의 값도 회색 (`:29-31`) |
| 반환값 표 | § 04 문서 7-3 참조 (값 원문) |

출처: `lib/badge-tone.ts:4-12`(타입), `:14-33`(함수)

### D-2. `statusBadgeClass(status)` — 업무 상태 전용 배지

```ts
// lib/task-ui.ts:8-20 (원문)
import type { TaskStatus } from "@/lib/constants";
export function statusBadgeClass(status: TaskStatus): string
```

| 항목 | 값 |
|---|---|
| import | `import { statusBadgeClass, statusDotClass } from "@/lib/task-ui";` |
| export 형태 | **named** |
| 인자 | **1개, 필수**. `TaskStatus` |
| `TaskStatus` 값 (4) | `"Not Started"` · `"In Progress"` · `"Pending"` · `"Completed"` — 노션 스키마 원문 유지 |
| 반환 | `string` (Tailwind 클래스) |
| 폴백 | `"Not Started"`가 `default`와 합쳐짐 → 회색 (`task-ui.ts:16-18`) |
| 짝 함수 | `statusDotClass(status)` — 캘린더 셀 점/막대용 **배경색** 반환. 값이 다르다(`bg-{색}-500/15 text-{색}-700 dark:text-{색}-300`) (`task-ui.ts:23-35`) |

출처: `lib/constants.ts:4-10`(`TASK_STATUSES` / `TaskStatus`), `lib/task-ui.ts:8-20`, `:23-35`

> **주의**: `TaskStatus`는 `lib/constants.ts`에서, `statusBadgeClass`는 `lib/task-ui.ts`에서 온다. 모듈이 다르다.

### D-3. `toneBadgeClass` vs `StatCard` 톤 키 — **키 집합이 다르다** ⚠️

세 곳의 톤 테이블이 **값은 같은데 키 이름이 다르다.** 서로 바꿔 쓸 수 없다.

| 출처 | 키 | 색 |
|---|---|---|
| `lib/badge-tone.ts:4-12` | `blue` / `green` / `amber`·`yellow` / `purple` / `violet` / `red` / `gray` | — |
| `components/stat-card.tsx:14-20` | `info` / `success` / `warning` / — / `violet` / `danger` / `neutral` | 같은 색값 |
| `lib/task-ui.ts:8-20` | `"In Progress"` / `"Completed"` / `"Pending"` / — / — / — / `"Not Started"` | 같은 색값 |

`StatCard`가 쓰는 톤은 **`stat-card.tsx`가 자체 정의한 `BadgeTone`**이며, `lib/badge-tone.ts`의 동명 타입과 **이름만 같고 값이 다른 별개 타입**이다. `stat-card` 쪽에는 `purple`이 없고, `badge-tone` 쪽에는 `neutral`이 없다.

```ts
// components/stat-card.tsx:14-20 (원문)
export type BadgeTone =
  | "neutral" | "danger" | "warning" | "info" | "success" | "violet";
```

**import 시 이름 충돌 주의**: 한 파일에서 둘 다 쓰면 `import { type BadgeTone as StatTone } from "@/components/stat-card";`처럼 별칭이 필요하다.

### D-4. `Stat` 타입 (StatCard props)

```ts
// components/stat-card.tsx:33-41 (원문)
export type Stat = {
  label: string;
  value: React.ReactNode;
  badge?: { text: string; icon?: React.ReactNode; tone?: BadgeTone };
  footerTitle?: React.ReactNode;
  footerSub?: React.ReactNode;
  danger?: boolean;
  href?: string;
};
```

| 항목 | 값 |
|---|---|
| import | `import { StatCard, StatGrid, type Stat } from "@/components/stat-card";` |
| `Stat` export | ✅ **export 됨** (`stat-card.tsx:33`) — 페이지에서 `const stats: Stat[] = [...]`로 쓴다 |
| `StatCard` props | `{ stat: Stat }` — 객체 1개. 개별 필드를 펼쳐 받지 **않는다** (`:45`) |
| `StatGrid` props | `{ stats: Stat[]; className?: string }` (`:98-104`) |
| `badge.tone` 생략 시 | `"neutral"`로 폴백 = 빈 문자열 클래스 → Badge outline 기본 외형 (`:62`, `:25`) |
| `danger: true` | 수치에 `text-destructive` 추가 (`:55`) |
| `href` 지정 시 | 카드 전체가 `<Link>`로 감싸짐 + `block transition-shadow hover:shadow-sm focus-visible:ring-2 focus-visible:ring-ring` (`:85-94`) |

실사용: `app/tasks/page.tsx:26`, `app/usage/page.tsx:17`, `app/agents/page.tsx:41`, `app/tools/page.tsx:17`, `app/briefings/page.tsx:16`, `app/automation/page.tsx:16`

### D-5. `useT()` — i18n 번역 함수

```ts
// lib/i18n.tsx:469-470, 492-495, 503 (원문)
type Ctx = { locale: Locale; setLocale: (l: Locale) => void; t: (ko: string) => string };
export const useT = () => useContext(LocaleContext).t;
```

| 항목 | 값 |
|---|---|
| import | `import { useT } from "@/lib/i18n";` |
| export 형태 | **named** (`lib/i18n.tsx:503`). default export 없음 |
| 반환 | 함수 `t: (ko: string) => string` |
| `t` 인자 | **1개, 필수. 한국어 원문 문자열** — 키가 곧 한글이다 (`t("새로고침")`) |
| **보간 인자** | **없음.** `t(ko, vars)` 형태 미지원 — 값 삽입은 JS 템플릿으로 바깥에서 조립한다 |
| **사전에 없는 키** | **원문(한국어)을 그대로 반환.** 빈 문자열도, 키 문자열도 아니다 |

동작 원문:

```ts
// lib/i18n.tsx:492-495 (원문)
const t = useCallback(
  (ko: string) => (locale === "ko" ? ko : DICT[ko]?.[locale] ?? ko),
  [locale],
);
```

- `locale === "ko"` → **사전을 아예 조회하지 않고** 인자를 그대로 반환.
- 그 외 로케일 → `DICT[ko]?.[locale] ?? ko`. 키 누락·로케일 누락 모두 **`?? ko`로 한국어 폴백**. 화면이 깨지지 않는다.
- 파일 상단 주석이 같은 말을 한다: `사전에 없으면 한글 그대로 폴백(깨지지 않음)` (`lib/i18n.tsx:4`).

| 부수 항목 | 값 | 출처 |
|---|---|---|
| 로케일 3종 | `"ko"` \| `"en"` \| `"ja"` | `lib/i18n.tsx:17-22` |
| 사전 병합 | `{ ...DICT_EXT, ...INLINE }` — **INLINE(큐레이트)이 자동생성을 덮어씀** | `:467` |
| 영속 | `localStorage("locale")` + `<html lang>` 동기화 | `:475-481` |
| 짝 훅 | `useLocale()` → `{ locale, setLocale, t }` 전체 | `:502` |
| Provider | `<LocaleProvider>` 필요 (`app/providers.tsx`에서 배선) | `:472` |
| 기본값(Provider 밖) | `t: (s) => s` — 항등 함수라 Provider 없이도 크래시 안 남 | `:470` |

**보간이 필요할 때의 실제 관례** — 문자열을 쪼개 `t()`를 각각 호출하고 JS로 잇는다:

```tsx
// app/usage/page.tsx:167 (원문 형태)
footerSub: `${(u?.byToolCategory ?? []).length}${t("개 행 집계")}`
// app/mail/page.tsx:706-710 (원문 형태)
`${t("발송 실패")}: ${res.error ?? t("알 수 없음")}`
```

> 하위 컴포넌트도 각자 `const t = useT()`를 호출한다(props로 내려주지 않는다) — `app/tasks/page.tsx:551`, `:642`, `:670`.
