---
name: aidu-design-system
description: "Figma Make 출력물을 MUI 기반 디자인 시스템으로 변환하는 AI 에이전트 팀 오케스트레이터. 사용자가 Figma Make로 제작한 프로젝트 폴더를 전달하면 (1) 디자인 토큰 추출, (2) CSS→MUI 컴포넌트 변환, (3) 레이아웃 시스템 구축, (4) Storybook v8 문서화, (5) @aidu npm 패키지 빌드를 병렬로 수행. 'pnpm storybook' 명령으로 실행 가능한 완전한 디자인 시스템 생성."
license: Proprietary
allowed-tools: []
---

# AIDU Design System Agent Team

Figma Make 프로젝트 → MUI 기반 디자인 시스템 + Storybook + npm 패키지 자동 변환

## 🎯 Core Purpose

**토큰 변경만으로 전체 테마 변경 가능한 시스템 구축**

```
tokens.ts 수정 → 모든 컴포넌트 자동 반영
├── colors.primary → 버튼, 링크, 아이콘...
├── typography.fontFamily → 모든 텍스트
├── spacing.base → 모든 간격
└── radius.base → 모든 라운드 처리
```

---

## 🔍 Phase 1: Project Analysis

### 메인 엔트리 감지 (우선순위)

```
1순위: src/main.tsx, src/main.ts, src/index.tsx
2순위: App.tsx, src/App.tsx, app/layout.tsx
3순위: pages/_app.tsx (Next.js Pages)
4순위: index.tsx, index.ts
실패 시: 사용자에게 확인 요청
```

### 프로젝트 패턴 감지

| 패턴 | 식별자 | 메인 엔트리 |
|------|--------|-------------|
| Figma Make 표준 | `components/`, `App.tsx` | App.tsx |
| Next.js App Router | `app/layout.tsx` | app/layout.tsx |
| Next.js Pages | `pages/_app.tsx` | pages/_app.tsx |
| Vite/CRA | `src/main.tsx` | src/main.tsx |

### 필수 분석 항목

```bash
# 실행할 분석
1. 폴더 구조 스캔 → 패턴 식별
2. package.json → 의존성 확인
3. 스타일 파일 위치 → globals.css, tailwind.config 등
4. 컴포넌트 목록 → 변환 대상 파악
```

---

## 🚀 Phase 2: Parallel Agent Execution

### 에이전트 구성

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                          │
│              (이 SKILL.md가 조율)                        │
└─────────────────────┬───────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Token   │    │Component│    │ Layout  │
│Extractor│    │Converter│    │Analyzer │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
                    ▼
           ┌───────────────┐
           │   Storybook   │
           │   Generator   │
           └───────┬───────┘
                   ▼
           ┌───────────────┐
           │   Package     │
           │   Builder     │
           └───────────────┘
