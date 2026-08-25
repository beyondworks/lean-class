# 04. 페이지 템플릿 — 유형별 뼈대·여백·타이포

원본 인트라넷(`<인트라넷 레포>`)의 실제 페이지 코드에서 추출한 재현용 템플릿.
**신규 기업용 앱에서 기능만 바꾸고 외형은 동일하게** 만들 때 이 문서의 스켈레톤을 복붙한다.

- 모든 클래스·수치는 **코드 원문**이며 각 항목에 `파일:라인` 출처를 단다.
- 추측·발명 값 없음. 확인 못 한 것은 "미확인"으로 표기.
- 스택: Next.js App Router + Tailwind v4 + shadcn/ui(radix) + refine v5 + lucide-react.

---

## 0. 전역 프레임 (모든 페이지 공통 전제)

페이지 컴포넌트는 **자기 패딩을 갖지 않는다.** 패딩·세로 리듬은 셸이 준다.

```tsx
// app/providers.tsx:84-108 (원문)
<SidebarProvider
  style={
    {
      "--sidebar-width": "calc(var(--spacing) * 60)",   // 15rem
      "--header-height": "calc(var(--spacing) * 12)",   // 3rem
    } as React.CSSProperties
  }
>
  <AppSidebar variant="inset" />
  <SidebarInset>
    <SiteHeader />
    <div className="flex flex-1 flex-col">
      <div className="@container/main flex flex-1 flex-col gap-2">
        <div
          id="page-content"
          className={cn(
            "flex flex-col gap-4 px-4 py-4 md:gap-6 md:py-6 lg:px-6"
          )}
        >
          {children}   {/* ← 여기에 page.tsx가 들어온다 */}
        </div>
      </div>
    </div>
  </SidebarInset>
</SidebarProvider>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 페이지 좌우 패딩 | `px-4` → `lg:px-6` | `app/providers.tsx:100` |
| 페이지 상하 패딩 | `py-4` → `md:py-6` | `app/providers.tsx:100` |
| 최상위 자식 간 간격 | `gap-4` → `md:gap-6` | `app/providers.tsx:100` |
| 사이드바 폭 | `15rem` (`spacing * 60`) | `app/providers.tsx:87` |
| 헤더 높이 | `3rem` (`spacing * 12`) | `app/providers.tsx:88` |
| 컨테이너 쿼리 이름 | `@container/main` | `app/providers.tsx:96` |

**페이지 타이틀(H1)은 페이지가 아니라 헤더바가 그린다.**

```tsx
// components/site-header.tsx:15-27 (원문)
<header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
  <div className="flex h-full w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
    <SidebarTrigger className="-ml-1" />
    <Separator
      orientation="vertical"
      className="mx-2 data-[orientation=vertical]:h-4 data-[orientation=vertical]:self-center"
    />
    <h1 className="text-base font-medium leading-none">{t(pageTitle(pathname))}</h1>
    <div className="ml-auto flex items-center gap-1">
      <NotificationBell />
    </div>
  </div>
</header>
```

→ **페이지 본문 최상단에는 H1을 쓰지 않는다.** 대신 설명 `<p>` 한 줄만 둔다(§ 타이포 계층).

### 루트 컨테이너 — 3가지 실사용 패턴 (일관되지 않음, 예외 표기)

| 패턴 | 쓰는 곳 | 출처 |
|---|---|---|
| 프래그먼트 `<>` (셸의 `gap-4/md:gap-6`에 위임) | 대시보드, 리포트 | `app/page.tsx:261`, `app/reports/page.tsx:190` |
| `<div className="space-y-4">` (가장 흔함) | 거래처·문서·회사정보·직원·업무·사용량 | `app/customers/page.tsx:339`, `app/documents/page.tsx:270`, `app/company/page.tsx:228`, `app/employees/page.tsx:99`, `app/tasks/page.tsx:999`, `app/usage/page.tsx:156` |
| `<div className="space-y-6">` | 설정 | `app/settings/page.tsx:57` |
| `<div className="flex flex-col gap-3">` | 메일 | `app/mail/page.tsx:733` |

> **예외**: 셸이 이미 `gap-4 md:gap-6`을 주므로 `space-y-4`는 중복 적용이다(실측상 더 큰 값이 이기지 않고 둘 다 적용됨 — 형제 간 간격은 셸 gap, 페이지 내부는 space-y). 신규 화면은 **`space-y-4` 패턴을 기본**으로 삼는 것이 코드베이스 다수결이다.

---

## 유형 1. 대시보드형

**대표**: `app/page.tsx` (555줄) + `components/stat-card.tsx`
**구성**: 설명 한 줄 → 스탯 5종 그리드 → 카드형 표 → 차트 → 카드형 표 → 2분할 카드

### 1-1. 뼈대 스켈레톤

```tsx
export default function Dashboard() {
  return (
    <>
      {/* ① 페이지 설명 — H1은 헤더바가 그리므로 p만 */}
      <div>
        <p className="mt-1 text-sm text-muted-foreground">
          {t("{{OWNER_NAME}}님의 1인 기업 관제탑")} · {dayjs().format("YYYY-MM-DD")}
        </p>
      </div>

      {/* ② 스탯 그리드 — 1 → 2 → 3 → 5열 (컨테이너 쿼리) */}
      <div className="grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @3xl/main:grid-cols-3 @5xl/main:grid-cols-5">
        {stats.map((s, i) => (
          <StatCard key={i} stat={s} />
        ))}
      </div>

      {/* ③ 카드 = 섹션. 헤더(제목+우측 링크) + 본문(표 or 빈 상태) */}
      <Card className="shadow-xs">
        <CardHeader>
          <CardTitle className="text-sm font-medium">{t("다가올 업무")}</CardTitle>
          <CardAction>
            <Link href="/tasks" className="text-xs text-muted-foreground hover:underline">
              {t("업무 보드")}
            </Link>
          </CardAction>
        </CardHeader>
        <CardContent>
          {upcoming.length === 0 ? (
            <p className="py-6 text-center text-sm text-muted-foreground">{t("다가올 업무 없음")}</p>
          ) : (
            <Table>{/* … */}</Table>
          )}
        </CardContent>
      </Card>

      {/* ④ 차트 카드 */}
      <ChartTokens data={tokensDaily} />

      {/* ⑤ 2분할 — 좌측이 넓은 비대칭 (1.4 : 1) */}
      <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <Card className="shadow-xs">{/* 활동 피드 */}</Card>
        <Card className="shadow-xs">{/* 브리핑 */}</Card>
      </div>
    </>
  );
}
```

출처: `app/page.tsx:260-273`(①②), `:343-405`(③), `:340`(④), `:408-542`(⑤)

### 1-2. 여백·크기

| 항목 | 값 | 출처 |
|---|---|---|
| 스탯 그리드 | `grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @3xl/main:grid-cols-3 @5xl/main:grid-cols-5` | `app/page.tsx:269` |
| 스탯 그리드(공용 기본) | `grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @5xl/main:grid-cols-4` | `components/stat-card.tsx:108` |

#### 1-2a. 스탯 카드 개수별 그리드 열 수 (실사용 전수)

`StatGrid`의 기본 클래스는 **4개용**이다. 개수가 다르면 `className`으로 덮거나 그리드를 직접 쓴다. 앱 전수:

| 카드 수 | 실제 코드 | 페이지 | 출처 |
|---|---|---|---|
| **3개** | `<StatGrid stats={stats} className="grid-cols-1 @xl/main:grid-cols-3" />` | 사용량 | `app/usage/page.tsx:164` |
| **3개** | `<StatGrid stats={stats} className="@xl/main:grid-cols-3" />` | 에이전트 | `app/agents/page.tsx:509` |
| 3개 | `<StatGrid stats={stats} />` (기본 = 4열 그리드에 3장) | 도구·브리핑·자동화 | `app/tools/page.tsx:271`, `app/briefings/page.tsx:94`, `app/automation/page.tsx:223` |
| **4개** | `<StatGrid stats={stats} />` (오버라이드 없음) | 업무 | `app/tasks/page.tsx:1006` |
| **5개** | `<div className="grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @3xl/main:grid-cols-3 @5xl/main:grid-cols-5">` — `StatGrid`를 쓰지 않고 직접 | 대시보드 | `app/page.tsx:269` |

**정본**
- **4개** → `<StatGrid stats={stats} />` 그대로. 오버라이드 금지.
- **3개** → `<StatGrid stats={stats} className="grid-cols-1 @xl/main:grid-cols-3" />`.
  코드 현황은 3열 오버라이드 2곳 / 기본 유지 3곳으로 갈리지만, 오버라이드 쪽에 **의도 주석이 달려 있어** 이를 정본으로 삼는다:
  > `{/* #8: 아래 섹션 카드와 열 수를 맞춤 — stats가 3개이므로 3열 고정 */}` (`app/usage/page.tsx:163`)

  두 오버라이드의 차이는 `grid-cols-1` 재선언 유무뿐이다(기본 클래스에 이미 `grid-cols-1`이 있어 **렌더 결과 동일**). 명시형(`usage`)을 정본으로 쓴다.
- **5개** → `StatGrid`로 표현할 수 없다(`@3xl` 3열 중간 단계가 필요). 대시보드 원문 그리드를 복사한다.
- 열 수 브레이크포인트는 전부 **컨테이너 쿼리(`@xl/main` 등)** — 뷰포트 `md:`/`lg:`가 아니다. 셸의 `@container/main` 배선이 전제다(§ 0).
| 2분할 비대칭 | `grid gap-4 lg:grid-cols-[1.4fr_1fr]` | `app/page.tsx:408` |
| 카드 내부 패딩 | `--card-spacing: --spacing(5)` = **20px** (상하 `py-`, 좌우 `px-`) | `components/ui/card.tsx:15` |
| 카드 `size="sm"` 시 | `--card-spacing: --spacing(4)` = **16px** | `components/ui/card.tsx:15` |
| 카드 라운드 | `rounded-[min(var(--radius-4xl),24px)]` | `components/ui/card.tsx:15` |
| 카드 표면 | `bg-card text-sm text-card-foreground shadow-sm ring-1 ring-foreground/5 dark:ring-foreground/10` | `components/ui/card.tsx:15` |
| 카드 그림자(페이지에서 덧입힘) | `shadow-xs` | 전 페이지 공통 (`app/page.tsx:343`, `app/settings/page.tsx:65`, `app/usage/page.tsx:184` 등) |
| CardHeader 그리드 | `grid auto-rows-min items-start gap-1.5 px-(--card-spacing)` | `components/ui/card.tsx:28` |
| CardAction 위치 | `col-start-2 row-span-2 row-start-1 self-start justify-self-end` | `components/ui/card.tsx:61` |
| 활동 행 높이 | `py-2.5 first:pt-0`, 아바타 `size-7` | `app/page.tsx:436-437` |
| 접기/더보기 버튼 | `mt-2 w-full rounded-md py-1.5 text-center text-xs` | `app/page.tsx:488`, `:530` |

### 1-3. StatCard 원문 (그대로 이식 가능)

```tsx
// components/stat-card.tsx:45-96 (원문)
export function StatCard({ stat }: { stat: Stat }) {
  const card = (
    <Card className="@container/card h-full shadow-xs">
      <CardHeader>
        <CardDescription>{stat.label}</CardDescription>
        <CardTitle
          className={cn(
            "text-2xl font-semibold tabular-nums @[250px]/card:text-3xl",
            stat.danger && "text-destructive"
          )}
        >
          {stat.value}
        </CardTitle>
        {stat.badge && (
          <CardAction>
            <Badge
              variant="outline"
              className={cn(TONE_CLASS[stat.badge.tone ?? "neutral"])}
            >
              {stat.badge.icon}
              {stat.badge.text}
            </Badge>
          </CardAction>
        )}
      </CardHeader>
      {(stat.footerTitle || stat.footerSub) && (
        <CardFooter className="flex-col items-start gap-1.5 text-sm">
          {stat.footerTitle && (
            <div className="line-clamp-1 flex gap-2 font-medium">
              {stat.footerTitle}
            </div>
          )}
          {stat.footerSub && (
            <div className="text-muted-foreground">{stat.footerSub}</div>
          )}
        </CardFooter>
      )}
    </Card>
  );

  if (stat.href) {
    return (
      <Link
        href={stat.href}
        className="block transition-shadow hover:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        {card}
      </Link>
    );
  }
  return card;
}
```

숫자 옆 단위는 **한 단계 작은 muted span**으로 붙인다:

```tsx
// app/page.tsx:200-205 (원문)
value: (
  <>
    {doneRate}
    <span className="text-lg text-muted-foreground">%</span>
  </>
),
```

### 1-4. 타이포 계층 (대시보드)

| 역할 | 클래스 | 출처 |
|---|---|---|
| 페이지 타이틀(H1, 헤더바) | `text-base font-medium leading-none` | `components/site-header.tsx:22` |
| 페이지 설명 | `mt-1 text-sm text-muted-foreground` | `app/page.tsx:263` |
| 섹션 제목(CardTitle) | `text-sm font-medium` | `app/page.tsx:345`, `:500` |
| 아이콘 동반 섹션 제목 | `flex items-center gap-1.5 text-sm font-medium` + `<Icon className="size-4 text-muted-foreground" />` | `app/page.tsx:281-282`, `:411-412` |
| 스탯 수치 | `text-2xl font-semibold tabular-nums @[250px]/card:text-3xl` | `components/stat-card.tsx:52` |
| 스탯 라벨 | CardDescription = `text-sm text-muted-foreground` | `components/ui/card.tsx:50` |
| 본문 | `text-sm` (Card 기본이 `text-sm`) | `components/ui/card.tsx:15` |
| 목록 요약문 | `text-[13px] leading-snug` | `app/page.tsx:473` |
| 보조텍스트 | `text-xs text-muted-foreground` | `app/page.tsx:288` |
| 미세 텍스트(타임스탬프·원문) | `text-[11px] text-muted-foreground` | `app/page.tsx:442`, `:475`, `:478` |

### 1-5. 상태 화면

```tsx
{/* 빈 상태 — 카드 본문 인라인 */}
<p className="py-6 text-center text-sm text-muted-foreground">
  {t("오늘 처리할 업무가 없습니다")}
</p>
```
출처: `app/page.tsx:295-297`, `:354`, `:422`, `:536-538`

로딩·에러 전용 화면은 대시보드에 **없다**(refine `useList`가 비었으면 빈 상태로 수렴). 각 fetch는 `.catch(() => {})`로 조용히 실패한다 — `app/page.tsx:129-154`.

---

## 유형 2. 2패널형 (목록 + 상세)

**대표**: `app/mail/page.tsx` (1231줄)
**구성**: 경고 배너 → 툴바(탭 + 검색 + 우측 액션) → `[목록 2/5 | 상세 3/5]` 고정 높이 분할

### 2-1. 뼈대 스켈레톤

```tsx
// 전역 프레임: SiteHeader(3rem) + 콘텐츠 py-6(상하 1.5rem씩) → 본문 가용 높이.
const FULL_H = "h-[calc(100svh-9rem)]";           // app/mail/page.tsx:64

