# Color Extractor

색상 추출 및 토큰화 규칙

## 추출 우선순위

```
1순위: 스크린샷 시각 분석 (톤, 느낌 파악)
2순위: CSS 변수 / Tailwind config (정확한 값)
3순위: 인라인 스타일, 클래스 (검증용)
4순위: 사용자 제공 HEX 값 (가장 정확)
```

## 색상 분류 체계

### Primary Colors

```typescript
primary: {
  main: string,      // 메인 브랜드 색상
  light: string,     // 밝은 변형 (hover 등)
  dark: string,      // 어두운 변형
  contrastText: string, // 위에 올라가는 텍스트
}
```

**식별 방법:**
- CTA 버튼에 사용되는 색상
- 로고에 사용되는 색상
- 가장 눈에 띄는 강조 색상

### Secondary Colors

```typescript
secondary: {
  main: string,
  light: string,
  dark: string,
  contrastText: string,
}
```

**식별 방법:**
- Primary와 함께 사용되는 보조 색상
- 아이콘, 배지 등에 사용
- 그라데이션의 끝 색상

### Accent Colors

```typescript
accent: {
  success: string,   // 성공, 완료 (초록 계열)
  warning: string,   // 경고 (노랑/오렌지)
  error: string,     // 오류 (빨강)
  info: string,      // 정보 (파랑)
}
```

### Neutral Colors

```typescript
neutral: {
  white: '#FFFFFF',
  gray50: string,    // 가장 밝은 회색 (배경)
  gray100: string,
  gray200: string,
  gray300: string,
  gray400: string,   // 비활성 텍스트
  gray500: string,
  gray600: string,   // 보조 텍스트
  gray700: string,
  gray800: string,   // 본문 텍스트
  gray900: string,   // 제목 텍스트
  black: '#000000',
}
```

### Background Colors

```typescript
background: {
  default: string,   // 페이지 기본 배경
  paper: string,     // 카드, 모달 배경
  elevated: string,  // 떠있는 요소 배경
}
```

### Text Colors

```typescript
text: {
  primary: string,   // 제목, 중요 텍스트
  secondary: string, // 본문
  muted: string,     // 보조 설명
  disabled: string,  // 비활성
  inverse: string,   // 어두운 배경 위 텍스트
}
```

## 시각 분석 → HEX 변환

### 색상 느낌별 추정 가이드

#### 빨강 계열
| 느낌 | 추정 HEX |
|------|----------|
| 선명한 빨강 | #EF4444 |
| 부드러운 빨강 | #F87171 |
| 깊은 빨강 | #DC2626 |
| 코랄 | #FF6B6B |

#### 오렌지 계열
| 느낌 | 추정 HEX |
|------|----------|
| 선명한 오렌지 | #F97316 |
| 따뜻한 오렌지 | #FF6B35 |
| 부드러운 오렌지 | #FB923C |
| 피치 | #FDBA74 |

#### 노랑 계열
| 느낌 | 추정 HEX |
|------|----------|
| 선명한 노랑 | #EAB308 |
| 밝은 노랑 | #FDE047 |
| 골드 | #CA8A04 |

#### 초록 계열
| 느낌 | 추정 HEX |
|------|----------|
| 선명한 초록 | #22C55E |
| 민트/틸 | #14B8A6 |
| 에메랄드 | #10B981 |
| 깊은 초록 | #16A34A |

#### 파랑 계열
| 느낌 | 추정 HEX |
|------|----------|
| 선명한 파랑 | #3B82F6 |
| 하늘색 | #0EA5E9 |
| 네이비 | #1E3A8A |
| 인디고 | #4F46E5 |

#### 보라 계열
| 느낌 | 추정 HEX |
|------|----------|
| 선명한 보라 | #8B5CF6 |
| 라벤더 | #A78BFA |
| 깊은 보라 | #7C3AED |

