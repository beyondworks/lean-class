# Token Extractor Agent

CSS/스타일 파일에서 디자인 토큰을 추출하여 MUI 테마 호환 형식으로 변환

## 입력 소스 우선순위

```
1. globals.css / global.css - CSS 변수 (--color-primary 등)
2. tailwind.config.js/ts - Tailwind 설정
3. theme.ts / theme.js - 기존 테마 파일
4. 컴포넌트 인라인 스타일 - 반복 사용 값 수집
5. styled-components / Emotion - 테마 값
```

## 추출 규칙

### 색상 (Colors)

**CSS 변수 패턴:**
```css
/* 입력 */
:root {
  --color-primary: #3B82F6;
  --color-primary-light: #60A5FA;
  --color-primary-dark: #2563EB;
  --text-primary: #1F2937;
  --text-secondary: #6B7280;
  --bg-primary: #FFFFFF;
  --bg-secondary: #F3F4F6;
}
```

**출력 형식:**
```typescript
// src/theme/tokens/colors.ts
export const colors = {
  primary: {
    main: '#3B82F6',
    light: '#60A5FA',
    dark: '#2563EB',
    contrastText: '#FFFFFF', // 자동 계산
  },
  secondary: {
    main: '#6B7280',
    light: '#9CA3AF',
    dark: '#4B5563',
    contrastText: '#FFFFFF',
  },
  text: {
    primary: '#1F2937',
    secondary: '#6B7280',
    disabled: '#9CA3AF',
  },
  background: {
    default: '#FFFFFF',
    paper: '#F3F4F6',
  },
  // MUI 필수 색상
  error: { main: '#EF4444', light: '#F87171', dark: '#DC2626' },
  warning: { main: '#F59E0B', light: '#FBBF24', dark: '#D97706' },
  info: { main: '#3B82F6', light: '#60A5FA', dark: '#2563EB' },
  success: { main: '#10B981', light: '#34D399', dark: '#059669' },
};
```

### 타이포그래피 (Typography)

**CSS 패턴 감지:**
```css
/* font-family 감지 */
body { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Poppins', sans-serif; }

/* font-size 감지 */
.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.text-2xl { font-size: 1.5rem; }
```

**출력 형식:**
```typescript
// src/theme/tokens/typography.ts
export const typography = {
  fontFamily: {
    base: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    heading: "'Poppins', 'Inter', sans-serif",
    mono: "'Fira Code', 'Consolas', monospace",
  },
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    md: '1rem',       // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem',// 30px
    '4xl': '2.25rem', // 36px
    '5xl': '3rem',    // 48px
  },
  fontWeight: {
    light: 300,
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    none: 1,
    tight: 1.25,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,
    loose: 2,
  },
  letterSpacing: {
    tighter: '-0.05em',
    tight: '-0.025em',
    normal: '0em',
    wide: '0.025em',
    wider: '0.05em',
  },
};
```

### 간격 (Spacing)

**감지 패턴:**
```css
/* padding, margin, gap 값에서 추출 */
padding: 4px;   → spacing.xs
padding: 8px;   → spacing.sm
padding: 16px;  → spacing.md
padding: 24px;  → spacing.lg
padding: 32px;  → spacing.xl
padding: 48px;  → spacing.xxl
```

**출력 형식:**
```typescript
// src/theme/tokens/spacing.ts
export const spacing = {
  px: '1px',
  0: '0px',
  0.5: '2px',
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',
  8: '32px',
  10: '40px',
  12: '48px',
  16: '64px',
  20: '80px',
  24: '96px',
};

// MUI spacing 함수용 기본값
export const spacingBase = 4; // theme.spacing(1) = 4px
```

### 라운드 (Border Radius)

```typescript
// src/theme/tokens/radius.ts
export const radius = {
  none: '0px',
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  '2xl': '24px',
  full: '9999px',
};
```

### 그림자 (Shadows)

```typescript
// src/theme/tokens/shadows.ts
export const shadows = {
  none: 'none',
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
};
```

### 브레이크포인트 (Breakpoints)

```typescript
// src/theme/tokens/breakpoints.ts
export const breakpoints = {
  values: {
    xs: 0,      // mobile
    sm: 600,    // tablet portrait
    md: 900,    // tablet landscape
    lg: 1200,   // desktop
    xl: 1536,   // large desktop
  },
};
```

## 토큰 인덱스 파일

```typescript
// src/theme/tokens/index.ts
export * from './colors';
export * from './typography';
export * from './spacing';
export * from './radius';
export * from './shadows';
export * from './breakpoints';

// 통합 토큰 객체
export const tokens = {
  colors,
  typography,
  spacing,
  radius,
  shadows,
  breakpoints,
} as const;

export type Tokens = typeof tokens;
```

## CSS 변수 변환 매핑

| CSS 변수 패턴 | 토큰 경로 |
|--------------|----------|
| `--color-*` | `colors.*` |
| `--text-*` | `colors.text.*` |
| `--bg-*` | `colors.background.*` |
| `--font-*` | `typography.fontFamily.*` |
| `--size-*` | `typography.fontSize.*` |
| `--spacing-*` | `spacing.*` |
| `--radius-*` | `radius.*` |
| `--shadow-*` | `shadows.*` |

## Tailwind 변환 매핑

| Tailwind 클래스 | 토큰 경로 |
|----------------|----------|
| `bg-blue-500` | `colors.primary.main` |
| `text-gray-900` | `colors.text.primary` |
| `text-sm` | `typography.fontSize.sm` |
| `font-bold` | `typography.fontWeight.bold` |
| `p-4` | `spacing.4` |
| `rounded-lg` | `radius.lg` |
| `shadow-md` | `shadows.md` |

## CRITICAL Rules

1. **일관성 유지**: 비슷한 값은 하나의 토큰으로 통합
   - `#3B82F6`, `#3b82f6`, `rgb(59, 130, 246)` → 하나의 primary.main

2. **semantic 명명**: 값이 아닌 용도로 이름 지정
   - ❌ `blue500` → ✅ `primary.main`
   - ❌ `gray100` → ✅ `background.paper`

3. **MUI 호환**: MUI 테마 구조와 일치해야 함

4. **기본값 제공**: 감지되지 않은 필수 토큰은 기본값 생성
