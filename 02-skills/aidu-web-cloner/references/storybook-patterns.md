# Storybook Patterns Guide

Production-Grade Storybook 작성을 위한 패턴 가이드

---

## 1. Story Meta 구조

### 1.1 Component Story (autodocs 사용)

```jsx
export default {
  title: 'Atoms/Button',           // 카테고리/컴포넌트명
  component: Button,
  tags: ['autodocs'],              // 자동 문서화
  parameters: {
    layout: 'centered',            // 또는 'fullscreen', 'padded'
    docs: {
      description: {
        component: `마크다운 문서`
      }
    }
  },
  argTypes: { /* ... */ }
}
```

### 1.2 Style Story (autodocs 미사용)

```jsx
export default {
  title: 'Style/Colors',
  parameters: {
    layout: 'padded'
    // autodocs 태그 없음
  }
}
```

### 1.3 Story Sort Order

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

---

## 2. argTypes 상세 작성

### 2.1 Control 타입 가이드

| Props 타입 | control | 예시 |
|-----------|---------|------|
| string | `'text'` | `control: 'text'` |
| boolean | `'boolean'` | `control: 'boolean'` |
| number | `{ type: 'number' }` | `control: { type: 'number', min: 0, max: 100 }` |
| enum/선택지 | `'select'` 또는 `'radio'` | `control: 'select', options: ['a', 'b']` |
| color | `'color'` | `control: 'color'` |
| object | `'object'` | `control: 'object'` |
| function | `action()` | `action: 'clicked'` |

### 2.2 argTypes 예시

```jsx
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
  },
  sx: {
    control: 'object',
    description: 'MUI sx prop 스타일 오버라이드',
    table: { category: 'Advanced' }
  }
}
```

---

## 3. Story 패턴 (Component)

### 3.1 Default (기본 - 필수)

```jsx
export const Default = {
  args: {
    children: 'Button',
    variant: 'primary',
    size: 'medium'
  },
  parameters: {
    docs: {
      description: {
        story: '가장 기본적인 버튼 상태. 대부분의 경우 이 형태로 사용됨.'
      }
    }
  }
}
```

### 3.2 Variants (변형 비교 - 선택)

**주의**: 과도한 베리에이션 금지. Controls로 확인 가능한 경우 생략.

```jsx
export const Variants = {
  render: () => (
    <Stack direction="row" spacing={2}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
    </Stack>
  ),
  parameters: {
    docs: {
      description: {
        story: '모든 버튼 변형 비교. Primary는 주요 CTA, Ghost는 부차적 액션.'
      }
    }
  }
}
```

### 3.3 RealWorld (실제 사용 예시 - 선택)

```jsx
export const InHeroSection = {
  render: () => (
    <Box sx={{ p: 6, bgcolor: 'background.paper', textAlign: 'center' }}>
      <Typography variant="h2" gutterBottom>
        Welcome to Our Platform
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        The best solution for your needs.
      </Typography>
      <Stack direction="row" spacing={2} justifyContent="center">
        <Button variant="primary" size="large">Get Started</Button>
        <Button variant="outline" size="large">Learn More</Button>
      </Stack>
    </Box>
  ),
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        story: '히어로 섹션에서의 실제 사용 예시.'
      }
    }
  }
}
```

---

## 4. Style Story 패턴 (디자인 토큰)

### 4.1 필수 구조

```
1. DocumentTitle (영문)
2. PageContainer
   ├── 페이지 제목 (h4)
   ├── 스토리 개요 (1줄 설명)
   ├── SectionTitle: "토큰 구조" → 트리 뷰 (필수)
   ├── SectionTitle: "토큰 값" → 테이블 (필수)
   ├── SectionTitle: "사용 예시" → 코드 블록 (필수)
   └── SectionTitle: "Vibe Coding Prompt" → AI 프롬프트 (필수)
```

### 4.2 Colors.stories.jsx 템플릿

