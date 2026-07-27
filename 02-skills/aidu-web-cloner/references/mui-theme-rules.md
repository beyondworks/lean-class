# MUI Custom Theme Rules

MUI 테마 커스터마이징 규칙 가이드.

## 기본 원칙

1. Custom theme은 별도의 파일(`theme.js`)로 관리
2. ThemeProvider로 전역 적용
3. 프로젝트 색상/타이포그래피에 맞게 커스터마이징

---

## Typography 규칙

### 본문 (Body Text)
```jsx
typography: {
  fontFamily: '"Pretendard Variable", -apple-system, BlinkMacSystemFont, sans-serif',
}
```

### Headline
```jsx
// 영어: Google Font Outfit
// 한글: Pretendard 가장 높은 weight
h1: {
  fontFamily: '"Outfit", "Pretendard Variable", sans-serif',
  fontWeight: 800,
},
h2: {
  fontFamily: '"Outfit", "Pretendard Variable", sans-serif',
  fontWeight: 700,
},
```

---

## Color 규칙

### Primary Color
프로젝트별로 지정. 예시:
```jsx
primary: { main: '#0000FF' }
```

### Secondary Color
일반적으로 blueGrey 계열 사용:
```jsx
import { blueGrey } from '@mui/material/colors';

secondary: { main: blueGrey[900] }
```

---

## Elevation / Shadow 규칙

Paper 컴포넌트의 기본 shadow:
- X, Y offset: 0
- Opacity: 낮게
- Blur: 높게 (dimmed shadow 효과)

```jsx
components: {
  MuiPaper: {
    styleOverrides: {
      root: {
        boxShadow: '0 0 24px rgba(0,0,0,0.05)',
      },
    },
  },
}
```

---

## BorderRadius 규칙

**기본값 0**: 인라인으로 직접 지정하지 않는 한 모든 컴포넌트의 borderRadius는 0

```jsx
shape: {
  borderRadius: 0,
}
```

개별 컴포넌트에서 필요 시 인라인 지정:
```jsx
<Box sx={{ borderRadius: 2 }}>Rounded Box</Box>
```

---

## 전체 Theme 예시

```jsx
// src/styles/theme.js
import { createTheme } from '@mui/material/styles';
import { blueGrey } from '@mui/material/colors';

const theme = createTheme({
  typography: {
    fontFamily: '"Pretendard Variable", -apple-system, sans-serif',
    h1: {
      fontFamily: '"Outfit", "Pretendard Variable", sans-serif',
      fontWeight: 800,
    },
    h2: {
      fontFamily: '"Outfit", "Pretendard Variable", sans-serif',
      fontWeight: 700,
    },
  },
  palette: {
    primary: { main: '#0000FF' },
    secondary: { main: blueGrey[900] },
    background: {
      default: '#F5F5F5',
      paper: '#FFFFFF',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: '0 0 24px rgba(0,0,0,0.05)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none', // 대문자 변환 비활성화
        },
      },
    },
  },
  shape: {
    borderRadius: 0,
  },
});

export default theme;
```

---

## ThemeProvider 적용

```jsx
// src/App.jsx
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './styles/theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* 앱 컨텐츠 */}
    </ThemeProvider>
  );
}
```

---

## Storybook에서 Theme 적용

```jsx
// .storybook/preview.jsx
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from '../src/styles/theme';

const preview = {
  decorators: [
    (Story) => (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Story />
      </ThemeProvider>
    ),
  ],
};

export default preview;
```
