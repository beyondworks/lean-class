---
name: aidu-web-cloner
description: 웹사이트 URL과 스크린샷을 분석하여 MUI 기반 Storybook 디자인 시스템으로 변환하는 AI 에이전트. 격자 오버레이 분석으로 정확한 그리드/여백 추출. 시각 우선 분석으로 사람이 눈으로 본 듯한 디자인 토큰 생성.
allowed-tools: []
---

# AIDU Web Cloner

웹사이트를 분석하여 Production-Grade MUI 디자인 시스템 + Storybook으로 변환

## META INSTRUCTION

**IMPORTANT**: 이 문서의 모든 규칙은 프로젝트 법률이다.
- YOU MUST 코드 작업 전 관련 규칙을 확인하라.
- YOU MUST NOT 명시적 허용 없이 규칙을 위반하는 코드를 작성하지 마라.
- **지시된 기능만 구현 (CRITICAL)**: 요청하지 않은 기능, 옵션, 예외 처리를 임의로 추가하지 말 것.

### Single Source of Truth

이 SKILL.md 파일이 유일한 원본이다. 충돌 시 이 문서의 규칙이 우선한다.

### 규칙 우선순위

| 등급 | 의미 | 예시 |
|------|------|------|
| **CRITICAL** | 절대 위반 불가 | MUI Grid import, 토큰 재활용, 색상 제한 |
| **MUST** | 반드시 준수 | Storybook 구조, Props 문서화, forwardRef |
| **SHOULD** | 가능하면 준수 | 주석 스타일, 파일 정리 |

### 충돌 처리

사용자 요청이 규칙과 충돌할 경우:
1. 충돌 사실과 해당 규칙 알림
2. 구체적 충돌 내용 설명
3. 명시적 예외 허용 전까지 진행 금지

## 개요

```
┌─────────────────┐     ┌─────────────────┐
│   URL 입력      │     │  스크린샷 첨부   │
│  (HTML/CSS)     │  +  │  (시각적 분석)   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌─────────────────────┐
         │   Visual Analyzer   │
         │   (시각 우선 분석)   │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │   Semantic Tokens   │
         │   (목적 기반 토큰)   │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │   MUI Components    │
         │   + Documentation   │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │   Storybook v8      │
         │   Production-Ready  │
         └─────────────────────┘
```

---

## Part 1: 핵심 원칙

### 1.1 시각 우선, 코드 검증 (Visual First)

```
기존 방식: 코드 분석 → 시각 보완
    ↓
이 스킬:   시각 분석(주) → 코드 검증(보조)
```

### 1.2 디자인 시스템 재활용 (CRITICAL)

새로운 컴포넌트를 만들기 전 반드시:
1. 기존 컴포넌트로 대체 가능한지 확인
2. 불필요한 중복 컴포넌트 생성 금지
3. 디자인 토큰 우선 사용 (임의의 값 직접 지정 금지)

```jsx
// ❌ 잘못된 예 - 임의 값 사용
<Box sx={{ color: '#333', padding: '20px' }} />

// ✅ 올바른 예 - 토큰 참조
<Box sx={{ color: 'text.primary', p: SPACING.inset.md }} />
```

### 1.3 Semantic Token Naming (목적 기반 토큰)

```typescript
// ❌ 숫자 기반 (의미 불분명)
spacing: { 1: 4, 2: 8, 3: 16, 4: 24 }

// ✅ 목적 기반 (명확한 용도)
SPACING: {
  inset: { xs: 8, sm: 16, md: 24, lg: 32 },     // 컴포넌트 내부 패딩
  gap: { xs: 4, sm: 8, md: 16, lg: 24 },        // Flex/Grid 간격
  stack: { xs: 8, sm: 16, md: 24, lg: 32 },     // 수직 쌓기
  inline: { xs: 4, sm: 8, md: 16, lg: 24 },     // 수평 나열
  section: { sm: 24, md: 48, lg: 64, xl: 96 },  // 섹션 간격
  page: {
    gutter: { xs: 16, sm: 24, md: 32, lg: 48 }, // 페이지 좌우 여백
    top: { sm: 24, md: 48, lg: 64 },            // 상단 여백
    bottom: { sm: 24, md: 48, lg: 64 }          // 하단 여백
  }
}
```

### 1.4 색상 제한 (4-6색 팔레트)

