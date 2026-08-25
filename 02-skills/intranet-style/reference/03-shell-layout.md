# 03 — 앱 셸 · 레이아웃 문법

원본 인트라넷(`<인트라넷 레포>`)의 **골격**을 픽셀 단위로 재현하기 위한 레퍼런스.
모든 값은 실제 소스에서 추출했고, 각 항목에 `파일:라인` 출처를 붙였다. 확인 못 한 것은 **미확인**으로 표기했다.

기술 베이스: Next.js App Router · Tailwind CSS **v4** (`package.json:57` → `"tailwindcss": "^4.3.1"`) · shadcn/ui 사이드바 · refine v5.

---

## 0. 선행 지식 — 계산의 기준이 되는 두 값

레이아웃 전체가 이 두 값에서 파생된다.

| 토큰 | 값 | 출처 |
|---|---|---|
| `--spacing` | `0.25rem` | `node_modules/tailwindcss/theme.css:325` (Tailwind v4 기본값. **`app/globals.css`의 `@theme inline` 블록에서 재정의하지 않음** → 기본값 그대로 적용) |
| `--radius` | `0.625rem` | `app/globals.css:76` |

`--radius` 파생 스케일 (`app/globals.css:42-48`):

```css
--radius-sm: calc(var(--radius) * 0.6);   /* 0.375rem */
--radius-md: calc(var(--radius) * 0.8);   /* 0.5rem */
--radius-lg: var(--radius);               /* 0.625rem */
--radius-xl: calc(var(--radius) * 1.4);   /* 0.875rem */
--radius-2xl: calc(var(--radius) * 1.8);  /* 1.125rem */
--radius-3xl: calc(var(--radius) * 2.2);  /* 1.375rem */
--radius-4xl: calc(var(--radius) * 2.6);  /* 1.625rem */
```

---

## 1. 전체 골격도

### 1-1. 라우트 구조 — 레이아웃은 **단 하나**

```
app/layout.tsx   ← 유일한 layout. 라우트 그룹 layout 없음
```

출처: `find app -name "layout.tsx"` → `app/layout.tsx` 1건만 존재. **라우트 그룹(`app/(group)/layout.tsx`)은 존재하지 않는다.**
셸(사이드바 + 헤더 + 콘텐츠)은 layout이 아니라 **`app/providers.tsx`의 `<Providers>` 컴포넌트**가 전부 구성한다.

### 1-2. 루트 셸 (`app/layout.tsx`)

```tsx
const inter = Inter({subsets:['latin'],variable:'--font-sans'});   // :9

<html lang="ko" className={cn("font-sans", inter.variable)} suppressHydrationWarning>   // :20
  <body suppressHydrationWarning>                                                      // :21
    <Suspense>
      <Providers>{children}</Providers>
    </Suspense>
    <AgentationDev />
  </body>
</html>
```

- 폰트: `next/font/google`의 **Inter**, latin subset, CSS 변수 `--font-sans`로 노출 (`app/layout.tsx:9`).
- `@theme inline`에서 `--font-sans: var(--font-sans)` / `--font-heading: var(--font-sans)` (`app/globals.css:9-10`) → **heading과 body가 같은 폰트**.
- metadata: `title: "Lean - AX"` (`app/layout.tsx:12`).
- `<html>`에 `font-sans` 클래스 직접 부여 — body가 아니다.

### 1-3. Providers 중첩 순서 (`app/providers.tsx:19-114`)

```
ThemeProvider (next-themes, attribute="class", defaultTheme="system", enableSystem, disableTransitionOnChange)
└ Refine (routerProvider / dataProvider / resources 14개 / syncWithLocation:true, disableTelemetry:true)
  ├ TooltipProvider (delayDuration={0})
  │ └ LocaleProvider
  │   └ ChatProvider                    ← 우하단 플로팅 챗 FAB를 여기서 렌더
  │     └ SidebarProvider (style로 --sidebar-width / --header-height 주입)
  │       ├ AppSidebar variant="inset"
  │       └ SidebarInset
  │         ├ SiteHeader
  │         └ div.flex.flex-1.flex-col
  │           └ div.@container/main.flex.flex-1.flex-col.gap-2
  │             └ div#page-content   ← 페이지 콘텐츠 컨테이너
  └ Toaster (sonner) — TooltipProvider 바깥, Refine 안쪽
```

`themes` 배열에 **33개 테마**가 등록되어 있다 (`app/providers.tsx:24-58`): `light, dark, tokyo-night, nord, everforest, claude, monokai-sun, solarized-dark, dracula-soft, material-hc, monokai-pro, slack, rose-pine, quiet-light, earthbound, base16-grayscale, solarized-autumn, turtle, semantic-colors, natural, thanatos, mossy-forest, codex, anthropic-inspired, retro-keyboard, savanna-dusk, savanna-dawn, mocaccino-light, claude-warm-light, claude-vscode, paper-notebook, sociedade-pinguim, orange-flavor`.

### 1-4. 텍스트 다이어그램 (데스크톱 ≥768px, 사이드바 펼침 상태)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│ div[data-slot=sidebar-wrapper]                                                │
│   group/sidebar-wrapper flex min-h-svh w-full has-data-[variant=inset]:bg-sidebar
│   style: --sidebar-width: calc(var(--spacing)*60) = 15rem (240px)             │
│          --sidebar-width-icon: 3rem (48px)                                    │
│          --header-height:  calc(var(--spacing)*12) = 3rem (48px)              │
│                                                                               │
│ ┌─ [sidebar-gap] ─┐┌─ <main data-slot=sidebar-inset> ────────────────────────┐│
│ │ w-(--sidebar-   ││  relative flex w-full flex-1 flex-col bg-background      ││
│ │      width)     ││  md:m-2  md:ml-0  md:rounded-2xl  md:shadow-sm          ││
│ │  = 15rem        ││  (collapsed일 때 md:ml-2)                                ││
│ │  (자리만 차지)   ││                                                          ││
│ │                 ││ ┌─ <header> SiteHeader ─────────────────────────────┐   ││
│ │ 실제 패널은      ││ │ h-(--header-height)=3rem · shrink-0 · border-b     │   ││
│ │ [sidebar-       ││ │ 내부: flex h-full w-full items-center              │   ││
│ │  container]가   ││ │       gap-1 px-4  ·  lg:gap-2 lg:px-6              │   ││
│ │ fixed inset-y-0 ││ │ [트리거] [세로구분선] [타이틀] ······· [알림벨]      │   ││
│ │ z-10 h-svh      ││ └───────────────────────────────────────────────────┘   ││
│ │ w-(--sidebar-   ││ ┌─ div.flex.flex-1.flex-col ────────────────────────┐   ││
│ │  width) p-2     ││ │ ┌ div.@container/main.flex.flex-1.flex-col.gap-2 ┐│   ││
│ │ (inset variant) ││ │ │ ┌ div#page-content ───────────────────────────┐ ││   ││
│ │                 ││ │ │ │ flex flex-col gap-4                         │ ││   ││
│ │  ┌ header p-2 ┐ ││ │ │ │ px-4 py-4                                   │ ││   ││
│ │  ├ content    ┤ ││ │ │ │ md:gap-6 md:py-6                            │ ││   ││
│ │  │  (스크롤)   │ ││ │ │ │ lg:px-6                                     │ ││   ││
│ │  ├ footer p-2 ┤ ││ │ │ │   {children}  ← 각 page.tsx                  │ ││   ││
│ │  └───────────┘ ││ │ │ └─────────────────────────────────────────────┘ ││   ││
│ └─────────────────┘│ │ └────────────────────────────────────────────────┘│   ││
│                    │ └──────────────────────────────────────────────────┘   ││
│                    └────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────┘
        ▲ 화면 우하단 고정: 챗 FAB  fixed bottom-5 right-5 z-40 size-12
