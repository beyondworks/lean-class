# Component Converter Agent

원본 컴포넌트(CSS/Tailwind 기반)를 MUI 래핑 컴포넌트로 변환

## 변환 원칙

### CRITICAL: 하드코딩 금지

```typescript
// ❌ 절대 금지
const Button = styled('button')({
  backgroundColor: '#3B82F6',  // 하드코딩 금지
  padding: '8px 16px',         // 하드코딩 금지
  borderRadius: '8px',         // 하드코딩 금지
});

// ✅ 올바른 방식
const Button = styled(MuiButton)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  padding: theme.spacing(1, 2),
  borderRadius: theme.shape.borderRadius,
}));
```

## 컴포넌트 분류 (Atomic Design)

### Atoms (기본 요소)
```
Button, IconButton, Input, TextField, Select,
Checkbox, Radio, Switch, Avatar, Badge, Chip,
Typography, Link, Icon, Divider, Skeleton
```

### Molecules (조합 요소)
```
Card, MenuItem, ListItem, Accordion, Alert,
Breadcrumbs, Pagination, Tabs, Tooltip, Snackbar,
SearchField, FormField, MediaCard
```

### Organisms (복합 요소)
```
Navigation, Header, Footer, Sidebar,
HeroSection, ContactSection, ServicesSection,
DataTable, Form, Modal, Drawer
```

### Templates (페이지 레이아웃)
```
DashboardLayout, LandingPage, AuthLayout,
BlogLayout, PortfolioLayout
```

## CSS → MUI 변환 규칙

### 기본 속성 매핑

| CSS 속성 | MUI/sx 변환 |
|---------|-------------|
| `display: flex` | `display: 'flex'` |
| `flex-direction: column` | `flexDirection: 'column'` |
| `justify-content: center` | `justifyContent: 'center'` |
| `align-items: center` | `alignItems: 'center'` |
| `gap: 16px` | `gap: 2` (theme.spacing 단위) |
| `padding: 16px` | `p: 2` 또는 `padding: 2` |
| `margin: 8px 16px` | `m: '8px 16px'` 또는 `margin: theme.spacing(1, 2)` |
| `width: 100%` | `width: '100%'` |
| `max-width: 1200px` | `maxWidth: 'lg'` 또는 `maxWidth: 1200` |

### 색상 변환

```typescript
// 입력: CSS
.button {
  background-color: #3B82F6;
  color: white;
  border: 1px solid #3B82F6;
}

// 출력: MUI sx
sx={{
  bgcolor: 'primary.main',
  color: 'primary.contrastText',
  border: 1,
  borderColor: 'primary.main',
}}
```

### 타이포그래피 변환

```typescript
// 입력: CSS
.heading {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  font-family: 'Poppins', sans-serif;
}

// 출력: MUI Typography
<Typography
  variant="h2"
  sx={{
    fontFamily: 'heading',
    fontWeight: 'bold',
    lineHeight: 'tight',
  }}
/>
```

### 반응형 변환

```typescript
// 입력: CSS Media Query
@media (min-width: 768px) {
  .container {
    padding: 32px;
  }
}

// 출력: MUI sx
sx={{
  p: { xs: 2, md: 4 },
}}

// 또는 styled
const Container = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  [theme.breakpoints.up('md')]: {
    padding: theme.spacing(4),
  },
}));
```

## 컴포넌트 구조 템플릿

### 기본 컴포넌트 구조

```typescript
// src/components/atoms/Button/Button.tsx
import { forwardRef } from 'react';
import { Button as MuiButton, ButtonProps as MuiButtonProps } from '@mui/material';
import { styled } from '@mui/material/styles';

export interface ButtonProps extends MuiButtonProps {
  // 커스텀 props 정의
}

const StyledButton = styled(MuiButton)(({ theme }) => ({
  // 기본 스타일 (토큰 참조만 사용)
  textTransform: 'none',
  borderRadius: theme.shape.borderRadius,
}));

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button(props, ref) {
    const { children, ...other } = props;
    return (
      <StyledButton ref={ref} {...other}>
        {children}
      </StyledButton>
    );
  }
);
```

### 타입 파일

```typescript
// src/components/atoms/Button/Button.types.ts
import { ButtonProps as MuiButtonProps } from '@mui/material';

export interface ButtonProps extends MuiButtonProps {
  /**
   * 버튼 크기
   * @default 'medium'
   */
  size?: 'small' | 'medium' | 'large';
  
  /**
   * 버튼 변형
   * @default 'contained'
   */
  variant?: 'contained' | 'outlined' | 'text';
  
  /**
   * 로딩 상태
   */
  loading?: boolean;
}
```