```jsx
import { useTheme } from '@mui/material/styles';
import { DocumentTitle, PageContainer, SectionTitle, TreeNode } from '../../storybookDocumentation';

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
          note="Brand color palette and semantic tokens"
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

          {/* 토큰 구조 */}
          <SectionTitle title="토큰 구조" description="theme.palette 계층 구조" />
          <Box sx={{ p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1, mb: 4 }}>
            <TreeNode keyName="palette" value={theme.palette} />
          </Box>

          {/* 토큰 값 */}
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
                <TableRow>
                  <TableCell sx={{ fontFamily: 'monospace' }}>secondary.main</TableCell>
                  <TableCell sx={{ fontFamily: 'monospace' }}>#FFC66E</TableCell>
                  <TableCell>액센트, CTA</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          {/* 사용 예시 */}
          <SectionTitle title="사용 예시" description="MUI sx prop에서의 토큰 활용" />
          <Box
            component="pre"
            sx={{
              backgroundColor: 'grey.100',
              p: 2,
              fontSize: 12,
              fontFamily: 'monospace',
              overflow: 'auto',
              borderRadius: 1,
              mb: 4
            }}
          >
{`// 색상 토큰 사용
<Box sx={{ backgroundColor: 'primary.main' }} />
<Typography sx={{ color: 'text.secondary' }} />