```typescript
// ✅ 그래디언트/글로우/블러 금지, 4-6색 제한
palette: {
  background: { default: '#F5F2EE', paper: '#FFFFFF' },
  text: { primary: '#12100E', secondary: 'rgba(18,16,14,0.8)' },
  primary: { main: '#12100E' },      // 라이트 모드 텍스트/아이콘
  secondary: { main: '#FFC66E' }     // CTA, 액센트
}
```

---

## Part 2: 디렉토리 구조

```
src/
  components/           # 재사용 가능한 UI 컴포넌트 모음
    atoms/              # Button, Badge, Typography
    molecules/          # Card, NavigationItem
    organisms/          # Header, Hero, Footer
    templates/          # HeroStack, SplitScreen, GridLayout
    *.stories.jsx       # 각 컴포넌트의 Storybook 문서 (같은 위치)

  common/               # 공통 유틸 컴포넌트
    ui/                 # ArrowButton, Indicator 등
    media/              # MediaRenderer 등

  styles/               # 테마, 전역 스타일
    tokens.js           # SPACING, COLORS 등
    theme.js            # MUI 테마 설정
    ThemeProvider.jsx

  stories/              # 스토리북 문서 전용
    Overview.stories.jsx    # 프로젝트 개요
    style/                  # 디자인 토큰 문서
      Colors.stories.jsx
      Typography.stories.jsx
      Spacing.stories.jsx
      Icons.stories.jsx

  storybookDocumentation/   # 문서용 헬퍼 컴포넌트
    DocumentTitle.jsx
    PageContainer.jsx
    SectionTitle.jsx
    ColorSwatch.jsx
    TreeNode.jsx

.storybook/             # Storybook 설정
  main.js
  preview.jsx
```

---

## Part 3: Storybook 작성 규칙 (CRITICAL)

### 3.1 스토리 카테고리 구조

| 카테고리 | title 접두사 | 설명 |
|---------|-------------|------|
| **Style** | `Style/` | 디자인 토큰 문서 (색상, 타이포그래피, 간격 등) |
| **Atoms** | `Atoms/` | 기본 UI 컴포넌트 (Button, Badge, Typography) |
| **Molecules** | `Molecules/` | 복합 컴포넌트 (Card, NavigationItem) |
| **Organisms** | `Organisms/` | 섹션 컴포넌트 (Header, Footer, Hero) |
| **Templates** | `Templates/` | 레이아웃 템플릿 (HeroStack, SplitScreen) |
| **Pages** | `Pages/` | 전체 페이지 레벨 |

### 3.2 Story Sort Order

```javascript
// .storybook/preview.jsx
options: {
  storySort: {
    order: [
      'Overview',
      'Style', ['Colors', 'Typography', 'Spacing', 'Icons', '*'],
      'Atoms', ['Button', 'Badge', 'Typography', '*'],
      'Molecules',
      'Organisms',
      'Templates',
      'Pages',
      '*'
    ]
  }
}
```

### 3.3 필수 규칙 (MUST)

| Rule | Description |
|------|-------------|
| **First Story Named "Default"** | 첫 번째 스토리의 export 이름은 반드시 `Default` |
| **Single Component per Story** | 스토리 한 개당 단일 컴포넌트만 보여줌 |
| **Docs First with Controls** | 모든 props를 `argTypes`와 `control`로 조작 가능하게 |
| **Minimal Variations** | 과도한 스토리 베리에이션 금지 (1-3개 권장) |
| **Props Table Required** | 모든 스토리 Doc 최상단에 Props 테이블 표시 |
| **DocumentTitle English** | DocumentTitle의 모든 props 값은 영어로 작성 |
| **Description Korean** | 설명은 한글로 작성 |

### 3.4 Component Story (autodocs)

```jsx
export default {
  title: 'Atoms/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: `
## Button Component

기본 버튼 컴포넌트. 모든 인터랙션의 핵심 요소.

### Layout Structure
\`\`\`
┌─────────────────────────────┐
│  [Icon?]  Label  [Icon?]    │
└─────────────────────────────┘
\`\`\`
        `
      }
    }
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost'],
      description: '버튼 스타일 변형',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'primary' },
        category: 'Appearance'
      }
    },
    size: {
      control: { type: 'radio' },
      options: ['small', 'medium', 'large'],
      description: '버튼 크기',
      table: { category: 'Size' }
    },
    disabled: {
      control: 'boolean',
      description: '비활성화 상태',
      table: { category: 'State' }
    },
    onClick: {
      action: 'clicked',
      description: '클릭 이벤트 핸들러',
      table: { category: 'Events' }
    }
  }
};

