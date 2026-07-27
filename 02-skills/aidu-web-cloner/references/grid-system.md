# Grid System

그리드 시스템 분석 및 토큰화

## 그리드 구성 요소

```
│← Margin →│←──────── Container ────────→│← Margin →│
│          │                              │          │
│          │ Col │ Gutter │ Col │ Gutter │          │
│          │  1  │        │  2  │        │          │
│          │     │        │     │        │          │
```

### 구성 요소 정의

- **Margin**: 화면 가장자리 여백 (반응형)
- **Container**: 콘텐츠 최대 너비
- **Column**: 콘텐츠가 배치되는 영역
- **Gutter**: 컬럼 사이 간격

## 표준 그리드 프리셋

### 12컬럼 시스템 (가장 일반적)

```typescript
export const grid = {
  columns: 12,
  
  container: {
    sm: 540,
    md: 720,
    lg: 960,
    xl: 1140,
    xxl: 1320,
    // 또는 단일 값
    default: 1200,
  },
  
  gutter: {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
  },
  
  margin: {
    xs: 16,
    sm: 24,
    md: 32,
    lg: 'auto',
  },
};
```

### 컬럼 조합

| 요소 | 컬럼 배분 | 비율 |
|------|----------|------|
| 전체 너비 | 12 | 100% |
| 반반 | 6 + 6 | 50/50 |
| 1/3씩 | 4 + 4 + 4 | 33/33/33 |
| 1/4씩 | 3 + 3 + 3 + 3 | 25/25/25/25 |
| 사이드바 | 3 + 9 | 25/75 |
| 넓은 사이드바 | 4 + 8 | 33/67 |

## 스크린샷 분석 방법

### 1단계: 컨테이너 너비 추정

```
격자 오버레이로 콘텐츠 영역 측정

일반적인 값:
- 960px: 작은 컨테이너
- 1140px: Bootstrap 기본
- 1200px: 일반적
- 1280px: Material Design
- 1440px: 와이드
```

### 2단계: 컬럼 수 추정

```
카드/요소 배치 패턴 관찰:

- 3개 나란히 → 12컬럼 (각 4컬럼)
- 4개 나란히 → 12컬럼 (각 3컬럼)
- 2개 비대칭 → 12컬럼 (8+4 또는 9+3)
```

### 3단계: 거터 측정

```
요소 사이 간격 측정:

- 16px: 촘촘한 레이아웃
- 20px: Bootstrap 기본
- 24px: 일반적
- 32px: 여유로운 레이아웃
```

### 4단계: 마진 측정

```
콘텐츠와 화면 가장자리 사이:

데스크톱: auto (중앙 정렬)
태블릿: 32px
모바일: 16-24px
```

## 격자 분석 스크립트

```bash
# 초기 추정값으로 분석
python scripts/grid_analyzer.py screenshot.png \
    --columns 12 \
    --gutter 24 \
    --margin 32 \
    --container 1200

# 결과 확인 후 조정
python scripts/grid_analyzer.py screenshot.png \
    --columns 12 \
    --gutter 20 \
    --margin 48 \
    --container 1140
```

## 반응형 그리드

### 브레이크포인트

```typescript
export const breakpoints = {
  xs: 0,
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  xxl: 1536,
};
```

### 반응형 컬럼 변화

```
Desktop (1024px+): 12컬럼 → 4개 카드
Tablet (768px):    8컬럼 → 2개 카드  
Mobile (< 640px):  4컬럼 → 1개 카드
```

### 반응형 거터/마진

```typescript
export const responsiveGrid = {
  gutter: {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
  },
  margin: {
    xs: 16,
    sm: 24,
    md: 32,
    lg: 48,
  },
  container: {
    xs: '100%',
    sm: 540,
    md: 720,
    lg: 960,
    xl: 1140,
  },
};
```

## 레이아웃 패턴

### 표준 레이아웃