```

**핵심 트릭 — 2단 구조**: 사이드바는 `sidebar-gap`(자리를 차지하는 빈 div)과 `sidebar-container`(`fixed`로 실제 그려지는 패널) 두 겹으로 되어 있다 (`components/ui/sidebar.tsx:217-248`). 애니메이션은 gap의 `width`와 container의 `left`를 동시에 트랜지션해서 만든다.

---

## 2. 사이드바 스펙

### 2-1. 폭 토큰 — **앱이 shadcn 기본값을 덮어쓴다** (중요)

| 토큰 | shadcn 기본 상수 | 앱 실제 적용값 | 출처 |
|---|---|---|---|
| `--sidebar-width` (데스크톱) | `SIDEBAR_WIDTH = "16rem"` | **`calc(var(--spacing) * 60)` = 15rem = 240px** | 기본 `components/ui/sidebar.tsx:29` / 오버라이드 `app/providers.tsx:87` |
| `--sidebar-width-icon` | `SIDEBAR_WIDTH_ICON = "3rem"` | `3rem` (48px, 그대로) | `components/ui/sidebar.tsx:31` |
| 모바일 시트 폭 | `SIDEBAR_WIDTH_MOBILE = "18rem"` | `18rem` (288px, 그대로) | `components/ui/sidebar.tsx:30, 192` |
| `--header-height` | (shadcn에 없음) | **`calc(var(--spacing) * 12)` = 3rem = 48px** | `app/providers.tsx:88` |

오버라이드가 성립하는 이유 — `SidebarProvider`가 style을 합칠 때 **전달받은 `style`을 뒤에 스프레드**한다:

```tsx
// components/ui/sidebar.tsx:132-138
style={
  {
    "--sidebar-width": SIDEBAR_WIDTH,
    "--sidebar-width-icon": SIDEBAR_WIDTH_ICON,
    ...style,          // ← providers.tsx가 넘긴 값이 뒤에 와서 이김
  } as React.CSSProperties
}
```

```tsx
// app/providers.tsx:84-91
<SidebarProvider
  style={
    {
      "--sidebar-width": "calc(var(--spacing) * 60)",
      "--header-height": "calc(var(--spacing) * 12)",
    } as React.CSSProperties
  }
>
```

### 2-2. 상태 · 동작

| 항목 | 값 | 출처 |
|---|---|---|
| variant | `"inset"` | `app/providers.tsx:92` (`<AppSidebar variant="inset" />`) |
| collapsible | `"offcanvas"` | `components/app-sidebar.tsx:94` |
| 기본 열림 | `defaultOpen = true` | `components/ui/sidebar.tsx:56` |
| 상태 저장 | 쿠키 `sidebar_state`, `max-age = 60*60*24*7` (7일) | `components/ui/sidebar.tsx:27-28, 85` |
| 키보드 토글 | `Cmd/Ctrl + B` | `components/ui/sidebar.tsx:32, 96-109` |
| 접힘 시 동작 | `offcanvas` → gap이 `w-0`, container가 `left-[calc(var(--sidebar-width)*-1)]`로 화면 밖으로 슬라이드 | `components/ui/sidebar.tsx:221, 232` |
| 트랜지션 | `duration-200 ease-linear` (gap은 `transition-[width]`, container는 `transition-[left,right,width]`) | `components/ui/sidebar.tsx:220, 232` |

> **주의**: `collapsible="offcanvas"`이므로 이 앱에서 **아이콘 축소 모드(48px 레일)는 실제로 발생하지 않는다.** `--sidebar-width-icon`과 `group-data-[collapsible=icon]:*` 스타일은 정의만 되어 있고 미사용 경로다.

### 2-3. 컨테이너 클래스 원문

```tsx
// sidebar-gap — components/ui/sidebar.tsx:219-226
"relative w-(--sidebar-width) bg-transparent transition-[width] duration-200 ease-linear"
"group-data-[collapsible=offcanvas]:w-0"
"group-data-[side=right]:rotate-180"
// inset/floating일 때:
"group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)+(--spacing(4)))]"
```

```tsx
// sidebar-container — components/ui/sidebar.tsx:232-236
"fixed inset-y-0 z-10 hidden h-svh w-(--sidebar-width) transition-[left,right,width] duration-200 ease-linear data-[side=left]:left-0 data-[side=left]:group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)] data-[side=right]:right-0 data-[side=right]:group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)] md:flex"
// inset/floating variant일 때 추가:
"p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)+(--spacing(4))+2px)]"
```

```tsx
// sidebar-inner — components/ui/sidebar.tsx:244
"flex size-full flex-col bg-sidebar group-data-[variant=floating]:rounded-2xl group-data-[variant=floating]:shadow-sm group-data-[variant=floating]:ring-1 group-data-[variant=floating]:ring-sidebar-border"
```

**inset variant는 컨테이너에 `p-2`(0.5rem)를 준다** → 실제 패널 시각 폭 = `15rem − 1rem` = **14rem(224px)**, 좌우 각 8px 여백. 배경은 wrapper의 `has-data-[variant=inset]:bg-sidebar`가 깔린다 (`components/ui/sidebar.tsx:140`).

### 2-4. 색 토큰 (사이드바 전용)

`@theme inline`에 `--color-sidebar-*` → `--sidebar-*` 매핑 (`app/globals.css:11-18`).

| 토큰 | light (`:root`) | dark (`.dark`) | 출처 |
|---|---|---|---|
| `--sidebar` | `oklch(0.982 0 0)` | `oklch(0.226 0 0)` | `globals.css:77` / `:111` |
| `--sidebar-foreground` | `oklch(0.226 0 0)` | `oklch(0.985 0 0)` | `:78` / `:112` |
| `--sidebar-primary` | `oklch(0.205 0 0)` | `oklch(0.738 0.127 282.8)` | `:79` / `:113` |
| `--sidebar-primary-foreground` | `oklch(0.985 0 0)` | `oklch(0.226 0 0)` | `:80` / `:114` |
| `--sidebar-accent` | `oklch(0.952 0.019 282.8)` | `oklch(0.321 0 0)` | `:81` / `:115` |
| `--sidebar-accent-foreground` | `oklch(0.226 0 0)` | `oklch(0.985 0 0)` | `:82` / `:116` |
| `--sidebar-border` | `oklch(0.940 0 0)` | `oklch(1 0 0 / 10%)` | `:83` / `:117` |
| `--sidebar-ring` | `oklch(0.738 0.127 282.8)` | `oklch(0.738 0.127 282.8)` | `:84` / `:118` |

(테마별 오버라이드가 33개 더 있다 — 예: `tokyo-night` `globals.css:137-140`, `nord` `:155-158`. 상세는 별도 색 문서 소관.)

### 2-5. 슬롯별 패딩 · 크기

| 슬롯 | 클래스 원문 | 출처 |
|---|---|---|
| `SidebarHeader` | `flex flex-col gap-2 p-2 [--radius:var(--radius-xl)]` | `sidebar.tsx:337` |
| `SidebarContent` | `no-scrollbar flex min-h-0 flex-1 flex-col gap-2 overflow-auto overscroll-contain [--radius:var(--radius-xl)] group-data-[collapsible=icon]:overflow-hidden` | `sidebar.tsx:376` |
| `SidebarFooter` | `flex flex-col gap-2 p-2` | `sidebar.tsx:350` |
| `SidebarGroup` | `relative flex w-full min-w-0 flex-col p-2` | `sidebar.tsx:389` |
| `SidebarGroupContent` | `w-full text-sm` | `sidebar.tsx:443` |
| `SidebarMenu` | `flex w-full min-w-0 flex-col gap-0.5` | `sidebar.tsx:454` |
| `SidebarMenuItem` | `group/menu-item relative` | `sidebar.tsx:465` |
| `SidebarSeparator` | `mx-2 w-auto bg-sidebar-border` | `sidebar.tsx:364` |

**`SidebarHeader`/`SidebarContent`가 `[--radius:var(--radius-xl)]`로 지역 radius를 올린다** → 그 안의 `rounded-xl` 유틸이 `0.875rem`이 아니라 `--radius-xl` 재정의를 따라간다. 사이드바 내부만 더 둥근 이유.

### 2-6. 그룹 라벨 ("업무" / "회사" / "시스템")

```tsx
// components/ui/sidebar.tsx:406-408
"flex h-8 shrink-0 items-center rounded-xl px-3 text-xs font-medium text-sidebar-foreground/70 ring-sidebar-ring outline-hidden transition-[margin,opacity] duration-200 ease-linear group-data-[collapsible=icon]:-mt-8 group-data-[collapsible=icon]:opacity-0 focus-visible:ring-3 [&>svg]:size-4 [&>svg]:shrink-0"
```

- 높이 `h-8` (2rem/32px), 좌우 `px-3` (0.75rem), 글자 `text-xs` (0.75rem) `font-medium`, 색 `text-sidebar-foreground/70` (70% 투명도).
- 라벨이 붙는 그룹은 `NavMain`에서 `className="py-1"`을 추가로 받는다 (`components/nav-main.tsx:26`) → 그룹 세로 패딩이 `p-2`(0.5rem)에서 **`py-1`(0.25rem)로 덮인다**.
- 그룹 내부 메뉴 래퍼: `SidebarGroupContent className="flex flex-col gap-1"` (`nav-main.tsx:28`).

### 2-7. 메뉴 아이템 (버튼)

```tsx
// sidebarMenuButtonVariants base — components/ui/sidebar.tsx:472
"peer/menu-button group/menu-button flex w-full items-center gap-2 overflow-hidden rounded-xl px-3 py-2 text-left text-sm whitespace-nowrap ring-sidebar-ring outline-hidden transition-[width,height,padding] duration-200 group-has-data-[sidebar=menu-action]/menu-item:pr-8 group-data-[collapsible=icon]:size-8! group-data-[collapsible=icon]:p-2! hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-3 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 has-[>svg:first-child]:pl-2.5 has-[>svg:last-child]:pr-2.5 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-open:hover:bg-sidebar-accent data-open:hover:text-sidebar-accent-foreground data-active:bg-sidebar-accent data-active:font-medium data-active:text-sidebar-accent-foreground [&_svg]:size-4 [&_svg]:shrink-0 [&>span:last-child]:truncate"
```

size 변형 (`sidebar.tsx:480-484`):

```
default: "h-8 text-sm"                                       ← 32px, 일반 내비 항목
sm:      "h-7 text-xs"                                       ← 28px
lg:      "h-12 px-3 text-sm group-data-[collapsible=icon]:p-0!"  ← 48px, NavUser가 사용
```

정리:

| 속성 | 값 |
|---|---|
| 높이 | `h-8` = 2rem = **32px** (default) |
| 좌우 패딩 | `px-3` = 0.75rem, 단 **아이콘이 첫 자식이면 `pl-2.5`(0.625rem)로 좁혀짐** (`has-[>svg:first-child]:pl-2.5`) |
| 상하 패딩 | `py-2` = 0.5rem (`h-8`과 함께 작용) |
| 아이콘–라벨 간격 | `gap-2` = 0.5rem |
| 아이콘 크기 | `[&_svg]:size-4` = 1rem = **16px**, `shrink-0` |
| 라운드 | `rounded-xl` (사이드바 안에서는 `--radius-xl` 지역 재정의 적용) |
| 글자 | `text-sm` (0.875rem) |
| hover | `bg-sidebar-accent` + `text-sidebar-accent-foreground` |
| **활성** | `data-active:bg-sidebar-accent` + `data-active:font-medium` + `data-active:text-sidebar-accent-foreground` |
| 포커스 | `focus-visible:ring-3` + `ring-sidebar-ring` |
| 라벨 넘침 | `[&>span:last-child]:truncate` |

**활성 판정 로직** (`components/nav-main.tsx:31-34`):

```tsx
const isActive =
  item.url === "/"
    ? pathname === "/"                 // 대시보드는 정확 매칭
    : pathname.startsWith(item.url)    // 나머지는 prefix 매칭
