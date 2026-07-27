# Typography Analyzer

타이포그래피 시스템 분석 및 토큰화 규칙

## 수집 항목

### 1. Font Family

```css
/* 수집 대상 */
font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;

/* 분류 */
- base: 본문용 폰트
- heading: 제목용 폰트 (다른 경우)
- mono: 코드/숫자용 (있을 경우)
```

#### 한국어 웹폰트 우선순위
```
1순위: Pretendard (모던, 깔끔)
2순위: Noto Sans KR (범용, 안정적)
3순위: Spoqa Han Sans (깔끔)
4순위: Apple SD Gothic Neo (맥 기본)
5순위: Malgun Gothic (윈도우 기본)
```

### 2. Font Size

```css
/* 수집 대상 */
font-size: 16px;
font-size: 1rem;
font-size: 1.25em;

/* px로 정규화 */
1rem = 16px (기본)
1em = 부모 기준 계산
```

#### 표준 스케일 (8px 기반)
```
xs:   12px  (0.75rem)
sm:   14px  (0.875rem)
base: 16px  (1rem)
lg:   18px  (1.125rem)
xl:   20px  (1.25rem)
2xl:  24px  (1.5rem)
3xl:  32px  (2rem)
4xl:  40px  (2.5rem)
5xl:  48px  (3rem)
6xl:  64px  (4rem)
```

### 3. Font Weight

```css
/* 수집 대상 */
font-weight: 400;
font-weight: normal;
font-weight: bold;

/* 표준 분류 */
thin:      100
extralight: 200
light:     300
regular:   400
medium:    500
semibold:  600
bold:      700
extrabold: 800
black:     900
```

### 4. Line Height

```css
/* 수집 대상 */
line-height: 1.5;
line-height: 24px;
line-height: 150%;

/* 비율로 정규화 */
24px / 16px = 1.5

/* 표준 분류 */
tight:   1.2  (제목, 짧은 텍스트)
normal:  1.5  (본문)
relaxed: 1.75 (긴 텍스트, 가독성 중시)
loose:   2.0  (특수 경우)
```

### 5. Letter Spacing

```css
/* 수집 대상 */
letter-spacing: -0.02em;
letter-spacing: 0.5px;

/* 표준 분류 */
tighter: -0.05em
tight:   -0.025em
normal:  0
wide:    0.025em
wider:   0.05em
```

## 역할별 분류

### 제목 (Headings)
```
h1: 32-48px, bold (700), tight (1.2)
h2: 24-32px, bold (700), tight (1.2)
h3: 20-24px, semibold (600), normal (1.5)
h4: 18-20px, semibold (600), normal (1.5)
h5: 16-18px, medium (500), normal (1.5)
h6: 14-16px, medium (500), normal (1.5)
```

### 본문 (Body)
```
body1: 16px, regular (400), relaxed (1.75)
body2: 14px, regular (400), relaxed (1.75)
```

### 캡션/라벨
```
caption: 12px, regular (400), normal (1.5)
label:   14px, medium (500), normal (1.5)
```

### 버튼
```
button: 14-16px, semibold (600), normal (1.5)
```

## 스케일 정규화

### 8px 기반 정규화
```javascript
// 실제 값 → 가장 가까운 8px 배수
13px → 12px (xs)
15px → 16px (base)
17px → 16px (base)
22px → 24px (2xl)
```

### 비율 스케일 (1.25 배율)
```
12 × 1.25 = 15 → 16
16 × 1.25 = 20
20 × 1.25 = 25 → 24
24 × 1.25 = 30 → 32
32 × 1.25 = 40
40 × 1.25 = 50 → 48
```

## 출력 형식

### typography.json
```json
{
  "fontFamily": {
    "base": "'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif",
    "heading": "'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif",
    "mono": "'Roboto Mono', monospace"
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
  },
  "letterSpacing": {
    "tight": "-0.025em",
    "normal": "0",
    "wide": "0.025em"
  },
  "textStyles": {
    "h1": {
      "fontSize": "48px",
      "fontWeight": 700,
      "lineHeight": 1.2,
      "letterSpacing": "-0.025em"
    },
    "h2": {
      "fontSize": "32px",
      "fontWeight": 700,
      "lineHeight": 1.2,
      "letterSpacing": "-0.025em"
    },
    "h3": {
      "fontSize": "24px",
      "fontWeight": 600,
      "lineHeight": 1.5
    },
    "body1": {
      "fontSize": "16px",
      "fontWeight": 400,
      "lineHeight": 1.75
    },
    "body2": {
      "fontSize": "14px",
      "fontWeight": 400,
      "lineHeight": 1.75
    },
    "caption": {
      "fontSize": "12px",
      "fontWeight": 400,
      "lineHeight": 1.5
    },
    "button": {
      "fontSize": "14px",
      "fontWeight": 600,
      "lineHeight": 1.5,
      "textTransform": "none"
    }
  }
}
```

## 분석 리포트 형식

```markdown
## 타이포그래피 분석

### Font Family
- **본문**: 'Noto Sans KR'
- **제목**: 동일 (또는 다른 폰트)

### Size Scale
| 용도 | 크기 | Weight | Line Height |
|------|------|--------|-------------|
| H1 | 48px | Bold | 1.2 |
| H2 | 32px | Bold | 1.2 |
| Body | 16px | Regular | 1.75 |

### 인상
"{타이포그래피 전체 느낌 묘사}"
```

## 검증

### 가독성 확인
```
- 본문 최소 14px 이상?
- 줄간격 1.4 이상?
- 한글 폰트 지원?
```

### 스케일 일관성
```
- 일정한 배율로 증가?
- 역할별 명확한 구분?
```

## 주의사항

1. **한글 최적화** - 영문 폰트만 있으면 한글 대체 폰트 추가
2. **모바일** - 본문 최소 14px 권장
3. **제목** - 너무 크면 모바일에서 잘림 주의
