# Package Builder Agent

npm 배포 가능한 패키지 구조 생성 및 빌드 설정

## 패키지 구조

```
@aidu/design-system/
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── vite.config.ts
├── README.md
├── CHANGELOG.md
├── LICENSE
├── src/
│   ├── index.ts              # 메인 엔트리
│   ├── theme/
│   │   ├── index.ts
│   │   ├── tokens/
│   │   ├── theme.ts
│   │   └── ThemeProvider.tsx
│   ├── components/
│   │   ├── index.ts
│   │   ├── atoms/
│   │   ├── molecules/
│   │   ├── organisms/
│   │   └── templates/
│   └── layouts/
│       └── index.ts
├── .storybook/
│   ├── main.ts
│   ├── preview.tsx
│   └── manager.ts
└── dist/                     # 빌드 출력
```

## package.json

```json
{
  "name": "@aidu/design-system",
  "version": "0.1.0",
  "description": "MUI-based tokenized design system",
  "type": "module",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": { "types": "./dist/index.d.ts", "default": "./dist/index.mjs" },
      "require": { "types": "./dist/index.d.ts", "default": "./dist/index.js" }
    },
    "./theme": {
      "import": { "types": "./dist/theme/index.d.ts", "default": "./dist/theme/index.mjs" },
      "require": { "types": "./dist/theme/index.d.ts", "default": "./dist/theme/index.js" }
    },
    "./components": {
      "import": { "types": "./dist/components/index.d.ts", "default": "./dist/components/index.mjs" },
      "require": { "types": "./dist/components/index.d.ts", "default": "./dist/components/index.js" }
    }
  },
  "files": ["dist", "README.md"],
  "sideEffects": false,
  "scripts": {
    "dev": "vite",
    "build": "tsc -p tsconfig.build.json && vite build",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "lint": "eslint src --ext ts,tsx",
    "type-check": "tsc --noEmit",
    "prepublishOnly": "pnpm build"
  },
  "peerDependencies": {
    "@emotion/react": "^11.0.0",
    "@emotion/styled": "^11.0.0",
    "@mui/material": "^6.0.0",
    "react": "^18.0.0 || ^19.0.0",
    "react-dom": "^18.0.0 || ^19.0.0"
  },
  "devDependencies": {
    "@emotion/react": "^11.13.0",
    "@emotion/styled": "^11.13.0",
    "@mui/material": "^6.3.0",
    "@storybook/addon-a11y": "^8.4.0",
    "@storybook/addon-essentials": "^8.4.0",
    "@storybook/addon-themes": "^8.4.0",
    "@storybook/react-vite": "^8.4.0",
    "@types/react": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "storybook": "^8.4.0",
    "typescript": "^5.6.0",
    "vite": "^6.0.0",
    "vite-plugin-dts": "^4.3.0"
  }
}
```

## vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    react(),
    dts({
      insertTypesEntry: true,
      include: ['src'],
      exclude: ['**/*.stories.tsx', '**/*.test.tsx'],
    }),
  ],
  build: {
    lib: {
      entry: {
        index: resolve(__dirname, 'src/index.ts'),
        'theme/index': resolve(__dirname, 'src/theme/index.ts'),
        'components/index': resolve(__dirname, 'src/components/index.ts'),
      },
      formats: ['es', 'cjs'],
      fileName: (format, entryName) => {
        const ext = format === 'es' ? 'mjs' : 'js';
        return `${entryName}.${ext}`;
      },
    },
    rollupOptions: {
      external: [
        'react',
        'react-dom',
        'react/jsx-runtime',
        '@mui/material',
        '@mui/material/styles',
        '@emotion/react',
        '@emotion/styled',
      ],
    },
    sourcemap: true,
  },
  resolve: {
    alias: { '@': resolve(__dirname, './src') },
  },
});
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "declaration": true,
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"]
}
```

## tsconfig.build.json

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": false,
    "declaration": true,
    "emitDeclarationOnly": true,
    "outDir": "dist"
  },
  "exclude": ["**/*.stories.tsx", "**/*.test.tsx"]
}
```

## 엔트리 파일 구조

### src/index.ts
```typescript
export * from './theme';
export * from './components';
export * from './layouts';
```

### src/theme/index.ts
```typescript
export * from './tokens';
export { theme, darkTheme } from './theme';
export { ThemeProvider, useThemeMode } from './ThemeProvider';
```

### src/components/index.ts
```typescript
// Atoms
export * from './atoms/Button';
// Molecules
export * from './molecules/Card';
// Organisms
export * from './organisms/HeroSection';
// ... 모든 컴포넌트 export
```

## ThemeProvider 구현

```typescript
// src/theme/ThemeProvider.tsx
import { ReactNode, useMemo, useState, createContext, useContext } from 'react';
import { ThemeProvider as MuiThemeProvider, CssBaseline } from '@mui/material';
import { theme as lightTheme, darkTheme } from './theme';

type ThemeMode = 'light' | 'dark';

interface ThemeContextValue {
  mode: ThemeMode;
  toggleMode: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export interface ThemeProviderProps {
  children: ReactNode;
  defaultMode?: ThemeMode;
}

export const ThemeProvider = ({ children, defaultMode = 'light' }: ThemeProviderProps) => {
  const [mode, setMode] = useState<ThemeMode>(defaultMode);
  const theme = useMemo(() => (mode === 'light' ? lightTheme : darkTheme), [mode]);
  const toggleMode = () => setMode((prev) => (prev === 'light' ? 'dark' : 'light'));
  
  return (
    <ThemeContext.Provider value={{ mode, toggleMode }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

export const useThemeMode = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useThemeMode must be used within ThemeProvider');
  return context;
};
```

## 빌드 및 배포 명령어

```bash
# 개발
pnpm dev

# 빌드
pnpm build

# Storybook
pnpm storybook

# npm 배포
pnpm publish --access public
```

## 체크리스트

### 빌드 전
- [ ] TypeScript 에러 없음
- [ ] Storybook 빌드 성공
- [ ] 모든 export 확인

### 배포 전
- [ ] package.json 버전 업데이트
- [ ] README.md 최신화
- [ ] peerDependencies 정확