```

**툴팁**: 모든 메인 메뉴 항목이 `tooltip={t(item.title)}`을 받지만 (`nav-main.tsx:39`), `TooltipContent`가 `hidden={state !== "collapsed" || isMobile}` (`sidebar.tsx:536`)이라 **접힘 상태에서만 표시**된다. offcanvas 모드에서는 접히면 패널 자체가 화면 밖이므로 사실상 노출되지 않는다.

### 2-8. 사이드바 헤더 (브랜드)

```tsx
// components/app-sidebar.tsx:95-120
<SidebarHeader>
  <SidebarMenu><SidebarMenuItem>
    <SidebarMenuButton asChild className="data-[slot=sidebar-menu-button]:p-1.5!">
      <a href="/">
        <svg viewBox="0 0 622 622" className="size-5! shrink-0" fill="currentColor">…4원 로고…</svg>
        <span className="text-base font-semibold">Lean - AX</span>
      </a>
    </SidebarMenuButton>
  </SidebarMenuItem></SidebarMenu>
</SidebarHeader>
```

- 패딩을 `p-1.5!`(0.375rem, `!important`)로 강제 축소 — 일반 항목의 `px-3 py-2`보다 좁다.
- 로고 `size-5!` = 1.25rem = **20px** (일반 아이콘 16px보다 큼, `!`로 `[&_svg]:size-4` 무력화).
- 워드마크: `text-base font-semibold` (1rem).
- 로고 SVG: 622×622 viewBox, 4개 원. 불투명도 `1 / 0.4 / 0.4 / 0.2` (좌상 → 우상 → 좌하 → 우하).

### 2-9. 내비 구조 (그룹 4개 + 보조 1개)

`components/app-sidebar.tsx:47-89` 원문 구조:

| 그룹 라벨 | 항목 (title → url, icon) |
|---|---|
| *(없음)* | 대시보드 `/` `LayoutDashboardIcon` · 메일 `/mail` `MailIcon` · 드라이브 `/drive` `HardDriveIcon` |
| **업무** | 업무 보드 `/tasks` `ListIcon` · 워크보드 `/workboard` `NotebookPenIcon` · 캘린더 `/calendar` `CalendarIcon` · 브리핑 `/briefings` `FileTextIcon` |
| **회사** | 거래처 `/customers` `Building2Icon` · 직원 `/employees` `UsersIcon` · 회사 정보 `/company` `BriefcaseIcon` · 문서함 `/documents` `FilesIcon` · 견적·계약 `/quote-contract` `ReceiptTextIcon` · 지식망 `/wiki` `BookOpenIcon` · 업무성과 `/reports` `AwardIcon` |
| **시스템** | 에이전트 `/agents` `NetworkIcon` · 자동화 현황 `/automation` `BotIcon` · 사용량 `/usage` `ChartBarIcon` · 도구 `/tools` `WrenchIcon` |
| `navSecondary` | 설정 `/settings` `Settings2Icon` · 도움말 `#` `CircleHelpIcon` |