```typescript
export const layouts = {
  // 풀 너비
  full: {
    cols: 12,
  },
  
  // 중앙 콘텐츠
  centered: {
    cols: 8,
    offset: 2,
  },
  
  // 좁은 콘텐츠 (블로그)
  narrow: {
    cols: 6,
    offset: 3,
    maxWidth: 720,
  },
  
  // 사이드바 레이아웃
  withSidebar: {
    main: 8,
    sidebar: 4,
  },
  
  // 넓은 사이드바
  withWideSidebar: {
    main: 9,
    sidebar: 3,
  },
};
```

### 카드 그리드

```typescript
export const cardGrids = {
  // 2컬럼
  two: {
    xs: { cols: 1 },
    sm: { cols: 2 },
  },
  
  // 3컬럼
  three: {
    xs: { cols: 1 },
    sm: { cols: 2 },
    md: { cols: 3 },
  },
  
  // 4컬럼
  four: {
    xs: { cols: 1 },
    sm: { cols: 2 },
    md: { cols: 3 },
    lg: { cols: 4 },
  },
};
```

## MUI Grid 변환

### Container

```tsx
import { Container } from '@mui/material';

<Container 
  maxWidth="lg"  // 1200px
  sx={{ 
    px: { xs: 2, sm: 3, md: 4 } // 반응형 패딩
  }}
>
  {children}
</Container>
```

### Grid2

```tsx
import { Grid2 as Grid } from '@mui/material';

// 3컬럼 카드 그리드
<Grid container spacing={3}> {/* spacing * 8 = 24px */}
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Card />
  </Grid>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Card />
  </Grid>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Card />
  </Grid>
</Grid>

// 사이드바 레이아웃
<Grid container spacing={4}>
  <Grid size={{ xs: 12, md: 8 }}>
    <MainContent />
  </Grid>
  <Grid size={{ xs: 12, md: 4 }}>
    <Sidebar />
  </Grid>
</Grid>
```

### 테마 설정

```typescript
const theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
  
  components: {
    MuiContainer: {
      defaultProps: {
        maxWidth: 'lg',
      },
      styleOverrides: {
        root: {
          paddingLeft: 24,
          paddingRight: 24,
          '@media (max-width: 640px)': {
            paddingLeft: 16,
            paddingRight: 16,
          },
        },
      },
    },
  },
});
```

## 출력 형식

### tokens/grid.ts

```typescript
export const grid = {
  columns: 12,
  
  breakpoints: {
    xs: 0,
    sm: 640,
    md: 768,
    lg: 1024,
    xl: 1280,
    xxl: 1536,
  },
  
  container: {
    xs: '100%',
    sm: 540,
    md: 720,
    lg: 960,
    xl: 1140,
    xxl: 1320,
    default: 1200,
  },
  
  gutter: {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
  },
  
  margin: {
    xs: 16,
    sm: 24,
    md: 32,
    lg: 48,
  },
} as const;
```

## 분석 결과 예시

```markdown
## 그리드 분석 결과

### 컨테이너
- 최대 너비: 1200px
- 중앙 정렬 (margin: auto)

### 컬럼 구조
- 12컬럼 시스템
- 거터: 24px

### 반응형
- Desktop: 12컬럼, 1200px 컨테이너
- Tablet: 8컬럼, 전체 너비
- Mobile: 4컬럼, 전체 너비

### 마진
- Desktop: auto (중앙 정렬)
- Tablet: 32px
- Mobile: 16px

### 레이아웃 패턴
- 히어로: 풀 너비
- 콘텐츠: 중앙 정렬 (offset 2)
- 카드 그리드: 3컬럼 (md), 2컬럼 (sm), 1컬럼 (xs)
```

## 체크리스트

- [ ] 컨테이너 최대 너비 결정됨
- [ ] 컬럼 수 결정됨
- [ ] 거터 크기 결정됨
- [ ] 마진 결정됨
- [ ] 브레이크포인트 정의됨
- [ ] 반응형 규칙 정의됨
- [ ] MUI Grid 설정됨
