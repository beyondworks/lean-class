# Typography Analyzer

타이포그래피 분석 및 토큰화 규칙

## 분석 요소

### 1. 폰트 패밀리 식별

#### CSS에서 추출

```css
font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
```

#### 시각적 추정

| 특징 | 폰트 분류 | 대표 폰트 |
|------|----------|----------|
| 기하학적, 원형 글자 | Geometric Sans | Inter, Circular, Gilroy |
| 인간적, 약간의 곡선 | Humanist Sans | Open Sans, Noto Sans |
| 클래식, 세리프 있음 | Serif | Georgia, Merriweather |
| 모던, 각진 느낌 | Grotesque | Helvetica, Arial |
| 기술적, 고정폭 | Monospace | JetBrains Mono, Fira Code |

#### 한글 폰트 추정

| 특징 | 대표 폰트 |
|------|----------|
| 깔끔, 현대적 | Pretendard, Noto Sans KR |
| 부드러운 | Spoqa Han Sans |
| 전통적 | Nanum Gothic |

### 2. 폰트 웨이트

```typescript
fontWeight: {
  thin: 100,
  extralight: 200,
  light: 300,
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
  extrabold: 800,
  black: 900,
}
```

#### 시각적 판단

| 느낌 | 추정 웨이트 |
|------|------------|
| 매우 가벼움 | 300 (Light) |
| 기본 본문 | 400 (Regular) |
| 약간 두꺼움 | 500 (Medium) |
| 강조, 버튼 | 600 (Semibold) |
| 제목, 헤더 | 700 (Bold) |
| 매우 두꺼움 | 800 (Extrabold) |

### 3. 폰트 사이즈 스케일

#### 일반적인 스케일 (Major Third - 1.25)

```typescript
fontSize: {
  xs: '0.75rem',     // 12px
  sm: '0.875rem',    // 14px
  base: '1rem',      // 16px
  lg: '1.125rem',    // 18px
  xl: '1.25rem',     // 20px
  '2xl': '1.5rem',   // 24px
  '3xl': '1.875rem', // 30px
  '4xl': '2.25rem',  // 36px
  '5xl': '3rem',     // 48px
  '6xl': '3.75rem',  // 60px
  '7xl': '4.5rem',   // 72px
}
```

#### 시각적 추정

| 요소 | 일반적인 크기 |
|------|--------------|
| 캡션, 라벨 | 12-14px |
| 본문 | 16px |
| 큰 본문 | 18px |
| 소제목 | 20-24px |
| 섹션 제목 | 30-36px |
| 히어로 소 | 48px |
| 히어로 대 | 60-72px |

### 4. Line Height (줄간격)

```typescript
lineHeight: {
  none: 1,
  tight: 1.1,    // 대형 히어로 제목
  snug: 1.25,    // 제목
  normal: 1.5,   // 기본 본문
  relaxed: 1.625, // 긴 본문
  loose: 2,      // 매우 여유로운
}
```

#### 시각적 판단

| 느낌 | 추정 값 |
|------|--------|
| 글자가 붙어 보임 | 1.1-1.2 |
| 적당히 타이트 | 1.25-1.3 |
| 편안한 읽기 | 1.5-1.6 |
| 여유로운 | 1.75+ |

### 5. Letter Spacing (자간)

```typescript
letterSpacing: {
  tighter: '-0.05em',
  tight: '-0.025em',
  normal: '0',
  wide: '0.025em',
  wider: '0.05em',
  widest: '0.1em',
}
```

#### 일반 규칙

- 대형 제목: 약간 타이트 (-0.02em)
- 본문: 기본 (0)
- 버튼/라벨: 약간 넓게 (0.02em)
- 대문자: 넓게 (0.05em+)

## 텍스트 스타일 정의

### 시맨틱 스타일