- 첫 그룹은 **라벨 없음** → `{group.label && …}` 조건부라 라벨 노드 자체가 렌더되지 않는다 (`nav-main.tsx:27`).
- `NavSecondary`는 `className="mt-auto"`로 **하단 밀착** (`app-sidebar.tsx:123`). 링크는 `<Link>`가 아니라 순수 `<a>`이고 활성 상태 표시가 없다 (`components/nav-secondary.tsx:32-35`).
- 아이콘은 컴포넌트가 아니라 **JSX 엘리먼트로 데이터에 인라인 저장**된다 (`icon: <MailIcon />`).

### 2-10. 하단 사용자 영역 (`SidebarFooter` → `NavUser`)

`components/nav-user.tsx:41-56`:

```tsx
<SidebarMenuButton size="lg"
  className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground">
  <Avatar className="h-8 w-8 rounded-lg grayscale">…</Avatar>
  <div className="grid flex-1 text-left text-sm leading-tight">
    <span className="truncate font-medium">{user.name}</span>
    <span className="truncate text-xs text-muted-foreground">{user.email}</span>
  </div>
  <EllipsisVerticalIcon className="ml-auto size-4" />
</SidebarMenuButton>
```

| 항목 | 값 |
|---|---|
| 버튼 높이 | `size="lg"` → `h-12` = 3rem = **48px** |
| 아바타 | `h-8 w-8 rounded-lg grayscale` = 32px, **흑백 필터** |
| 이름 | `text-sm font-medium truncate` |
| 이메일 | `text-xs text-muted-foreground truncate` |
| 우측 아이콘 | `EllipsisVerticalIcon` `ml-auto size-4` |
| 열림 상태 | `data-[state=open]:bg-sidebar-accent` |

드롭다운 (`nav-user.tsx:58-63`): `className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"`, `side={isMobile ? "bottom" : "right"}`, `align="end"`, `sideOffset={4}`. 메뉴 항목 — Account / Billing / Notifications / (구분선) / Log out. **하드코딩 영문 라벨이며 i18n `t()`를 거치지 않는다.**

사용자 데이터도 하드코딩 (`app-sidebar.tsx:41-45`): `name: "{{OWNER_NAME}}"`, `email: "{{OWNER_EMAIL}}"`, `avatar: ""` (빈 문자열 → `AvatarFallback` "CN" 표시, `nav-user.tsx:47`).

### 2-11. `nav-documents.tsx` — 정의만 있고 **미사용**

`components/nav-documents.tsx`는 `NavDocuments`를 export하지만, 저장소 전체 `.tsx` grep 결과 **호출부가 없다** (자기 정의 라인 `nav-documents.tsx:21` 1건만 매치). 새 앱 골격 재현 시 **이식 불필요한 데드 컴포넌트**로 취급하면 된다. (구조 참고용: `SidebarGroup class="group-data-[collapsible=icon]:hidden"` + `SidebarGroupLabel "Documents"` + 항목별 `SidebarMenuAction showOnHover` 드롭다운.)

---

## 3. 헤더 스펙 (`components/site-header.tsx`)

```tsx
// :15
<header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
  {/* :16 */}
  <div className="flex h-full w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
    <SidebarTrigger className="-ml-1" />                                       {/* :17 */}
    <Separator orientation="vertical"
      className="mx-2 data-[orientation=vertical]:h-4 data-[orientation=vertical]:self-center" />  {/* :18-21 */}
    <h1 className="text-base font-medium leading-none">{t(pageTitle(pathname))}</h1>  {/* :22 */}
    <div className="ml-auto flex items-center gap-1">                          {/* :23 */}
      <NotificationBell />
    </div>
  </div>
</header>
```

| 항목 | 값 | 비고 |
|---|---|---|
| 높이 | `h-(--header-height)` = **3rem = 48px** | `app/providers.tsx:88`에서 `calc(var(--spacing)*12)` |
| 축소 방지 | `shrink-0` | flex 부모에서 눌리지 않음 |
| 구분선 | `border-b` (하단 1px, `--border` 토큰) | 헤더 자체에 부여 |
| 외곽 gap | `gap-2` (헤더), 내부 래퍼는 `gap-1` → `lg:gap-2` | |
| 좌우 패딩 | `px-4` (1rem) → **`lg:px-6`** (1.5rem) | `page-content`와 동일한 패딩 리듬 |
| 트랜지션 | `transition-[width,height] ease-linear` | duration 미지정 |
| 사이드바 트리거 | `<SidebarTrigger className="-ml-1" />` — Button `variant="ghost" size="icon-sm"` = **`size-7`(28px)**, 아이콘 `PanelLeftIcon` | `sidebar.tsx:261-275`, size 정의 `components/ui/button.tsx:31` |
| 세로 구분선 | `mx-2`(0.5rem 좌우) + `h-4`(**16px**) + `self-center` | `Separator orientation="vertical"` |
| 타이틀 | `text-base font-medium leading-none` = 1rem / 500 / line-height 1 | `<h1>` |
| 우측 액션 | `ml-auto flex items-center gap-1` — 현재 `NotificationBell` 1개만 | 다중 액션 시 gap 0.25rem |

**타이틀 소스**: `pageTitle(pathname)` (`lib/page-meta.ts:24-31`) — `PAGE_META` 정확 매칭 우선 → 없으면 **최장 prefix 매칭** → 그래도 없으면 `"Lean - AX"` 폴백. `PAGE_META`는 19개 경로를 담고 사이드바 라벨과 동일 문자열을 쓴다 (`lib/page-meta.ts:3-21`). 주석 원문: `사이드바 navMain과 동일한 라벨을 단일 출처로 유지한다`.
표시 직전 `t()`로 로케일 변환된다 (`site-header.tsx:22`).

---

## 4. 콘텐츠 영역

### 4-1. 페이지 컨테이너 (`app/providers.tsx:93-107`)

```tsx
<SidebarInset>
  <SiteHeader />
  <div className="flex flex-1 flex-col">
    <div className="@container/main flex flex-1 flex-col gap-2">
      <div id="page-content" className={cn("flex flex-col gap-4 px-4 py-4 md:gap-6 md:py-6 lg:px-6")}>
        {children}
      </div>
    </div>
  </div>
</SidebarInset>
```

| 레이어 | 클래스 | 의미 |
|---|---|---|
| `SidebarInset` (`<main>`) | `relative flex w-full flex-1 flex-col bg-background md:peer-data-[variant=inset]:m-2 md:peer-data-[variant=inset]:ml-0 md:peer-data-[variant=inset]:rounded-2xl md:peer-data-[variant=inset]:shadow-sm md:peer-data-[variant=inset]:peer-data-[state=collapsed]:ml-2` (`sidebar.tsx:309`) | **md 이상**에서만 `m-2`(0.5rem) 여백 + `rounded-2xl` + `shadow-sm`. 왼쪽은 `ml-0`(사이드바에 붙임), 사이드바 접히면 `ml-2` 복구 |
| 중간 래퍼 | `flex flex-1 flex-col` | 구조용 |
| 컨테이너 쿼리 래퍼 | `@container/main flex flex-1 flex-col gap-2` | **`main`이라는 이름의 컨테이너 쿼리 컨텍스트** 등록. 하위에서 `@xl/main:` `@3xl/main:` `@5xl/main:` 사용 |
| `#page-content` | `flex flex-col gap-4 px-4 py-4 md:gap-6 md:py-6 lg:px-6` | 실제 페이지 패딩 |

**정확한 패딩 값**:

| 뷰포트 | 좌우 | 상하 | 자식 간 gap |
|---|---|---|---|
| 기본 (<768px) | `px-4` = **1rem** | `py-4` = **1rem** | `gap-4` = **1rem** |
| `md:` (≥768px) | `px-4` = 1rem | `py-6` = **1.5rem** | `gap-6` = **1.5rem** |
| `lg:` (≥1024px) | `px-6` = **1.5rem** | `py-6` = 1.5rem | `gap-6` = 1.5rem |