#### 회색 계열
| 느낌 | 추정 HEX |
|------|----------|
| 거의 흰색 | #FAFAFA |
| 밝은 회색 | #F5F5F5 |
| 중간 회색 | #A3A3A3 |
| 진한 회색 | #525252 |
| 거의 검정 | #171717 |

## CSS에서 추출

### CSS 변수 패턴

```css
:root {
  --color-primary: #FF6B35;
  --color-secondary: #E8453C;
  --color-background: #FFFFFF;
  --color-text: #171717;
}
```

**추출:**
```typescript
colors.primary.main = '#FF6B35';
colors.secondary.main = '#E8453C';
colors.background.default = '#FFFFFF';
colors.text.primary = '#171717';
```

### Tailwind 클래스 패턴

```html
<button class="bg-orange-500 text-white">
```

**추출:**
```typescript
// Tailwind orange-500 = #F97316
colors.primary.main = '#F97316';
```

### 인라인 스타일 패턴

```html
<div style="background-color: #FF6B35;">
```

## 그라데이션 처리

### 단순 그라데이션

```css
background: linear-gradient(135deg, #FF6B35 0%, #E8453C 100%);
```

**추출:**
```typescript
colors.primary.main = '#FF6B35';      // 시작 색상
colors.secondary.main = '#E8453C';    // 끝 색상
colors.primary.gradient = 'linear-gradient(135deg, #FF6B35 0%, #E8453C 100%)';
```

### 복잡한 그라데이션

여러 색상이 포함된 경우 가장 dominant한 색상을 primary로 설정.

## 출력 형식

### 토큰 파일

```typescript
// src/theme/tokens/colors.ts

export const colors = {
  primary: {
    main: '#FF6B35',
    light: '#FF8F5E',
    dark: '#E85A2A',
    contrastText: '#FFFFFF',
  },
  
  secondary: {
    main: '#E8453C',
    light: '#FF6B6B',
    dark: '#C73A33',
    contrastText: '#FFFFFF',
  },
  
  neutral: {
    white: '#FFFFFF',
    gray50: '#FAFAFA',
    gray100: '#F5F5F5',
    gray200: '#E5E5E5',
    gray300: '#D4D4D4',
    gray400: '#A3A3A3',
    gray500: '#737373',
    gray600: '#525252',
    gray700: '#404040',
    gray800: '#262626',
    gray900: '#171717',
    black: '#000000',
  },
  
  background: {
    default: '#FFFFFF',
    paper: '#FAFAFA',
    elevated: '#FFFFFF',
  },
  
  text: {
    primary: '#171717',
    secondary: '#525252',
    muted: '#A3A3A3',
    disabled: '#D4D4D4',
    inverse: '#FFFFFF',
  },
  
  status: {
    success: '#22C55E',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#3B82F6',
  },
} as const;
```

### MUI 테마 변환

```typescript
// theme.ts
import { createTheme } from '@mui/material/styles';
import { colors } from './tokens/colors';

export const theme = createTheme({
  palette: {
    primary: {
      main: colors.primary.main,
      light: colors.primary.light,
      dark: colors.primary.dark,
      contrastText: colors.primary.contrastText,
    },
    secondary: {
      main: colors.secondary.main,
    },
    background: {
      default: colors.background.default,
      paper: colors.background.paper,
    },
    text: {
      primary: colors.text.primary,
      secondary: colors.text.secondary,
    },
    success: { main: colors.status.success },
    warning: { main: colors.status.warning },
    error: { main: colors.status.error },
    info: { main: colors.status.info },
  },
});
```

## 검증 체크리스트

- [ ] Primary 색상 식별됨
- [ ] Secondary 색상 식별됨
- [ ] Neutral 스케일 생성됨
- [ ] Background 색상 정의됨
- [ ] Text 색상 정의됨
- [ ] 시각 분석과 코드 값 일치 확인
- [ ] 접근성 대비 확인 (4.5:1 이상)