```typescript
export const textStyles = {
  // 히어로 제목
  displayLarge: {
    fontFamily: 'primary',
    fontSize: '4.5rem',    // 72px
    fontWeight: 800,
    lineHeight: 1.1,
    letterSpacing: '-0.02em',
  },
  
  displayMedium: {
    fontFamily: 'primary',
    fontSize: '3.75rem',   // 60px
    fontWeight: 700,
    lineHeight: 1.1,
    letterSpacing: '-0.02em',
  },
  
  displaySmall: {
    fontFamily: 'primary',
    fontSize: '3rem',      // 48px
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.01em',
  },
  
  // 헤딩
  h1: {
    fontFamily: 'primary',
    fontSize: '2.25rem',   // 36px
    fontWeight: 700,
    lineHeight: 1.2,
  },
  
  h2: {
    fontFamily: 'primary',
    fontSize: '1.875rem',  // 30px
    fontWeight: 600,
    lineHeight: 1.3,
  },
  
  h3: {
    fontFamily: 'primary',
    fontSize: '1.5rem',    // 24px
    fontWeight: 600,
    lineHeight: 1.3,
  },
  
  h4: {
    fontFamily: 'primary',
    fontSize: '1.25rem',   // 20px
    fontWeight: 600,
    lineHeight: 1.4,
  },
  
  h5: {
    fontFamily: 'primary',
    fontSize: '1.125rem',  // 18px
    fontWeight: 600,
    lineHeight: 1.4,
  },
  
  h6: {
    fontFamily: 'primary',
    fontSize: '1rem',      // 16px
    fontWeight: 600,
    lineHeight: 1.4,
  },
  
  // 본문
  bodyLarge: {
    fontFamily: 'primary',
    fontSize: '1.125rem',  // 18px
    fontWeight: 400,
    lineHeight: 1.6,
  },
  
  body: {
    fontFamily: 'primary',
    fontSize: '1rem',      // 16px
    fontWeight: 400,
    lineHeight: 1.6,
  },
  
  bodySmall: {
    fontFamily: 'primary',
    fontSize: '0.875rem',  // 14px
    fontWeight: 400,
    lineHeight: 1.5,
  },
  
  // 캡션, 라벨
  caption: {
    fontFamily: 'primary',
    fontSize: '0.75rem',   // 12px
    fontWeight: 400,
    lineHeight: 1.4,
  },
  
  label: {
    fontFamily: 'primary',
    fontSize: '0.875rem',  // 14px
    fontWeight: 500,
    lineHeight: 1.4,
    letterSpacing: '0.02em',
  },
  
  // 버튼
  button: {
    fontFamily: 'primary',
    fontSize: '1rem',      // 16px
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '0.01em',
  },
  
  buttonSmall: {
    fontFamily: 'primary',
    fontSize: '0.875rem',  // 14px
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '0.01em',
  },
};
```

## MUI 테마 변환

```typescript
// theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, sans-serif',
    
    h1: {
      fontSize: '2.25rem',
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '1.875rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    caption: {
      fontSize: '0.75rem',
      lineHeight: 1.4,
    },
    button: {
      fontSize: '1rem',
      fontWeight: 600,
      textTransform: 'none',
      letterSpacing: '0.01em',
    },
  },
});
```

## 분석 출력 예시

```markdown
## 타이포그래피 분석

### 폰트 패밀리
- **추정**: Inter 또는 유사 Geometric Sans
- **특징**: 깔끔하고 현대적, 기하학적 형태
- **Fallback**: -apple-system, BlinkMacSystemFont, sans-serif

### 웨이트 사용
- 제목: Extra Bold (800)
- 섹션 타이틀: Bold (700)
- 소제목: Semibold (600)
- 본문: Regular (400)
- 버튼: Semibold (600)

### 사이즈 스케일
- 히어로 제목: 72px, 매우 임팩트 있음
- 섹션 제목: 48px
- 카드 제목: 24px
- 본문: 16-18px
- 캡션: 14px

### 특징
- 제목 줄간격이 타이트해서 덩어리감 있음
- 본문은 여유로운 줄간격으로 가독성 좋음
- 전체적으로 모던하고 깔끔한 인상
```

## 체크리스트

- [ ] 폰트 패밀리 식별/추정됨
- [ ] 웨이트 스케일 정의됨
- [ ] 사이즈 스케일 정의됨
- [ ] Line height 정의됨
- [ ] Letter spacing 정의됨
- [ ] 시맨틱 텍스트 스타일 정의됨
- [ ] MUI 테마 변환됨