- **최대폭 제약 없음** — `max-w-*`가 `#page-content`에 없다. 콘텐츠는 화면 폭을 그대로 채운다.
- **섹션 간 gap은 별도로 주지 않는다.** 각 `page.tsx`는 `<>…</>` 프래그먼트로 형제 섹션을 나열하고, 간격은 부모 `#page-content`의 `gap-4 / md:gap-6`이 만든다 (`app/page.tsx:260-262`, tail 참조).
- `id="page-content"`는 스크롤/앵커 타깃으로 쓸 수 있는 유일한 고정 훅.

### 4-2. 대시보드(`app/page.tsx`) 관례

```tsx
// :260-267 — 페이지 첫 섹션: 부제 한 줄
<>
  <div>
    <p className="mt-1 text-sm text-muted-foreground">
      {t("{{OWNER_NAME}}님의 1인 기업 관제탑")} · {dayjs().format("YYYY-MM-DD")}
    </p>
  </div>

  {/* :269 — 스탯 5종 */}
  <div className="grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @3xl/main:grid-cols-3 @5xl/main:grid-cols-5">
```

- **상단 여백**: 페이지 제목을 다시 찍지 않는다(헤더가 담당). 첫 요소는 `mt-1`(0.25rem)만 준 설명 문단.
- **카드 그리드 gap**: `gap-4` (1rem) 고정.
- **2열 비대칭 섹션**: `<div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">` (`app/page.tsx:408`) — 좌 1.4 : 우 1 비율, `lg:`(≥1024px) 이상에서만 분할.
- 카드 그림자 관례: `shadow-xs`, 클릭 가능한 카드는 `cursor-pointer shadow-xs transition-shadow hover:shadow-md` (`app/page.tsx:276-277`, `:343`, `:409`, `:498`).

### 4-3. 스크롤 컨테이너 관례 — 페이지마다 다르다

| 페이지 | 높이 계산식 | 출처 |
|---|---|---|
| 메일 | `h-[calc(100svh-9rem)]` (`FULL_H` 상수) | `app/mail/page.tsx:64` |
| 지식망 | `flex h-[calc(100svh-7rem)] flex-col` (인라인) | `app/wiki/page.tsx:97` |
| 워크보드 | `flex h-[calc(100svh-7rem)] flex-col` (인라인) | `app/workboard/page.tsx:561` |
| 드라이브 | `flex min-h-[calc(100vh-3.5rem)]` (인라인, **`svh` 아닌 `vh`**) | `app/drive/page.tsx:360` |

> **불일치 주의**: 같은 셸을 쓰는데 차감값이 `9rem / 7rem / 3.5rem`으로 제각각이고, 드라이브만 `vh` 단위다. 상수로 추출된 것은 메일의 `FULL_H` 하나뿐이며 다른 페이지는 인라인이다. 신규 앱에서는 **하나로 통일**하는 것을 권한다.
> `FULL_H`의 `9rem` 근거는 코드 주석에 `SiteHeader(3rem) + 콘텐츠 py-6(상하 1.5rem씩)`로 적혀 있으나(`app/mail/page.tsx:63`), 그 합은 6rem이다. 나머지 3rem의 출처는 **미확인**(코드에 설명 없음).

`100svh`(small viewport height)를 쓰는 이유는 모바일 브라우저 주소창 접힘에 따른 점프 방지로 보이나, **코드에 근거 주석이 없어 의도는 미확인**.

---

## 5. 2패널(목록 + 상세) 문법 — 메일 페이지 기준

`app/mail/page.tsx:814-894` 원문 골격:

```tsx
<div className={`flex gap-4 ${FULL_H}`}>                                       {/* :814 */}
  {/* 목록 */}
  <div className="flex h-full w-2/5 min-w-[280px] max-w-md shrink-0 flex-col"> {/* :816 */}
    <div className={`h-full overflow-y-auto rounded-md border ${SLIM}`}>       {/* :817 */}
      <div className="divide-y"> …항목 버튼들… </div>                            {/* :832 */}
    </div>
  </div>

  {/* 상세 */}
  <div className="h-full min-w-0 flex-1">                                      {/* :875 */}
    {/* 빈 상태 */}
    <div className="flex h-full items-center justify-center rounded-md border text-sm text-muted-foreground"> {/* :877 */}
    {/* 본문 */}
    <div className="flex h-full flex-col rounded-md border">                   {/* :894 */}
      <div className="space-y-3 border-b p-4"> …헤더 블록… </div>                {/* :895 */}
      <div className={`min-h-0 flex-1 overflow-auto bg-muted/20 p-3 ${SLIM}`}> {/* :987 */}
      <div className="flex flex-wrap gap-2 border-t p-3"> …첨부… </div>          {/* :1006 */}
    </div>
  </div>
</div>
```

| 요소 | 값 | 출처 |
|---|---|---|
| 래퍼 | `flex gap-4` + `FULL_H` → 패널 사이 간격 **1rem** | `:814` |
| 좌측 목록 폭 | `w-2/5` (40%) · `min-w-[280px]` · `max-w-md` (**28rem = 448px**) · `shrink-0` | `:816` |
| 좌측 스크롤 박스 | `h-full overflow-y-auto rounded-md border` + `SLIM` | `:817` |
| 목록 항목 구분선 | `divide-y` (컨테이너에 부여) | `:832` |
| 우측 상세 | `h-full min-w-0 flex-1` — **`min-w-0` 필수** (긴 제목/URL의 flex 오버플로 방지) | `:875` |
| 상세 프레임 | `flex h-full flex-col rounded-md border` | `:894` |
| 상세 헤더 블록 | `space-y-3 border-b p-4` | `:895` |
| 상세 본문(스크롤) | `min-h-0 flex-1 overflow-auto bg-muted/20 p-3` + `SLIM` — **`min-h-0`이 flex 자식 스크롤의 핵심** | `:987` |
| 상세 푸터(첨부) | `flex flex-wrap gap-2 border-t p-3` | `:1006` |
| 라운드 | 두 패널 모두 `rounded-md` = `--radius-md` = `calc(0.625rem*0.8)` = **0.5rem** | |
| 보더 | 두 패널 모두 `border` (1px, `--border`) | |

상세 본문 안의 렌더 모드별 처리:
- 평문: `whitespace-pre-wrap break-words rounded-md border bg-background p-4 font-sans text-sm leading-relaxed` (`:989`)
- HTML(iframe): `h-full min-h-[400px] w-full border-0 bg-white` (`:997`)
- 첨부 칩: `flex items-center gap-2 rounded-md border bg-muted/40 px-2.5 py-1.5 text-xs transition-colors hover:bg-accent`, 파일명 `max-w-[180px] truncate font-medium` (`:1012, :1015`)

### 5-1. 2패널 위 툴바 행 (`app/mail/page.tsx:743-812`)

```tsx
<div className="flex flex-col gap-3">                            {/* :733 — 페이지 루트, 섹션 간 0.75rem */}
  <div className="flex items-center justify-between gap-3">      {/* :743 — 툴바 행 */}
    <Tabs><TabsList>…메일함 탭…</TabsList></Tabs>
    <div className="relative mx-2 hidden min-w-0 flex-1 sm:block">  {/* :764 — 검색, sm 미만 숨김 */}
      <Search className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground" />
      <Input className="h-9 pl-8" />
      <button className="absolute top-1/2 right-2 -translate-y-1/2 …" />   {/* 지우기 */}
    </div>
    <div className="flex items-center gap-2">…버튼 3개 (모두 h-9 py-2)…</div>  {/* :788 */}
  </div>
  <div className={`flex gap-4 ${FULL_H}`}> … </div>
</div>
```

