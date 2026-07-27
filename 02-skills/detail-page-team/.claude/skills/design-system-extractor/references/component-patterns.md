# Component Patterns

이커머스 상세페이지 컴포넌트 패턴 분석

## 핵심 컴포넌트

### 1. 히어로 섹션 (Hero)

```
┌─────────────────────────────────────────┐
│  [뱃지] [뱃지] [뱃지]                    │
│                                         │
│  # 상품명                               │
│  ## 서브카피                            │
│                                         │
│  ⭐ 4.8 (1,234개 리뷰)                  │
│                                         │
│  ₩29,900 ~~₩39,900~~ 25% 할인          │
│                                         │
│  🎁 추가 혜택 안내                      │
│                                         │
│  [CTA 버튼]                             │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "hero",
  "layout": "centered",
  "background": "primary-light 또는 gradient",
  "padding": "48-64px",
  "elements": [
    "badges",
    "title",
    "subtitle",
    "rating",
    "price",
    "benefits",
    "cta"
  ]
}
```

### 2. 혜택 카드 그리드 (Benefits Grid)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 🎯           │ │ ✅           │ │ 💎           │
│              │ │              │ │              │
│ 혜택 제목1   │ │ 혜택 제목2   │ │ 혜택 제목3   │
│              │ │              │ │              │
│ 설명 텍스트  │ │ 설명 텍스트  │ │ 설명 텍스트  │
└──────────────┘ └──────────────┘ └──────────────┘
```

**패턴 속성:**
```json
{
  "type": "benefitsGrid",
  "columns": 3,
  "gap": "24px",
  "cardStyle": {
    "background": "white",
    "padding": "24px",
    "borderRadius": "12px",
    "shadow": "sm"
  }
}
```

### 3. 비교 테이블 (Comparison Table)

```
┌─────────────┬─────────────┬─────────────┐
│ 항목        │ 우리 제품   │ 일반 제품   │
├─────────────┼─────────────┼─────────────┤
│ 특징1       │ ✅ 있음     │ ❌ 없음     │
│ 특징2       │ ✅ 우수     │ △ 보통      │
│ 특징3       │ ✅ 포함     │ ❌ 미포함   │
└─────────────┴─────────────┴─────────────┘
```

**패턴 속성:**
```json
{
  "type": "comparisonTable",
  "headerBackground": "primary-light",
  "highlightColumn": 1,
  "icons": {
    "positive": "✅",
    "negative": "❌",
    "neutral": "△"
  }
}
```

### 4. 신뢰 배지 섹션 (Trust Badges)

```
┌─────────────────────────────────────────┐
│  🏆 HACCP   📋 ISO9001   🔬 특허10건   │
│                                         │
│  [인증서 이미지들]                      │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "trustBadges",
  "layout": "horizontal-center",
  "badgeStyle": {
    "icon": true,
    "text": true,
    "border": "1px solid neutral-200"
  }
}
```

### 5. 이미지 갤러리 (Image Gallery)

```
┌─────────────────────────────────────────┐
│                                         │
│         [메인 이미지 - 100% 너비]        │
│                                         │
├─────────────────────────────────────────┤
│ [썸네일1] [썸네일2] [썸네일3] [썸네일4] │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "imageGallery",
  "mainImage": "full-width",
  "thumbnails": "horizontal-scroll",
  "aspectRatio": "4:3 또는 1:1"
}
```

### 6. 스펙/정보 테이블 (Spec Table)

```
┌─────────────────────────────────────────┐
│ 상품명        │ {상품명}                │
├───────────────┼─────────────────────────┤
│ 용량          │ 500ml x 6개             │
├───────────────┼─────────────────────────┤
│ 원산지        │ 국내산                  │
└───────────────┴─────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "specTable",
  "layout": "2-column",
  "headerWidth": "30%",
  "border": "1px solid neutral-200",
  "striped": true
}
```

### 7. FAQ 아코디언 (FAQ Accordion)

```
┌─────────────────────────────────────────┐
│ Q. 질문 내용? [▼]                       │
├─────────────────────────────────────────┤
│ A. 답변 내용이 여기에 표시됩니다.       │
│    상세한 설명을 포함할 수 있습니다.    │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "faqAccordion",
  "style": "bordered",
  "questionPrefix": "Q.",
  "answerPrefix": "A.",
  "icon": "chevron"
}
```

### 8. 리뷰 카드 (Review Card)

```
┌─────────────────────────────────────────┐
│ ⭐⭐⭐⭐⭐                              │
│                                         │
│ "리뷰 내용이 여기에 표시됩니다.         │
│  정말 좋아요!"                          │
│                                         │
│ — 구매자명 | 2024.01.15                 │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "reviewCard",
  "showRating": true,
  "showDate": true,
  "showVerified": true,
  "maxLines": 3
}
```

### 9. CTA 섹션 (Call to Action)

```
┌─────────────────────────────────────────┐
│                                         │
│      지금 바로 주문하세요!              │
│                                         │
│      ⏰ 오후 2시 전 주문 → 오늘 도착    │
│                                         │
│      [ 장바구니 담기 ]  [ 바로구매 ]    │
│                                         │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "ctaSection",
  "background": "primary-light 또는 neutral-100",
  "alignment": "center",
  "buttons": ["secondary", "primary"],
  "urgency": "optional"
}
```

### 10. 사용법 스텝 (How-to Steps)

```
┌─────────────────────────────────────────┐
│                                         │
│  Step 1     Step 2     Step 3           │
│  ○──────────○──────────○                │
│                                         │
│ [이미지]   [이미지]   [이미지]          │
│  설명1      설명2      설명3            │
│                                         │
└─────────────────────────────────────────┘
```

**패턴 속성:**
```json
{
  "type": "howToSteps",
  "layout": "horizontal",
  "showNumbers": true,
  "showConnector": true,
  "stepCount": 3
}
```

## 섹션 구조 패턴

### 9단계 구조
```
1. Hero (첫 화면)
2. Pain Points (공감)
3. Benefits (가치)
4. Features (상세)
5. Trust (신뢰)
6. How-to (사용법)
7. Specs (정보)
8. Reviews (후기)
9. CTA (전환)
```

## 출력 형식

### components.json
```json
{
  "patterns": {
    "hero": { ... },
    "benefitsGrid": { ... },
    "comparisonTable": { ... },
    "trustBadges": { ... },
    "imageGallery": { ... },
    "specTable": { ... },
    "faqAccordion": { ... },
    "reviewCard": { ... },
    "ctaSection": { ... },
    "howToSteps": { ... }
  },
  "detected": [
    "hero",
    "benefitsGrid",
    "specTable",
    "ctaSection"
  ],
  "structure": [
    { "section": 1, "component": "hero" },
    { "section": 2, "component": "benefitsGrid" },
    { "section": 3, "component": "specTable" },
    { "section": 4, "component": "ctaSection" }
  ]
}
```

## 스타일 변형

### 카드 스타일
```
- flat: 배경색만, 그림자 없음
- elevated: 그림자 있음
- outlined: 테두리 있음
- glass: 반투명 효과
```

### 버튼 스타일
```
- contained: 채워진 버튼 (Primary)
- outlined: 테두리 버튼 (Secondary)
- text: 텍스트만 (Tertiary)
```

### 배경 스타일
```
- solid: 단색
- gradient: 그라데이션
- image: 이미지 배경
- pattern: 패턴 배경
```