return (
  <div className="flex flex-col gap-3">
    {/* ① (조건부) 경고 배너 */}
    {needsReconnect && (
      <div className="flex items-center justify-between gap-3 rounded-md border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-sm text-amber-700 dark:text-amber-400">
        <span>{t("Gmail 토큰이 만료되어 동기화가 막혔습니다. 재연결이 필요합니다.")}</span>
        <Button asChild size="sm" className="h-8 shrink-0">
          <a href="/api/auth/google/start">{t("재연결")}</a>
        </Button>
      </div>
    )}

    {/* ② 툴바 — 좌: 탭 / 중: 검색(가변) / 우: 액션 */}
    <div className="flex items-center justify-between gap-3">
      <Tabs value={box} onValueChange={…}>
        <TabsList>
          {BOXES.map((b) => (
            <TabsTrigger key={b.key} value={b.key}>{b.label}</TabsTrigger>
          ))}
        </TabsList>
      </Tabs>

      <div className="relative mx-2 hidden min-w-0 flex-1 sm:block">
        <Search className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground" />
        <Input … placeholder={t("메일 검색 (Enter)")} className="h-9 pl-8" />
        {query && (
          <button
            type="button"
            className="absolute top-1/2 right-2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            aria-label={t("검색 지우기")}
          >
            <X className="size-3.5" />
          </button>
        )}
      </div>

      <div className="flex items-center gap-2">
        <Button variant="outline" className="h-9 py-2">…</Button>
        <Button variant="outline" className="h-9 py-2">…</Button>
        <Button className="h-9 py-2">…</Button>
      </div>
    </div>

    {/* ③ 2분할 본문 — 고정 높이, 각 패널이 독립 스크롤 */}
    <div className={`flex gap-4 ${FULL_H}`}>
      {/* 좌: 목록 — 2/5 폭, 최소 280px, 최대 max-w-md */}
      <div className="flex h-full w-2/5 min-w-[280px] max-w-md shrink-0 flex-col">
        <div className={`h-full overflow-y-auto rounded-md border ${SLIM}`}>
          <div className="divide-y">{/* 행들 */}</div>
        </div>
      </div>

      {/* 우: 상세 — 남는 폭 전부 */}
      <div className="h-full min-w-0 flex-1">
        {/* 미선택 / 에러 / 로딩 / 본문 4분기 */}
      </div>
    </div>
  </div>
);
```

출처: `app/mail/page.tsx:732-875`

### 2-2. 여백·크기

| 항목 | 값 | 출처 |
|---|---|---|
| 루트 세로 간격 | `flex flex-col gap-3` | `app/mail/page.tsx:733` |
| 툴바 | `flex items-center justify-between gap-3` | `:743` |
| 검색창 컨테이너 | `relative mx-2 hidden min-w-0 flex-1 sm:block` | `:764` |
| 검색 아이콘 | `pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground` | `:763` |
| 검색 입력 | `h-9 pl-8` | `:771` |
| 우측 액션 그룹 | `flex items-center gap-2`, 버튼마다 `h-9 py-2` | `:789-810` |
| 본문 높이 | `h-[calc(100svh-9rem)]` | `:64`, `:814` |
| 패널 간격 | `gap-4` | `:814` |
| 목록 패널 폭 | `w-2/5 min-w-[280px] max-w-md shrink-0` | `:816` |
| 상세 패널 | `min-w-0 flex-1` | `:875` |
| 패널 테두리 | `rounded-md border` | `:817`, `:894` |
| 목록 행 패딩 | `px-3 py-2.5` | `:828` |
| 목록 행 gap | `gap-2.5` | `:828` |
| 상세 헤더 | `space-y-3 border-b p-4` | `:895` |
| 상세 본문 | `min-h-0 flex-1 overflow-auto bg-muted/20 p-3` | `:987` |
| 상세 액션 버튼 | `h-8` (`size="sm"`) | `:934`, `:952`, `:955` |

### 2-3. 목록 행 원문 (아바타 + 2줄 + 타임스탬프)

```tsx
// app/mail/page.tsx:825-867 (원문)
<button
  key={m.id}
  onClick={() => openMessage(m.id)}
  className={`relative flex w-full gap-2.5 px-3 py-2.5 text-left transition-colors hover:bg-accent ${
    selId === m.id ? "bg-accent" : m.unread ? "bg-primary/[0.045]" : ""
  }`}
>
  <span className="relative shrink-0">
    <Avatar name={m.from_name} email={m.from_email} size={9} />
    {m.unread ? (
      <span className="absolute -bottom-0.5 -right-0.5 size-2.5 rounded-full border-2 border-background bg-primary" aria-hidden />
    ) : null}
  </span>
  <div className={`flex min-w-0 flex-1 flex-col gap-0.5 ${m.unread ? "" : "opacity-70"}`}>
    <div className="flex items-center justify-between gap-2">
      <span className="flex min-w-0 items-center gap-1.5">
        <span className={`truncate text-sm ${m.unread ? "font-semibold text-foreground" : "font-normal text-muted-foreground"}`}>
          {m.from_name || m.from_email}
        </span>
      </span>
      <span className="flex shrink-0 items-center gap-1.5">
        <span
          role="button"
          tabIndex={-1}
          onClick={(e) => toggleStarMsg(m.id, e)}
          className="text-muted-foreground/40 transition-colors hover:text-amber-400"
          aria-label={t("별표")}
        >
          <Star className={`size-3.5 ${isStarred(m.label_ids) ? "fill-amber-400 text-amber-400" : ""}`} />
        </span>
        <span className="text-[11px] text-muted-foreground">
          {m.internal_date ? formatKST(m.internal_date) : ""}
        </span>
      </span>
    </div>
    <span className={`truncate text-[13px] ${m.unread ? "font-medium" : "text-muted-foreground"}`}>
      {m.subject || t("(제목 없음)")}
    </span>
    <span className="truncate text-xs text-muted-foreground">{m.snippet}</span>
  </div>
</button>
```

**3줄 위계**: `text-sm`(발신자, 미읽음=semibold) → `text-[13px]`(제목) → `text-xs text-muted-foreground`(스니펫). 타임스탬프는 `text-[11px]`.

### 2-4. 상태 화면 4분기 (2패널형의 핵심)

```tsx
// app/mail/page.tsx:876-893 (원문)
{!selId ? (
  /* 미선택 */
  <div className="flex h-full items-center justify-center rounded-md border text-sm text-muted-foreground">
    <span className="flex items-center gap-2">
      <Mail className="size-4" /> {t("왼쪽에서 메일을 선택하세요")}
    </span>
  </div>
) : fullError && !loadingFull ? (
  /* 에러 + 재시도 */
  <div className="flex h-full flex-col items-center justify-center gap-3 rounded-md border text-sm text-muted-foreground">
    <span>{t("메일을 불러오지 못했습니다")}</span>
    <Button variant="outline" size="sm" onClick={() => selId && openMessage(selId)}>
      <RefreshCw className="size-3.5" /> {t("다시 시도")}
    </Button>
  </div>
) : loadingFull || !full ? (
  /* 로딩 */
  <div className="flex h-full items-center justify-center rounded-md border text-sm text-muted-foreground">
    {t("불러오는 중…")}
  </div>
) : (
  /* 본문 */
  <div className="flex h-full flex-col rounded-md border">…</div>
)}
```

목록 쪽 빈 상태 (로딩 문구를 겸함):

```tsx
// app/mail/page.tsx:818-821 (원문)
<p className="py-12 text-center text-sm text-muted-foreground">
  {syncing ? t("동기화 중…") : t("메일 없음")}
</p>
```

미연결(선행 조건 미충족) 화면 — 페이지 전체를 대체:

```tsx
// app/mail/page.tsx:718-730 (원문)
<Card className="shadow-xs">
  <CardContent className="flex flex-col items-center gap-3 py-12 text-center">
    <Plug className="size-6 text-muted-foreground" />
    <p className="text-sm text-muted-foreground">{t("Google 계정이 연결되지 않았습니다.")}</p>
    <Button asChild className="h-9 py-2">
      <Link href="/settings">{t("설정에서 연결")}</Link>
    </Button>
  </CardContent>
</Card>
```

### 2-5. 슬림 스크롤바 (2패널 필수)

```tsx
// app/mail/page.tsx:60-61 (원문)
const SLIM =
  "[scrollbar-width:thin] [scrollbar-color:var(--border)_transparent] [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar]:bg-transparent [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-border hover:[&::-webkit-scrollbar-thumb]:bg-muted-foreground/40";
