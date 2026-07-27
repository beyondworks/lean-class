# Pattern Detection Agent

프로젝트 구조 자동 감지 및 적응

## 메인 엔트리 감지

### 감지 우선순위

```typescript
const ENTRY_DETECTION_PRIORITY = [
  // 1순위: Vite/CRA 표준
  'src/main.tsx',
  'src/main.ts',
  'src/index.tsx',
  'src/index.ts',
  
  // 2순위: App 파일
  'App.tsx',
  'src/App.tsx',
  
  // 3순위: Next.js App Router
  'app/layout.tsx',
  'app/layout.ts',
  
  // 4순위: Next.js Pages Router
  'pages/_app.tsx',
  'pages/_app.js',
  
  // 5순위: 루트 index
  'index.tsx',
  'index.ts',
];
```

### 감지 실패 시 처리

```
1. 모든 .tsx/.ts 파일 스캔
2. 'App', 'Main', 'Root', 'Entry' 키워드 검색
3. ReactDOM.render 또는 createRoot 호출 검색
4. 사용자에게 확인 요청:
   "메인 엔트리 파일을 찾지 못했습니다. 
    다음 중 메인 엔트리 파일을 선택해주세요: [파일 목록]"
```

## 프로젝트 패턴 감지

### Pattern A: Figma Make 표준

**식별자:**
```
✓ components/ 폴더 존재
✓ App.tsx 루트에 존재
✓ styles/globals.css 존재
✓ package.json에 특별한 프레임워크 없음
```

**구조:**
```
project/
├── components/
│   ├── figma/
│   ├── ui/
│   └── *.tsx
├── pages/
├── styles/
│   └── globals.css
├── App.tsx          ← 메인 엔트리
└── package.json
```

**변환 전략:**
- App.tsx를 참조하여 전체 구조 파악
- globals.css에서 토큰 추출
- components/ 전체 변환

### Pattern B: Next.js App Router

**식별자:**
```
✓ app/ 폴더 존재
✓ app/layout.tsx 존재
✓ app/page.tsx 존재
✓ package.json에 "next" 의존성
```

**구조:**
```
project/
├── app/
│   ├── layout.tsx   ← 메인 엔트리
│   ├── page.tsx
│   └── globals.css
├── components/
└── package.json
```

**변환 전략:**
- app/layout.tsx에서 전역 설정 파악
- app/globals.css에서 토큰 추출
- components/ 폴더 변환

### Pattern C: Next.js Pages Router

**식별자:**
```
✓ pages/ 폴더 존재
✓ pages/_app.tsx 존재
✓ pages/index.tsx 존재
✓ package.json에 "next" 의존성
```

**구조:**
```
project/
├── pages/
│   ├── _app.tsx     ← 메인 엔트리
│   ├── _document.tsx
│   └── index.tsx
├── components/
├── styles/
│   └── globals.css
└── package.json
```

**변환 전략:**
- pages/_app.tsx에서 전역 설정 파악
- styles/globals.css에서 토큰 추출

### Pattern D: Vite/CRA

**식별자:**
```
✓ src/ 폴더 존재
✓ src/main.tsx 또는 src/index.tsx 존재
✓ src/App.tsx 존재
✓ vite.config.ts 또는 react-scripts 의존성
```

**구조:**
```
project/
├── src/
│   ├── main.tsx     ← 메인 엔트리
│   ├── App.tsx
│   ├── components/
│   └── index.css
├── index.html
└── package.json
```

**변환 전략:**
- src/main.tsx에서 프로바이더 구조 파악
- src/index.css 또는 src/App.css에서 토큰 추출

### Pattern E: 커스텀/비표준

**감지 방법:**
```
위 패턴에 맞지 않는 경우:
1. package.json의 main 필드 확인
2. 모든 .tsx 파일에서 ReactDOM 검색
3. 사용자에게 구조 확인 요청
```

## 스타일 파일 감지

### CSS 변수 파일 우선순위

```typescript
const STYLE_FILE_PRIORITY = [
  // 1순위: 글로벌 스타일
  'styles/globals.css',
  'src/styles/globals.css',
  'app/globals.css',
  'src/index.css',
  'src/App.css',
  
  // 2순위: Tailwind 설정
  'tailwind.config.js',
  'tailwind.config.ts',
  
  // 3순위: 테마 파일
  'src/theme.ts',
  'src/theme/index.ts',
  'theme.ts',
];
```

