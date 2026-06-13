---
name: design-system-extractor
description: |
  레퍼런스 URL에서 디자인 시스템을 추출하는 스킬.
  Playwright 스크린샷 + HTML/CSS 분석으로 컬러, 타이포, 그리드, 컴포넌트 패턴 추출.
  "디자인 분석해줘", "레퍼런스 분석" 요청 시 사용합니다.
allowed-tools: []
---

# Design System Extractor

레퍼런스 URL → 디자인 토큰 + 컴포넌트 패턴 추출

## 개요

상세페이지 레퍼런스 URL을 분석하여:
1. **컬러 시스템** - Primary, Secondary, Neutral, Text, Background
2. **타이포그래피** - Font Family, Size Scale, Weight, Line Height
3. **그리드 시스템** - Container, Columns, Gutter, Margin
4. **간격 시스템** - Spacing Scale (4px/8px 기반)
5. **컴포넌트 패턴** - 섹션 구조, 카드, 버튼, 배너

## 워크플로우

```
[레퍼런스 URL]
      │
      ▼
┌─────────────────┐
│  1. Screenshot  │ ← Playwright 전체 페이지 캡처
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. HTML/CSS    │ ← web_fetch로 소스 추출
│     Extraction  │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────────┐
│ Color │ │ Typo  │ │ Grid  │ │ Component │
│Extract│ │Analyze│ │Analyze│ │  Pattern  │
└───┬───┘ └───┬───┘ └───┬───┘ └─────┬─────┘
    │         │        │            │
    └─────────┴────────┴────────────┘
                       │
                       ▼
              ┌───────────────┐
              │ Design Tokens │
              │    Output     │
              └───────────────┘
```

## 실행 단계

### Step 1: 스크린샷 캡처

```python
# Playwright로 전체 페이지 스크린샷
playwright screenshot {url} \
  --full-page \
  --wait-until networkidle \
  --output outputs/reference-screenshot.png
```

### Step 2: HTML/CSS 추출

```bash
# web_fetch로 페이지 소스 가져오기
# 인라인 스타일, 외부 CSS 모두 분석
```

### Step 3: 컬러 추출
**참조:**

1. CSS에서 색상 값 수집 (hex, rgb, hsl)
2. 사용 빈도 분석
3. 역할별 분류:
   - Primary: 메인 액션 색상
   - Secondary: 보조 색상
   - Accent: 강조 색상
   - Neutral: 회색 계열
   - Text: 텍스트 색상들
   - Background: 배경 색상들

### Step 4: 타이포그래피 분석
**참조:**

1. font-family 추출
2. font-size 사용 패턴 분석
3. font-weight 분류
4. line-height 패턴
5. 스케일 정규화 (8px 기반)

### Step 5: 그리드 분석
**참조:**

1. 컨테이너 max-width 측정
2. 컬럼 수 추정 (12컬럼 기본)
3. 거터/마진 측정
4. 반응형 브레이크포인트

### Step 6: 간격 분석
**참조:**

1. padding/margin 값 수집
2. 패턴 분석 (4px/8px 배수)
3. 간격 스케일 생성

### Step 7: 컴포넌트 패턴 분석
**참조:**

1. 섹션 구조 패턴
2. 카드 컴포넌트 스타일
3. 버튼 스타일
4. 배너/히어로 패턴

## 출력 구조

```
outputs/design-tokens/
├── colors.json         # 컬러 시스템
├── typography.json     # 타이포그래피
├── grid.json          # 그리드 시스템
├── spacing.json       # 간격 시스템
├── components.json    # 컴포넌트 패턴
├── tokens.css         # CSS 변수 형식
└── analysis.md        # 분석 리포트
```

### colors.json 형식
```json
{
  "primary": {
    "main": "#FF6B35",
    "light": "#FF8F66",
    "dark": "#CC5429"
  },
  "secondary": {
    "main": "#004E89",
    "light": "#3371A1",
    "dark": "#003D6B"
  },
  "neutral": {
    "50": "#FAFAFA",
    "100": "#F5F5F5",
    "200": "#EEEEEE",
    "300": "#E0E0E0",
    "400": "#BDBDBD",
    "500": "#9E9E9E",
    "600": "#757575",
    "700": "#616161",
    "800": "#424242",
    "900": "#212121"
  },
  "text": {
    "primary": "#212121",
    "secondary": "#757575",
    "disabled": "#BDBDBD"
  },
  "background": {
    "default": "#FFFFFF",
    "paper": "#F5F5F5",
    "dark": "#212121"
  },
  "success": "#4CAF50",
  "warning": "#FF9800",
  "error": "#F44336"
}
```