// 반응형 적용
<Box sx={{
  backgroundColor: { xs: 'background.paper', md: 'background.default' }
}} />`}
          </Box>

          {/* Vibe Coding Prompt */}
          <SectionTitle
            title="Vibe Coding Prompt"
            description="AI 코딩 도구에서 활용할 수 있는 프롬프트 예시"
          />
          <Box
            component="pre"
            sx={{
              backgroundColor: 'grey.900',
              color: 'grey.100',
              p: 2,
              fontSize: 12,
              fontFamily: 'monospace',
              overflow: 'auto',
              borderRadius: 1
            }}
          >
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

### 4.3 Spacing.stories.jsx 템플릿

```jsx
export const Default = {
  render: () => {
    return (
      <>
        <DocumentTitle
          title="Spacing System"
          status="Available"
          note="8px-based semantic spacing tokens"
          brandName="Design System"
          systemName="Starter Kit"
          version="1.0"
        />
        <PageContainer>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
            Spacing System
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            8px 기반 시맨틱 간격 시스템입니다.
          </Typography>

          {/* 토큰 구조 */}
          <SectionTitle title="토큰 구조" description="SPACING 계층 구조" />
          <Box
            component="pre"
            sx={{
              p: 2,
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1,
              fontFamily: 'monospace',
              fontSize: 12,
              mb: 4
            }}
          >
{`SPACING
├── inset     # 컴포넌트 내부 패딩
├── gap       # Flex/Grid 간격
├── stack     # 수직 쌓기
├── inline    # 수평 나열
├── section   # 섹션 구분
└── page
    ├── gutter  # 페이지 여백
    ├── top     # 상단
    └── bottom  # 하단`}
          </Box>

          {/* 토큰 값 */}
          <SectionTitle title="토큰 값" description="주요 토큰의 실제 값" />
          <TableContainer sx={{ mb: 4 }}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>Token</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Value</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Usage</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell sx={{ fontFamily: 'monospace' }}>SPACING.inset.sm</TableCell>
                  <TableCell>16px</TableCell>
                  <TableCell>일반 버튼, 작은 카드</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell sx={{ fontFamily: 'monospace' }}>SPACING.gap.md</TableCell>
                  <TableCell>16px</TableCell>
                  <TableCell>카드 그리드</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell sx={{ fontFamily: 'monospace' }}>SPACING.section.lg</TableCell>
                  <TableCell>96px</TableCell>
                  <TableCell>데스크탑 섹션</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          {/* 사용 예시 */}
          <SectionTitle title="사용 예시" />
          <Box component="pre" sx={{ bgcolor: 'grey.100', p: 2, mb: 4 }}>
{`// 카드 패딩
<Box sx={{ p: SPACING.inset.md / 8 }} />

// 그리드 간격
<Grid container spacing={SPACING.gap.md / 8}>

// 섹션 구분
<Box sx={{ my: SPACING.section.lg / 8 }} />`}
          </Box>

          {/* Vibe Coding Prompt */}
          <SectionTitle title="Vibe Coding Prompt" />
          <Box component="pre" sx={{ bgcolor: 'grey.900', color: 'grey.100', p: 2 }}>
{`"카드 내부 패딩 SPACING.inset.md (24px),
카드 그리드 간격 SPACING.gap.md (16px)로 설정해줘."

"섹션 간격은 모바일 48px, 데스크탑 96px로 반응형 적용해줘."`}
          </Box>
        </PageContainer>
      </>
    );
  }
};
```

---

## 5. 문서용 헬퍼 컴포넌트

### 5.1 DocumentTitle.jsx

```jsx
export const DocumentTitle = ({
  title,
  status = 'Available',
  note,
  brandName,
  systemName,
  version
}) => (
  <Box sx={{ mb: 4, pb: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
    <Typography variant="overline" color="text.secondary">
      {brandName} • {systemName} v{version}
    </Typography>
    <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
      {title}
    </Typography>
    <Stack direction="row" spacing={1} alignItems="center">
      <Chip label={status} size="small" color="success" />
      {note && (
        <Typography variant="body2" color="text.secondary">
          {note}
        </Typography>
      )}
    </Stack>
  </Box>
);
```

### 5.2 PageContainer.jsx

```jsx
export const PageContainer = ({ children }) => (
  <Container maxWidth="xl" sx={{ py: 4 }}>
    {children}
  </Container>
);
```

### 5.3 SectionTitle.jsx

```jsx
export const SectionTitle = ({ title, description }) => (
  <Box sx={{ mb: 2, mt: 4, pb: 1, borderBottom: '1px solid', borderColor: 'divider' }}>
    <Typography variant="h6" sx={{ fontWeight: 600 }}>
      {title}
    </Typography>
    {description && (
      <Typography variant="body2" color="text.secondary">
        {description}
      </Typography>
    )}
  </Box>
);
```

### 5.4 TreeNode.jsx

```jsx
export const TreeNode = ({ keyName, value, depth = 0 }) => {
  const isObject = value && typeof value === 'object' && !Array.isArray(value);

  return (
    <Box sx={{ ml: depth * 2 }}>
      <Typography
        component="span"
        sx={{ fontFamily: 'monospace', fontSize: 12 }}
      >
        {keyName}
        {!isObject && `: ${JSON.stringify(value)}`}
      </Typography>
      {isObject && (
        <Box>
          {Object.entries(value).map(([k, v]) => (
            <TreeNode key={k} keyName={k} value={v} depth={depth + 1} />
          ))}
        </Box>
      )}
    </Box>
  );
};
```

---

## 6. 체크리스트

### Component 스토리
- [ ] `tags: ['autodocs']` 적용
- [ ] 모든 props에 argTypes 정의
- [ ] control 타입이 데이터 타입과 일치
- [ ] Default 스토리 있음
- [ ] 과도한 베리에이션 없음 (1-3개 권장)

### Style 스토리
- [ ] autodocs 미사용
- [ ] DocumentTitle 영문
- [ ] 토큰 구조 (트리 뷰)
- [ ] 토큰 값 (테이블)
- [ ] 사용 예시 (코드 블록)
- [ ] Vibe Coding Prompt
- [ ] `useTheme()` 훅 사용

### 문서 스타일
- [ ] Paper/Card 장식적 사용 없음
- [ ] elevation/boxShadow 없음
- [ ] 그라데이션 없음
- [ ] 이모지 과다 사용 없음