```

### 병렬 실행 규칙

**동시 실행 가능:**
- Token Extractor + Layout Analyzer (서로 독립적)

**순차 대기:**
- Component Converter ← Token Extractor 완료 후
- Storybook Generator ← 모든 컴포넌트 변환 완료 후
- Package Builder ← Storybook 설정 완료 후

---

## 📋 Agent Tasks

### Agent 1: Token Extractor
**참조:**

**입력:** globals.css, 인라인 스타일, Tailwind 설정
**출력:** `src/theme/tokens/`

```typescript
// 출력 형식
export const tokens = {
  colors: {
    primary: { main: '#...', light: '#...', dark: '#...' },
    secondary: { ... },
    // semantic colors
  },
  typography: {
    fontFamily: { base: '...', heading: '...' },
    fontSize: { xs: '...', sm: '...', ... },
    fontWeight: { regular: 400, medium: 500, bold: 700 },
    lineHeight: { tight: 1.2, normal: 1.5, relaxed: 1.75 },
  },
  spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48 },
  radius: { sm: 4, md: 8, lg: 16, full: 9999 },
  shadows: { sm: '...', md: '...', lg: '...' },
  breakpoints: { xs: 0, sm: 600, md: 900, lg: 1200, xl: 1536 },
};
```

### Agent 2: Component Converter
**참조:**

**입력:** 원본 컴포넌트 (.tsx), 추출된 토큰
**출력:** MUI 래핑 컴포넌트

**변환 규칙:**
```
CSS class → MUI sx prop (토큰 참조)
inline style → styled() 또는 sx
Tailwind class → MUI 테마 값
```

**CRITICAL:** 하드코딩 금지, 모든 값은 토큰 참조

### Agent 3: Layout Analyzer
**참조:**

**입력:** 페이지/섹션 컴포넌트
**출력:** 그리드 시스템, 브레이크포인트, 컨테이너

```typescript
// 출력 예시
export const Container = styled(MuiContainer)(({ theme }) => ({
  maxWidth: theme.breakpoints.values.lg,
  paddingInline: theme.spacing(2),
  [theme.breakpoints.up('md')]: {
    paddingInline: theme.spacing(4),
  },
}));
```

### Agent 4: Storybook Generator
**참조:**

**입력:** 변환된 컴포넌트
**출력:** `.storybook/` 설정 + `*.stories.tsx`

**필수 설정:**
- Storybook v8
- @storybook/addon-a11y
- @storybook/addon-viewport
- 테마 스위칭 (light/dark)

### Agent 5: Package Builder
**참조:**

**출력:** npm 배포 가능한 패키지 구조

---

## 📁 Output Structure

```
@aidu/design-system/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── index.ts
│   ├── theme/
│   │   ├── index.ts
│   │   ├── tokens/
│   │   │   ├── index.ts
│   │   │   ├── colors.ts      ← 이것만 수정하면 전체 색상 변경
│   │   │   ├── typography.ts  ← 이것만 수정하면 전체 폰트 변경
│   │   │   ├── spacing.ts
│   │   │   └── ...
│   │   ├── theme.ts
│   │   └── ThemeProvider.tsx
│   ├── components/
│   │   ├── index.ts
│   │   ├── atoms/
│   │   ├── molecules/
│   │   ├── organisms/
│   │   └── templates/
│   └── layouts/
├── .storybook/
│   ├── main.ts
│   ├── preview.tsx
│   └── manager.ts
└── dist/
```

---

## ⚡ Execution Commands

### 전체 실행

```bash
# 1. 프로젝트 폴더로 이동
cd /path/to/figma-make-project

# 2. 디자인 시스템 생성 (이 스킬 실행)
# Claude가 자동으로 모든 에이전트 실행

# 3. 의존성 설치
pnpm install

# 4. Storybook 실행
pnpm storybook

# 5. 패키지 빌드
pnpm build
```

### 개별 명령어

```bash
# Storybook 개발 서버
pnpm storybook          # localhost:6006

# 빌드
pnpm build              # dist/ 생성

# npm 배포
pnpm publish --access public
```

---

## ✅ Quality Checklist

### 토큰 검증
- [ ] 모든 색상이 토큰에서 참조됨
- [ ] 모든 폰트 사이즈가 토큰에서 참조됨
- [ ] 하드코딩된 값 없음

### 컴포넌트 검증
- [ ] MUI 래핑 완료
- [ ] Props 타입 정의됨
- [ ] 반응형 동작 확인

### Storybook 검증
- [ ] 모든 컴포넌트에 Story 존재
- [ ] Controls 동작 확인
- [ ] `pnpm storybook` 정상 실행

### 패키지 검증
- [ ] TypeScript 빌드 성공
- [ ] exports 필드 정확
- [ ] 의존성 명확

---

## 📖 Design Principles

### MUI 공식 가이드 준수

**https://mui.com/material-ui/getting-started/ 공식 가이드 문서를 잘 따라줘.**

- 컴포넌트 사용법은 공식 문서 API 참조
- 테마 커스터마이징은 Theming 가이드 준수
- sx prop 사용법은 System 문서 참조
- 타입 정의는 TypeScript 가이드 준수

---

## 🚫 Don't Do This

- ❌ 토큰 없이 직접 값 하드코딩
- ❌ MUI 테마 무시하고 인라인 스타일
- ❌ 컴포넌트에 비즈니스 로직 포함
- ❌ Storybook 없이 패키지 배포
- ❌ MUI 공식 가이드와 다른 방식으로 구현

---

## 📚 References


---

## 🔧 Dependencies

```bash
# 필수 설치
pnpm add @mui/material @emotion/react @emotion/styled
pnpm add -D typescript vite @vitejs/plugin-react
pnpm add -D storybook @storybook/react-vite
pnpm add -D @storybook/addon-essentials @storybook/addon-a11y
```