- 페이지 루트가 `gap-3`(0.75rem)로 자체 리듬을 갖는다 — `#page-content`의 `gap-4/gap-6`과 별개.
- 툴바 버튼 높이는 전부 `h-9 py-2`로 통일 (`:793, :803, :808`) — Button 기본 `h-8`을 덮어쓴 것.
- 검색 입력 `h-9 pl-8`, 아이콘 `size-3.5`(14px)를 `left-2.5`(0.625rem)에 절대배치.
- 경고 배너 패턴: `flex items-center justify-between gap-3 rounded-md border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-sm text-amber-700 dark:text-amber-400` (`:735`).

---

## 6. 플로팅 / 오버레이

### 6-1. 챗 FAB (우하단 런처) — `components/chat-panel.tsx:259-273`

```tsx
"fixed bottom-5 right-5 z-40 flex size-12 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg ring-1 ring-foreground/10 transition-transform hover:scale-105 active:scale-95"
// 안 읽음 있을 때 추가:
totalUnread > 0 && "animate-pulse shadow-primary/60 ring-2 ring-primary/60"
```

| 항목 | 값 |
|---|---|
| 위치 | `fixed bottom-5 right-5` = 화면 하단·우측 **1.25rem(20px)** |
| z-index | `z-40` |
| 크기 | `size-12` = 3rem = **48px** 원형 |
| 색 | `bg-primary text-primary-foreground` |
| 그림자·링 | `shadow-lg` + `ring-1 ring-foreground/10` |
| 인터랙션 | `hover:scale-105` / `active:scale-95` (`transition-transform`) |
| 아이콘 | `MessageSquare className="size-5"` (20px) |
| 미확인 뱃지 | `absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1 text-[11px] font-bold text-white ring-2 ring-background`, 99 초과 시 `"99+"` (`:269-271`) |
| 렌더 조건 | `{!open && …}` — 패널이 열리면 FAB는 사라진다 (`:257`) |

### 6-2. 챗 패널 (우측 도킹 드로어) — `components/chat-panel.tsx:592-596`

```tsx
<div ref={panelRef}
  className="fixed bottom-0 right-0 top-0 z-40 flex flex-col border-l bg-background shadow-2xl"
  style={{ width }} />
```

| 항목 | 값 | 출처 |
|---|---|---|
| 위치 | `fixed bottom-0 right-0 top-0` — 우측 **전체 높이** 도킹 (플로팅 카드 아님) | `:594` |
| z-index | `z-40` (FAB와 동일) | `:594` |
| 폭 | 인라인 `style={{ width }}`, 기본 **720px** | `:352` `useState(720)` |
| 폭 범위 | `MIN_W = 560` / `MAX_W = 1000` (px) | `:70-71` |
| 좌측 리사이즈 핸들 | `absolute left-0 top-0 z-10 h-full w-1 cursor-ew-resize bg-transparent hover:bg-primary/30` | `:599-601` |
| 경계 | `border-l` + `shadow-2xl`, 배경 `bg-background` | `:594` |
| 내부 2단 | `flex min-h-0 flex-1` → 좌 목록 `flex shrink-0 flex-col border-r` (`style={{ width: listWidth }}`) + 우 스레드 | `:605-607` |
| 목록 폭 | 기본 **268px**, 범위 `LIST_MIN = 200` / `LIST_MAX = 440` | `:353`, `:72-73` |
| 폭 영속화 | localStorage `chat:width`, `chat:listWidth` | `:64-65`, `:376-378` |
| 팝아웃 창 | `window.open(…, "popup=yes,width=440,height=720")` | `:580-585` |
| 단축키 | `Shift+←` 열기 / `Shift+→` 닫기 / `Shift+/` 한↔영 토글 | `:94-106` |

> `MIN_W` 주석 원문: `2단(대화 목록 + 스레드)이 함께 들어갈 최소 너비` (`:70`).

### 6-3. 알림 벨 (`components/notification-bell.tsx`)

트리거 버튼 (`:113-134`): `Button variant="ghost" size="icon"` → **`size-8`(32px)** (`components/ui/button.tsx:29`), `className="relative ml-auto"`. 아이콘은 미확인 건이 있으면 `BellRing`, 없으면 `Bell` — 둘 다 `size-4`(16px).

뱃지 (`:127-133`):

```tsx
"absolute -top-0.5 -right-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-destructive px-1 text-[10px] font-semibold leading-none text-destructive-foreground"
```
- 오프셋 `-top-0.5 -right-0.5` (각 −0.125rem), 크기 `h-4 min-w-4` (**16px**), 글자 `text-[10px] font-semibold`, 9 초과 시 `"9+"`.
- 챗 FAB 뱃지(`h-5 min-w-5`, `text-[11px]`, `bg-red-500`)와 **크기·색 규칙이 다르다** — 통일되어 있지 않음.

팝오버 (`:137-143`):

```tsx
align="end"  sideOffset={8}
"z-50 w-80 origin-(--radix-popover-content-transform-origin) overflow-hidden rounded-2xl bg-popover p-0 text-popover-foreground shadow-lg ring-1 ring-foreground/5 duration-100 outline-none dark:ring-foreground/10"
"data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95"
```

| 항목 | 값 |
|---|---|
| 폭 | `w-80` = **20rem = 320px** |
| z-index | `z-50` (챗 `z-40`보다 위) |
| 라운드 | `rounded-2xl` = `--radius-2xl` = **1.125rem** |
| 링 | `ring-1 ring-foreground/5`, 다크 `ring-foreground/10` |
| 애니메이션 | fade + `zoom-95`, `duration-100` |
| 헤더 행 | `flex items-center justify-between border-b px-3 py-2` (`:145`) |
| 리스트 영역 | `max-h-96 overflow-y-auto` (**24rem = 384px**) (`:156`) |
| 항목 | `flex items-start gap-2.5 px-3 py-2.5 transition-colors hover:bg-muted`, 읽은 건 `opacity-60` (`:169-170`) |
| 폴링 | 60초 간격, `document.hidden`이면 스킵 (`:75-77`) |

### 6-4. 토스트 (sonner) — `components/ui/sonner.tsx`

```tsx
// app/providers.tsx:112 — TooltipProvider 바깥, Refine 안쪽에 1개
<Toaster />
```

- **`position` prop을 코드에서 지정하지 않는다** → sonner 라이브러리 기본 위치가 적용된다. 이 저장소 코드만으로는 최종 좌표를 확정할 수 없음 → **미확인**.
- 스타일은 CSS 변수 주입으로 테마를 따라간다 (`components/ui/sonner.tsx` style 블록):
  ```tsx
  "--normal-bg": "var(--popover)",
  "--normal-text": "var(--popover-foreground)",
  "--normal-border": "var(--border)",
  "--border-radius": "var(--radius)",
  ```
- `theme={theme}` — `next-themes`의 현재 테마 연동.
- `className="toaster group"`, `toastOptions.classNames.toast = "cn-toast cursor-pointer"`.
- 아이콘 5종을 lucide로 교체: success `CircleCheckIcon` / info `InfoIcon` / warning `TriangleAlertIcon` / error `OctagonXIcon` / loading `Loader2Icon animate-spin` — 전부 `size-4`.
- **커스텀 동작**: 토스트 본문 아무 곳이나 클릭하면 닫힘. sonner에 빌트인이 없어 `document`에 클릭 위임(`e.target.closest("[data-sonner-toast]")` → `toast.dismiss()`)으로 구현 (주석 원문: `Sonner는 클릭-닫힘 빌트인이 없어(타이머·스와이프·닫기버튼만) 문서 위임으로 처리(포털 안전)`).

