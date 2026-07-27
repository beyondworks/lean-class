# Storybook Generator Agent

Storybook v8 설정 및 컴포넌트 Story 자동 생성

## Storybook 설정 파일

### main.ts

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-onboarding',
    '@storybook/addon-essentials',
    '@chromatic-com/storybook',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    '@storybook/addon-viewport',
    '@storybook/addon-themes',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  typescript: {
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      shouldRemoveUndefinedFromOptional: true,
      propFilter: (prop) =>
        prop.parent ? !/node_modules/.test(prop.parent.fileName) : true,
    },
  },
  docs: {
    autodocs: 'tag',
  },
};

export default config;
```

### preview.tsx

```typescript
// .storybook/preview.tsx
import type { Preview } from '@storybook/react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { withThemeFromJSXProvider } from '@storybook/addon-themes';
import { theme, darkTheme } from '../src/theme';

// 뷰포트 설정
const customViewports = {
  mobile: {
    name: 'Mobile',
    styles: { width: '375px', height: '667px' },
  },
  tablet: {
    name: 'Tablet',
    styles: { width: '768px', height: '1024px' },
  },
  desktop: {
    name: 'Desktop',
    styles: { width: '1280px', height: '800px' },
  },
  wide: {
    name: 'Wide',
    styles: { width: '1920px', height: '1080px' },
  },
};

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      expanded: true,
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    viewport: {
      viewports: customViewports,
    },
    layout: 'centered',
    docs: {
      toc: true,
    },
  },
  decorators: [
    withThemeFromJSXProvider({
      themes: {
        light: theme,
        dark: darkTheme,
      },
      defaultTheme: 'light',
      Provider: ThemeProvider,
      GlobalStyles: CssBaseline,
    }),
  ],
  tags: ['autodocs'],
};

export default preview;
```

### manager.ts

```typescript
// .storybook/manager.ts
import { addons } from '@storybook/manager-api';
import { create } from '@storybook/theming/create';

const aiduTheme = create({
  base: 'light',
  
  // 브랜드
  brandTitle: '@aidu/design-system',
  brandUrl: 'https://aidu.design',
  brandTarget: '_self',
  
  // 색상
  colorPrimary: '#3B82F6',
  colorSecondary: '#6366F1',
  
  // UI
  appBg: '#F8FAFC',
  appContentBg: '#FFFFFF',
  appBorderColor: '#E2E8F0',
  appBorderRadius: 8,
  
  // 텍스트
  textColor: '#1E293B',
  textInverseColor: '#FFFFFF',
  
  // 툴바
  barTextColor: '#64748B',
  barSelectedColor: '#3B82F6',
  barBg: '#FFFFFF',
  
  // 폼
  inputBg: '#FFFFFF',
  inputBorder: '#CBD5E1',
  inputTextColor: '#1E293B',
  inputBorderRadius: 6,
});

addons.setConfig({
  theme: aiduTheme,
  sidebar: {
    showRoots: true,
  },
});
```

## Story 템플릿

### 기본 컴포넌트 Story

```typescript
// src/components/atoms/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: '기본 버튼 컴포넌트. MUI Button을 래핑하여 디자인 시스템 토큰을 적용합니다.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['contained', 'outlined', 'text'],
      description: '버튼 스타일 변형',
      table: {
        defaultValue: { summary: 'contained' },
      },
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: '버튼 크기',
      table: {
        defaultValue: { summary: 'medium' },
      },
    },
    color: {
      control: 'select',
      options: ['primary', 'secondary', 'error', 'warning', 'info', 'success'],
      description: '버튼 색상',
      table: {
        defaultValue: { summary: 'primary' },
      },
    },
    disabled: {
      control: 'boolean',
      description: '비활성화 상태',
    },
    fullWidth: {
      control: 'boolean',
      description: '전체 너비 사용',
    },
  },
  args: {
    onClick: fn(),
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// 기본 스토리
export const Default: Story = {
  args: {
    children: 'Button',
    variant: 'contained',
  },
};

// 변형별 스토리
export const Contained: Story = {
  args: {
    children: 'Contained',
    variant: 'contained',
  },
};

export const Outlined: Story = {
  args: {
    children: 'Outlined',
    variant: 'outlined',
  },
};

export const Text: Story = {
  args: {
    children: 'Text',
    variant: 'text',
  },
};

// 크기별 스토리
export const Small: Story = {
  args: {
    children: 'Small',
    size: 'small',
  },
};

export const Large: Story = {
  args: {
    children: 'Large',
    size: 'large',
  },
};

// 색상별 스토리
export const Secondary: Story = {
  args: {
    children: 'Secondary',
    color: 'secondary',
  },
};

export const Error: Story = {
  args: {
    children: 'Error',
    color: 'error',
  },
};

// 상태 스토리
export const Disabled: Story = {
  args: {
    children: 'Disabled',
    disabled: true,
  },
};

// 모든 변형 비교
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
      <Button variant="contained">Contained</Button>
      <Button variant="outlined">Outlined</Button>
      <Button variant="text">Text</Button>
    </div>
  ),
};
```

### Organism 컴포넌트 Story

```typescript
// src/components/organisms/HeroSection/HeroSection.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { HeroSection } from './HeroSection';

