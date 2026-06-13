---
name: layout-system
description: "16:9 슬라이드 비율 기반 그리드/레이아웃 시스템. 12-column 그리드, 안전 영역(Safe Area), 도형/이미지 배치, 반응형 규칙. PPT 레이아웃을 웹으로 충실히 재현."
---

# Layout System

16:9 HTML 슬라이드 전용 그리드 및 레이아웃 시스템

## Core Purpose

**PPT의 레이아웃 자유도를 웹에서 재현하되, CSS Grid/Flexbox의 강점 활용**

PPT는 절대좌표 기반, 웹은 플로우 기반 -- 이 갭을 메운다.

---

## Slide Canvas

### 16:9 비율 고정 캔버스

```css
/* theme/layout.css */

.slide-deck {
  --slide-width: 1280;
  --slide-height: 720;
  --slide-ratio: calc(var(--slide-width) / var(--slide-height));
}

.slide {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  max-width: 1280px;
  margin: 0 auto;
  overflow: hidden;
  background-color: var(--color-surface-base);
}

/* 전체화면 프레젠테이션 모드 */
.slide-deck.presentation-mode .slide {
  max-width: 100vw;
  max-height: 100vh;
  width: 100vw;
  height: 100vh;
  aspect-ratio: auto;
}
```

### Safe Area (안전 영역)

PPT와 마찬가지로 가장자리에 콘텐츠가 붙지 않도록:

```css
.slide-content {
  position: absolute;
  inset: 0;
  padding: var(--slide-padding-y) var(--slide-padding-x);
  display: flex;
  flex-direction: column;
}

/* Safe area 가이드 (개발 시 표시) */
.slide-content[data-guides] {
  outline: 1px dashed rgba(255, 0, 0, 0.3);
  outline-offset: calc(var(--slide-padding-x) * -1);
}
```

---

## Grid System

### 12-Column Grid

```css
.slide-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--card-gap);
  width: 100%;
  height: 100%;
  align-content: center;
}

/* Column span 유틸리티 */
.col-1  { grid-column: span 1; }
.col-2  { grid-column: span 2; }
.col-3  { grid-column: span 3; }
.col-4  { grid-column: span 4; }
.col-5  { grid-column: span 5; }
.col-6  { grid-column: span 6; }
.col-7  { grid-column: span 7; }
.col-8  { grid-column: span 8; }
.col-9  { grid-column: span 9; }
.col-10 { grid-column: span 10; }
.col-11 { grid-column: span 11; }
.col-12 { grid-column: span 12; }

/* Column start 유틸리티 */
.col-start-1  { grid-column-start: 1; }
.col-start-2  { grid-column-start: 2; }
.col-start-3  { grid-column-start: 3; }
.col-start-4  { grid-column-start: 4; }
.col-start-5  { grid-column-start: 5; }
.col-start-6  { grid-column-start: 6; }
.col-start-7  { grid-column-start: 7; }
```

---

## Layout Templates

### PPT 슬라이드 유형별 레이아웃

#### Type A: Title Slide (표지/섹션 구분)

```css
.layout-title {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  gap: var(--content-gap);
}

.layout-title .title-main {
  max-width: 80%;
}

.layout-title .title-sub {
  max-width: 60%;
}
```

```html
<div class="slide">
  <div class="slide-content layout-title">
    <span class="text-overline">CHAPTER 01</span>
    <h1 class="text-display-xl title-main">핵심 메시지</h1>
    <p class="text-body-lg title-sub">부제목 설명 텍스트</p>
  </div>
</div>
```

#### Type B: Content (텍스트 중심)

```css
.layout-content {
  display: flex;
  flex-direction: column;
  gap: var(--content-gap);
}

.layout-content .content-header {
  flex-shrink: 0;
}

.layout-content .content-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--content-gap);
}
```

#### Type C: Split (좌우 분할)

```css
.layout-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--section-gap);
  align-items: center;
  height: 100%;
}

/* 비대칭 분할 */
.layout-split-40-60 {
  grid-template-columns: 2fr 3fr;
}

.layout-split-60-40 {
  grid-template-columns: 3fr 2fr;
}

.layout-split-30-70 {
  grid-template-columns: 3fr 7fr;
}
```

```html
<div class="slide">
  <div class="slide-content layout-split">
    <div class="split-left">
      <h2 class="text-heading-lg">제목</h2>
      <p class="text-body">설명 텍스트</p>
    </div>
    <div class="split-right">
      <img src="image.jpg" class="slide-image" alt="" />
    </div>
  </div>
</div>
```

#### Type D: Cards Grid (카드 그리드)

```css
.layout-cards {
  display: flex;
  flex-direction: column;
  gap: var(--content-gap);
  height: 100%;
}

.layout-cards .cards-header {
  flex-shrink: 0;
  text-align: center;
}

.layout-cards .cards-grid {
  flex: 1;
  display: grid;
  gap: var(--card-gap);
  align-items: stretch;
}

/* 카드 개수별 자동 그리드 */
.cards-grid[data-cols="2"] { grid-template-columns: repeat(2, 1fr); }
.cards-grid[data-cols="3"] { grid-template-columns: repeat(3, 1fr); }
.cards-grid[data-cols="4"] { grid-template-columns: repeat(4, 1fr); }
.cards-grid[data-cols="2x2"] {
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
}
```

#### Type E: Data/Metrics (수치 강조)

