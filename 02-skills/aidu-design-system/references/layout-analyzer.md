# Layout Analyzer Agent

레이아웃 시스템, 그리드, 브레이크포인트, 컨테이너 분석 및 생성

## 분석 대상

### 페이지 레이아웃 패턴 감지

```
1. 헤더-컨텐츠-푸터 (Standard)
2. 사이드바-컨텐츠 (Dashboard)
3. 풀스크린 섹션 (Landing)
4. 그리드 레이아웃 (Portfolio)
5. 매거진 레이아웃 (Blog)
```

### 섹션 패턴 감지

```
1. Hero Section - 전체 화면 또는 큰 영역
2. Feature Grid - 3-4 컬럼 그리드
3. CTA Section - 중앙 정렬 콜투액션
4. Testimonial - 카드 캐러셀 또는 그리드
5. Contact Form - 폼 + 정보
6. Footer - 멀티 컬럼 링크
```

## 그리드 시스템

### 12 컬럼 그리드 (기본)

```typescript
// src/layouts/Grid.tsx
import { Grid2 as Grid } from '@mui/material';
import { styled } from '@mui/material/styles';

export const GridContainer = styled(Grid)(({ theme }) => ({
  width: '100%',
}));

// 사용 예시
<GridContainer container spacing={3}>
  <Grid size={{ xs: 12, md: 6, lg: 4 }}>
    <Card />
  </Grid>
  <Grid size={{ xs: 12, md: 6, lg: 4 }}>
    <Card />
  </Grid>
  <Grid size={{ xs: 12, md: 6, lg: 4 }}>
    <Card />
  </Grid>
</GridContainer>
```

### 감지 패턴 → 그리드 매핑

| 감지 패턴 | 그리드 설정 |
|----------|------------|
| 3개 아이템 행 | `xs: 12, md: 4` |
| 4개 아이템 행 | `xs: 12, sm: 6, lg: 3` |
| 2컬럼 레이아웃 | `xs: 12, md: 6` |
| 사이드바 + 메인 | 사이드바: `xs: 12, md: 3`, 메인: `xs: 12, md: 9` |
| 비대칭 2컬럼 | `xs: 12, md: 5` + `xs: 12, md: 7` |

## 브레이크포인트 시스템

### MUI 기본 브레이크포인트

```typescript
// src/theme/tokens/breakpoints.ts
export const breakpoints = {
  values: {
    xs: 0,      // 모바일
    sm: 600,    // 태블릿 세로
    md: 900,    // 태블릿 가로
    lg: 1200,   // 데스크톱
    xl: 1536,   // 대형 데스크톱
  },
};
```

### 커스텀 브레이크포인트 감지

```css
/* 입력: CSS Media Query */
@media (max-width: 480px) { ... }
@media (min-width: 481px) and (max-width: 768px) { ... }
@media (min-width: 769px) and (max-width: 1024px) { ... }
@media (min-width: 1025px) and (max-width: 1440px) { ... }
@media (min-width: 1441px) { ... }
```

```typescript
// 출력: 커스텀 브레이크포인트
export const breakpoints = {
  values: {
    xs: 0,      // ~ 480px
    sm: 481,    // 481px ~ 768px
    md: 769,    // 769px ~ 1024px
    lg: 1025,   // 1025px ~ 1440px
    xl: 1441,   // 1441px ~
  },
};
```

## 컨테이너 시스템

### 기본 컨테이너

```typescript
// src/layouts/Container.tsx
import { Container as MuiContainer, ContainerProps } from '@mui/material';
import { styled } from '@mui/material/styles';

export const Container = styled(MuiContainer)(({ theme }) => ({
  paddingLeft: theme.spacing(2),
  paddingRight: theme.spacing(2),
  [theme.breakpoints.up('sm')]: {
    paddingLeft: theme.spacing(3),
    paddingRight: theme.spacing(3),
  },
  [theme.breakpoints.up('lg')]: {
    paddingLeft: theme.spacing(4),
    paddingRight: theme.spacing(4),
  },
}));

// maxWidth 프리셋
export const containerMaxWidths = {
  xs: 444,
  sm: 600,
  md: 900,
  lg: 1200,
  xl: 1536,
};
```

### 섹션 컨테이너

```typescript
// src/layouts/Section.tsx
import { Box, BoxProps } from '@mui/material';
import { styled } from '@mui/material/styles';

export interface SectionProps extends BoxProps {
  fullHeight?: boolean;
  centered?: boolean;
  background?: 'default' | 'paper' | 'primary';
}

export const Section = styled(Box, {
  shouldForwardProp: (prop) => 
    !['fullHeight', 'centered', 'background'].includes(prop as string),
})<SectionProps>(({ theme, fullHeight, centered, background = 'default' }) => ({
  width: '100%',
  paddingTop: theme.spacing(8),
  paddingBottom: theme.spacing(8),
  
  ...(fullHeight && {
    minHeight: '100vh',
  }),
  
  ...(centered && {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  }),
  
  ...(background === 'paper' && {
    backgroundColor: theme.palette.background.paper,
  }),
  
  ...(background === 'primary' && {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
  }),
  
  [theme.breakpoints.up('md')]: {
    paddingTop: theme.spacing(12),
    paddingBottom: theme.spacing(12),
  },
}));
```