// 1. Default - 기본 상태 (필수)
export const Default = {
  args: {
    children: 'Button',
    variant: 'primary',
    size: 'medium'
  }
};

// 2. Variants - 변형 비교 (선택)
export const Variants = {
  render: () => (
    <Stack direction="row" spacing={2}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
    </Stack>
  )
};

// 3. RealWorld - 실제 사용 예시 (선택)
export const InHeroSection = {
  render: () => (
    <Box sx={{ p: 4, textAlign: 'center' }}>
      <Typography variant="h2" gutterBottom>Hero Title</Typography>
      <Stack direction="row" spacing={2} justifyContent="center">
        <Button variant="primary" size="large">Get Started</Button>
        <Button variant="outline" size="large">Learn More</Button>
      </Stack>
    </Box>
  ),
  parameters: { layout: 'fullscreen' }
};
```

### 3.5 Style Story 필수 구조 (디자인 토큰 문서)

Style 섹션은 autodocs를 사용하지 않고 직접 작성한다.

```
1. DocumentTitle (영문)
2. PageContainer
   ├── 페이지 제목 (h4)
   ├── 스토리 개요 (1줄 설명)
   ├── SectionTitle: "토큰 구조" → 트리 뷰로 theme 계층 표시 (필수)
   ├── SectionTitle: "토큰 값" → 테이블로 토큰값 표시 (필수)
   ├── SectionTitle: "사용 예시" → MUI sx prop 코드 예시 (필수)
   └── SectionTitle: "Vibe Coding Prompt" → AI 코딩용 프롬프트 예시 (필수)
```

```jsx
// Style/Colors.stories.jsx
export default {
  title: 'Style/Colors',
  parameters: { layout: 'padded' }
};

