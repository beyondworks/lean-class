# Spacing System

간격 시스템 설계 및 토큰화

## 핵심 원칙

### 기본 단위 (Base Unit)

```
대부분의 디자인 시스템: 4px 또는 8px 기반

4px 기반: 세밀한 조정 가능 (4, 8, 12, 16, 20, 24...)
8px 기반: 더 일관된 리듬 (8, 16, 24, 32, 40, 48...)
```

### 시각적 판단

스크린샷에서 간격 측정 후 가장 가까운 기본 단위 배수로 정규화:

```
측정값 7px → 8px로 정규화
측정값 25px → 24px로 정규화
측정값 50px → 48px로 정규화
```

## 간격 스케일

### 절대 스케일

```typescript
export const spacing = {
  unit: 8,
  
  scale: {
    '0': 0,
    '0.5': 2,    // 4px 기반 시스템용
    '1': 4,
    '2': 8,
    '3': 12,
    '4': 16,
    '5': 20,
    '6': 24,
    '7': 28,
    '8': 32,
    '9': 36,
    '10': 40,
    '12': 48,
    '14': 56,
    '16': 64,
    '20': 80,
    '24': 96,
    '28': 112,
    '32': 128,
    '36': 144,
    '40': 160,
  },
};
```

### 시맨틱 스케일

```typescript
export const semanticSpacing = {
  // 컴포넌트 내부 패딩
  inset: {
    xs: 4,     // 태그, 뱃지 내부
    sm: 8,     // 작은 버튼, 칩
    md: 12,    // 기본 버튼, 인풋
    lg: 16,    // 카드 내부
    xl: 24,    // 모달, 큰 카드
    '2xl': 32, // 섹션 내부
  },
  
  // 수평 간격 (인라인 요소)
  inline: {
    xs: 4,     // 아이콘-텍스트
    sm: 8,     // 버튼 그룹 내
    md: 12,    // 탭 사이
    lg: 16,    // 네비게이션 아이템
    xl: 24,    // 헤더 섹션 사이
  },
  
  // 수직 간격 (스택 요소)
  stack: {
    xs: 4,     // 라벨-인풋
    sm: 8,     // 리스트 아이템 내
    md: 12,    // 폼 필드 사이
    lg: 16,    // 카드 내 요소
    xl: 24,    // 콘텐츠 블록 사이
    '2xl': 32, // 큰 블록 사이
  },
  
  // 섹션 간격
  section: {
    xs: 32,    // 소형 섹션
    sm: 48,    // 모바일 섹션
    md: 64,    // 기본 섹션
    lg: 80,    // 강조 섹션
    xl: 96,    // 대형 섹션
    '2xl': 128, // 히어로 후 첫 섹션
  },
  
  // 페이지 여백
  page: {
    xs: 16,    // 모바일
    sm: 24,    // 태블릿
    md: 32,    // 소형 데스크톱
    lg: 48,    // 대형 데스크톱
  },
};
```

## 반응형 간격

### 브레이크포인트별 조정

```typescript
export const responsiveSpacing = {
  // 컨테이너 패딩
  containerPadding: {
    xs: 16,   // 0-639px
    sm: 24,   // 640-767px
    md: 32,   // 768-1023px
    lg: 48,   // 1024px+
  },
  
  // 섹션 수직 패딩
  sectionPadding: {
    xs: { y: 48 },
    sm: { y: 64 },
    md: { y: 80 },
    lg: { y: 96 },
  },
  
  // 그리드 거터
  gridGutter: {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
  },
  
  // 카드 간격
  cardGap: {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
  },
};
```

## 스크린샷 분석 방법

### 격자 오버레이 사용

```bash
python scripts/grid_analyzer.py screenshot.png --grid 8
```

생성된 기준선 격자(8px)와 요소를 대조하여 측정.

### 측정 포인트

```
1. 섹션 간 간격
   → 두 섹션 사이 빈 공간 높이
   
2. 컨테이너 패딩
   → 콘텐츠와 화면 가장자리 사이
   
3. 카드 간격
   → 카드 사이 빈 공간
   
4. 카드 내부 패딩
   → 카드 테두리와 콘텐츠 사이
   
5. 요소 간 간격
   → 제목-본문, 본문-버튼 등
```

### 측정 결과 기록

```markdown
## 간격 측정 결과

### 섹션 간격
- 히어로 → 첫 섹션: ~120px → 128px로 정규화
- 일반 섹션 간: ~80px → 80px
- 모바일 섹션 간: ~48px → 48px

### 컨테이너 패딩
- 데스크톱: ~48px
- 태블릿: ~32px
- 모바일: ~16px

### 카드 간격
- 데스크톱: ~24px
- 모바일: ~16px

### 카드 내부 패딩
- 일반: ~24px
- 작은 카드: ~16px

### 요소 간 간격
- 제목-본문: ~16px
- 본문-버튼: ~24px
- 아이콘-텍스트: ~8px
```

## MUI 테마 변환

### spacing 함수

```typescript
// MUI는 spacing 단위를 곱해서 사용
// spacing(1) = 8px (기본)

const theme = createTheme({
  spacing: 8, // 기본 단위
});

// 사용 예:
// spacing(1) = 8px
// spacing(2) = 16px
// spacing(3) = 24px
```

### sx prop 사용

```tsx
<Box sx={{
  p: 2,        // padding: 16px
  m: 3,        // margin: 24px
  gap: 2,      // gap: 16px
  mt: 4,       // marginTop: 32px
  px: 3,       // paddingX: 24px
}} />
```

### 시맨틱 값 사용

```typescript
// theme.ts
const theme = createTheme({
  spacing: 8,
  
  // 커스텀 간격 변수
  customSpacing: {
    section: {
      sm: 48,
      md: 64,
      lg: 80,
    },
    card: {
      padding: 24,
      gap: 24,
    },
  },
});

// 사용
<Box sx={{ 
  py: theme => theme.customSpacing.section.md / 8,
  // 또는
  py: '64px',
}} />
```

## 출력 형식

### tokens/spacing.ts

```typescript
export const spacing = {
  unit: 8,
  
  // 절대 스케일
  scale: {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    8: 32,
    10: 40,
    12: 48,
    16: 64,
    20: 80,
    24: 96,
    32: 128,
  },
  
  // 시맨틱 스케일
  semantic: {
    inset: {
      xs: 4,
      sm: 8,
      md: 12,
      lg: 16,
      xl: 24,
    },
    inline: {
      xs: 4,
      sm: 8,
      md: 12,
      lg: 16,
      xl: 24,
    },
    stack: {
      xs: 4,
      sm: 8,
      md: 12,
      lg: 16,
      xl: 24,
    },
    section: {
      sm: 48,
      md: 64,
      lg: 80,
      xl: 96,
    },
    page: {
      xs: 16,
      sm: 24,
      md: 32,
      lg: 48,
    },
  },
} as const;
```

## 체크리스트

- [ ] 기본 단위 결정됨 (4px or 8px)
- [ ] 절대 스케일 정의됨
- [ ] 시맨틱 스케일 정의됨
- [ ] 반응형 간격 정의됨
- [ ] 섹션 간격 측정됨
- [ ] 컴포넌트 간격 측정됨
- [ ] MUI spacing 설정됨