### typography.json 형식
```json
{
  "fontFamily": {
    "base": "'Noto Sans KR', sans-serif",
    "heading": "'Noto Sans KR', sans-serif"
  },
  "fontSize": {
    "xs": "12px",
    "sm": "14px",
    "base": "16px",
    "lg": "18px",
    "xl": "20px",
    "2xl": "24px",
    "3xl": "32px",
    "4xl": "40px",
    "5xl": "48px"
  },
  "fontWeight": {
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700
  },
  "lineHeight": {
    "tight": 1.2,
    "normal": 1.5,
    "relaxed": 1.75
  }
}
```

### grid.json 형식
```json
{
  "columns": 12,
  "container": {
    "sm": "540px",
    "md": "720px",
    "lg": "960px",
    "xl": "1140px",
    "default": "860px"
  },
  "gutter": {
    "xs": "16px",
    "sm": "20px",
    "md": "24px",
    "lg": "32px"
  },
  "margin": {
    "xs": "16px",
    "sm": "24px",
    "md": "32px",
    "lg": "auto"
  }
}
```

### spacing.json 형식
```json
{
  "base": 8,
  "scale": {
    "0": "0px",
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px"
  }
}
```

### tokens.css 형식
```css
:root {
  /* Colors */
  --color-primary-main: #FF6B35;
  --color-primary-light: #FF8F66;
  --color-primary-dark: #CC5429;
  
  --color-text-primary: #212121;
  --color-text-secondary: #757575;
  
  --color-bg-default: #FFFFFF;
  --color-bg-paper: #F5F5F5;
  
  /* Typography */
  --font-family-base: 'Noto Sans KR', sans-serif;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
  --font-size-2xl: 32px;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  
  /* Grid */
  --container-max: 860px;
  --gutter: 24px;
}
```

## 분석 리포트 형식

```markdown
# 디자인 시스템 분석 리포트

## 레퍼런스
- URL: {url}
- 분석 일시: {datetime}
- 스크린샷: outputs/reference-screenshot.png

---

## 브랜드 인상 (Visual First)

"{사람 눈으로 본 듯한 전체 인상 묘사}"

---

## 컬러 시스템

### Primary Color
- **{hex}** - {역할 설명}
- 사용처: {버튼, 링크, 강조 등}

### Secondary Color
- **{hex}** - {역할 설명}

### Neutral Scale
{회색 계열 스케일}

---

## 타이포그래피

### Font Family
- 본문: {font}
- 제목: {font}

### Size Scale
- H1: {size}
- H2: {size}
...

---

## 그리드 시스템

- Container: {width}
- Columns: {n}
- Gutter: {px}

---

## 주요 컴포넌트 패턴

### 히어로 섹션
{패턴 설명}

### 카드 컴포넌트
{패턴 설명}

### CTA 버튼
{패턴 설명}
```

## 참조 문서

| 문서 | 용도 |
|------|------|
| | 컬러 추출 규칙 |
| | 타이포 분석 규칙 |
| | 그리드 분석 규칙 |
| | 간격 분석 규칙 |
| | 컴포넌트 패턴 |

## 스크립트

| 스크립트 | 용도 |
|----------|------|
| `scripts/extract_colors.py` | CSS에서 색상 추출 |
| `scripts/analyze_typography.py` | 타이포 분석 |
| `scripts/measure_grid.py` | 그리드 측정 |

## 체크리스트

- [ ] 스크린샷 캡처 완료
- [ ] 컬러 시스템 추출 완료
- [ ] 타이포그래피 분석 완료
- [ ] 그리드 시스템 측정 완료
- [ ] 간격 시스템 분석 완료
- [ ] 컴포넌트 패턴 식별 완료
- [ ] JSON 토큰 파일 생성
- [ ] CSS 변수 파일 생성
- [ ] 분석 리포트 작성