export const Default = {
  render: () => {
    const theme = useTheme();

    return (
      <>
        <DocumentTitle
          title="Color System"
          status="Available"
          note="Brand color palette"
          brandName="Design System"
          systemName="Starter Kit"
          version="1.0"
        />
        <PageContainer>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
            Color System
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            프로젝트에서 사용하는 색상 팔레트와 시멘틱 컬러 토큰입니다.
          </Typography>

          {/* 필수: 토큰 구조 */}
          <SectionTitle title="토큰 구조" description="MUI theme.palette 계층" />
          <Box sx={{ p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1, mb: 4 }}>
            <TreeNode keyName="palette" value={theme.palette} />
          </Box>

          {/* 필수: 토큰 값 */}
          <SectionTitle title="토큰 값" description="주요 토큰의 실제 값" />
          <TableContainer sx={{ mb: 4 }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>Token</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Value</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>설명</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell sx={{ fontFamily: 'monospace' }}>primary.main</TableCell>
                  <TableCell sx={{ fontFamily: 'monospace' }}>#12100E</TableCell>
                  <TableCell>주요 브랜드 색상</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          {/* 필수: 사용 예시 */}
          <SectionTitle title="사용 예시" description="MUI sx prop에서의 토큰 활용" />
          <Box component="pre" sx={{ bgcolor: 'grey.100', p: 2, mb: 4 }}>
{`<Box sx={{ backgroundColor: 'primary.main' }} />
<Typography sx={{ color: 'text.secondary' }} />`}
          </Box>

          {/* 필수: Vibe Coding Prompt */}
          <SectionTitle title="Vibe Coding Prompt" />
          <Box component="pre" sx={{ bgcolor: 'grey.900', color: 'grey.100', p: 2 }}>
{`"primary.main (#12100E)을 사용해서 CTA 버튼을 만들어줘.
hover 시 primary.dark로 변경되도록 해줘."

"배경 #F5F2EE, 텍스트 #12100E로 조명 제품 카드를 만들어줘.
그래디언트 금지, 날카로운 모서리."`}
          </Box>
        </PageContainer>
      </>
    );
  }
};
```

### 3.6 문서 스타일링 금지 사항

- Paper, Card 컴포넌트의 장식적 사용 금지
- elevation, boxShadow 사용 금지
- 불필요한 배경색, 그라데이션 금지
- 이모지 과다 사용 금지
- 마케팅 문구 금지

```jsx
// ❌ 금지
<Paper sx={{ p: 3, elevation: 2 }}>
  <Typography>내용</Typography>
</Paper>

// ✅ 권장
<TableContainer>
  <Table size="small">...</Table>
</TableContainer>
```

---

## Part 4: 컴포넌트 작성 규칙

### 4.1 Props 관리 규칙

```jsx
/**
 * Button 컴포넌트
 *
 * Props:
 * @param {string} label - 버튼에 표시할 텍스트 [Required]
 * @param {function} onClick - 버튼 클릭 시 실행할 함수 [Optional]
 * @param {boolean} isActive - 버튼 활성화 여부 [Optional, 기본값: true]
 *
 * Example usage:
 * <Button label="확인" onClick={handleClick} />
 */
function Button({ label, onClick, isActive = true }) {
  return (
    <button onClick={onClick} disabled={!isActive}>
      {label}
    </button>
  );
}
```

### 4.2 컴포넌트 품질 요구사항

- `forwardRef` 지원
- Semantic Props (align, justify, spacing)
- `sx` prop 오버라이드 지원
- 상세 JSDoc 주석
- MUI 최신 버전 사용

### 4.3 MUI Grid 사용법 (CRITICAL)

```jsx
// ❌ 잘못된 Import (절대 사용 금지)
import Grid from '@mui/material/Grid2';  // 틀림! 사용 금지!

// ✅ 올바른 Import (반드시 이것만 사용)
import Grid from '@mui/material/Grid';   // 정확함! 이것만 사용!

// ✅ 올바른 Grid 사용법 (MUI v6+)
<Grid container spacing={2}>
  <Grid size={{ xs: 6, md: 8 }}>
    <Item>xs=6 md=8</Item>
  </Grid>
  <Grid size={{ xs: 6, md: 4 }}>
    <Item>xs=6 md=4</Item>
  </Grid>
</Grid>
```

**중요**: MUI v7에서는 `Grid2`가 아닌 `Grid`를 직접 import해야 한다.

### 4.4 MUI Custom Theme 규칙

```jsx
// theme.js - 별도 파일로 관리
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  typography: {
    // 본문: Pretendard Variable (웹폰트)
    fontFamily: '"Pretendard Variable", -apple-system, sans-serif',
    // Headline 영어: Outfit, 한글: Pretendard Bold
    h1: { fontFamily: '"Outfit", "Pretendard Variable", sans-serif' },
  },
  palette: {
    primary: { main: '#0000FF' },           // 프로젝트별 Primary
    secondary: { main: blueGrey[900] },     // Secondary: blueGrey 가장 어두운색
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          // elevation shadow: offset 0, opacity 낮음, blur 높음
          boxShadow: '0 0 24px rgba(0,0,0,0.05)',
        },
      },
    },
  },
  shape: {
    borderRadius: 0,  // 기본 borderRadius 0 (인라인 지정 제외)
  },
});
```

### 4.5 Declarative 주석 규칙

디자이너 관점에서 각 컴포넌트의 동작 방식을 서술한다.

```jsx
/**
 * HeroSection 컴포넌트
 *
 * 동작 흐름:
 * 1. 사용자가 페이지에 진입하면 배경 이미지가 페이드인
 * 2. 0.3초 후 타이틀 텍스트가 아래에서 슬라이드업
 * 3. CTA 버튼 hover 시 배경색 primary.dark로 전환
 *
 * 시각적 변화:
 * - 초기 상태: 배경 opacity 0, 텍스트 translateY(20px)
 * - 최종 상태: 배경 opacity 1, 텍스트 translateY(0)
 */