### 스타일 방식 감지

| 방식 | 감지 방법 | 토큰 추출 |
|------|----------|----------|
| CSS Variables | `:root { --*` 패턴 | CSS 파일 파싱 |
| Tailwind | `tailwind.config` 존재 | config 파싱 |
| Styled Components | `styled.` import | 테마 파일 검색 |
| Emotion | `@emotion` import | 테마 파일 검색 |
| SCSS | `.scss` 파일 | 변수 파일 검색 |

## 컴포넌트 폴더 감지

### 우선순위

```typescript
const COMPONENT_FOLDER_PRIORITY = [
  'components/',
  'src/components/',
  'app/components/',
  'lib/components/',
];
```

### 컴포넌트 분류

```
컴포넌트 크기/복잡도로 자동 분류:

Atoms (< 50 줄, 1개 요소):
- Button, Input, Icon, Badge

Molecules (50-150 줄, 2-5개 요소):
- Card, MenuItem, SearchField

Organisms (> 150 줄, 섹션 단위):
- Navigation, HeroSection, Footer

Templates (페이지 레이아웃):
- *Layout, *Page, *Template
```

## 의존성 감지

### package.json 분석

```typescript
interface DetectedDependencies {
  framework: 'next' | 'vite' | 'cra' | 'unknown';
  styling: 'tailwind' | 'styled-components' | 'emotion' | 'css' | 'scss';
  ui: 'mui' | 'chakra' | 'antd' | 'none';
  stateManagement: 'redux' | 'zustand' | 'jotai' | 'none';
}

function detectDependencies(packageJson: any): DetectedDependencies {
  const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
  
  return {
    framework: deps.next ? 'next' : deps.vite ? 'vite' : 'unknown',
    styling: deps.tailwindcss ? 'tailwind' : deps['styled-components'] ? 'styled-components' : 'css',
    ui: deps['@mui/material'] ? 'mui' : deps['@chakra-ui/react'] ? 'chakra' : 'none',
    stateManagement: deps.redux ? 'redux' : deps.zustand ? 'zustand' : 'none',
  };
}
```

## 감지 결과 출력

```typescript
interface ProjectAnalysis {
  pattern: 'figma-make' | 'nextjs-app' | 'nextjs-pages' | 'vite' | 'custom';
  mainEntry: string;
  styleFiles: string[];
  componentFolder: string;
  dependencies: DetectedDependencies;
  warnings: string[];
}

// 출력 예시
{
  pattern: 'figma-make',
  mainEntry: 'App.tsx',
  styleFiles: ['styles/globals.css'],
  componentFolder: 'components/',
  dependencies: {
    framework: 'vite',
    styling: 'css',
    ui: 'none',
    stateManagement: 'none'
  },
  warnings: [
    'MUI 미설치 - 새로 추가 필요',
    'TypeScript 설정 필요'
  ]
}
```

## 변환 전략 결정

### 패턴별 변환 접근

| 패턴 | 토큰 소스 | 컴포넌트 위치 | 출력 구조 |
|------|----------|--------------|----------|
| Figma Make | globals.css | components/ | 전체 재구성 |
| Next.js App | app/globals.css | components/ | 병합 |
| Next.js Pages | styles/globals.css | components/ | 병합 |
| Vite | src/index.css | src/components/ | 병합 |

### 충돌 해결

```
기존 MUI 설치 시:
1. 버전 확인 (v5 vs v6)
2. 기존 테마 백업
3. 토큰 병합 제안
4. 사용자 확인 요청

기존 Storybook 설치 시:
1. 버전 확인 (v7 vs v8)
2. 기존 설정 백업
3. 설정 병합
4. 사용자 확인 요청
```

## 사용자 확인 프롬프트

```
프로젝트 분석 완료:
- 패턴: [감지된 패턴]
- 메인 엔트리: [파일명]
- 스타일 파일: [파일 목록]
- 컴포넌트 폴더: [폴더명]

[경고 사항 있으면 표시]

변환을 진행하시겠습니까? (Y/n)
```