```

대시보드에도 이름만 다른 변형이 있다(`SLIM_SCROLL`, `app/page.tsx:72-73`) — `scrollbar-gutter:stable`가 추가되고 `scrollbar-color`/hover 규칙이 없다. **예외(두 정의가 통일되지 않음)**.

---

## 유형 3. 목록/테이블형

**대표**: `app/customers/page.tsx`, `app/documents/page.tsx`, `app/employees/page.tsx`
**구성**: 설명+우측 액션 → (선택) 부가 위젯 → (선택) 검색 → 일괄바 → `py-0` 카드 안의 풀블리드 표

### 3-1. 뼈대 스켈레톤

```tsx
return (
  <div className="space-y-4">
    {/* ① 헤더: 좌 설명 / 우 액션 그룹 */}
    <div className="flex items-center justify-between">
      <div>
        <p className="mt-1 text-sm text-muted-foreground">
          {t("Notion 거래처 DB · 고객·협력사·공급사 아카이브")}
        </p>
      </div>
      <div className="flex gap-2">
        <Button variant="outline" onClick={() => load(true)} disabled={syncing} className="h-9 py-2">
          <RefreshCw className={`size-3.5 ${syncing ? "animate-spin" : ""}`} /> {t("새로고침")}
        </Button>
        <Button onClick={openCreate} className="h-9 py-2">
          <Plus className="size-3.5" /> {t("거래처 추가")}
        </Button>
      </div>
    </div>

    {/* ② 일괄 선택 플로팅 바 (선택 시에만) */}
    {bulk.count > 0 && (
      <BulkActionBar
        total={customers.length}
        count={bulk.count}
        allSelected={bulk.allSelected(customers.map((c) => c.id))}
        onToggleAll={() => bulk.toggleAll(customers.map((c) => c.id))}
        onDelete={bulkDelete}
        noun="거래처"
      />
    )}

    {/* ③ 표 카드 — py-0 + CardContent p-0 로 표를 카드 가장자리까지 */}
    <Card className="shadow-xs py-0">
      <CardContent className="p-0">
        {customers.length === 0 ? (
          <div className="flex flex-col items-center gap-3 py-12 text-center">
            <Building2 className="size-6 text-muted-foreground" />
            <p className="text-sm text-muted-foreground">
              {syncing ? t("동기화 중...") : t("등록된 거래처가 없습니다")}
            </p>
          </div>
        ) : (
          <Table className="[&_:is(th,td)]:px-4">
            <TableHeader>
              <TableRow>
                <TableHead className="w-10">
                  <Checkbox checked={…} onCheckedChange={…} aria-label={t("전체 선택")} />
                </TableHead>
                <TableHead>{t("회사명")}</TableHead>
                <TableHead>{t("담당자")}</TableHead>
                <TableHead className="text-center">{t("상태")}</TableHead>
                <TableHead className="w-20" />{/* 행 액션 */}
              </TableRow>
            </TableHeader>
            <TableBody>
              {customers.map((c) => (
                <TableRow key={c.id} className="cursor-pointer" onClick={() => openEdit(c)}>
                  <TableCell onClick={(e) => e.stopPropagation()}>
                    <Checkbox checked={bulk.has(c.id)} onCheckedChange={() => bulk.toggle(c.id)} />
                  </TableCell>
                  <TableCell className="font-medium">{c.company}</TableCell>
                  <TableCell className="text-muted-foreground">{c.manager ?? "-"}</TableCell>
                  <TableCell className="text-center">
                    {c.status ? (
                      <Badge variant="outline" className={STATUS_VARIANT[c.status] ?? ""}>{t(c.status)}</Badge>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell onClick={(e) => e.stopPropagation()}>
                    <div className="flex items-center gap-1">
                      <Button variant="ghost" size="icon" className="size-7" onClick={() => openEdit(c)}>
                        <Pencil className="size-3.5" />
                      </Button>
                      <Button variant="ghost" size="icon" className="size-7 text-destructive hover:text-destructive" onClick={() => setDeleteTarget(c)}>
                        <Trash2 className="size-3.5" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  </div>
);
```

출처: `app/customers/page.tsx:338-464`

> **스켈레톤 1곳은 정본을 반영했다(원문과 다름)** — 설명 `<p>`의 `mt-1`.
> 거래처 원문(`app/customers/page.tsx:342`)에는 `mt`가 없으나, 앱 전수 조사 결과 **정본은 `mt-1`**(8:4 다수결, § 8-6a)이라 스켈레톤에는 `mt-1`을 넣었다. 나머지 값은 전부 원문 그대로다.

### 3-2. 여백·크기

| 항목 | 값 | 출처 |
|---|---|---|
| 표 카드 | `shadow-xs py-0` + `<CardContent className="p-0">` | `app/customers/page.tsx:367-368`, `app/documents/page.tsx:358-359`, `app/tasks/page.tsx:1063-1064` |
| 표 셀 좌우 패딩 오버라이드 | `[&_:is(th,td)]:px-4` | `app/customers/page.tsx:377`, `app/documents/page.tsx:374`, `app/tasks/page.tsx:919`, `:1065` |
| TableHead 기본 | `h-10 px-2 text-left align-middle font-medium whitespace-nowrap` | `components/ui/table.tsx:73` |
| TableCell 기본 | `p-2 align-middle whitespace-nowrap` | `components/ui/table.tsx:86` |
| TableRow 기본 | `border-b transition-colors hover:bg-muted/50 has-aria-expanded:bg-muted/50 data-[state=selected]:bg-muted` | `components/ui/table.tsx:60` |
| 체크박스 컬럼 폭 | `w-10` | `app/customers/page.tsx:380`, `app/documents/page.tsx:377` |
| 행 액션 컬럼 폭 | `w-20` (거래처) / `w-24` (문서) | `app/customers/page.tsx:393`, `app/documents/page.tsx:390` |
| 행 액션 아이콘 버튼 | `variant="ghost" size="icon" className="size-7"` | `app/customers/page.tsx:441-443` |
| 헤더 액션 버튼 | `className="h-9 py-2"` | `app/customers/page.tsx:347`, `:350` |
| 액션 그룹 간격 | `flex gap-2` | `app/customers/page.tsx:346` |

**대시보드의 표는 다르다** — `[&_:is(th,td)]:px-4` 없이 기본 `p-2`를 쓰고 컬럼 폭을 직접 준다:
`<TableHead className="w-36 text-center">` (`app/page.tsx:303`), `w-32`/`w-28`/`w-20` (`:361-363`).

#### 3-2a. 셀 정렬 관례 — 좌(기본) · 중앙 · 우측

`TableHead` 기본이 `text-left`(`components/ui/table.tsx:73`)라 **좌측은 클래스를 붙이지 않는다.** 나머지 둘만 명시한다.

| 정렬 | 클래스 원문 | 쓰는 데이터 | 출처 |
|---|---|---|---|
| 좌 (기본) | 없음 | 이름·제목·담당자·이메일 등 텍스트 | `app/customers/page.tsx:386-390` |
| 중앙 | `className="text-center"` | 배지 컬럼(분류·상태) | `app/customers/page.tsx:391-392`, `app/page.tsx:303` |
| **우측** | `className="text-right"` — **`TableHead`와 `TableCell` 양쪽에 똑같이 붙인다** | 수치(호출 수·금액·크기) | `app/usage/page.tsx:197`·`:209`, `:312`·`:326` |

```tsx
// app/usage/page.tsx:197, 209 (원문) — 헤더와 셀이 짝
<TableHead className="text-right">{t("호출 수")}</TableHead>
...
<TableCell className="text-right">{fmt(r.total)}</TableCell>
```

- **한쪽만 붙이면 헤더와 값이 어긋난다.** 반드시 짝으로.
- 수치 컬럼은 `tabular-nums`와 함께 쓰는 것이 규칙(§ 8-6). 표 밖 그리드형 금액 셀 원문:
  `<div className="col-span-1 text-right text-sm pt-2 tabular-nums">` (`app/quote-contract/page.tsx:43`)
- 표가 아닌 flex 목록 행에서 우측 정렬 메타를 붙일 때는 **고정폭 + `shrink-0`**를 함께 준다:
  `<span className="hidden w-16 shrink-0 text-right text-xs text-muted-foreground md:block">` (`app/drive/page.tsx:643`),
  `w-32`(수정일, `:646`).

### 3-3. 목록형 변형 — 표 대신 `divide-y` 행 (직원 페이지)

```tsx
// app/employees/page.tsx:135-167 (원문 발췌)
<Card className="shadow-xs py-0">
  <CardContent className="py-1">
    {employees.length === 0 ? (
      <p className="py-8 text-center text-sm text-muted-foreground">
        {t("등록된 직원이 없습니다. 위에서 추가하세요.")}
      </p>
    ) : (
      <div className="divide-y">
        {/* 일괄 선택 헤더 행 */}
        <div className="flex items-center gap-3 py-2">…</div>
        {/* 데이터 행 */}
        <div key={e.id} className="flex items-center gap-3 py-3">…</div>
      </div>
    )}
  </CardContent>
</Card>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 카드 | `shadow-xs py-0` + `<CardContent className="py-1">` | `app/employees/page.tsx:135-136` |
| 헤더 행 높이 | `py-2` | `:144` |
| 데이터 행 높이 | `py-3` | `:167` |
| 행 gap | `gap-3` | `:144`, `:167` |
| 빈 상태 | `py-8 text-center text-sm text-muted-foreground` | `:138` |

회사정보 페이지는 **테두리 있는 그룹 리스트** 변형:
```tsx
// app/company/page.tsx:286-290 (원문)
<div className="divide-y divide-border rounded-md border">
  <div className="flex items-center gap-2.5 px-3 py-2.5 cursor-pointer hover:bg-muted/50 transition-colors" …>
```

### 3-4. 검색창 (목록 페이지)

```tsx
// app/documents/page.tsx:336-344 (원문)
<div className="relative max-w-sm">
  <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 size-3.5 text-muted-foreground" />
  <Input
    className="pl-8 h-9"
    placeholder={t("제목·파일명·본문 검색...")}
    value={searchInput}
    onChange={(e) => setSearchInput(e.target.value)}
  />
</div>
```

메일 툴바 검색과 값은 같고(`size-3.5`, `left-2.5`, `h-9 pl-8`) 폭 제약만 다르다(`max-w-sm` vs `flex-1`).

### 3-5. 드롭존 (문서 업로드)

```tsx
// app/documents/page.tsx:311-333 (원문)
<div
  onDragOver={handleDragOver}
  onDragLeave={handleDragLeave}
  onDrop={handleDrop}
  onClick={() => !uploading && fileInputRef.current?.click()}
  className={[
    "flex flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed px-6 py-8 text-center transition-colors cursor-pointer select-none",
    isDragOver
      ? "border-primary bg-primary/5 text-primary"
      : "border-muted-foreground/25 hover:border-muted-foreground/50 text-muted-foreground",
    uploading ? "pointer-events-none opacity-60" : "",
  ]
    .filter(Boolean)
    .join(" ")}
>
  <Upload className="size-5" />
  <p className="text-sm font-medium">{t("파일을 끌어다 놓거나 클릭해서 선택")}</p>
  <p className="text-xs">{t("PDF, 이미지, 문서 · 최대 20MB · 다중 선택 가능")}</p>
</div>
```

### 3-6. 상태 화면 (목록형)

| 상태 | 마크업 | 출처 |
|---|---|---|
| 미연결(페이지 대체) | `<Card className="shadow-xs"><CardContent className="flex flex-col items-center gap-3 py-12 text-center">` + `size-6` 아이콘 + `text-sm text-muted-foreground` | `app/customers/page.tsx:326-333`, `app/documents/page.tsx:257-264`, `app/company/page.tsx:208-215` |
| 빈 상태(표 자리) | `<div className="flex flex-col items-center gap-3 py-12 text-center">` + `size-6` 아이콘 + p | `app/customers/page.tsx:370-375`, `app/documents/page.tsx:361-372` |
| 동기화 중 | 같은 자리에 문구만 교체 — `{syncing ? t("동기화 중...") : t("등록된 거래처가 없습니다")}` | `app/customers/page.tsx:373` |
| 다분기 빈 상태 | 동기화 / 업로드 / 검색결과 없음 / 데이터 없음 4단 삼항 | `app/documents/page.tsx:364-370` |

> **예외**: 말줄임표 표기가 통일되지 않았다. 목록형은 `"동기화 중..."`(마침표 3개, `app/documents/page.tsx:365`), 메일·리포트·워크보드는 `"불러오는 중…"`/`"동기화 중…"`(U+2026, `app/mail/page.tsx:820`, `app/reports/page.tsx:241`, `app/workboard/page.tsx:579`). **신규 화면은 U+2026(`…`)을 쓴다**(다수).

### 3-7. 탭 + 검색 + 주액션 한 줄 툴바 — **유형 2에서 이식한다** (규정)

**앱에 유형 3(목록/테이블형) 선례가 없다.** 전수 확인 결과:

| 페이지 | 탭 위치 | 검색 위치 |
|---|---|---|
| 메일 (**유형 2**) | 툴바 좌측 + 검색 + 우측 액션 **한 줄** | 같은 줄 (`app/mail/page.tsx:741-810`) |
| 업무 (유형 3/4 혼합) | 헤더·스탯 **아래 별도 줄**, 검색 없음 | — (`app/tasks/page.tsx:1020-1026`) |
| 문서함 (유형 3) | 탭 없음 | 헤더 **아래 별도 줄** `max-w-sm` (`app/documents/page.tsx:335-344`) |
| 거래처 (유형 3) | 탭 없음 | 검색 없음 |
| 견적·계약 (유형 5) | 헤더 아래 별도 줄 | 검색 없음 (`app/quote-contract/page.tsx:284-287`) |

**규정**: 유형 3에서 이 조합이 필요하면 **유형 2(메일)의 툴바 원문을 그대로 이식한다.** 새 값을 만들지 않는다.

```tsx
{/* app/mail/page.tsx:741-810 원문을 유형 3 헤더 자리에 그대로 이식 */}
<div className="flex items-center justify-between gap-3">
  {/* 좌: 탭 */}
  <Tabs value={filter} onValueChange={setFilter}>
    <TabsList>
      <TabsTrigger value="all">{t("전체")}</TabsTrigger>
      <TabsTrigger value="active">{t("활성")}</TabsTrigger>
    </TabsList>
  </Tabs>

  {/* 중: 검색 — 가변폭, 모바일에서 숨김 */}
  <div className="relative mx-2 hidden min-w-0 flex-1 sm:block">
    <Search className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground" />
    <Input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => { if (e.key === "Enter") runSearch(query); }}
      placeholder={t("검색 (Enter)")}
      className="h-9 pl-8"
    />
    {query && (
      <button
        type="button"
        onClick={() => { setQuery(""); runSearch(""); }}
        className="absolute top-1/2 right-2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
        aria-label={t("검색 지우기")}
      >
        <X className="size-3.5" />
      </button>
    )}
  </div>

  {/* 우: 액션 — 보조(outline) → 주(default) 순 */}
  <div className="flex items-center gap-2">
    <Button variant="outline" onClick={() => load(true)} disabled={syncing} className="h-9 py-2">
      <RefreshCw className={`size-3.5 ${syncing ? "animate-spin" : ""}`} /> {t("새로고침")}
    </Button>
    <Button onClick={openCreate} className="h-9 py-2">
      <Plus className="size-3.5" /> {t("거래처 추가")}
    </Button>
  </div>
</div>
```

**이식 시 지켜야 할 값** (전부 § 2-2 원문 그대로)

| 항목 | 값 | 출처 |
|---|---|---|
| 툴바 래퍼 | `flex items-center justify-between gap-3` | `app/mail/page.tsx:741` |
| 검색 컨테이너 | `relative mx-2 hidden min-w-0 flex-1 sm:block` | `:762` |
| 검색 아이콘 | `pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground` | `:763` |
| 검색 입력 | `h-9 pl-8` | `:771` |
| 지우기 버튼 | `absolute top-1/2 right-2 -translate-y-1/2 text-muted-foreground hover:text-foreground` + `<X className="size-3.5" />` | `:779-785` |
| 액션 그룹 | `flex items-center gap-2`, 버튼마다 `h-9 py-2` | `:787-808` |

**이식 시 바뀌는 것 — 유형 3에서 지킬 것**

1. **설명 `<p>`가 사라지지 않는다.** 유형 2는 헤더 설명이 없지만 유형 3은 있다(§ 3-1 ①). 툴바는 설명 줄 **아래**에 별도 줄로 놓는다 — 설명과 탭을 한 줄에 섞지 않는다.
2. 검색 폭은 **`flex-1`(툴바 안, 메일식)** 을 쓴다. 툴바 밖 독립 배치라면 `max-w-sm`(문서함식, § 3-4).
3. `mx-2`는 탭·액션 사이 숨통이다. 검색이 없으면 이 줄은 § 3-1 ① 헤더로 되돌아간다.
4. 툴바를 넣어도 **일괄 선택 바(② BulkActionBar)와 표 카드(③)의 순서·값은 § 3-1 그대로**다.

---

## 유형 4. 보드/칸반형

**대표(칸반)**: `app/tasks/page.tsx` (1217줄)
**대표(트리+에디터)**: `app/workboard/page.tsx` (943줄) — 칸반이 아니라 **좌측 페이지 트리 + 우측 에디터** 구조다(실측).

### 4-1. 칸반 — 뼈대 스켈레톤

```tsx
// app/tasks/page.tsx:999-1049 (원문 골격)
<div className="space-y-4">
  {/* ① 단독 액션 */}
  <div className="flex items-center justify-between">
    <Button onClick={openCreate} className="h-9 py-2">
      <Plus className="mr-1.5 size-4" /> {t("새 업무")}
    </Button>
  </div>

  {/* ② 스탯 */}
  <StatGrid stats={stats} />

  {/* ③ 일괄바 (리스트·그룹 탭에서만) */}
  {(activeTab === "list" || activeTab === "group") && bulk.count > 0 && (
    <BulkActionBar … noun="업무" />
  )}

  {/* ④ 뷰 전환 탭 */}
  <Tabs value={activeTab} onValueChange={setActiveTab}>
    <TabsList>
      <TabsTrigger value="list">{t("리스트")}</TabsTrigger>
      <TabsTrigger value="group">{t("그룹")}</TabsTrigger>
      <TabsTrigger value="smart">{t("스마트")}</TabsTrigger>
      <TabsTrigger value="kanban">{t("칸반")}</TabsTrigger>
    </TabsList>

    <TabsContent value="smart" className="mt-4">
      <SortFilterBar />
      <div className="grid gap-3 md:grid-cols-3">
        <Column title={t("못한 일 (지남)")} items={smartBuckets.overdue} dot="bg-destructive" />
        <Column title={t("해야 할 일 (오늘/미정)")} items={smartBuckets.todo} dot="bg-foreground" />
        <Column title={t("다가올 일정")} items={smartBuckets.upcoming} dot="bg-muted-foreground" />
      </div>
    </TabsContent>

    <TabsContent value="kanban" className="mt-4">
      <SortFilterBar />
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {TASK_STATUSES.map((s) => (
          <Column key={s} title={s} dot="bg-muted-foreground" items={listTasks.filter((t) => t.status === s)} />
        ))}
      </div>
    </TabsContent>
  </Tabs>
</div>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 탭 콘텐츠 상단 여백 | `className="mt-4"` (모든 TabsContent) | `app/tasks/page.tsx:1028`, `:1037`, `:1052`, `:1077` |
| 칸반 열 그리드 | `grid gap-3 md:grid-cols-2 xl:grid-cols-4` | `:1039` |
| 3버킷 그리드 | `grid gap-3 md:grid-cols-3` | `:1030` |

### 4-2. 칸반 열 (Column) 원문

```tsx
// app/tasks/page.tsx:641-665 (원문)
const Column = ({ title, items, dot }: { title: string; items: Task[]; dot: string }) => {
  const tc = useT();
  return (
    <Card className="shadow-xs">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-sm font-medium">
          <span className={`size-2 rounded-full ${dot}`} />
          {title}
        </CardTitle>
        <CardAction>
          <Badge variant="secondary" className="font-normal">{items.length}</Badge>
        </CardAction>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {items.length === 0 ? (
            <p className="py-4 text-center text-xs text-muted-foreground">{tc("없음")}</p>
          ) : (
            items.map((task) => <TaskCard key={task.id} t={task} />)
          )}
        </div>
      </CardContent>
    </Card>
  );
};
```

- 열 상태 점: `size-2 rounded-full` + `bg-destructive` / `bg-foreground` / `bg-muted-foreground` (`:1031-1033`)
- 카드 간 간격: `space-y-2` (`:655`)
- 열 빈 상태: `py-4 text-center text-xs text-muted-foreground` (`:657`) — 카드보다 한 단계 작은 `text-xs`

### 4-3. 보드 카드 (TaskCard) 원문

```tsx
// app/tasks/page.tsx:555-637 (원문 골격)
<div className="rounded-lg border bg-card p-3">
  {/* 제목 + 메뉴 */}
  <div className="flex items-start justify-between gap-2">
    <button
      type="button"
      onClick={() => setDetailId(task.id)}
      className={`text-left text-sm font-medium hover:underline ${isDone(task) ? "text-muted-foreground line-through" : ""}`}
    >
      {task.title}
    </button>
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="text-muted-foreground hover:text-foreground" aria-label={tc("메뉴")}>
          <MoreHorizontal className="size-4" />
        </button>
      </DropdownMenuTrigger>
      …
    </DropdownMenu>
  </div>

  {/* 인라인 편집 칩 줄 */}
  <div className="mt-2.5 flex flex-wrap items-center gap-1.5">
    <Select value={task.status} onValueChange={…}>
      <SelectTrigger size="sm" className={`h-7 w-auto gap-1 border-0 px-2 py-0 text-xs ${statusBadgeClass(task.status)}`}>
        <SelectValue />
      </SelectTrigger>
      …
    </Select>
    <Select …>
      <SelectTrigger size="sm" className="h-7 w-auto gap-1 px-2 py-0 text-xs"><SelectValue placeholder={tc("분류")} /></SelectTrigger>
      …
    </Select>
    {task.priority && <Badge variant="outline" className="font-normal">{task.priority}</Badge>}
  </div>

  {/* 날짜 */}
  <div className="mt-2 flex items-center gap-2">
    <Input type="date" className={`h-7 w-36 px-2 py-0 text-xs ${overdue ? "text-destructive" : ""}`} … />
  </div>

  {/* 푸터(구분선 위) */}
  {task.automatable && (
    <div className="mt-2.5 flex items-center gap-1.5 border-t pt-2 text-xs text-muted-foreground">
      <Bot className="size-3.5" /> {tc("자동화")}: {task.automatable}
    </div>
  )}
</div>
```

**보드 카드는 `Card` 컴포넌트가 아니라 `rounded-lg border bg-card p-3`** — 카드 안의 카드라서 라운드·패딩을 한 단계 줄인다.

### 4-4. 그룹 섹션 헤더 (진행률 막대 포함)

```tsx
// app/tasks/page.tsx:826-928 (원문 골격)
<Card className="shadow-xs">
  <CardHeader className="gap-3">
    <div className="group/cat flex items-center gap-2">
      <button type="button" onClick={onToggle} className="flex items-center gap-2 text-left" aria-expanded={!collapsed}>
        <ChevronRight className={`size-4 text-muted-foreground transition-transform ${collapsed ? "" : "rotate-90"}`} />
        <CardTitle className="text-sm font-medium">{label}</CardTitle>
        <Badge variant="secondary" className="font-normal">{total}</Badge>
      </button>
      {/* hover 시에만 노출되는 편집 액션 */}
      <div className="flex items-center gap-0.5 opacity-0 transition-opacity group-hover/cat:opacity-100">
        <Button size="icon" variant="ghost" className="size-6 text-muted-foreground">
          <Pencil className="size-3.5" />
        </Button>
        …
      </div>
    </div>

    {/* 진행률 */}
    <div className="flex items-center gap-3 pl-6">
      <div className="h-1.5 w-40 overflow-hidden rounded-full bg-muted">
        <div className="h-full rounded-full bg-chart-1 transition-all" style={{ width: `${rate}%` }} />
      </div>
      <span className="text-xs tabular-nums text-muted-foreground">
        {tc("완료")} {done}/{total} · {rate}%
      </span>
    </div>
  </CardHeader>
  {!collapsed && (
    <CardContent className="p-0">
      <Table className="[&_:is(th,td)]:px-4">…</Table>
    </CardContent>
  )}
</Card>
```

- 접기 아이콘: `size-4` + `rotate-90` 전환
- 들여쓰기 정렬: `pl-6` (아이콘 폭 보정)
- 진행률 막대: `h-1.5 w-40 rounded-full bg-muted` / 채움 `bg-chart-1`
- hover 액션 버튼: `size-6` (표 행의 `size-7`보다 작다)

### 4-5. 정렬/필터 바

```tsx
// app/tasks/page.tsx:935-978 (원문 발췌)
<div className="mb-3 flex flex-wrap items-center gap-2">
  <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
    <ArrowUpDown className="size-3.5" /> {tc("정렬")}
  </div>
  <Select value={sortKey} onValueChange={…}>
    <SelectTrigger size="sm" className="h-8 w-32"><SelectValue /></SelectTrigger>
    …
  </Select>
  <Button variant="outline" size="sm" className="h-8 gap-1.5" onClick={…}>
    <ArrowUpNarrowWide className="size-3.5" />
    {dateAsc ? tc("날짜 오름차순") : tc("날짜 내림차순")}
  </Button>
  <Select …><SelectTrigger size="sm" className="h-8 w-32"><SelectValue /></SelectTrigger>…</Select>
  <Select …><SelectTrigger size="sm" className="h-8 w-36"><SelectValue /></SelectTrigger>…</Select>
</div>
```

**필터 컨트롤은 전부 `h-8`**, 폭은 `w-32`(기본) / `w-36`(긴 라벨). 바 하단 여백 `mb-3`.

### 4-6. 워크보드 — 트리 + 에디터 분할

```tsx
// app/workboard/page.tsx:560-605 (원문 골격)
<div className="flex h-[calc(100svh-7rem)] flex-col">
  <div className="grid min-h-0 flex-1 grid-cols-1 md:grid-cols-[260px_1fr]">
    {/* 좌: 트리 — 보드와는 세로 라인(border-r)으로만 구분 */}
    <div className="flex min-h-0 flex-col border-r">
      <div className="flex items-center justify-between border-b px-3 py-2">
        <span className="text-sm font-medium">{t("페이지")}</span>
        <Button variant="ghost" size="sm" className="h-7 gap-1 px-2 text-xs" onClick={() => createNote()}>
          <Plus className="size-3.5" /> {t("새 노트")}
        </Button>
      </div>
      <ScrollArea className="min-h-0 flex-1">
        <div className="p-1.5">…</div>
      </ScrollArea>
    </div>

    {/* 우: 에디터 — 테두리 없이 좌측 라인으로만 구분 */}
    <div className="flex min-h-0 flex-col">…</div>
  </div>
</div>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 전체 높이 | `h-[calc(100svh-7rem)]` | `app/workboard/page.tsx:561` |
| 분할 | `grid min-h-0 flex-1 grid-cols-1 md:grid-cols-[260px_1fr]` | `:562` |
| 패널 구분 | `border-r` **만** (카드/테두리 없음) | `:564` |
| 트리 헤더 | `flex items-center justify-between border-b px-3 py-2` | `:565` |
| 트리 본문 패딩 | `p-1.5` | `:577` |
| 툴바 버튼 | `h-7 gap-1 px-2 text-xs` / `h-7 gap-1 text-xs` | `:570`, `:620`, `:628` |
| 에디터 툴바 | `flex items-center justify-between px-3 py-1.5` | `:615` |
| 문서 제목 입력 | `mb-3 w-full border-0 bg-transparent pl-14 pr-8 text-2xl font-bold outline-none placeholder:text-muted-foreground/40 disabled:opacity-100` | `:682` |
| 문서 본문 | `markdown-body py-4 text-sm leading-relaxed` | `:667` |

> **예외**: 전체 높이 계산이 메일(`100svh-9rem`)과 워크보드(`100svh-7rem`)로 다르다. 메일 쪽 주석은 "헤더 3rem + py-6 상하 1.5rem씩"으로 9rem을 설명한다(`app/mail/page.tsx:63-64`). 워크보드가 7rem인 근거는 코드에 주석이 없어 **미확인**.

워크보드 상태 화면:

```tsx
{/* 로딩(트리) — app/workboard/page.tsx:579 */}
<p className="px-2 py-3 text-xs text-muted-foreground">{t("불러오는 중…")}</p>

{/* 빈 트리 — :581-583 */}
<p className="px-2 py-3 text-xs text-muted-foreground">
  {t('노트가 없습니다. "새 노트"로 시작하세요.')}
</p>

{/* 미선택(우측) — :607-612 */}
<div className="flex h-full flex-col items-center justify-center gap-3 text-center">
  <FileText className="size-6 text-muted-foreground" />
  <p className="text-sm text-muted-foreground">{t("좌측에서 노트를 선택하거나 새 노트를 만드세요.")}</p>
</div>

{/* 문서 로딩(스피너) — :660-662 */}
<div className="flex min-h-0 flex-1 items-center justify-center">
  <Loader2 className="size-5 animate-spin text-muted-foreground" />
</div>

{/* 저장 상태 인디케이터 — :637-646 */}
<Loader2 className="size-3 animate-spin" /> {t("저장 중…")}
<Check className="size-3 text-emerald-500" /> {t("저장됨")}
```

---

## 유형 5. 폼·설정형

**대표**: `app/settings/page.tsx` (201줄), `app/company/page.tsx`, `app/employees/page.tsx`(인라인 폼)

### 5-1. 설정 — 뼈대 스켈레톤

```tsx
// app/settings/page.tsx:56-198 (원문 골격)
<div className="space-y-6">                     {/* 설정은 space-y-6 (다른 페이지보다 넓음) */}
  <div>
    <p className="mt-1 text-sm text-muted-foreground">{t("외부 서비스(…)를 인트라넷에 연결합니다.")}</p>
  </div>

  {/* 설정 1건 = 카드 1개. 우측 상태 배지는 CardAction */}
  <Card className="shadow-xs">
    <CardHeader>
      <CardTitle className="text-sm font-medium">{t("표시 언어")}</CardTitle>
      <CardDescription>{t("인터페이스 전체 언어를 선택합니다")}</CardDescription>
      <CardAction>
        <LocaleSelect />
      </CardAction>
    </CardHeader>
  </Card>                                        {/* ← CardContent 없이 헤더만인 카드도 정상 */}

  {/* 결과 배너 (쿼리스트링 기반) */}
  {googleResult === "connected" && (
    <div className="flex items-center gap-2 rounded-md border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-700 dark:text-emerald-400">
      <CheckCircle2 className="size-4" /> {t("Google 계정이 연결되었습니다.")}
    </div>
  )}
  {googleResult === "error" && (
    <div className="flex items-center gap-2 rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
      <AlertTriangle className="size-4" /> {t("Google 연결 실패")}
    </div>
  )}

  {/* 연동 카드 — 아이콘 제목 + 상태 배지 + 권한 칩 + 액션 */}
  <Card className="shadow-xs">
    <CardHeader>
      <CardTitle className="flex items-center gap-2 text-sm font-medium">
        <Plug className="size-4 text-muted-foreground" /> Google (Gmail · Calendar)
      </CardTitle>
      <CardAction>{/* 상태 배지 5분기 */}</CardAction>
    </CardHeader>
    <CardContent className="space-y-4">
      {/* 권한 칩 */}
      <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5 rounded-md bg-muted px-2 py-1">
          <Mail className="size-3.5" /> {t("메일 읽기/발송")}
        </span>
      </div>
      {/* 상태별 본문 */}
      <Button asChild className="h-9 py-2">
        <a href="/api/auth/google/start">{t("Google 계정 연결")}</a>
      </Button>
    </CardContent>
  </Card>
</div>
```

### 5-2. 상태 배지 5분기 (설정형 핵심 패턴)

```tsx
// app/settings/page.tsx:95-115 (원문)
<CardAction>
  {!g ? (
    <Badge variant="outline">{t("확인 중…")}</Badge>
  ) : g.connected && g.needsReconnect ? (
    <Badge variant="outline" className="border-amber-500/30 bg-amber-500/10 text-amber-600 dark:text-amber-500">
      {t("재연결 필요")}
    </Badge>
  ) : g.connected ? (
    <Badge variant="outline" className="border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
      {t("연결됨")}
    </Badge>
  ) : g.configured ? (
    <Badge variant="outline" className="border-amber-500/30 bg-amber-500/10 text-amber-600 dark:text-amber-500">
      {t("미연결")}
    </Badge>
  ) : (
    <Badge variant="outline" className="border-destructive/30 bg-destructive/10 text-destructive">
      {t("미구성")}
    </Badge>
  )}
</CardAction>
```

### 5-3. 인라인 추가 폼 (직원 페이지)

```tsx
// app/employees/page.tsx:105-132 (원문)
<Card className="shadow-xs">
  <CardContent className="flex flex-wrap items-end gap-2 py-4">
    <div className="flex-1 min-w-32">
      <label className="mb-1 block text-xs text-muted-foreground">{t("이름")}</label>
      <Input value={name} onChange={(e) => setName(e.target.value)} placeholder={t("직원 이름")} />
    </div>
    <div className="flex-1 min-w-32">
      <label className="mb-1 block text-xs text-muted-foreground">{t("역할")}</label>
      <Input … />
    </div>
    <div className="min-w-28">
      <label className="mb-1 block text-xs text-muted-foreground">{t("에이전트")}</label>
      <Select value={agent} onValueChange={setAgent}>
        <SelectTrigger><SelectValue /></SelectTrigger>
        <SelectContent>…</SelectContent>
      </Select>
    </div>
    <Button onClick={add} disabled={adding || !name.trim()} className="gap-1.5">
      <UserPlus className="size-4" /> {t("추가")}
    </Button>
  </CardContent>
</Card>
```

- 필드 배치: `flex flex-wrap items-end gap-2 py-4`
- 가변 필드 `flex-1 min-w-32`, 고정 필드 `min-w-28`
- 라벨: `mb-1 block text-xs text-muted-foreground` (**`<label>` 태그, `Label` 컴포넌트 아님** — 다이얼로그 폼과 다르다)

### 5-4. 다이얼로그 폼 (거래처 추가/편집)

```tsx
// app/customers/page.tsx:467-500 (원문 골격)
<Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
  <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto">
    <DialogHeader>
      <DialogTitle>{editTarget ? t("거래처 수정") : t("거래처 추가")}</DialogTitle>
    </DialogHeader>
    <div className="space-y-4 py-2">
      {/* 1열 필드 */}
      <div className="space-y-1.5">
        <Label htmlFor="company">{t("회사명 *")}</Label>
        <Input id="company" value={form.company} onChange={…} placeholder={t("(주)예시컴퍼니")} />
      </div>
      {/* 2열 필드 */}
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5">
          <Label htmlFor="manager">{t("담당자")}</Label>
          <Input id="manager" … placeholder={t("홍길동")} />
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="phone">{t("연락처")}</Label>
          <Input id="phone" … placeholder="010-0000-0000" />
        </div>
      </div>
    </div>
  </DialogContent>
</Dialog>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 다이얼로그 폭(폼) | `sm:max-w-lg` | `app/customers/page.tsx:468` |
| 다이얼로그 높이 | `max-h-[90vh] overflow-y-auto` | `:468` |
| 폼 필드 간격 | `space-y-4 py-2` | `:472` |
| 라벨↔입력 간격 | `space-y-1.5` | `:473` |
| 2열 필드 | `grid grid-cols-2 gap-3` | `:482` |

> **예외**: 다이얼로그 최대 높이가 `max-h-[90vh]`(거래처)와 `max-h-[88vh]`(업무 상세·일정)로 갈린다 — `components/task-detail-dialog.tsx:118`, `components/notion-entry-dialog.tsx:231`. **신규는 `max-h-[88vh]`**(2:1 다수).

> **`[&>*]:min-w-0` 관련** — 위 스켈레톤의 폼 컨테이너(`<div className="space-y-4 py-2">`)에 `min-w-0`이 없는 것은 누락이 아니다. `DialogContent`의 전역 안전망이 **직계 자식**을 커버하고, 이 폼은 짧은 라벨·입력만 담기 때문이다. 다만 **긴 URL·에디터·표 등 와이드 콘텐츠를 담는 컨테이너에는 깊이와 무관하게 `min-w-0`을 직접 붙인다**(메일 작성창 실사례). 판정 기준과 근거는 [`02-primitives.md` 부록 C-1a](02-primitives.md) 참조.

#### 5-4a. 다이얼로그 푸터 — 생성/수정 폼 (삭제 버튼 없음)

**정본: `<DialogFooter>` 안에 `취소(outline)` → `저장(default)` 2버튼. 순서는 보조 → 주(오른쪽이 주).**

```tsx
// app/customers/page.tsx:678-685 (원문)
<DialogFooter>
  <Button variant="outline" onClick={() => setDialogOpen(false)} disabled={saving}>
    {t("취소")}
  </Button>
  <Button onClick={handleSave} disabled={saving}>
    {saving ? t("저장 중...") : editTarget ? t("수정") : t("추가")}
  </Button>
</DialogFooter>
```

**3개 페이지에서 완전히 동일하다** — `app/customers/page.tsx:678-685`, `app/company/page.tsx:463-470`, `app/agents/page.tsx:718-725`(라벨만 다름).

| 항목 | 값 | 근거 |
|---|---|---|
| 래퍼 | `<DialogFooter>` — **클래스 오버라이드 없음** | 3곳 모두 |
| 버튼 높이 | **명시 안 함** = Button 기본 `h-8`. 페이지 헤더의 `h-9 py-2`와 **다르다** | `components/ui/button.tsx:24-25` |
| 취소 | `variant="outline"`, `onClick`으로 `setOpen(false)`, `disabled={saving}` | `app/customers/page.tsx:679-681` |
| 저장 | `variant` 없음(default), `disabled={saving}` | `:682-684` |
| 라벨 삼항 | `saving ? t("저장 중...") : editTarget ? t("수정") : t("추가")` — 저장중/수정/생성 3분기 | `:683` |
| 순서 | 취소 먼저, 주 액션 오른쪽 | 3곳 모두 |

**변형 — 단일 전폭 버튼** (액션이 하나뿐인 조회형 다이얼로그)

```tsx
// app/calendar/page.tsx:266-270 (원문)
<DialogFooter>
  <Button onClick={() => openNew(selDay)} className="w-full">
    <Plus className="size-3.5" /> {t("이 날 일정 추가")}
  </Button>
</DialogFooter>
```

**삭제가 있는 경우와의 차이**: 삭제는 **이 푸터에 넣지 않는다.** 별도 `AlertDialog`로 분리하고(§ 7-13), 삭제 트리거는 표 행 액션 셀의 아이콘 버튼이다(`app/customers/page.tsx:449-455`). 즉 **생성/수정 폼 푸터에는 파괴적 액션이 절대 오지 않는다.**

---

## 유형 6. 리포트/차트형

**대표**: `app/reports/page.tsx` (401줄), `app/usage/page.tsx` (359줄)

### 6-1. 리포트(카드 그리드) — 뼈대 스켈레톤

```tsx
// app/reports/page.tsx:189-253 (원문 골격)
<>
  {/* ① 헤더 — 우측 액션이 sm 버튼(다른 페이지의 h-9와 다름, 예외) */}
  <div className="flex items-center justify-between">
    <div>
      <p className="mt-0.5 text-sm text-muted-foreground">{t("외부 에이전트 크론이 생성한 평가 레포트")}</p>
    </div>
    <Button variant="outline" size="sm" disabled={syncing} onClick={() => load(true)}>
      <RefreshCw className={`mr-1.5 size-3.5 ${syncing ? "animate-spin" : ""}`} />
      {t("동기화")}
    </Button>
  </div>

  {/* ② 필터 — 탭 + 셀렉트 나란히 */}
  <div className="flex flex-wrap items-center gap-3">
    <Tabs value={scopeTab} onValueChange={setScopeTab}>
      <TabsList>
        <TabsTrigger value="all">{t("전체")}</TabsTrigger>
        …
      </TabsList>
    </Tabs>
    <Select value={subjectFilter} onValueChange={setSubjectFilter}>
      <SelectTrigger className="w-44"><SelectValue placeholder={t("평가대상 전체")} /></SelectTrigger>
      <SelectContent>…</SelectContent>
    </Select>
  </div>

  {/* ③ 3열 카드 그리드 */}
  <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
    {filtered.map((r) => (
      <Card key={r.id} className="cursor-pointer shadow-xs transition-shadow hover:shadow-md" onClick={() => setSelected(r)}>
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between gap-2">
            <CardTitle className="text-sm font-medium leading-snug">{r.title}</CardTitle>
            <Badge variant="outline" className="shrink-0 text-xs">{t(r.scope)}</Badge>
          </div>
          <CardDescription className="flex flex-wrap items-center gap-2 pt-1">
            <Badge variant="outline" className={`text-xs ${subjectTypeBadgeClass(r.subjectType)}`}>{t(r.subjectType)}</Badge>
            <span className="flex items-center gap-1 text-xs text-muted-foreground">
              <User className="size-3" />
              {r.subject}
            </span>
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              <Calendar className="size-3" />
              {r.period ?? formatKST(r.created).slice(0, 10)}
            </div>
            <div className="flex items-center gap-1">
              <Star className="size-3.5 text-amber-500" />
              <span className="text-sm font-semibold tabular-nums">{r.total ?? "-"}</span>
            </div>
          </div>
          {r.author && <p className="mt-1 text-xs text-muted-foreground">{t("작성")}: {r.author}</p>}
        </CardContent>
      </Card>
    ))}
  </div>
</>
```

**클릭 가능한 카드 공식**: `cursor-pointer shadow-xs transition-shadow hover:shadow-md` (`app/reports/page.tsx:257`, `app/page.tsx:277`)

### 6-2. 리포트 상태 화면

```tsx
{/* 로딩 — app/reports/page.tsx:239-242 */}
<p className="py-12 text-center text-sm text-muted-foreground">{t("불러오는 중…")}</p>

{/* 빈 상태(큰 아이콘형) — :243-251 */}
<div className="py-16 text-center">
  <Award className="mx-auto mb-3 size-10 text-muted-foreground/40" />
  <p className="text-sm text-muted-foreground">
    {reports.length === 0
      ? t("아직 레포트가 없습니다. 외부 에이전트 크론이 생성합니다.")
      : t("해당 필터에 맞는 레포트가 없습니다.")}
  </p>
</div>

{/* 차트 데이터 없음 — :105-109 */}
<p className="py-8 text-center text-sm text-muted-foreground">{t("항목별 점수 데이터 없음")}</p>
```

> 리포트의 빈 상태만 `size-10 text-muted-foreground/40` + `py-16`을 쓴다. 목록형(`size-6`, `py-12`)과 다른 **더 큰 변형**이다.

### 6-3. 차트 컨테이너 (레이더)

```tsx
// app/reports/page.tsx:111-126 (원문)
<ChartContainer config={radarChartConfig} className="h-[260px] w-full min-w-0">
  <ResponsiveContainer width="100%" height="100%">
    <RadarChart data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12 }} />
      <Radar dataKey="score" stroke="var(--color-score)" fill="var(--color-score)" fillOpacity={0.3} />
    </RadarChart>
  </ResponsiveContainer>
</ChartContainer>
```

점수 표시 타이포 (임계값 색상):

```tsx
// app/reports/page.tsx:78-91 (원문)
const color = pct >= 80 ? "text-green-600" : pct >= 60 ? "text-yellow-600" : "text-red-500";
<div className={`text-3xl font-bold tabular-nums ${color}`}>
  {value !== null ? value : "-"}
  {value !== null && <span className="text-base font-normal text-muted-foreground">/100</span>}
</div>
```

> **예외**: 이 점수 색상만 `text-green-600` / `text-yellow-600` / `text-red-500` 원색을 직접 쓴다. 나머지 상태색은 전부 `emerald/amber/red-500` + `/10` 배경 톤 규칙(§ 7-3)을 따른다.

### 6-4. 사용량(진행률 바 + 기간 토글)

```tsx
// app/usage/page.tsx:155-243 (원문 골격)
<div className="space-y-4">
  <div>
    <p className="mt-1 text-sm text-muted-foreground">{t("세 툴의 MCP·Skill·Tool 사용량과 일별 토큰.")}</p>
  </div>

  {/* 스탯 열 수를 아래 카드에 맞춰 3열 고정 오버라이드 */}
  <StatGrid stats={stats} className="grid-cols-1 @xl/main:grid-cols-3" />

  {/* 정보/경고 인라인 배너 */}
  <div className={`flex items-start gap-2 rounded-md border p-3 text-sm ${
    u.available ? "bg-muted text-muted-foreground" : "border-destructive/40 bg-destructive/5 text-destructive"
  }`}>
    {u.available ? <Info className="mt-0.5 size-4 shrink-0" /> : <AlertTriangle className="mt-0.5 size-4 shrink-0" />}
    <span>{t(u.note)}</span>
  </div>

  {/* 헤더 우측에 토글 버튼 그룹이 붙는 카드 */}
  <Card className="shadow-xs">
    <CardHeader className="flex flex-row items-center justify-between gap-2">
      <CardTitle className="text-sm font-medium">{t("토큰 추세 (Claude)")}</CardTitle>
      <div className="flex gap-1">
        {(["day", "week", "month"] as TokenPeriod[]).map((p) => (
          <button
            key={p}
            onClick={() => setTokenPeriod(p)}
            className={`rounded px-2 py-0.5 text-xs transition-colors ${
              tokenPeriod === p
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            }`}
          >
            {p === "day" ? t("일") : p === "week" ? t("주") : t("월")}
          </button>
        ))}
      </div>
    </CardHeader>
    <CardContent>
      <div className="space-y-3 overflow-y-auto …">
        <div key={tok.label}>
          <p className="mb-1 text-xs text-muted-foreground">
            {tok.label} — {t("입력")} {fmt(tok.input)} / {t("출력")} {fmt(tok.output)}
          </p>
          <Progress value={…} className="h-1.5 bg-muted [&_[data-slot=progress-indicator]]:bg-chart-1" />
        </div>
      </div>
      <Button variant="ghost" size="sm" className="mt-3 h-7 w-full text-xs text-muted-foreground hover:text-foreground" onClick={…}>
        <ChevronUp className="mr-1 size-3" />
        {t("접기")}
      </Button>
    </CardContent>
  </Card>
</div>
```

| 항목 | 값 | 출처 |
|---|---|---|
| 스탯 열 오버라이드 | `grid-cols-1 @xl/main:grid-cols-3` | `app/usage/page.tsx:164` |
| 헤더 우측 토글 | `CardHeader className="flex flex-row items-center justify-between gap-2"` | `:220` |
| 토글 버튼(작은 pill) | `rounded px-2 py-0.5 text-xs` / 활성 `bg-primary text-primary-foreground` | `:233-237` |
| 진행률 바 | `h-1.5 bg-muted [&_[data-slot=progress-indicator]]:bg-chart-1` | `:261` |
| 항목 간격 | `space-y-3` | `:250` |
| 접기 버튼 | `mt-3 h-7 w-full text-xs` | `:270` |
| 표 정렬(수치) | `<TableHead className="text-right">` + `<TableCell className="text-right">` | `:197`, `:209` |
| 빈 상태 | `py-6 text-center text-sm text-muted-foreground` | `:190`, `:246` |

---

## 7. 반복 패턴 카탈로그

각 패턴은 **클래스 원문 그대로** 옮긴다. 값을 바꾸면 인트라넷 외형이 아니게 된다.

### 7-1. 목록 행 (아바타 + 2줄 + 타임스탬프)

```tsx
{/* 메일 목록 행 — app/mail/page.tsx:828-866 */}
"relative flex w-full gap-2.5 px-3 py-2.5 text-left transition-colors hover:bg-accent"
/* 선택: "bg-accent" · 미읽음: "bg-primary/[0.045]" */

  아바타 래퍼   "relative shrink-0"
  미읽음 점     "absolute -bottom-0.5 -right-0.5 size-2.5 rounded-full border-2 border-background bg-primary"
  본문 컬럼     "flex min-w-0 flex-1 flex-col gap-0.5"   /* 읽음 시 "opacity-70" 추가 */
  1줄(발신자)   "truncate text-sm font-semibold text-foreground"  /* 읽음: "font-normal text-muted-foreground" */
  타임스탬프    "text-[11px] text-muted-foreground"
  2줄(제목)     "truncate text-[13px] font-medium"               /* 읽음: "truncate text-[13px] text-muted-foreground" */
  3줄(스니펫)   "truncate text-xs text-muted-foreground"
```

```tsx
{/* 활동 피드 행 — app/page.tsx:436-473 */}
행            "flex gap-3 py-2.5 first:pt-0"
이니셜 아바타  "flex size-7 shrink-0 items-center justify-center rounded-full bg-muted text-[11px] font-medium text-muted-foreground"
본문 컬럼      "min-w-0 flex-1"
메타 줄        "mb-0.5 flex flex-wrap items-center gap-1.5"
타임스탬프     "shrink-0 text-[11px] text-muted-foreground"
요약           "text-[13px] leading-snug"
원문 토글      "cursor-pointer text-[11px] text-muted-foreground"
```

아바타 컬러 해시(메일):

```tsx
// app/mail/page.tsx:133-152 (원문)
const AVATAR_COLORS = [
  "bg-rose-500", "bg-orange-500", "bg-amber-500", "bg-emerald-500", "bg-teal-500",
  "bg-sky-500", "bg-indigo-500", "bg-violet-500", "bg-fuchsia-500", "bg-pink-500",
];
// 래퍼: "flex shrink-0 items-center justify-center rounded-full font-semibold text-white ${color}"
// 크기는 style로: width/height = size * 0.25rem, fontSize = size >= 8 ? "0.75rem" : "0.65rem"
```

#### 7-1a. 목록 행 우측 끝 메타 (배지 · 타임스탬프 · 액션 아이콘)

행 우측에 붙는 메타는 **하나의 `shrink-0` 묶음**으로 만든다. 좌측 본문이 `min-w-0 flex-1`이라 줄어들고, 우측은 절대 안 줄어드는 구조다.

**A. 아이콘 액션 + 타임스탬프** (메일 목록 — 정본 조합)

```tsx
// app/mail/page.tsx:843-857 (원문)
<span className="flex shrink-0 items-center gap-1.5">
  <span
    role="button"
    tabIndex={-1}
    onClick={(e) => toggleStarMsg(m.id, e)}
    className="text-muted-foreground/40 transition-colors hover:text-amber-400"
    aria-label={t("별표")}
  >
    <Star className={`size-3.5 ${isStarred(m.label_ids) ? "fill-amber-400 text-amber-400" : ""}`} />
  </span>
  <span className="text-[11px] text-muted-foreground">
    {m.internal_date ? formatKST(m.internal_date) : ""}
  </span>
</span>
```

**B. 타임스탬프(윗줄) + 카운트 배지(아랫줄)** (채팅 목록 — 2줄 분산형)

```tsx
// components/chat-panel.tsx:904-923 (원문 발췌)
{/* 윗줄 우측: 시각 — 이름과 한 줄을 공유, shrink-0라 목록이 좁아져도 안 숨는다 */}
<span className="shrink-0 whitespace-nowrap text-[10px] leading-none text-muted-foreground">
  {formatChatStamp(lastTime[p])}
</span>
{/* 아랫줄 우측: 안읽음 카운트 배지 */}
<span className="mt-px flex h-5 min-w-5 shrink-0 items-center justify-center rounded-full bg-destructive px-1 text-[11px] font-bold text-destructive-foreground">
  {unread[p] > 99 ? "99+" : unread[p]}
</span>
```

> **색은 정본이다** — `bg-destructive`/`text-destructive-foreground` 토큰 사용(하드코딩 아님).
> **형상은 두 벌이 남아 있다**: 채팅 `h-5 min-w-5 text-[11px]` vs 알림벨 `h-4 min-w-4 text-[10px] font-semibold`(`components/notification-bell.tsx:128`). 카운트 배지 형상 정본은 **알림벨 쪽**(README 정규화 표).

**C. 고정폭 메타 + 액션 아이콘** (드라이브 파일 행 — 표 없이 열 정렬)

```tsx
// app/drive/page.tsx:641-658 (원문 발췌)
<span className="hidden w-24 shrink-0 truncate text-xs text-muted-foreground sm:block">{f.owners ?? ""}</span>
<span className="hidden w-16 shrink-0 text-right text-xs text-muted-foreground md:block">{humanSize(f.size)}</span>
<span className="hidden w-32 shrink-0 text-right text-xs text-muted-foreground lg:block">{formatKST(f.modifiedTime)}</span>
<button onClick={() => toggleFav(f)} className={`shrink-0 ${isFav(f.id) ? "text-amber-500" : "text-muted-foreground hover:text-foreground"}`}>
  <Star className={`size-4 ${isFav(f.id) ? "fill-current" : ""}`} />
</button>
```

**D. 표 행에서의 등가물** — 별도 `TableCell` + `stopPropagation`

```tsx
// app/customers/page.tsx:438-455 · app/documents/page.tsx:461-472 (원문 형태)
<TableCell onClick={(e) => e.stopPropagation()}>
  <div className="flex items-center gap-1">
    <Button variant="ghost" size="icon" className="size-7">…</Button>
  </div>
</TableCell>
```

**공통 규칙**

| 항목 | 값 | 출처 |
|---|---|---|
| 묶음 래퍼 | `flex shrink-0 items-center gap-1.5` | `app/mail/page.tsx:843` |
| 좌측 본문(짝) | `min-w-0 flex-1` — 이게 없으면 우측이 밀려 잘린다 | `app/mail/page.tsx:836` |
| 타임스탬프 | `text-[11px] text-muted-foreground` | `app/mail/page.tsx:855` |
| 액션 아이콘(목록 행) | `size-3.5` — 표 행 액션 버튼은 `size="icon" className="size-7"` 안에 `size-3.5` | `app/mail/page.tsx:851-852` / `app/customers/page.tsx:441-447` |
| 반응형 숨김 | 고정폭 메타는 `hidden … sm:block`/`md:block`/`lg:block`로 좁은 화면에서 뺀다 | `app/drive/page.tsx:641-647` |
| 표 행일 때 | 액션 셀에 `onClick={(e) => e.stopPropagation()}` **필수**(행 전체가 클릭 가능) | `app/customers/page.tsx:438` |

#### 7-1b. 이니셜 아바타 — 글자 수 규칙

**두 규칙이 용도별로 갈린다. 섞지 않는다.**

| 규칙 | 글자 수 | 대문자화 | 쓰는 곳 | 출처 |
|---|---|---|---|---|
| **A. 사람/발신자 아바타** | **1자** | ✅ `.toUpperCase()` | 메일 발신자, 채팅 상대 | `app/mail/page.tsx:139`, `components/chat-thread.tsx:80` |
| **B. 이름 칩(한글 이름)** | **2자** | ❌ 없음 | 활동 피드 작성자, 멘션 후보 | `app/page.tsx:439`, `components/chat-thread.tsx:812` |

```ts
// A — app/mail/page.tsx:138-139 · components/chat-thread.tsx:79-80 (원문, 두 파일 동일)
const base = (name || email || "?").trim();
const initial = base.charAt(0).toUpperCase() || "?";
```

```tsx
// B — app/page.tsx:438-440 (원문)
<div className="flex size-7 shrink-0 items-center justify-center rounded-full bg-muted text-[11px] font-medium text-muted-foreground">
  {who.slice(0, 2)}
</div>
// components/chat-thread.tsx:811-813 — size-6 판, 같은 slice(0, 2)
```

**한글 처리 — 실제 동작**

- `charAt(0)` / `slice(0, 2)`는 **UTF-16 코드 유닛** 기준이다. 한글 음절(가–힣)은 BMP 1유닛이라 **"하늘" → `slice(0,2)` = "하늘"**로 정확히 2글자가 나온다. 절단 문제 없음.
- `.toUpperCase()`는 한글에 **무영향**(A 규칙에서 한글 이름이 와도 그대로).
- 이모지·서로게이트 페어는 깨질 수 있으나 **앱에 그런 경로가 없다 — 방어 코드도 없다**(원문 그대로).
- 빈 문자열 폴백은 A만 있다(`|| "?"`). **B에는 폴백이 없다** — 대신 호출부에서 값을 보장한다:
  `const who = a.who || a.summary.match(/[가-힣]{2,3}(?=\s|\/)/)?.[0] || "·"` (`app/page.tsx:435`) — 한글 2~3자를 정규식으로 뽑고 최후 폴백은 가운뎃점.

**형상 값**

| 항목 | A(사람 아바타) | B(이름 칩) |
|---|---|---|
| 배경 | 해시 기반 컬러 10종 + `text-white` | `bg-muted text-muted-foreground` |
| 크기 | `style`로 `size * 0.25rem` (메일 목록 `size={9}` = 36px) | `size-7`(28px, 활동 피드) / `size-6`(24px, 멘션) |
| 글자 | `font-semibold`, `fontSize` = `size >= 8 ? "0.75rem" : "0.65rem"` | `text-[11px] font-medium` |
| 래퍼 | `flex shrink-0 items-center justify-center rounded-full font-semibold text-white ${color}` | `flex size-7 shrink-0 items-center justify-center rounded-full` |
| 출처 | `app/mail/page.tsx:137-150` | `app/page.tsx:438`, `components/chat-thread.tsx:811` |

컬러 해시 함수(A 전용, 두 파일 동일 원문):

```ts
// app/mail/page.tsx:140-143 · components/chat-thread.tsx:81-84
const key = email || base;              // chat-thread: hashKey || base
let h = 0;
for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
const color = AVATAR_COLORS[h % AVATAR_COLORS.length];
```

### 7-2. 통계 카드 — § 1-3 원문 참조

핵심 클래스만: 카드 `@container/card h-full shadow-xs` / 수치 `text-2xl font-semibold tabular-nums @[250px]/card:text-3xl` / 푸터 `flex-col items-start gap-1.5 text-sm` + 제목행 `line-clamp-1 flex gap-2 font-medium` + 부제 `text-muted-foreground`.

### 7-3. 배지 / 상태칩 — **단일 출처 2개 함수**

> **API 계약**(export 이름·인자 시그니처·톤 키 전체·반환값·세 톤 테이블의 키 차이)은
> [`02-primitives.md` 부록 D-1~D-4](02-primitives.md)에 있다. 아래는 **반환 클래스 값**만 다룬다.
> 특히 `toneBadgeClass`의 톤 키(`blue`/`green`/…)와 `StatCard`의 톤 키(`info`/`success`/…)는
> **값만 같고 이름이 달라 서로 대입할 수 없다** — 부록 D-3 참조.

```ts
// lib/task-ui.ts:8-20 (원문) — 업무 상태 전용
"In Progress"  → "border-blue-500/30 bg-blue-500/10 text-blue-600 dark:text-blue-400"
"Completed"    → "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
"Pending"      → "border-amber-500/30 bg-amber-500/10 text-amber-600 dark:text-amber-500"
"Not Started"  → "border-border bg-muted text-muted-foreground"
```

```ts
// lib/badge-tone.ts:14-32 (원문) — 범용 톤
"blue"   → "border-blue-500/30 bg-blue-500/10 text-blue-600 dark:text-blue-400"
"green"  → "border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
"amber"  → "border-amber-500/30 bg-amber-500/10 text-amber-600 dark:text-amber-500"
"yellow" → (amber와 동일)
"purple" → "border-purple-500/30 bg-purple-500/10 text-purple-600 dark:text-purple-400"
"violet" → "border-violet-500/30 bg-violet-500/10 text-violet-600 dark:text-violet-400"
"red"    → "border-red-500/30 bg-red-500/10 text-red-600 dark:text-red-400"
"gray"   → "border-border bg-muted text-muted-foreground"
```

```ts
// components/stat-card.tsx:24-31 (원문) — 스탯 배지 톤 (위와 값 동일, 키만 다름)
neutral / danger(red) / warning(amber) / info(blue) / success(emerald) / violet
```

**공식**: `border-{색}-500/30 bg-{색}-500/10 text-{색}-600 dark:text-{색}-400` — 단, **amber만 `dark:text-amber-500`**.
사용법은 항상 `<Badge variant="outline" className={…}>`.

```tsx
{/* 실사용 */}
<Badge variant="outline" className={statusBadgeClass(task.status)}>{task.status}</Badge>   // app/page.tsx:315
<Badge variant="outline" className="font-normal">{e.role}</Badge>                          // app/employees/page.tsx:176
<Badge variant="secondary" className="font-normal">{items.length}</Badge>                  // app/tasks/page.tsx:651
<Badge variant="secondary" className="text-xs">{tag}</Badge>                               // app/documents/page.tsx:444
```

Badge 기본 형상: `h-5 rounded-2xl px-2 py-0.5 text-xs font-medium` + 내부 svg `[&>svg]:size-3!` (`components/ui/badge.tsx:8`).

### 7-4. 테이블 행 — § 3-1 참조

```tsx
{/* 클릭 가능 행 + 액션 셀 stopPropagation — app/customers/page.tsx:398-457 */}
<TableRow className="cursor-pointer" onClick={() => openEdit(c)}>
  <TableCell onClick={(e) => e.stopPropagation()}>…</TableCell>  {/* 체크박스 */}
  <TableCell className="font-medium">{c.company}</TableCell>     {/* 주 컬럼 */}
  <TableCell className="text-muted-foreground">{c.manager ?? "-"}</TableCell>  {/* 부 컬럼 */}
  <TableCell className="text-center">{/* 배지 */}</TableCell>
  <TableCell onClick={(e) => e.stopPropagation()}>{/* 액션 */}</TableCell>
</TableRow>
```

- 주 컬럼 = `font-medium`, 부 컬럼 = `text-muted-foreground`, 빈 값 = `"-"` 문자열
- 아이콘 동반 셀: `<TableCell className="font-medium max-w-xs truncate">` + `flex items-center gap-2` + `<FileText className="size-3.5 shrink-0 text-muted-foreground" />` + `<span className="truncate">` (`app/documents/page.tsx:407-411`)
- 배지 없을 때 자리 표시: `<span className="text-muted-foreground">-</span>` (`app/customers/page.tsx:423`)

hover 시에만 보이는 체크박스(노션식):

```tsx
// app/tasks/page.tsx:677-687 (원문)
<Checkbox
  className={cn(
    "transition-opacity",
    bulk.has(task.id) || bulk.count > 0 ? "opacity-100" : "opacity-0 group-hover:opacity-100",
  )}
/>
{/* 행에 className="group", 헤더에 className="group/lh" + "group-hover/lh:opacity-100" (:674, :775, :783) */}
```

### 7-5. 섹션 헤더

```tsx
{/* A. 제목만 */}
<CardHeader>
  <CardTitle className="text-sm font-medium">{t("다가올 업무")}</CardTitle>
</CardHeader>
{/* app/page.tsx:344-345, app/usage/page.tsx:185-186 */}

{/* B. 아이콘 + 제목 */}
<CardTitle className="flex items-center gap-1.5 text-sm font-medium">
  <ListTodo className="size-4 text-muted-foreground" /> {t("오늘 할 일")}
  <span className="text-xs font-normal text-muted-foreground">{todayList.length}{t("건")}</span>
</CardTitle>
{/* app/page.tsx:281-285 — gap-1.5 */}

<CardTitle className="flex items-center gap-2 text-sm font-medium">
  <Plug className="size-4 text-muted-foreground" /> Google (Gmail · Calendar)
</CardTitle>
{/* app/settings/page.tsx:92-94 — gap-2 (예외: gap-1.5와 gap-2 혼용) */}

{/* C. 제목 + 우측 링크/액션 */}
<CardAction>
  <Link href="/tasks" className="text-xs text-muted-foreground hover:underline">
    {t("업무 보드")}
  </Link>
</CardAction>
{/* app/page.tsx:287-291, :346-350, :414-418, :501-505 */}
```

### 7-6. 액션 버튼 그룹 (페이지 헤더 우측)

```tsx
// app/customers/page.tsx:346-353 · app/company/page.tsx:235-242 (원문, 동일)
<div className="flex gap-2">
  <Button variant="outline" onClick={() => load(true)} disabled={syncing} className="h-9 py-2">
    <RefreshCw className={`size-3.5 ${syncing ? "animate-spin" : ""}`} /> {t("새로고침")}
  </Button>
  <Button onClick={openCreate} className="h-9 py-2">
    <Plus className="size-3.5" /> {t("거래처 추가")}
  </Button>
</div>
```

- **주 액션은 `variant` 없음(default), 보조는 `variant="outline"`. 순서는 보조 → 주(오른쪽이 주).**
- 동기화 중 회전: `${syncing ? "animate-spin" : ""}`
- 메일은 `flex items-center gap-2`로 3개까지 (`app/mail/page.tsx:789-811`)

### 7-7. 빈 상태 — 4가지 크기

| 크기 | 마크업 | 쓰는 곳 |
|---|---|---|
| XS (열·칸반) | `py-4 text-center text-xs text-muted-foreground` | `app/tasks/page.tsx:657` |
| S (카드 본문) | `py-6 text-center text-sm text-muted-foreground` | `app/page.tsx:295`, `:354`, `:422`; `app/usage/page.tsx:190`, `:246` |
| M (목록·표) | `py-8 text-center text-sm text-muted-foreground` | `app/employees/page.tsx:138`; `app/reports/page.tsx:106` |
| L (아이콘 동반) | `flex flex-col items-center gap-3 py-12 text-center` + `<Icon className="size-6 text-muted-foreground" />` + `<p className="text-sm text-muted-foreground">` | `app/customers/page.tsx:370-375`, `app/documents/page.tsx:361-372`, `app/company/page.tsx:258-263`, `app/mail/page.tsx:721-727`, `app/workboard/page.tsx:550-555` |
| XL (리포트 전용, 예외) | `py-16 text-center` + `<Icon className="mx-auto mb-3 size-10 text-muted-foreground/40" />` | `app/reports/page.tsx:244-245` |

#### 7-7a. 빈 상태를 **독립 배치**할 때의 래퍼 — 카드로 감싼다 (정본)

위 표는 **카드 안 문맥**(표 자리·카드 본문)이다. 화면 전체가 빈 상태일 때(미연결·권한 없음 등 페이지 대체) 무엇으로 감싸는지는 별개 결정이다.

**정본: `<div className="space-y-4">` → `<Card className="shadow-xs">` → `<CardContent>`**

```tsx
// app/customers/page.tsx:325-334 (원문) — 페이지 전체를 대체하는 미연결 화면
if (connected === false) {
  return (
    <div className="space-y-4">
      <Card className="shadow-xs">
        <CardContent className="flex flex-col items-center gap-3 py-12 text-center">
          <Building2 className="size-6 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            {t("Notion이 연결되지 않았습니다. (.env.local의 NOTION_TOKEN 확인)")}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
```

**전수 집계 — 카드 래핑이 다수 (5 : 2)**

| 래퍼 | 페이지 | 출처 |
|---|---|---|
| ✅ `Card > CardContent` | 거래처 | `app/customers/page.tsx:325-334` |
| ✅ `Card > CardContent` | 캘린더 | `app/calendar/page.tsx:135-143` |
| ✅ `Card > CardContent` | 문서함 | `app/documents/page.tsx:255-264` |
| ✅ `Card > CardContent` | 회사정보 | `app/company/page.tsx:207-215` |
| ✅ `Card > CardContent` | 메일 | `app/mail/page.tsx:716-725` |
| ⚠️ 테두리 `div` (`rounded-lg border`) | 지식망 | `app/wiki/page.tsx:86-92` |
| ⚠️ 테두리 `div` (`rounded-lg border`) | 워크보드 | `app/workboard/page.tsx:549-556` |

**규칙**

1. 내부 정렬 블록은 **L 크기 그대로** — `flex flex-col items-center gap-3 py-12 text-center` + `<Icon className="size-6 text-muted-foreground" />` + `<p className="text-sm text-muted-foreground">`. 카드로 감싸도 이 값은 변하지 않는다.
2. `space-y-4` 루트로 한 번 더 감싼다(§ 0 정본 루트 컨테이너). **메일만 예외** — `Card`를 바로 반환한다(`app/mail/page.tsx:717`). 유형 2는 루트가 `flex flex-col gap-3`이라 대체 화면에서 루트를 버린다.
3. 복구 액션이 있으면 `<p>` 아래에 버튼을 넣는다 — `<Button asChild className="h-9 py-2"><Link href="/settings">{t("설정에서 연결")}</Link></Button>` (`app/mail/page.tsx:722-724`).
4. **테두리 `div` 변형(지식망·워크보드)은 따라 하지 않는다.** 두 곳 모두 전체높이 2분할 레이아웃이라 카드 패딩이 방해되는 특수 사정이고, 표면 규약(`ring-1 ring-foreground/5`)이 아닌 `border`를 써서 § 정체성 3번과도 어긋난다.

### 7-8. 로딩 상태

```tsx
{/* 텍스트형 — 가장 흔함 */}
"불러오는 중…"
  · 패널 중앙: "flex h-full items-center justify-center rounded-md border text-sm text-muted-foreground"   // app/mail/page.tsx:890-892
  · 페이지 중앙: "py-12 text-center text-sm text-muted-foreground"                                          // app/reports/page.tsx:240
  · 사이드 트리: "px-2 py-3 text-xs text-muted-foreground"                                                  // app/workboard/page.tsx:579

{/* 스피너형 */}
<Loader2 className="size-5 animate-spin text-muted-foreground" />   // app/workboard/page.tsx:661 (컨테이너: "flex min-h-0 flex-1 items-center justify-center")
<Loader2 className="size-3 animate-spin" /> {t("저장 중…")}         // app/workboard/page.tsx:639 (인라인)

{/* 동기화 중 = 아이콘 회전 */}
<RefreshCw className={`size-3.5 ${syncing ? "animate-spin" : ""}`} />   // app/customers/page.tsx:348

{/* 빈 상태 문구를 겸하는 방식 */}
{syncing ? t("동기화 중…") : t("메일 없음")}                            // app/mail/page.tsx:820
```

### 7-9. 에러 / 경고 배너 (인라인, 페이지 상단)

```tsx
{/* 경고(amber) + 우측 조치 버튼 — app/mail/page.tsx:735-740 */}
<div className="flex items-center justify-between gap-3 rounded-md border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-sm text-amber-700 dark:text-amber-400">
  <span>{t("Gmail 토큰이 만료되어 동기화가 막혔습니다. 재연결이 필요합니다.")}</span>
  <Button asChild size="sm" className="h-8 shrink-0">
    <a href="/api/auth/google/start">{t("재연결")}</a>
  </Button>
</div>

{/* 성공(emerald) — app/settings/page.tsx:79-81 */}
<div className="flex items-center gap-2 rounded-md border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-700 dark:text-emerald-400">
  <CheckCircle2 className="size-4" /> {t("Google 계정이 연결되었습니다.")}
</div>

{/* 실패(destructive) — app/settings/page.tsx:84-86 */}
<div className="flex items-center gap-2 rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">
  <AlertTriangle className="size-4" /> {t("Google 연결 실패")}
</div>

{/* 여러 줄 경고(아이콘 상단 정렬) — app/settings/page.tsx:134-137 */}
<p className="flex items-start gap-2 rounded-md border border-amber-500/40 bg-amber-500/10 p-2.5 text-sm text-amber-700 dark:text-amber-400">
  <AlertTriangle className="mt-0.5 size-4 shrink-0" />
  {t("토큰이 만료되어 …")}
</p>

{/* 정보/경고 겸용 — app/usage/page.tsx:167-180 */}
`flex items-start gap-2 rounded-md border p-3 text-sm ${
  u.available ? "bg-muted text-muted-foreground" : "border-destructive/40 bg-destructive/5 text-destructive"
}`
```

> **예외**: 워크보드 readOnly 배너만 `bg-amber-50 … dark:bg-amber-950/30 dark:text-amber-400` (`app/workboard/page.tsx:653`)로, 다른 배너의 `bg-amber-500/10` 규칙을 따르지 않는다.

### 7-10. 일괄 선택 바 (플로팅 pill) — 원문

```tsx
// components/bulk-action-bar.tsx:43-55 (원문)
<div className="pointer-events-none fixed inset-x-0 bottom-5 z-40 flex justify-center px-4">
  <div className="pointer-events-auto flex items-center gap-3 rounded-full border bg-card/95 px-4 py-2 shadow-lg backdrop-blur supports-[backdrop-filter]:bg-card/80">
    <Checkbox checked={allSelected} onCheckedChange={onToggleAll} aria-label={t("전체 선택")} />
    <span className="text-sm font-medium">{count}{t("개 선택됨")}</span>
    <Button
      variant="ghost"
      size="sm"
      className="h-8 gap-1 text-destructive hover:text-destructive"
      onClick={() => setConfirm(true)}
    >
      <Trash2 className="size-3.5" /> {t("선택 삭제")}
    </Button>
  </div>
</div>
```

`fixed` 오버레이라 선택해도 형제 레이아웃이 밀리지 않는다(주석 `components/bulk-action-bar.tsx:39-40`). 호출부는 `{bulk.count > 0 && <BulkActionBar … noun="거래처" />}`.

### 7-11. 속성 행 (다이얼로그 좌라벨/우값)

```tsx
{/* 업무 상세 — components/task-detail-dialog.tsx:107-113 (원문) */}
<div className="flex items-center gap-3 py-1.5">
  <div className="flex w-28 shrink-0 items-center gap-1.5 text-xs text-muted-foreground">
    {icon}
    {label}
  </div>
  <div className="min-w-0 flex-1 text-sm">{children}</div>
</div>
{/* 아이콘: size-3.5 · 컨테이너: "divide-y rounded-lg border bg-card/50 px-3 py-1" (:133) */}

{/* 일정 상세 — components/notion-entry-dialog.tsx:381-386 (원문) */}
<div className="flex items-center gap-2 py-1.5">
  <span className="flex w-24 shrink-0 items-center gap-1.5 text-muted-foreground">
    {icon} {label}
  </span>
  <div className="min-w-0 flex-1">{children}</div>
</div>
{/* 아이콘: size-4 · 컨테이너: "divide-y text-sm" (:242) */}
```

> **예외**: 두 속성 행이 라벨 폭(`w-28` vs `w-24`), gap(`gap-3` vs `gap-2`), 아이콘 크기(`size-3.5` vs `size-4`)에서 불일치. **신규는 업무 상세(`w-28`/`gap-3`/`size-3.5`) 쪽을 따른다** — 컨테이너에 테두리·배경이 있어 더 완성형이다.

### 7-12. 인라인 편집 컨트롤 (노션식)

```tsx
{/* 표 안 — 폭 100%, 가운데 정렬 — app/tasks/page.tsx:707-731 */}
<SelectTrigger size="sm" className={`h-7 w-full justify-center gap-1 border-0 px-2 py-0 text-xs ${statusBadgeClass(task.status)}`} />
<Input type="date" className={`h-7 w-full px-2 py-0 text-center text-xs ${overdue ? "text-destructive" : ""}`} />

{/* 카드 안 — 폭 자동 — app/tasks/page.tsx:595-627 */}
<SelectTrigger size="sm" className={`h-7 w-auto gap-1 border-0 px-2 py-0 text-xs ${statusBadgeClass(task.status)}`} />
<Input type="date" className={`h-7 w-36 px-2 py-0 text-xs ${overdue ? "text-destructive" : ""}`} />

{/* 다이얼로그 안 — 투명 배경 + hover 강조 — components/notion-entry-dialog.tsx:245-276 */}
<SelectTrigger size="sm" className="h-7 w-[9.5rem] border-0 bg-transparent shadow-none hover:bg-accent data-[state=open]:bg-accent" />
<Input type="date" className="h-7 w-[8.5rem] border-0 bg-transparent px-1 shadow-none hover:bg-accent" />
<Input className="h-7 border-0 bg-transparent px-1 shadow-none hover:bg-accent placeholder:text-muted-foreground/50" />

{/* 다이얼로그 안 — 일반(테두리 유지) — components/task-detail-dialog.tsx:137-151 */}
<SelectTrigger className="h-8 w-44" />
<Input type="date" className="h-8 w-44" />
```

**인라인 편집 = `h-7 px-2 py-0 text-xs`**. 다이얼로그 정식 폼 = `h-8 w-44`.

### 7-13. 확인 다이얼로그 (삭제)

```tsx
// components/bulk-action-bar.tsx:57-78 · app/workboard/page.tsx:697-718 (동일 패턴)
<AlertDialog open={confirm} onOpenChange={setConfirm}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>{t("이 노트를 삭제할까요?")}</AlertDialogTitle>
      <AlertDialogDescription>
        <strong>{deleteTarget?.title}</strong> {t("페이지가 Notion에서 보관 처리됩니다.")}
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>{t("취소")}</AlertDialogCancel>
      <AlertDialogAction
        onClick={(e) => { e.preventDefault(); doDelete(); }}
        className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
      >
        {t("삭제")}
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

`AlertDialogAction`에 **항상 `bg-destructive text-destructive-foreground hover:bg-destructive/90`을 직접 붙인다**(기본 variant가 destructive가 아니므로).

### 7-14. 다이얼로그 셸

```tsx
{/* 상세형(넓음) — components/task-detail-dialog.tsx:117-130 */}
<DialogContent className="max-h-[88vh] overflow-y-auto sm:max-w-3xl">
  <DialogHeader>
    <DialogTitle className="pr-8 text-lg leading-snug">{task.title}</DialogTitle>
  </DialogHeader>

{/* 일정형(중간) + 제목 인라인 편집 — components/notion-entry-dialog.tsx:231-240 */}
<DialogContent className="max-h-[88vh] overflow-y-auto sm:max-w-2xl" onOpenAutoFocus={(e) => e.preventDefault()}>
  <DialogHeader>
    <DialogTitle className="sr-only">{t("일정 상세")}</DialogTitle>
    <input
      value={draft.title}
      placeholder={t("제목 없음")}
      className="w-full border-0 bg-transparent p-0 text-lg font-semibold outline-none placeholder:text-muted-foreground/50"
    />
  </DialogHeader>

{/* 폼형(좁음) — app/customers/page.tsx:468-471 */}
<DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto">
  <DialogHeader><DialogTitle>{t("거래처 추가")}</DialogTitle></DialogHeader>

{/* 푸터: 좌 삭제 / 우 취소·저장 — components/task-detail-dialog.tsx:255-271 */}
<DialogFooter className="flex-row justify-between sm:justify-between">
  <Button variant="ghost" size="sm" className="text-destructive" onClick={() => onDelete(task.id)}>
    <Trash2 className="mr-1.5 size-3.5" /> {t("삭제")}
  </Button>
  <div className="flex gap-2">
    <Button variant="outline" size="sm" onClick={…}>{t("취소")}</Button>
    <Button size="sm" onClick={handleSave}>{t("저장")}</Button>
  </div>
</DialogFooter>
```

폭 3단: `sm:max-w-lg`(폼) / `sm:max-w-2xl`(일정·리포트) / `sm:max-w-3xl`(업무 상세).

### 7-15. 본문 블록 (다이얼로그 내 자유 텍스트)

```tsx
// components/task-detail-dialog.tsx:235-253 (원문)
<div className="space-y-1.5">
  <div className="text-xs font-medium text-muted-foreground">{t("본문")}</div>
  {editing ? (
    <Textarea rows={6} … placeholder={t("업무 상세 메모를 적어주세요")} />
  ) : task.notes ? (
    <p className="whitespace-pre-wrap rounded-lg border bg-card/50 p-3 text-sm leading-relaxed">{task.notes}</p>
  ) : (
    <p className="rounded-lg border border-dashed p-3 text-sm text-muted-foreground">
      {t("본문이 비어 있습니다.")}
    </p>
  )}
</div>
```

**값 있음 = 실선 테두리 + `bg-card/50` / 값 없음 = `border-dashed`.**

### 7-16. 접기·더보기 토글

```tsx
{/* 카드 하단 전폭 — app/page.tsx:486-491 */}
<button
  onClick={() => setActivityExpanded((v) => !v)}
  className="mt-2 w-full rounded-md py-1.5 text-center text-xs text-muted-foreground transition-colors hover:bg-muted/50 hover:text-foreground"
>
  {activityExpanded ? t("접기") : `${t("더 보기")} (${activity.length - ACTIVITY_FOLD}${t("개")})`}
</button>

{/* Button 컴포넌트판 — app/usage/page.tsx:267-272 */}
<Button variant="ghost" size="sm" className="mt-3 h-7 w-full text-xs text-muted-foreground hover:text-foreground">
  <ChevronUp className="mr-1 size-3" /> {t("접기")}
</Button>
```

### 7-17. 권한/속성 칩 (읽기 전용 태그)

```tsx
// app/settings/page.tsx:118-125 (원문)
<div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
  <span className="flex items-center gap-1.5 rounded-md bg-muted px-2 py-1">
    <Mail className="size-3.5" /> {t("메일 읽기/발송")}
  </span>
</div>
```

### 7-18. 마스킹 값 + 복사 버튼 (토큰)

```tsx
// app/employees/page.tsx:187-204 (원문)
<button
  type="button"
  onClick={() => setRevealed((s) => new Set(s).add(e.id))}
  className="flex items-center gap-1.5 rounded-md border bg-muted/40 px-2 py-1 font-mono text-xs text-muted-foreground hover:bg-muted"
  title={t("클릭하여 토큰 표시")}
>
  <KeyRound className="size-3" />
  {revealed.has(e.id) ? e.cli_token : "cli_••••••••••"}
</button>
<Button variant="ghost" size="sm" className="h-8 w-8 p-0" onClick={…} title={t("토큰 복사")}>
  {copied === e.id ? <Check className="size-3.5 text-emerald-500" /> : <Copy className="size-3.5" />}
</Button>
```

> **예외**: 여기만 아이콘 버튼을 `size="sm" className="h-8 w-8 p-0"`로 만든다. 다른 곳은 `size="icon" className="size-7"`(표 행) 또는 `size-6`(hover 액션).

### 7-19. 진행률 막대

```tsx
{/* 수제 막대 — app/tasks/page.tsx:906-914 */}
<div className="flex items-center gap-3 pl-6">
  <div className="h-1.5 w-40 overflow-hidden rounded-full bg-muted">
    <div className="h-full rounded-full bg-chart-1 transition-all" style={{ width: `${rate}%` }} />
  </div>
  <span className="text-xs tabular-nums text-muted-foreground">{tc("완료")} {done}/{total} · {rate}%</span>
</div>

{/* Progress 컴포넌트 — app/usage/page.tsx:259-262 */}
<Progress value={…} className="h-1.5 bg-muted [&_[data-slot=progress-indicator]]:bg-chart-1" />
```

둘 다 **높이 `h-1.5`, 트랙 `bg-muted`, 채움 `bg-chart-1`**로 동일.

### 7-20. 슬림 스크롤바 — § 2-5 참조

---

## 8. do / don't

코드에서 **반복 관찰된** 규칙만 적는다. 어긋난 사례는 "예외"로 명시.

### 8-1. 레이아웃

| ✅ do | ❌ don't |
|---|---|
| 페이지 컴포넌트는 패딩 없이 시작, 셸의 `px-4 lg:px-6 py-4 md:py-6`에 맡긴다 (`app/providers.tsx:100`) | 페이지 루트에 `p-6` 등 자체 패딩을 추가 |
| 페이지 본문 최상단은 설명 `<p className="mt-1 text-sm text-muted-foreground">` 한 줄 | 페이지 안에 `<h1>` 추가 — H1은 `SiteHeader`가 그린다 (`components/site-header.tsx:22`) |
| 루트 래퍼는 `<div className="space-y-4">` | `space-y-2`/`space-y-8` 같은 임의 값 |
| 섹션 = `<Card className="shadow-xs">` | 카드 없이 `<section>` + 자체 테두리 |
| 표를 카드 가장자리까지 붙일 땐 `Card className="shadow-xs py-0"` + `CardContent className="p-0"` (`app/customers/page.tsx:367-368`) | `CardContent` 기본 패딩 안에 표를 넣어 좌우 20px 들여쓰기 |
| 표 셀 좌우는 `[&_:is(th,td)]:px-4`로 일괄 확장 (`app/customers/page.tsx:377`) | 셀마다 `px-4`를 개별 부착 |
| 2패널은 `flex gap-4` + 좌 `w-2/5 min-w-[280px] max-w-md shrink-0` + 우 `min-w-0 flex-1` (`app/mail/page.tsx:814-875`) | 우측 패널에 `min-w-0` 누락 (긴 콘텐츠가 레이아웃을 밀어냄) |
| 고정 높이 화면은 `h-[calc(100svh-9rem)]` (`app/mail/page.tsx:64`) | `100vh` 사용 (모바일 주소창 보정 안 됨) |
| 반응형 열은 컨테이너 쿼리 `@xl/main:` / `@5xl/main:` (`components/stat-card.tsx:108`) | 뷰포트 브레이크포인트로 스탯 그리드를 짜기 |
| **예외** — 워크보드만 `100svh-7rem` (`app/workboard/page.tsx:561`). 근거 주석 없음(미확인) | |

### 8-2. 아이콘 크기

| 상황 | 크기 | 출처 |
|---|---|---|
| 버튼 안·인라인·행 액션 (**기본값**) | `size-3.5` | `app/customers/page.tsx:348`, `:446`; `app/mail/page.tsx:798`, `:806`; `app/tasks/page.tsx:575` |
| 카드 제목 옆 아이콘 | `size-4` | `app/page.tsx:282`, `:412`; `app/settings/page.tsx:93`, `:173` |
| 배너 아이콘 | `size-4` | `app/settings/page.tsx:80`, `:85`, `:135` |
| 드롭다운 트리거(⋯) | `size-4` | `app/tasks/page.tsx:567`, `:751` |
| 배지 **안** | `size-3` (Badge가 `[&>svg]:size-3!`로 강제) | `components/ui/badge.tsx:8`; 실사용 `app/page.tsx:458`, `:469` |
| 카드 메타 줄의 미세 아이콘 | `size-3` | `app/reports/page.tsx:282`, `:291` |
| 빈 상태(L) | `size-6` | `app/customers/page.tsx:371`, `app/mail/page.tsx:722` |
| 드롭존 | `size-5` | `app/documents/page.tsx:326` |
| 스피너(패널 중앙) | `size-5` | `app/workboard/page.tsx:661` |
| **예외** 리포트 빈 상태(XL) | `size-10 text-muted-foreground/40` | `app/reports/page.tsx:245` |

> Button은 크기 미지정 svg를 `size-4`로 자동 강제한다(`components/ui/button.tsx:8`, `[&_svg:not([class*='size-'])]:size-4`). **버튼 안 아이콘은 명시적으로 `size-3.5`를 준다** — 그래야 기본 `size-4` 강제를 이기고 인트라넷 톤이 된다.

### 8-3. 버튼 높이

| 상황 | 값 | 출처 |
|---|---|---|
| 페이지 헤더 우측 액션 | `className="h-9 py-2"` (default variant의 `h-8`을 덮어씀) | `app/customers/page.tsx:347`, `:350`; `app/documents/page.tsx:283`, `:291`; `app/company/page.tsx:236`, `:239`; `app/mail/page.tsx:795`, `:805`, `:808`; `app/settings/page.tsx:145`, `:153`, `:161`; `app/tasks/page.tsx:1001` |
| 툴바·필터·상세 액션 | `h-8` (또는 `size="sm"` + `className="h-8"`) | `app/tasks/page.tsx:940`, `:953`, `:966`; `app/mail/page.tsx:934`, `:952`; `components/bulk-action-bar.tsx:50` |
| 조밀 영역(워크보드 트리·에디터 툴바) | `h-7` | `app/workboard/page.tsx:570`, `:620`, `:628` |
| 인라인 편집(Select/Input) | `h-7 px-2 py-0 text-xs` | `app/tasks/page.tsx:597`, `:610`, `:627` |
| 표 행 아이콘 버튼 | `size="icon" className="size-7"` | `app/customers/page.tsx:443`, `:451`; `app/company/page.tsx:322`, `:330` |
| hover 노출 편집 버튼 | `size="icon" className="size-6"` | `app/tasks/page.tsx:883`, `:895` |
| **예외** 리포트 헤더 동기화 | `size="sm"` 만 (=`h-7`), `h-9` 없음 | `app/reports/page.tsx:197-207` |
| **예외** 직원 토큰 복사/삭제 | `size="sm" className="h-8 w-8 p-0"` | `app/employees/page.tsx:199`, `:208` |

Button 기본 높이 표(`components/ui/button.tsx:24-32`): `default h-8 px-3` / `xs h-6` / `sm h-7` / `lg h-9` / `icon size-8` / `icon-xs size-6` / `icon-sm size-7` / `icon-lg size-9`.

> `h-9 py-2`는 `size="lg"`(`h-9 px-4`)를 쓰지 않고 className으로 높이만 올린 관용구다. 좌우 패딩은 default의 `px-3`을 유지한다.

### 8-4. 라운드 / 표면

| ✅ do | 근거 |
|---|---|
| 카드 라운드는 컴포넌트에 위임: `rounded-[min(var(--radius-4xl),24px)]` | `components/ui/card.tsx:15` |
| 카드 표면은 `bg-card shadow-sm ring-1 ring-foreground/5 dark:ring-foreground/10` (컴포넌트 기본) + 페이지에서 `shadow-xs` 덧입힘 | `components/ui/card.tsx:15`; 전 페이지 |
| 카드 **안**의 블록은 `rounded-lg border` (한 단계 작게) | `app/tasks/page.tsx:555`; `components/task-detail-dialog.tsx:133`, `:245` |
| 패널·배너·검색 등 중간 요소는 `rounded-md border` | `app/mail/page.tsx:817`, `:735`; `app/company/page.tsx:286` |
| pill/토글은 `rounded-full` | `components/bulk-action-bar.tsx:44`; `app/tasks/page.tsx:906` |
| Button·Badge 라운드는 건드리지 않는다 (둘 다 `rounded-2xl` 고정) | `components/ui/button.tsx:8`, `components/ui/badge.tsx:8` |
| ❌ 카드에 `rounded-xl`/`rounded-2xl`을 직접 지정 | 컴포넌트 토큰과 어긋남 |

### 8-5. 색상 / 상태

| ✅ do | ❌ don't |
|---|---|
| 상태색은 `statusBadgeClass()` / `toneBadgeClass()`를 **호출**한다 (`lib/task-ui.ts`, `lib/badge-tone.ts`) | 페이지에서 `bg-green-100 text-green-800` 같은 임의 조합 작성 |
| 새 톤이 필요하면 `border-{색}-500/30 bg-{색}-500/10 text-{색}-600 dark:text-{색}-400` 공식을 따른다 | 불투명 배경(`bg-blue-500`)을 배지에 사용 |
| amber만 `dark:text-amber-500` (다른 색은 `-400`) | amber에 `dark:text-amber-400` 사용 |
| 중립/미설정 = `border-border bg-muted text-muted-foreground` | `text-gray-500` 직접 지정 |
| 파괴적 액션 = `text-destructive hover:text-destructive` | `text-red-600` 직접 지정 |
| 차트·진행률 채움은 `bg-chart-1` | `bg-blue-500` |
| **예외** 리포트 점수만 `text-green-600`/`text-yellow-600`/`text-red-500` 원색 | `app/reports/page.tsx:78-83` |
| **예외** 워크보드 readOnly 배너만 `bg-amber-50 dark:bg-amber-950/30` | `app/workboard/page.tsx:653` |

### 8-6. 타이포

| 역할 | 클래스 | 비고 |
|---|---|---|
| 페이지 H1 | `text-base font-medium leading-none` | 헤더바 전용 (`components/site-header.tsx:22`) |
| 페이지 설명 | **`mt-1 text-sm text-muted-foreground`** (정본 — § 8-6a 전수 집계) | `app/page.tsx:263` 외 7곳 |
| 섹션 제목 | `text-sm font-medium` | CardTitle 기본(`text-base font-medium`)을 항상 `text-sm`으로 낮춘다 |
| 다이얼로그 제목 | `pr-8 text-lg leading-snug` / `pr-6 text-base leading-snug` | `components/task-detail-dialog.tsx:128` / `app/reports/page.tsx:317` |
| 상세 패널 제목 | `text-base font-semibold` | `app/mail/page.tsx:896` |
| 문서 제목 입력 | `text-2xl font-bold` | `app/workboard/page.tsx:682` |
| 스탯 수치 | `text-2xl font-semibold tabular-nums @[250px]/card:text-3xl` | `components/stat-card.tsx:52` |
| 큰 점수 | `text-3xl font-bold tabular-nums` | `app/reports/page.tsx:85` |
| 본문 | `text-sm` | Card가 이미 `text-sm` |
| 목록 2줄 본문 | `text-[13px]` | `app/mail/page.tsx:862`, `app/page.tsx:473` |
| 보조 | `text-xs text-muted-foreground` | 전역 |
| 미세(타임스탬프) | `text-[11px] text-muted-foreground` | `app/mail/page.tsx:857`, `app/page.tsx:442` |

**규칙**: 숫자에는 항상 `tabular-nums` (`components/stat-card.tsx:52`, `app/tasks/page.tsx:912`, `app/reports/page.tsx:85`, `:296`).
**규칙**: 배지 안 텍스트는 굵기를 낮춘다 — `className="font-normal"` (`app/employees/page.tsx:176`, `app/tasks/page.tsx:619`, `:651`, `:742`).

#### 8-6a. 페이지 설명 `<p>`의 `mt-1` — 전수 집계로 정본 확정

문서 내부에서 § 3-1 스켈레톤(`mt` 없음)과 § 8-6 표(`mt-1`)가 충돌했다. **앱의 페이지 헤더 설명 `<p>`를 전수 조사해 다수결로 확정한다.**

집계 대상 = 페이지 루트 최상단의 **화면 설명 한 줄**(카드 안 문구·빈 상태 문구·탭 패널 설명은 제외).

| `mt-1` 있음 (8) | `mt` 없음 (4) | 기타 (2) |
|---|---|---|
| `app/page.tsx:263` | `app/customers/page.tsx:342` | `app/reports/page.tsx:193` → `mt-0.5` |
| `app/settings/page.tsx:59` | `app/automation/page.tsx:208` | `app/wiki/page.tsx:98` → `mb-3` (전체높이 레이아웃) |
| `app/tools/page.tsx:261` | `app/employees/page.tsx:100` | |
| `app/calendar/page.tsx:152` | `app/quote-contract/page.tsx:280` | |
| `app/briefings/page.tsx:84` | | |
| `app/usage/page.tsx:158` | | |
| `app/documents/page.tsx:274` | | |
| `app/company/page.tsx:231` | | |

**정본: `<p className="mt-1 text-sm text-muted-foreground">`** — 8 : 4 다수결.

- `mt-1`(4px)은 헤더바 H1과 본문 사이 시각 간격을 맞추는 값이다. 페이지 본문에 H1이 없으므로(§ 0) 이 `<p>`가 사실상 첫 요소이고, `mt-1`이 셸의 `py-6` 위에 미세 오프셋을 얹는다.
- 제외 사례: `app/wiki/page.tsx:98`은 `h-[calc(100svh-7rem)]` 전체높이 레이아웃이라 `mb-3`으로 아래 간격을 준다 — 다른 패턴이므로 정본 판단에서 뺀다.
- § 3-1 스켈레톤은 이 정본을 반영해 `mt-1`로 갱신했다(원문과 다름을 해당 위치에 명시).

### 8-7. 상호작용

| ✅ do | 근거 |
|---|---|
| 클릭 가능 카드 = `cursor-pointer shadow-xs transition-shadow hover:shadow-md` | `app/reports/page.tsx:257`, `app/page.tsx:277` |
| 클릭 가능 표 행 = `<TableRow className="cursor-pointer" onClick={…}>` + 액션 셀에 `onClick={(e) => e.stopPropagation()}` | `app/customers/page.tsx:398-403`, `:438` |
| hover 노출 컨트롤 = 부모 `group`/`group/이름` + `opacity-0 transition-opacity group-hover:opacity-100` | `app/tasks/page.tsx:674`, `:681-686`, `:879` |
| 목록 행 hover = `transition-colors hover:bg-accent` / 표 행 = `hover:bg-muted/50`(컴포넌트 기본) | `app/mail/page.tsx:828`; `components/ui/table.tsx:60` |
| 로딩 중 액션은 `disabled={syncing}` + 아이콘 `animate-spin` | `app/customers/page.tsx:347-348` |
| 토스트는 `sonner`의 `toast.success` / `toast.error`, 실패 문구는 `` `${t("발송 실패")}: ${res.error ?? t("알 수 없음")}` `` | `app/mail/page.tsx:706-710`, `app/employees/page.tsx:64-69` |
| ❌ 삭제 확인 없이 즉시 삭제 | 확인은 `AlertDialog` (§ 7-13) |

### 8-8. i18n·문자열

| ✅ do | 근거 |
|---|---|
| 모든 사용자 문자열은 `const t = useT()`로 감싼다 — `{t("새로고침")}` | 전 페이지 (`@/lib/i18n`) |
| 하위 컴포넌트에서도 `useT()`를 각자 호출 (`const tc = useT()`) | `app/tasks/page.tsx:551`, `:642`, `:670` |
| 말줄임표는 U+2026 `…` | `app/mail/page.tsx:820`, `app/reports/page.tsx:241` |
| 빈 값 표기는 표에서 `"-"`, 상세/속성에서 `"—"`(em dash) | `app/customers/page.tsx:411` / `components/task-detail-dialog.tsx:153`, `app/tasks/page.tsx:744` |
| **예외** 목록형 일부가 `"동기화 중..."`(마침표 3개) 사용 | `app/documents/page.tsx:365`, `app/customers/page.tsx:373` |

---

## 9. 신규 화면 만들 때 순서

1. **유형 고르기** — 지표 요약이면 1, 좌우 탐색이면 2, 레코드 CRUD면 3, 상태별 분류면 4, 연동·환경이면 5, 집계·평가면 6.
2. 해당 유형의 **스켈레톤을 복붙**하고 데이터만 갈아끼운다.
3. 상태 화면 4종(로딩/빈/에러/미연결)을 § 7-7~7-9에서 골라 **먼저** 박는다.
4. 배지·버튼·아이콘 크기는 § 8-2~8-5 표에서 조회해 쓴다. 새 값 만들지 않는다.
5. 상태색이 필요하면 `lib/badge-tone.ts`의 `toneBadgeClass()`를 호출한다(새 클래스 문자열 작성 금지).

---

### 부록: 이 문서가 다루지 않은 것

- 사이드바(`components/app-sidebar.tsx`) 내부 구조 — **미확인**(본 문서 범위 밖)
- 차트 컴포넌트(`components/chart-tokens.tsx`) 내부 — **미확인**
- 캘린더 화면, 에이전트/조직도 화면(`components/org-chart.tsx`) — **미확인**
- 색 토큰 원본 정의(`app/globals.css`의 `--card`, `--chart-1`, `--radius-4xl` 실제 값) — **미확인**