### 인덱스 파일

```typescript
// src/components/atoms/Button/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button.types';
```

## Organism 컴포넌트 변환 예시

### 원본 (Figma Make 출력)

```tsx
// 입력: HeroSection.tsx
export const HeroSection = () => {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <h1 className="hero-title">Welcome</h1>
        <p className="hero-subtitle">Description text</p>
        <button className="hero-cta">Get Started</button>
      </div>
    </section>
  );
};
```

### 변환 후 (MUI 래핑)

```tsx
// 출력: HeroSection.tsx
import { Box, Container, Typography, Button } from '@mui/material';
import { styled } from '@mui/material/styles';

const HeroRoot = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  display: 'flex',
  alignItems: 'center',
  backgroundColor: theme.palette.background.default,
}));

const HeroContent = styled(Box)(({ theme }) => ({
  textAlign: 'center',
  maxWidth: theme.breakpoints.values.md,
  margin: '0 auto',
}));

export interface HeroSectionProps {
  title?: string;
  subtitle?: string;
  ctaText?: string;
  onCtaClick?: () => void;
}

export const HeroSection = ({
  title = 'Welcome',
  subtitle = 'Description text',
  ctaText = 'Get Started',
  onCtaClick,
}: HeroSectionProps) => {
  return (
    <HeroRoot component="section">
      <Container maxWidth="lg">
        <HeroContent>
          <Typography
            variant="h1"
            sx={{
              mb: 2,
              fontWeight: 'bold',
            }}
          >
            {title}
          </Typography>
          <Typography
            variant="h5"
            color="text.secondary"
            sx={{ mb: 4 }}
          >
            {subtitle}
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={onCtaClick}
          >
            {ctaText}
          </Button>
        </HeroContent>
      </Container>
    </HeroRoot>
  );
};
```

## 변환 체크리스트

### 필수 변환 항목
- [ ] HTML 요소 → MUI 컴포넌트 (div→Box, button→Button 등)
- [ ] CSS 클래스 → sx prop 또는 styled()
- [ ] 하드코딩 값 → theme 참조
- [ ] 인라인 스타일 → sx prop
- [ ] className → sx 또는 styled

### Props 추출
- [ ] 텍스트 콘텐츠 → props로 분리
- [ ] 이벤트 핸들러 → callback props
- [ ] 조건부 스타일 → variant props
- [ ] 반복 데이터 → items props

### 타입 정의
- [ ] Props 인터페이스 정의
- [ ] JSDoc 주석 추가
- [ ] 기본값 정의

## Tailwind → MUI 클래스 매핑

| Tailwind | MUI sx |
|----------|--------|
| `flex` | `display: 'flex'` |
| `flex-col` | `flexDirection: 'column'` |
| `items-center` | `alignItems: 'center'` |
| `justify-center` | `justifyContent: 'center'` |
| `gap-4` | `gap: 2` |
| `p-4` | `p: 2` |
| `px-4` | `px: 2` |
| `py-2` | `py: 1` |
| `m-4` | `m: 2` |
| `mx-auto` | `mx: 'auto'` |
| `w-full` | `width: '100%'` |
| `h-screen` | `height: '100vh'` |
| `min-h-screen` | `minHeight: '100vh'` |
| `max-w-lg` | `maxWidth: 'lg'` |
| `text-center` | `textAlign: 'center'` |
| `text-left` | `textAlign: 'left'` |
| `font-bold` | `fontWeight: 'bold'` |
| `text-lg` | `fontSize: 'lg'` |
| `text-primary` | `color: 'primary.main'` |
| `bg-white` | `bgcolor: 'background.paper'` |
| `rounded-lg` | `borderRadius: 2` |
| `shadow-md` | `boxShadow: 2` |
| `hover:bg-gray-100` | `'&:hover': { bgcolor: 'grey.100' }` |
| `transition-all` | `transition: 'all 0.3s ease'` |

## CRITICAL Rules

1. **모든 값은 테마에서**: 색상, 간격, 폰트 모두 theme 참조
2. **styled() 우선**: 복잡한 스타일은 styled() 사용
3. **sx는 조건부**: 동적 스타일에만 sx 사용
4. **Props 분리**: 하드코딩된 텍스트는 props로 추출
5. **타입 필수**: 모든 컴포넌트에 TypeScript 타입 정의