function HeroSection({ title, ctaText, onCtaClick }) {
  // ...
}
```

**주의**: 리팩토링 시 기능과 기본 로직, 형태가 변경되지 않도록 주의

---

## Part 5: 실행 순서

### Phase 1: 시각 분석
1. 스크린샷 전체 분석 (브랜드 인상, 레이아웃, 컴포넌트 식별)
2. 섹션별 상세 분석

### Phase 2: Semantic Token 생성
1. 색상 토큰 (4-6색 제한)
2. 타이포그래피 토큰 (Display/Body 구분)
3. 간격 토큰 (inset, gap, stack, inline, section, page)
4. 그리드 토큰

### Phase 3: 컴포넌트 생성
1. Atoms → Molecules → Organisms → Templates
2. 각 컴포넌트에 Storybook 스토리 함께 작성

### Phase 4: Storybook 생성
1. Design Token Stories (Colors, Typography, Spacing, Icons)
2. Component Stories (Default + Variants + RealWorld)
3. Layout Stories (Templates, Pages)

---

## Part 6: 품질 체크리스트

### 토큰 품질
- [ ] 색상 4-6개로 제한된 팔레트
- [ ] Semantic Spacing (inset, gap, stack, inline, section, page)
- [ ] 타이포그래피 Display/Body 구분
- [ ] 8px 그리드 기반
- [ ] 그래디언트/글로우/블러 사용 안 함

### 컴포넌트 품질
- [ ] forwardRef 지원
- [ ] Semantic Props (align, justify, spacing)
- [ ] sx prop 오버라이드
- [ ] 상세 JSDoc 주석
- [ ] 기존 컴포넌트 재활용 확인

### Storybook 품질

**공통**
- [ ] 스토리 한 개당 단일 컴포넌트/토큰만 보여주는가?
- [ ] DocumentTitle props가 모두 영어로 작성되었는가?
- [ ] 설명이 한글로 작성되었는가?
- [ ] 2개 이상의 섹션에 SectionTitle이 사용되었는가?

**Component 스토리**
- [ ] `tags: ['autodocs']`가 적용되었는가?
- [ ] 모든 props에 argTypes와 control이 적용되었는가?
- [ ] 과도한 베리에이션 스토리를 생성하지 않았는가? (1-3개 권장)

**Style 스토리**
- [ ] autodocs 없이 직접 Doc 스토리를 작성했는가?
- [ ] 1줄 개요가 페이지 제목 아래에 있는가?
- [ ] 토큰 구조가 트리 뷰로 표시되어 있는가?
- [ ] 토큰 값이 테이블로 정리되어 있는가?
- [ ] MUI sx prop 사용 예시가 포함되어 있는가?
- [ ] Vibe Coding Prompt 예시가 포함되어 있는가?
- [ ] `useTheme()` 훅으로 실제 theme 값을 참조하는가?

### 스토리 정렬
- [ ] Overview → Style → Atoms → Molecules → Organisms → Templates → Pages

---

## Part 7: 출력 구조

```
@cloned/design-system/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .storybook/
│   ├── main.js
│   ├── preview.jsx
│   └── manager.js
├── src/
│   ├── index.ts
│   ├── styles/
│   │   ├── tokens.js              # SPACING, COLORS 등
│   │   ├── theme.js               # MUI 테마 설정
│   │   └── ThemeProvider.jsx
│   ├── components/
│   │   ├── atoms/
│   │   │   ├── Button/
│   │   │   │   ├── Button.jsx
│   │   │   │   └── Button.stories.jsx
│   │   │   └── ...
│   │   ├── molecules/
│   │   ├── organisms/
│   │   └── templates/
│   ├── stories/
│   │   ├── Overview.stories.jsx
│   │   └── style/
│   │       ├── Colors.stories.jsx
│   │       ├── Typography.stories.jsx
│   │       ├── Spacing.stories.jsx
│   │       └── Icons.stories.jsx
│   └── storybookDocumentation/
│       ├── DocumentTitle.jsx
│       ├── PageContainer.jsx
│       ├── SectionTitle.jsx
│       ├── ColorSwatch.jsx
│       └── TreeNode.jsx
└── analysis/
    └── design-system-analysis.md
```

---

## Part 8: 참조 문서

| 문서 | 용도 | 우선순위 |
|------|------|----------|
| | MUI Grid import/size prop 규칙 | CRITICAL |
| | MUI 테마 커스터마이징 | CRITICAL |
| | Storybook 패턴 가이드 | MUST |
| | 스크린샷 시각 분석 규칙 | MUST |
| | 색상 추출 규칙 | MUST |
| | 타이포그래피 분석 | MUST |
| | Semantic 간격 시스템 | MUST |
| | 그리드 시스템 설계 | SHOULD |
| | MUI 컴포넌트 생성 | SHOULD |

---

## Part 9: 의존성

```bash
# Core
pnpm add react react-dom
pnpm add @mui/material @emotion/react @emotion/styled
pnpm add @mui/icons-material lucide-react

# Storybook v8
pnpm add -D storybook @storybook/react-vite
pnpm add -D @storybook/addon-docs @storybook/addon-a11y
pnpm add -D @storybook/addon-themes @storybook/addon-interactions

# Build
pnpm add -D typescript vite @vitejs/plugin-react
```

## 실행 명령어

```bash
pnpm storybook          # Storybook 개발 서버
pnpm build-storybook    # Storybook 빌드
```
