---
name: theme-system
description: "CSS Custom Properties 기반 디자인 토큰 시스템. MUI 팔레트 구조를 CSS 변수로 매핑하여 HTML 슬라이드 전용 테마를 구축. 색상, 간격, 그림자, radius, 그라데이션 토큰을 정의하고, 테마 전환(Light/Dark)을 지원."
---

# Theme System

HTML 슬라이드 전용 CSS Custom Properties 기반 디자인 토큰 시스템

## Core Purpose

**토큰 하나만 바꾸면 전체 슬라이드 테마가 바뀌는 시스템**

```
tokens.css 수정 -> 모든 슬라이드 자동 반영
  --color-primary    -> 제목, 강조, CTA
  --font-heading     -> 모든 제목
  --section-gap       -> 모든 섹션 간격
  --radius-card       -> 모든 카드 모서리
```

## Token Architecture

### 3-Layer Token Structure

```
Layer 1: Primitive (원시값)
  --primitive-blue-500: #3B82F6;
  --primitive-gray-900: #111827;

Layer 2: Semantic (의미)
  --color-primary: var(--primitive-blue-500);
  --color-text-heading: var(--primitive-gray-900);

Layer 3: Component (컴포넌트)
  --card-bg: var(--color-surface-elevated);
  --button-bg: var(--color-primary);
```

CRITICAL: 슬라이드 HTML에서는 Layer 2(Semantic) 또는 Layer 3(Component) 토큰만 사용.
Layer 1(Primitive) 직접 참조 금지.

---

## Color Tokens

### MUI 팔레트 구조를 CSS 변수로 매핑

```css
/* theme/tokens.css */

:root {
  /* ===== Layer 1: Primitives ===== */
  /* 프로젝트별 색상 원시값 -- Design Cloner가 채움 */

  /* ===== Layer 2: Semantic Colors ===== */

  /* Brand */
  --color-primary: ;
  --color-primary-light: ;
  --color-primary-dark: ;
  --color-primary-contrast: ;
  --color-primary-rgb: ;          /* rgba()용 RGB 값 (예: 59, 130, 246) */

  --color-secondary: ;
  --color-secondary-light: ;
  --color-secondary-dark: ;
  --color-secondary-contrast: ;

  --color-accent: ;

  /* Surface (배경) */
  --color-surface-base: ;        /* 슬라이드 기본 배경 */
  --color-surface-elevated: ;    /* 카드, 패널 배경 */
  --color-surface-overlay: ;     /* 오버레이 배경 */
  --color-surface-inverse: ;     /* 반전 배경 (다크 섹션) */

  /* Text */
  --color-text-heading: ;        /* 제목 */
  --color-text-body: ;           /* 본문 */
  --color-text-muted: ;          /* 보조 설명 */
  --color-text-inverse: ;        /* 반전 배경 위 텍스트 */
  --color-text-accent: ;         /* 강조 텍스트 */
  --color-text-link: ;           /* 링크 */

  /* Status */
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* Border */
  --color-border-default: ;
  --color-border-subtle: ;
  --color-border-strong: ;

  /* Gradient */
  --gradient-primary: ;
  --gradient-subtle: ;
  --gradient-overlay: ;
  --gradient-hero: ;
}
```

### Dark Theme Override

```css
[data-theme="dark"] {
  --color-surface-base: #0F172A;
  --color-surface-elevated: #1E293B;
  --color-surface-overlay: rgba(0, 0, 0, 0.6);
  --color-surface-inverse: #F8FAFC;

  --color-text-heading: #F1F5F9;
  --color-text-body: #CBD5E1;
  --color-text-muted: #64748B;
  --color-text-inverse: #0F172A;

  --color-border-default: #334155;
  --color-border-subtle: #1E293B;
}
```

---

## Spacing Tokens

### 8px 기반 스케일 + Semantic 이름

```css
:root {
  /* Scale */
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */

  /* Semantic spacing */
  --slide-padding-x: var(--space-16);      /* 슬라이드 좌우 패딩 */
  --slide-padding-y: var(--space-12);      /* 슬라이드 상하 패딩 */
  --section-gap: var(--space-16);          /* 섹션 간 간격 */
  --content-gap: var(--space-6);           /* 콘텐츠 요소 간격 */
  --card-padding: var(--space-8);          /* 카드 내부 패딩 */
  --card-gap: var(--space-6);             /* 카드 간 간격 */
  --inline-gap: var(--space-3);           /* 인라인 요소 간격 */
}
```

---