### 6-5. z-index 정리표

| 레이어 | z | 출처 |
|---|---|---|
| 사이드바 컨테이너 | `z-10` | `sidebar.tsx:232` |
| 챗 패널 리사이즈 핸들 (패널 내부) | `z-10` | `chat-panel.tsx:601` |
| 사이드바 레일 | `z-20` | `sidebar.tsx:291` |
| 챗 FAB / 챗 패널 | `z-40` | `chat-panel.tsx:261, 594` |
| 알림 팝오버 | `z-50` | `notification-bell.tsx:141` |

---

## 7. 반응형 규칙

### 7-1. 브레이크포인트

Tailwind v4 기본 스케일을 쓰고 **커스텀 브레이크포인트 정의는 없다** (`app/globals.css`의 `@theme inline`에 `--breakpoint-*` 없음). 실제 사용 지점:

| 접두사 | 최소 폭 | 셸에서의 쓰임 |
|---|---|---|
| `sm:` | 640px | 메일 툴바 검색창 `hidden … sm:block` (`app/mail/page.tsx:764`) · 사이드바 레일 `sm:flex` (`sidebar.tsx:291`) |
| `md:` | 768px | **사이드바 표시/숨김의 경계** · `SidebarInset`의 `m-2/rounded-2xl/shadow-sm` · `#page-content`의 `md:gap-6 md:py-6` |
| `lg:` | 1024px | 헤더 `lg:gap-2 lg:px-6` · `#page-content` `lg:px-6` · 대시보드 2열 `lg:grid-cols-[1.4fr_1fr]` |

컨테이너 쿼리(`@container/main`)도 병행한다 — **뷰포트가 아니라 콘텐츠 영역 폭 기준**이라 사이드바 개폐에 반응한다:

| 접두사 | 쓰임 | 출처 |
|---|---|---|
| `@xl/main:grid-cols-2` | 스탯 그리드 2열 | `app/page.tsx:269`, `components/stat-card.tsx:108` |
| `@3xl/main:grid-cols-3` | 스탯 그리드 3열 | `app/page.tsx:269` |
| `@5xl/main:grid-cols-4` | `StatGrid` 기본 4열 | `components/stat-card.tsx:108` |
| `@5xl/main:grid-cols-5` | 대시보드 5열 | `app/page.tsx:269` |
| `@container/card` + `@[250px]/card:text-3xl` | 카드 폭에 따라 숫자 크기 확대 | `components/stat-card.tsx:47, 52` |

### 7-2. 모바일 사이드바 동작

판정 기준 (`hooks/use-mobile.ts`):

```ts
const MOBILE_BREAKPOINT = 768
// matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`) → 767px 이하 = 모바일
```

동작 분기 (`components/ui/sidebar.tsx:181-205`):

- **모바일(<768px)**: 사이드바가 `Sheet`(오버레이 드로어)로 렌더된다.
  ```tsx
  className="w-(--sidebar-width) bg-sidebar p-0 text-sidebar-foreground [&>button]:hidden"
  style={{ "--sidebar-width": SIDEBAR_WIDTH_MOBILE }}   // 18rem = 288px
  side="left"
  ```
  - 모바일에서만 폭이 **18rem(288px)** 로 재정의된다 (데스크톱 15rem보다 넓다).
  - `[&>button]:hidden` — Sheet 기본 닫기 버튼 숨김.
  - 상태는 별도 `openMobile` state로 관리되며 **쿠키에 저장되지 않는다** (`:69`).
  - 접근성용 숨김 헤더: `<SheetHeader className="sr-only">Sidebar / Displays the mobile sidebar.</SheetHeader>` (`:197-200`).
- **데스크톱(≥768px)**: `<div className="group peer hidden text-sidebar-foreground md:block">` — **`hidden` + `md:block`이라 768px 미만에서는 데스크톱 사이드바 DOM이 아예 표시되지 않는다** (`:209`). 내부 container도 `hidden … md:flex` (`:232`).
- 토글 함수가 뷰포트에 따라 갈린다 (`:91-93`):
  ```ts
  const toggleSidebar = () => isMobile ? setOpenMobile(o => !o) : setOpen(o => !o)
  ```
- `SidebarInset`의 인셋 스타일(`m-2 / ml-0 / rounded-2xl / shadow-sm`)도 전부 `md:` 접두사 → **모바일에서는 여백·라운드 없이 화면을 꽉 채운다** (`:309`).
- 툴팁은 `isMobile`이면 강제로 숨긴다 (`:536`).
- `NavUser` 드롭다운 방향이 바뀐다: `side={isMobile ? "bottom" : "right"}` (`components/nav-user.tsx:60`).

---

## 8. 공통 상수 정의 원문

### 8-1. `SIDEBAR_*` — `components/ui/sidebar.tsx:27-32`

```ts
const SIDEBAR_COOKIE_NAME = "sidebar_state"
const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 7     // 7일
const SIDEBAR_WIDTH = "16rem"                        // ← providers.tsx가 15rem으로 덮음
const SIDEBAR_WIDTH_MOBILE = "18rem"                 // 모바일 Sheet 전용
const SIDEBAR_WIDTH_ICON = "3rem"                    // offcanvas라 실사용 안 됨
const SIDEBAR_KEYBOARD_SHORTCUT = "b"                // Cmd/Ctrl + B
```

쓰임: `SidebarProvider` style 주입(`:134-135`), 쿠키 기록(`:85`), 모바일 Sheet style(`:192`), 키 핸들러(`:99`).

### 8-2. `SLIM` — 슬림 스크롤바 (메일)

```ts
// app/mail/page.tsx:59-61
// 가드레일(트랙/거터) 없이 테마색 슬라이더만 — 슬림하게.
const SLIM =
  "[scrollbar-width:thin] [scrollbar-color:var(--border)_transparent] [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar]:bg-transparent [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-border hover:[&::-webkit-scrollbar-thumb]:bg-muted-foreground/40";
```

- Firefox(`scrollbar-width/color`) + WebKit(`::-webkit-scrollbar`) 양쪽 커버. 스크롤바 폭 `w-1.5` = **0.375rem(6px)**, 썸은 `rounded-full bg-border`, hover 시 `bg-muted-foreground/40`.
- 쓰임 (`app/mail/page.tsx`): 좌측 목록 스크롤 박스 `:817`, 상세 본문 스크롤 `:987`, 작성 다이얼로그 에디터 `:1076`.

### 8-3. `SLIM_SCROLL` — 슬림 스크롤바 (대시보드), `SLIM`의 변종

```ts
// app/page.tsx:72-73
const SLIM_SCROLL =
  "[scrollbar-width:thin] [scrollbar-gutter:stable] [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-border [&::-webkit-scrollbar-track]:bg-transparent";
