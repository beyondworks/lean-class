# Color Extractor

CSS/HTML에서 컬러 시스템을 추출하는 규칙

## 색상 수집

### 1. CSS 색상 값 추출

```
수집 대상:
- hex: #RRGGBB, #RGB
- rgb: rgb(r, g, b)
- rgba: rgba(r, g, b, a)
- hsl: hsl(h, s%, l%)
- 이름: red, blue, etc (변환 필요)
```

### 2. 수집 위치

```css
/* 인라인 스타일 */
style="color: #333; background: #fff;"

/* CSS 변수 */
:root {
  --primary: #FF6B35;
}

/* 클래스 정의 */
.button { background-color: #4CAF50; }
```

## 색상 분류

### Primary (메인 액션)
```
식별 기준:
- 버튼 배경색
- 링크 색상
- 로고 색상
- CTA 요소

특징:
- 가장 눈에 띄는 색상
- 브랜드 대표 색상
- 액션 유도 요소에 사용
```

### Secondary (보조)
```
식별 기준:
- 보조 버튼
- 부가 정보 강조
- 서브 섹션 배경

특징:
- Primary와 조화
- 보조적 역할
```

### Neutral (회색 계열)
```
식별 기준:
- 텍스트 색상
- 배경 색상
- 테두리 색상

스케일 생성:
50, 100, 200, 300, 400, 500, 600, 700, 800, 900
```

### Text Colors
```
분류:
- primary: 본문 텍스트 (#212121, #333)
- secondary: 부가 텍스트 (#757575, #666)
- disabled: 비활성 (#BDBDBD, #999)
```

### Background Colors
```
분류:
- default: 메인 배경 (#FFFFFF)
- paper: 카드/섹션 배경 (#F5F5F5)
- dark: 푸터/다크 섹션
```

### Semantic Colors
```
- success: 성공/완료 (녹색 계열)
- warning: 경고/주의 (노란/주황)
- error: 오류/위험 (빨간 계열)
- info: 정보 (파란 계열)
```

## 색상 변환

### HEX 정규화
```javascript
// 3자리 → 6자리
#RGB → #RRGGBB
#F00 → #FF0000

// 소문자 통일
#AABBCC → #aabbcc
```

### RGB → HEX
```javascript
rgb(255, 107, 53) → #FF6B35
```

### 투명도 처리
```javascript
rgba(0, 0, 0, 0.5) → opacity 별도 기록
```

## Light/Dark 변형 생성

```javascript
// Primary에서 Light/Dark 생성
primary.main: #FF6B35
primary.light: lighten(main, 20%) → #FF8F66
primary.dark: darken(main, 20%) → #CC5429
```

## 빈도 분석

```
색상별 사용 빈도 카운트:
1. #FF6B35 - 47회 (버튼, 링크, 아이콘)
2. #333333 - 128회 (텍스트)
3. #FFFFFF - 89회 (배경)
...

상위 10개 → 핵심 팔레트
```

## 출력 형식

### colors.json
```json
{
  "primary": {
    "main": "#FF6B35",
    "light": "#FF8F66",
    "dark": "#CC5429",
    "contrastText": "#FFFFFF"
  },
  "secondary": {
    "main": "#004E89",
    "light": "#3371A1",
    "dark": "#003D6B",
    "contrastText": "#FFFFFF"
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
  "error": "#F44336",
  "info": "#2196F3"
}
```

## 검증

### 대비 비율 확인
```
텍스트 가독성:
- 일반 텍스트: 최소 4.5:1
- 큰 텍스트: 최소 3:1
- 버튼 텍스트: 최소 4.5:1

도구: WCAG Contrast Checker
```

### 일관성 확인
```
- 유사한 역할 → 같은 색상?
- 버튼들 색상 통일?
- 링크 색상 일관?
```

## 주의사항

1. **이미지 색상 제외** - CSS 색상만 추출
2. **그라데이션** - 시작/끝 색상 모두 기록
3. **투명도** - 불투명 버전으로 변환 후 기록
4. **다크 모드** - 별도 팔레트로 분리