## Radius Tokens

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;     /* 4px */
  --radius-md: 0.5rem;      /* 8px */
  --radius-lg: 0.75rem;     /* 12px */
  --radius-xl: 1rem;        /* 16px */
  --radius-2xl: 1.5rem;     /* 24px */
  --radius-full: 9999px;

  /* Semantic */
  --radius-card: var(--radius-xl);
  --radius-button: var(--radius-lg);
  --radius-badge: var(--radius-full);
  --radius-image: var(--radius-lg);
}
```

---

## Shadow Tokens

```css
:root {
  --shadow-none: none;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
               0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
               0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
               0 8px 10px -6px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

  /* Color shadow (브랜드 컬러 glow) */
  --shadow-glow: 0 0 20px rgba(var(--color-primary-rgb), 0.3);
  --shadow-glow-lg: 0 0 40px rgba(var(--color-primary-rgb), 0.4);

  /* Semantic */
  --shadow-card: var(--shadow-md);
  --shadow-card-hover: var(--shadow-xl);
  --shadow-button: var(--shadow-sm);
  --shadow-modal: var(--shadow-2xl);
}
```

---

## Z-Index Tokens

```css
:root {
  --z-base: 0;
  --z-elevated: 10;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;
  --z-tooltip: 600;
  --z-slide-controls: 700;
}
```

---

## Transition Tokens

```css
:root {
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-spring: 500ms cubic-bezier(0.16, 1, 0.3, 1);

  /* Semantic */
  --transition-hover: var(--transition-fast);
  --transition-expand: var(--transition-normal);
  --transition-slide: var(--transition-spring);
  --transition-page: 600ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## Theme File Structure

```
theme/
  tokens.css          -- 모든 토큰 정의 (위 내용 통합)
  typography.css      -- 폰트/타이포 (Typography System에서 생성)
  layout.css          -- 그리드/레이아웃 (Layout System에서 생성)
  motion.css          -- 애니메이션 (Motion System에서 생성)
  components.css      -- 컴포넌트 기본 스타일 (버튼, 카드, 뱃지 등)
  theme.css           -- @import 통합 파일
  dark.css            -- 다크 테마 오버라이드 (선택)
```

### components.css (기본 컴포넌트 스타일)

```css
/* theme/components.css */

/* Button */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--inline-gap);
  padding: var(--button-padding);
  background: var(--button-bg);
  color: var(--button-text);
  border: none;
  border-radius: var(--button-radius);
  box-shadow: var(--button-shadow);
  font-family: var(--font-body);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-hover);
}
.btn:hover {
  background: var(--button-hover-bg);
  box-shadow: var(--button-hover-shadow);
}

/* Card */
.card {
  background: var(--card-bg);
  border: var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: var(--card-padding);
  transition: transform var(--transition-hover), box-shadow var(--transition-hover);
}
.card:hover {
  box-shadow: var(--card-hover-shadow);
  transform: var(--card-hover-transform);
}

/* Badge */
.badge {
  display: inline-block;
  padding: var(--badge-padding);
  background: var(--badge-bg);
  color: var(--badge-text);
  border-radius: var(--badge-radius);
  font-size: var(--text-caption);
  font-weight: 600;
}

/* Divider */
.divider {
  border: none;
  border-top: var(--divider-width) solid var(--divider-color);
  margin: var(--content-gap) 0;
}

/* Slide Controls */
.slide-controls {
  position: fixed;
  bottom: var(--space-6);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-2) var(--space-4);
  background: var(--controls-bg);
  color: var(--controls-text);
  border-radius: var(--controls-radius);
  z-index: var(--z-slide-controls);
}
.slide-controls button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1.2rem;
  padding: var(--space-1);
}
```

### theme.css (통합)

```css
/* theme/theme.css */
@import './tokens.css';
@import './typography.css';
@import './layout.css';
@import './motion.css';
@import './components.css';
```

---

## Component Token Mapping

### 컴포넌트별 CSS 변수 (Layer 3)

```css
:root {
  /* Button */
  --button-bg: var(--color-primary);
  --button-text: var(--color-primary-contrast);
  --button-radius: var(--radius-button);
  --button-padding: var(--space-3) var(--space-6);
  --button-shadow: var(--shadow-button);
  --button-hover-bg: var(--color-primary-dark);
  --button-hover-shadow: var(--shadow-md);

  /* Card */
  --card-bg: var(--color-surface-elevated);
  --card-border: 1px solid var(--color-border-subtle);
  --card-radius: var(--radius-card);
  --card-shadow: var(--shadow-card);
  --card-hover-shadow: var(--shadow-card-hover);
  --card-hover-transform: translateY(-4px);

  /* Badge */
  --badge-bg: var(--color-primary-light);
  --badge-text: var(--color-primary-dark);
  --badge-radius: var(--radius-badge);
  --badge-padding: var(--space-1) var(--space-3);

  /* Divider */
  --divider-color: var(--color-border-subtle);
  --divider-width: 1px;

  /* Slide Controls */
  --controls-bg: rgba(0, 0, 0, 0.5);
  --controls-text: #FFFFFF;
  --controls-radius: var(--radius-full);
}
```

---

## Theme Switching (JS)

```javascript
// scripts/theme-controller.js
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('slide-theme', theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
}

// 초기 테마 적용
const savedTheme = localStorage.getItem('slide-theme') || 'light';
setTheme(savedTheme);
```

---

## Design Cloner Integration Point

Design Cloner가 이미지를 분석한 후, 이 토큰 구조에 값을 채운다:

```
Design Cloner 출력 -> tokens.css 값 채움
  이미지 분석 "선명한 파란색 CTA" -> --color-primary: #3B82F6;
  이미지 분석 "밝은 배경" -> --color-surface-base: #FFFFFF;
  이미지 분석 "둥근 카드" -> --radius-card: 1rem;
```

CRITICAL: Design Cloner는 반드시 이 토큰 구조를 따라야 한다.
커스텀 변수명 생성 금지.

---

## Quality Checklist

- [ ] 모든 색상이 CSS 변수로 정의됨
- [ ] Semantic 토큰 네이밍 일관성
- [ ] Dark 테마 오버라이드 완성
- [ ] 접근성: 텍스트/배경 대비 4.5:1 이상
- [ ] 하드코딩된 값 없음 (슬라이드 HTML에서)
- [ ] theme.css import 순서 정확

## Don't Do This

- 슬라이드 HTML에서 색상 직접 하드코딩
- Primitive 토큰을 컴포넌트에서 직접 참조
- !important 사용
- 토큰 네이밍에 색상명 사용 (--blue 대신 --primary)
- CSS 변수 없이 인라인 스타일