## 레이아웃 패턴

### 1. Standard Layout (헤더-컨텐츠-푸터)

```typescript
// src/layouts/StandardLayout.tsx
import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

const LayoutRoot = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  minHeight: '100vh',
});

const Main = styled(Box)({
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
});

export interface StandardLayoutProps {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
}

export const StandardLayout = ({ header, footer, children }: StandardLayoutProps) => (
  <LayoutRoot>
    {header}
    <Main component="main">{children}</Main>
    {footer}
  </LayoutRoot>
);
```

### 2. Dashboard Layout (사이드바)

```typescript
// src/layouts/DashboardLayout.tsx
import { Box, Drawer } from '@mui/material';
import { styled } from '@mui/material/styles';

const SIDEBAR_WIDTH = 280;

const LayoutRoot = styled(Box)({
  display: 'flex',
  minHeight: '100vh',
});

const Sidebar = styled(Drawer)(({ theme }) => ({
  width: SIDEBAR_WIDTH,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: SIDEBAR_WIDTH,
    boxSizing: 'border-box',
    borderRight: `1px solid ${theme.palette.divider}`,
  },
}));

const MainContent = styled(Box)(({ theme }) => ({
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  marginLeft: SIDEBAR_WIDTH,
  [theme.breakpoints.down('md')]: {
    marginLeft: 0,
  },
}));

export interface DashboardLayoutProps {
  sidebar?: React.ReactNode;
  header?: React.ReactNode;
  children: React.ReactNode;
}

export const DashboardLayout = ({ sidebar, header, children }: DashboardLayoutProps) => (
  <LayoutRoot>
    <Sidebar variant="permanent" open>
      {sidebar}
    </Sidebar>
    <MainContent>
      {header}
      <Box component="main" sx={{ flex: 1, p: 3 }}>
        {children}
      </Box>
    </MainContent>
  </LayoutRoot>
);
```

### 3. Landing Layout (풀스크린 섹션)

```typescript
// src/layouts/LandingLayout.tsx
import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

const LayoutRoot = styled(Box)({
  '& > section': {
    scrollSnapAlign: 'start',
  },
});

export interface LandingLayoutProps {
  enableSnapScroll?: boolean;
  children: React.ReactNode;
}

export const LandingLayout = ({ enableSnapScroll, children }: LandingLayoutProps) => (
  <LayoutRoot
    sx={{
      ...(enableSnapScroll && {
        height: '100vh',
        overflowY: 'scroll',
        scrollSnapType: 'y mandatory',
      }),
    }}
  >
    {children}
  </LayoutRoot>
);
```

## Flexbox 유틸리티

```typescript
// src/layouts/Flex.tsx
import { Box, BoxProps } from '@mui/material';
import { styled } from '@mui/material/styles';

export interface FlexProps extends BoxProps {
  direction?: 'row' | 'column';
  align?: 'start' | 'center' | 'end' | 'stretch';
  justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
  wrap?: boolean;
  gap?: number;
}

const alignMap = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  stretch: 'stretch',
};

const justifyMap = {
  start: 'flex-start',
  center: 'center',
  end: 'flex-end',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
};

export const Flex = styled(Box, {
  shouldForwardProp: (prop) =>
    !['direction', 'align', 'justify', 'wrap', 'gap'].includes(prop as string),
})<FlexProps>(({
  theme,
  direction = 'row',
  align = 'stretch',
  justify = 'start',
  wrap = false,
  gap = 0,
}) => ({
  display: 'flex',
  flexDirection: direction,
  alignItems: alignMap[align],
  justifyContent: justifyMap[justify],
  flexWrap: wrap ? 'wrap' : 'nowrap',
  gap: theme.spacing(gap),
}));
```

## 레이아웃 인덱스

```typescript
// src/layouts/index.ts
export { Container } from './Container';
export { Section } from './Section';
export { StandardLayout } from './StandardLayout';
export { DashboardLayout } from './DashboardLayout';
export { LandingLayout } from './LandingLayout';
export { Flex } from './Flex';

// Grid는 MUI에서 직접 export
export { Grid2 as Grid } from '@mui/material';
```

## 분석 체크리스트

### 구조 분석
- [ ] 헤더/푸터 존재 여부
- [ ] 사이드바 존재 여부
- [ ] 섹션 구분 방식
- [ ] 네비게이션 위치

### 그리드 분석
- [ ] 컬럼 수 (2/3/4/6/12)
- [ ] 거터(gutter) 크기
- [ ] 반응형 변화 포인트

### 브레이크포인트 분석
- [ ] 사용된 미디어 쿼리
- [ ] 주요 변화 포인트
- [ ] 모바일 우선 여부

### 컨테이너 분석
- [ ] 최대 너비
- [ ] 패딩 값
- [ ] 반응형 패딩 변화