```

`SLIM`과의 차이: **`scrollbar-gutter:stable`을 추가**(스크롤바 등장 시 레이아웃 흔들림 방지)하고, `scrollbar-color`·`[&::-webkit-scrollbar]:bg-transparent`·hover 규칙은 **없다**. 즉 두 상수는 이름만 다른 게 아니라 실제 동작이 다르며, 공용 유틸로 추출되어 있지 않다.

### 8-4. `FULL_H` — 본문 가용 높이 (메일)

```ts
// app/mail/page.tsx:63-64
// 전역 프레임: SiteHeader(3rem) + 콘텐츠 py-6(상하 1.5rem씩) → 본문 가용 높이.
const FULL_H = "h-[calc(100svh-9rem)]";
```

쓰임: 2패널 래퍼 1곳 (`app/mail/page.tsx:814`). 다른 페이지는 이 상수를 import하지 않고 각자 인라인 값을 쓴다(§4-3 표 참조).

### 8-5. 챗 패널 치수 상수 — `components/chat-panel.tsx:63-73`

```ts
const GROUP: Room = { target: "@group", label: "전체", kind: "group" };
const WIDTH_KEY = "chat:width";
const LIST_WIDTH_KEY = "chat:listWidth";
const SEEN_KEY = "chat:lastSeen";
const LAST_VIEW_KEY = "chat:lastView";    // 마지막 화면(list|thread) — 재오픈·새로고침 시 복원
const LAST_ACTIVE_KEY = "chat:lastActive"; // 마지막으로 보던 방(target)
const PINNED_KEY = "chat:pinned";          // 상단 고정한 대화 target 순서(JSON 배열)
const MIN_W = 560;   // 2단(대화 목록 + 스레드)이 함께 들어갈 최소 너비
const MAX_W = 1000;
const LIST_MIN = 200; // 왼쪽 대화 목록 최소/최대 너비
const LIST_MAX = 440;
```

초기값 (`:352-353`):
```ts
const [width, setWidth] = useState(720);      // 2단(목록+스레드) 기본 너비
const [listWidth, setListWidth] = useState(268); // 왼쪽 대화 목록 너비(드래그 조절)
```

### 8-6. `MOBILE_BREAKPOINT` — `hooks/use-mobile.ts:3`

```ts
const MOBILE_BREAKPOINT = 768
```

### 8-7. 알림 상수 — `components/notification-bell.tsx:21`

```ts
const STORAGE_KEY = "notif:dismissed"   // 읽음 처리한 알림 id 배열(JSON)
```
폴링 주기 `60000`ms는 상수화되지 않고 인라인 (`:77`).

### 8-8. `StatCard` 톤 팔레트 — `components/stat-card.tsx:24-31`

```ts
// 상태별 칩 색 (주의=danger, 오늘=info, 예정=violet, 정상=success 등)
// lib/task-ui.ts statusBadgeClass와 동일한 서브틀 패턴 — 전 페이지 배지 일관성
const TONE_CLASS: Record<BadgeTone, string> = {
  neutral: "",
  danger: "border-red-500/30 bg-red-500/10 text-red-600 dark:text-red-400",
  warning: "border-amber-500/30 bg-amber-500/10 text-amber-600 dark:text-amber-500",
  info: "border-blue-500/30 bg-blue-500/10 text-blue-600 dark:text-blue-400",
  success: "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
  violet: "border-violet-500/30 bg-violet-500/10 text-violet-600 dark:text-violet-400",
};
```

공식: `border-{색}-500/30` + `bg-{색}-500/10` + `text-{색}-600` + `dark:text-{색}-400`(amber만 `dark:text-amber-500`).

`StatCard` / `StatGrid` 골격 (`components/stat-card.tsx:47, 108`):

```tsx
<Card className="@container/card h-full shadow-xs">
  <CardHeader>
    <CardDescription>{label}</CardDescription>
    <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">{value}</CardTitle>
    <CardAction><Badge variant="outline" className={TONE_CLASS[tone]} /></CardAction>
  </CardHeader>
  <CardFooter className="flex-col items-start gap-1.5 text-sm">
    <div className="line-clamp-1 flex gap-2 font-medium">{footerTitle}</div>
    <div className="text-muted-foreground">{footerSub}</div>
  </CardFooter>
</Card>

// StatGrid 기본 그리드
"grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @5xl/main:grid-cols-4"
```

- 숫자는 `tabular-nums`(고정폭 숫자) — 값이 바뀌어도 자릿수 흔들림 없음.
- `href`가 있으면 카드를 `<Link className="block transition-shadow hover:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">`로 감싼다 (`:87-89`).
- 주석 원문: `dashboard-01 SectionCards의 디자인 DNA를 박제한 재사용 지표 카드. 표면(그라데이션+그림자)을 카드에 직접 부여해 Link 래핑에도 깨지지 않음.` (`:43-44`)

> **주의**: 대시보드는 `StatGrid`를 쓰지 않고 그리드를 직접 인라인으로 쓴다 (`app/page.tsx:269`, 5열). `StatGrid`의 기본은 4열이다.

---

## 부록 A — 신규 앱 이식 체크리스트 (골격만)

1. `app/layout.tsx`: `Inter` + `variable:'--font-sans'`, `<html lang className={cn("font-sans", inter.variable)} suppressHydrationWarning>`.
2. `app/globals.css`: `@import "tailwindcss"` → `@theme inline`에 `--color-sidebar-*` 매핑 8개 + `--radius-*` 파생 7개. `--spacing`은 **재정의하지 말 것**(0.25rem 기본 유지해야 아래 계산식이 맞는다).
3. `SidebarProvider`에 반드시 두 변수 주입:
   ```tsx
   style={{ "--sidebar-width": "calc(var(--spacing) * 60)", "--header-height": "calc(var(--spacing) * 12)" }}
   ```
4. `<AppSidebar variant="inset" />` + `collapsible="offcanvas"`.
5. `SidebarInset` 안에 `SiteHeader` → `div.flex.flex-1.flex-col` → `div.@container/main.flex.flex-1.flex-col.gap-2` → `div#page-content.flex.flex-col.gap-4.px-4.py-4.md:gap-6.md:py-6.lg:px-6`.
6. 헤더: `h-(--header-height) shrink-0 border-b` + 내부 `px-4 lg:px-6`, `SidebarTrigger(-ml-1)` + `Separator(mx-2 h-4)` + `h1(text-base font-medium leading-none)` + `ml-auto` 액션.
7. `Toaster`는 Provider 트리 최상단 근처에 1개, `ChatProvider`가 FAB를 그리므로 셸 안쪽에 배치.
8. 2패널 페이지는 `flex gap-4 h-[calc(100svh-9rem)]` + 좌 `w-2/5 min-w-[280px] max-w-md shrink-0` + 우 `min-w-0 flex-1`.

## 부록 B — 미확인 · 불일치 목록

| 항목 | 상태 |
|---|---|
| sonner `Toaster` 최종 표시 위치 | **미확인** — 코드에 `position` 미지정, 라이브러리 기본값에 의존 (`app/providers.tsx:112`) |
| `FULL_H`의 `9rem` 중 나머지 `3rem`의 근거 | **미확인** — 주석이 설명하는 값(3rem + 1.5rem×2 = 6rem)과 실제 상수(9rem)가 불일치 (`app/mail/page.tsx:63-64`) |
| `100svh` 채택 사유 | **미확인** — 코드에 근거 주석 없음 |
| 스크롤 컨테이너 차감값 | **불일치** — 메일 `9rem` / 지식망·워크보드 `7rem` / 드라이브 `3.5rem`(+`vh` 단위). 공용 상수 없음 |
| `SLIM` vs `SLIM_SCROLL` | **불일치** — 두 파일에 각각 정의, `scrollbar-gutter`·hover 규칙이 다름 |
| 미확인 뱃지 규격 | **불일치** — 알림벨 `h-4 min-w-4 text-[10px] bg-destructive` vs 챗 FAB `h-5 min-w-5 text-[11px] bg-red-500` |
| `components/nav-documents.tsx` | **데드 코드** — export만 있고 저장소 내 호출부 없음 |
| `NavUser` 드롭다운 라벨 (Account/Billing/Notifications/Log out) | **i18n 미적용** — `t()` 미경유 하드코딩 (`components/nav-user.tsx:83-100`) |
| `--sidebar-width-icon` (3rem) 및 `group-data-[collapsible=icon]:*` 스타일 | **미사용 경로** — `collapsible="offcanvas"`라 아이콘 모드 진입 불가 |