```css
.layout-metrics {
  display: flex;
  flex-direction: column;
  gap: var(--content-gap);
  height: 100%;
}

.layout-metrics .metrics-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--card-gap);
  align-items: center;
}

.metric-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.metric-value {
  font-family: var(--font-display);
  font-size: var(--text-display-md);
  font-weight: var(--weight-extrabold);
  color: var(--color-primary);
  line-height: var(--leading-none);
}

.metric-label {
  font-size: var(--text-body-sm);
  color: var(--color-text-muted);
}
```

#### Type F: Timeline/Process (프로세스)

```css
.layout-timeline {
  display: flex;
  flex-direction: column;
  gap: var(--content-gap);
  height: 100%;
}

.timeline-track {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 0;
  position: relative;
}

.timeline-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-4);
  position: relative;
  padding: var(--space-4);
}

/* 연결선 */
.timeline-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 28px;  /* 아이콘 중앙 */
  right: 0;
  width: 50%;
  height: 2px;
  background: var(--color-border-default);
}

.timeline-step:not(:first-child)::before {
  content: '';
  position: absolute;
  top: 28px;
  left: 0;
  width: 50%;
  height: 2px;
  background: var(--color-border-default);
}

.timeline-number {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: var(--color-primary-contrast);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--weight-bold);
  font-size: var(--text-heading-sm);
  position: relative;
  z-index: 1;
}
```

#### Type G: Full Image (전체 이미지)

```css
.layout-fullimage {
  position: relative;
  height: 100%;
}

.layout-fullimage .bg-image {
  position: absolute;
  inset: 0;
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.layout-fullimage .overlay {
  position: absolute;
  inset: 0;
  background: var(--gradient-overlay);
}

.layout-fullimage .overlay-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: var(--slide-padding-y) var(--slide-padding-x);
  color: var(--color-text-inverse);
}
```

---

## Shape Primitives

### 기본 도형

```css
/* 원형 */
.shape-circle {
  border-radius: var(--radius-full);
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 둥근 사각형 */
.shape-rounded {
  border-radius: var(--radius-xl);
}

/* 알약형 */
.shape-pill {
  border-radius: var(--radius-full);
  padding: var(--space-2) var(--space-6);
}

/* 구분선 */
.shape-divider {
  width: 100%;
  height: var(--divider-width);
  background: var(--divider-color);
}

.shape-divider-accent {
  width: 80px;
  height: 4px;
  background: var(--color-primary);
  border-radius: var(--radius-full);
}

/* 장식 도트 */
.shape-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: var(--color-primary);
}

/* 아이콘 컨테이너 */
.shape-icon-box {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.shape-icon-box-lg {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
}
```

---

## Image Handling

```css
/* 슬라이드 내 이미지 */
.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--radius-image);
}

.slide-image-contain {
  object-fit: contain;
}

/* 이미지 + 오버레이 */
.image-overlay {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-image);
}

.image-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    transparent 50%,
    rgba(0, 0, 0, 0.6) 100%
  );
}

/* 아바타 */
.avatar {
  border-radius: var(--radius-full);
  object-fit: cover;
}
.avatar-sm { width: 32px; height: 32px; }
.avatar-md { width: 48px; height: 48px; }
.avatar-lg { width: 64px; height: 64px; }
.avatar-xl { width: 96px; height: 96px; }
```

---

## Alignment Utilities

```css
/* Flexbox 정렬 */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-col {
  display: flex;
  flex-direction: column;
}

.flex-row {
  display: flex;
  flex-direction: row;
}

.items-start    { align-items: flex-start; }
.items-center   { align-items: center; }
.items-end      { align-items: flex-end; }
.items-stretch  { align-items: stretch; }

.justify-start  { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end    { justify-content: flex-end; }
.justify-between { justify-content: space-between; }

.text-left   { text-align: left; }
.text-center { text-align: center; }
.text-right  { text-align: right; }

/* Gap */
.gap-sm { gap: var(--space-2); }
.gap-md { gap: var(--space-4); }
.gap-lg { gap: var(--space-6); }
.gap-xl { gap: var(--space-8); }
.gap-section { gap: var(--section-gap); }
```

---

## Responsive Rules

```css
/* 모바일 세로 보기 */
@media (max-width: 768px) {
  .slide {
    aspect-ratio: auto;
    min-height: 100vh;
    max-width: 100%;
  }

  .slide-content {
    padding: var(--space-8) var(--space-6);
  }

  .layout-split {
    grid-template-columns: 1fr;
    gap: var(--content-gap);
  }

  .layout-split-40-60,
  .layout-split-60-40,
  .layout-split-30-70 {
    grid-template-columns: 1fr;
  }

  .cards-grid[data-cols="3"],
  .cards-grid[data-cols="4"] {
    grid-template-columns: 1fr;
  }

  .cards-grid[data-cols="2"] {
    grid-template-columns: 1fr;
  }

  .timeline-track {
    flex-direction: column;
  }
}

/* 태블릿 가로 */
@media (min-width: 769px) and (max-width: 1024px) {
  .cards-grid[data-cols="4"] {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## Quality Checklist

- [ ] 16:9 비율 유지 확인
- [ ] Safe Area 내 콘텐츠 배치
- [ ] 12-column 그리드 정렬
- [ ] 모바일 반응형 전환 자연스러움
- [ ] 이미지 object-fit 확인
- [ ] 도형 크기/비율 일관성
- [ ] 전체화면 모드 동작

## Don't Do This

- position: absolute로 모든 요소 배치 (PPT 방식 금지)
- 고정 px 크기로 슬라이드 사이즈 지정
- Safe Area 무시하고 가장자리에 콘텐츠 배치
- 반응형 미대응
- aspect-ratio 미지원 브라우저 고려 없이 배포