const meta: Meta<typeof HeroSection> = {
  title: 'Organisms/HeroSection',
  component: HeroSection,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: '랜딩 페이지 히어로 섹션. 타이틀, 서브타이틀, CTA 버튼을 포함합니다.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    title: {
      control: 'text',
      description: '메인 타이틀',
    },
    subtitle: {
      control: 'text',
      description: '서브 타이틀',
    },
    ctaText: {
      control: 'text',
      description: 'CTA 버튼 텍스트',
    },
    background: {
      control: 'select',
      options: ['default', 'paper', 'primary'],
      description: '배경 스타일',
    },
  },
  args: {
    onCtaClick: fn(),
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: 'Build Something Amazing',
    subtitle: 'Create beautiful, responsive designs with our design system.',
    ctaText: 'Get Started',
  },
};

export const WithPrimaryBackground: Story = {
  args: {
    title: 'Welcome to AIDU',
    subtitle: 'Your complete design system solution.',
    ctaText: 'Learn More',
    background: 'primary',
  },
};

export const Minimal: Story = {
  args: {
    title: 'Simple. Elegant.',
    ctaText: 'Explore',
  },
};

// 반응형 테스트
export const Mobile: Story = {
  args: {
    title: 'Mobile First',
    subtitle: 'Responsive design for all devices.',
    ctaText: 'Try Now',
  },
  parameters: {
    viewport: {
      defaultViewport: 'mobile',
    },
  },
};
```

## 문서 페이지 (MDX)

### 소개 페이지

```mdx
{/* src/docs/Introduction.mdx */}
import { Meta } from '@storybook/blocks';

<Meta title="Introduction" />

# @aidu/design-system

MUI 기반의 토큰화된 디자인 시스템입니다.

## 특징

- **토큰 기반**: 색상, 타이포그래피, 간격 등 모든 값이 토큰으로 관리됩니다.
- **테마 변경**: 토큰 파일만 수정하면 전체 디자인이 변경됩니다.
- **MUI 호환**: Material UI와 완벽하게 호환됩니다.
- **반응형**: 모든 컴포넌트가 반응형으로 설계되었습니다.

## 설치

```bash
pnpm add @aidu/design-system
```

## 사용법

```tsx
import { ThemeProvider, Button } from '@aidu/design-system';

function App() {
  return (
    <ThemeProvider>
      <Button variant="contained">Click me</Button>
    </ThemeProvider>
  );
}
```
```

### 토큰 문서

```mdx
{/* src/docs/Tokens.mdx */}
import { Meta, ColorPalette, ColorItem } from '@storybook/blocks';
import { colors } from '../theme/tokens';

<Meta title="Tokens/Colors" />

# Color Tokens

디자인 시스템의 색상 토큰입니다.

## Primary Colors

<ColorPalette>
  <ColorItem
    title="Primary"
    subtitle="주요 브랜드 색상"
    colors={{
      Main: colors.primary.main,
      Light: colors.primary.light,
      Dark: colors.primary.dark,
    }}
  />
</ColorPalette>

## Secondary Colors

<ColorPalette>
  <ColorItem
    title="Secondary"
    subtitle="보조 색상"
    colors={{
      Main: colors.secondary.main,
      Light: colors.secondary.light,
      Dark: colors.secondary.dark,
    }}
  />
</ColorPalette>
```

## package.json 스크립트

```json
{
  "scripts": {
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "test-storybook": "test-storybook"
  }
}
```

## 의존성

```json
{
  "devDependencies": {
    "storybook": "^8.4.0",
    "@storybook/react-vite": "^8.4.0",
    "@storybook/addon-essentials": "^8.4.0",
    "@storybook/addon-interactions": "^8.4.0",
    "@storybook/addon-a11y": "^8.4.0",
    "@storybook/addon-viewport": "^8.4.0",
    "@storybook/addon-themes": "^8.4.0",
    "@storybook/test": "^8.4.0",
    "@chromatic-com/storybook": "^3.0.0"
  }
}
```

## Story 생성 체크리스트

### 필수 항목
- [ ] Meta 설정 (title, component, tags)
- [ ] Default 스토리
- [ ] argTypes 정의 (모든 props)
- [ ] JSDoc 설명

### 권장 항목
- [ ] 변형별 스토리 (variants)
- [ ] 크기별 스토리 (sizes)
- [ ] 색상별 스토리 (colors)
- [ ] 상태별 스토리 (states)
- [ ] 반응형 스토리 (viewport)
- [ ] 조합 스토리 (AllVariants)

### 문서화
- [ ] 컴포넌트 설명
- [ ] 사용 예시
- [ ] Props 테이블
- [ ] 접근성 정보
