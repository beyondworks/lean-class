# MUI Grid Usage Rules (CRITICAL)

MUI Grid 컴포넌트 사용 규칙. **절대 위반 금지**.

---

## Import 규칙

### ❌ 잘못된 Import (절대 사용 금지)
```jsx
import Grid from '@mui/material/Grid2';  // 틀림! 사용 금지!
```

### ✅ 올바른 Import (반드시 이것만 사용)
```jsx
import Grid from '@mui/material/Grid';   // 정확함! 이것만 사용!
```

**중요**: MUI v7에서는 `Grid2`가 아닌 `Grid`를 직접 import해야 한다.

---

## Props 규칙 (MUI v6+)

### ❌ 잘못된 Props (구버전 문법)
```jsx
<Grid container>
  <Grid item xs={6} md={8}>  {/* 틀림! */}
    <Item />
  </Grid>
</Grid>
```

### ✅ 올바른 Props (v6+ 문법)
```jsx
<Grid container spacing={2}>
  <Grid size={{ xs: 6, md: 8 }}>  {/* 정확함! */}
    <Item />
  </Grid>
</Grid>
```

---

## 완전한 예시

```jsx
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: (theme.vars ?? theme).palette.text.secondary,
  ...theme.applyStyles('dark', {
    backgroundColor: '#1A2027',
  }),
}));

export default function FullWidthGrid() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid size={{ xs: 6, md: 8 }}>
          <Item>xs=6 md=8</Item>
        </Grid>
        <Grid size={{ xs: 6, md: 4 }}>
          <Item>xs=6 md=4</Item>
        </Grid>
        <Grid size={{ xs: 6, md: 4 }}>
          <Item>xs=6 md=4</Item>
        </Grid>
        <Grid size={{ xs: 6, md: 8 }}>
          <Item>xs=6 md=8</Item>
        </Grid>
      </Grid>
    </Box>
  );
}
```

---

## Size Prop 사용법

### 반응형 크기 지정
```jsx
<Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
  {/*
    xs (0-600px): 전체 너비
    sm (600-900px): 절반
    md (900-1200px): 1/3
    lg (1200px+): 1/4
  */}
</Grid>
```

### 고정 크기
```jsx
<Grid size={6}>  {/* 모든 브레이크포인트에서 6/12 = 50% */}
</Grid>
```

### Auto 크기
```jsx
<Grid size="auto">  {/* 콘텐츠에 맞춤 */}
</Grid>
```

### Grow (남은 공간 채우기)
```jsx
<Grid size="grow">  {/* flex-grow: 1 */}
</Grid>
```

---

## Container Props

```jsx
<Grid
  container
  spacing={2}           // gap 설정 (theme.spacing 단위)
  direction="row"       // row | row-reverse | column | column-reverse
  justifyContent="center"
  alignItems="stretch"
>
  {/* children */}
</Grid>
```

---

## Nested Grid

```jsx
<Grid container spacing={2}>
  <Grid size={{ xs: 12, md: 6 }}>
    {/* Nested container */}
    <Grid container spacing={1}>
      <Grid size={6}>
        <Item>Nested 1</Item>
      </Grid>
      <Grid size={6}>
        <Item>Nested 2</Item>
      </Grid>
    </Grid>
  </Grid>
</Grid>
```

---

## 주의사항

1. **절대로 `Grid2` import 사용 금지**
2. **`item` prop 사용하지 않음** (v6+에서는 불필요)
3. **`xs`, `md` 등을 직접 prop으로 사용하지 않음** → `size` prop 사용
4. **container와 size는 동시 사용 가능** (v6+)
