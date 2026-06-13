---
name: slide-generation
description: "대화 기반 HTML 슬라이드 생성 스킬. 사용자와 대화하며 내용 구조화, 디자인 토큰 적용, 레이아웃 배치, 애니메이션 연결까지 완성된 HTML 프레젠테이션을 출력. 모든 하위 스킬(theme/typography/layout/motion)을 통합 소비."
---

# Slide Generation

대화 기반 HTML 프레젠테이션 생성 -- 모든 스킬의 최종 통합점

## Core Purpose

**사용자가 내용을 말하면, 프로급 HTML 슬라이드가 나온다**

```
사용자: "AI 트렌드에 대한 10장짜리 발표자료 만들어줘"
    |
    v
[Content Structuring] 내용 -> 슬라이드 구조
    |
    v
[Theme Application] 디자인 토큰 적용
    |
    v
[Layout Mapping] 슬라이드별 레이아웃 선택
    |
    v
[Animation Assignment] 모션 효과 배정
    |
    v
[HTML Assembly] 완성된 슬라이드 덱 출력
```

---

## Input Modes

### Mode A: 레퍼런스 이미지 + 내용

```
입력: PPT 이미지 + "이 디자인으로 AI 트렌드 발표자료"
       (선택) 원고/리포트 파일 또는 텍스트 붙여넣기
처리: Design Cloner -> 토큰 추출 -> 원고 파싱 -> 슬라이드 생성
```

#### 원고/리포트 첨부 시 자동 파싱 프로토콜

```
Step 1: 원고 유형 감지
  - 보고서 (섹션/목차 구조)
  - 기획서/제안서 (문제-해결-기대효과)
  - 논문/리서치 (서론-본론-결론-참고)
  - 자유 형식 (단락 나열)

Step 2: 핵심 메시지 추출
  - 각 섹션에서 핵심 문장 1-2개 추출
  - 수치/데이터 포인트 자동 감지 (매출, 성장률, 시장 규모 등)
  - 키워드/고유명사 보존

Step 3: 슬라이드 분배
  - 원고 분량 기준 슬라이드 수 자동 결정
    · ~1,000자: 5-7장
    · 1,000~3,000자: 8-12장
    · 3,000~5,000자: 12-15장
    · 5,000자+: 15-20장 (초과 시 사용자 확인)
  - 섹션 → 슬라이드 1:1~1:3 매핑
  - 수치 데이터 → layout-metrics 자동 배정
  - 비교/목록 → layout-cards 자동 배정
  - 설명+이미지 → layout-split 자동 배정

Step 4: 구조안 확인 (질문 최소화)
  - "원고를 분석하여 {N}장 구조로 정리했습니다."
  - 슬라이드 목록 + 각 슬라이드 핵심 내용 요약 제시
  - "이대로 진행할까요? 수정할 부분이 있으면 말씀해주세요."
  - 확인 후 바로 HTML 조립 진행
```

CRITICAL: 원고 파싱 시 원문의 핵심 메시지와 수치를 왜곡하지 않는다.
슬라이드용으로 요약할 뿐, 의미를 변경하거나 없는 내용을 추가하지 않는다.

### Mode B: 대화로 처음부터

```
입력: "투자자 피칭 발표자료 15장"
처리: 테마 제안 -> 사용자 선택 -> 슬라이드 생성
```

### Mode C: 기존 슬라이드 수정

```
입력: "3번 슬라이드 레이아웃을 좌우 분할로 바꿔줘"
처리: 해당 슬라이드만 수정
```

---

## Phase 0: Narrative Thinking (내부 추론 -- 출력하지 않음)

슬라이드 구조 설계 전, 다음 사고 프레임워크를 **내부적으로** 실행한다.
이 과정의 결과물은 사용자에게 출력하지 않고, 슬라이드 구조 설계에만 반영한다.

```
Step 1: 주제 클러스터링
  - 입력 자료(원고/대화)에서 핵심 주제 3-5개 추출
  - 각 주제 간 관계 파악 (인과/병렬/시간순)

Step 2: 핵심 질문 정의
  - "청중이 가장 궁금해할 질문은?"
  - "이 발표가 답해야 할 핵심 질문 1가지는?"

Step 3: 논증 구조 수립
  - 주장(Thesis): 발표의 핵심 메시지 1문장
  - 키워드: 슬라이드 전체를 관통하는 핵심어 3-5개

Step 4: 증거 매핑
  - 각 주장을 뒷받침하는 데이터/사례/인용 연결
  - 증거 없는 주장은 제거하거나 "의견" 표시

Step 5: 내러티브 연결
  - 슬라이드 간 논리적 흐름 설계
  - 각 슬라이드의 "이 슬라이드가 왜 여기에 있는가" 답변 가능해야 함

Step 6: 반론/리스크 검토
  - 청중이 반박할 수 있는 포인트 사전 식별
  - FAQ 슬라이드 또는 선제적 답변 삽입 여부 결정

Step 7: 자기검증
  - 근거 없는 주장이 있는가?
  - 논리적 비약이 있는가?
  - 슬라이드 순서가 자연스러운가?
```

CRITICAL: 이 프레임워크는 내부 추론용이다.
사용자에게 Step 1~7 결과를 출력하지 않는다.
결과는 슬라이드 구조와 내용에 자연스럽게 녹여낸다.

---

## Phase 1: Content Structuring

### 1.1 발표 목적 파악

```
질문 (최대 3개):
1. "어떤 주제의 발표인가요?"
2. "청중은 누구인가요?" (경영진/개발자/일반/투자자)
3. "몇 장 분량인가요?" (기본: 10장)
```

### 1.2 슬라이드 구조 자동 설계

발표 유형별 표준 구조:

#### 비즈니스 보고

```
1. Cover (표지)               -> layout-title
2. Agenda (목차)               -> layout-content
3. Executive Summary (요약)    -> layout-content
4-6. Key Findings (핵심 내용)  -> layout-split / layout-cards
7. Data/Metrics (성과)         -> layout-metrics
8. Action Items (다음 단계)    -> layout-content
9. Timeline (일정)             -> layout-timeline
10. Thank You (마무리)         -> layout-title
```

#### 투자자 피칭

```
1. Cover + 한줄 소개           -> layout-title
2. Problem (문제)              -> layout-split
3. Solution (솔루션)           -> layout-split
4. Market Size (시장 규모)     -> layout-metrics
5. Product (제품 데모)         -> layout-fullimage
6. Traction (견인력)           -> layout-metrics
7. Business Model (수익 모델)  -> layout-cards
8. Competition (경쟁 분석)     -> layout-cards
9. Team (팀 소개)              -> layout-cards
10. Ask (투자 요청)            -> layout-title
```

#### 교육/강연

```
1. Cover                       -> layout-title
2. Today's Topic (주제 소개)   -> layout-content
3-7. Main Content (핵심 내용)  -> layout-split / layout-content
8. Summary (요약)              -> layout-cards
9. Q&A                         -> layout-title
10. Contact (연락처)           -> layout-title
```

#### 프로젝트 제안

```
1. Cover                       -> layout-title
2. Background (배경)           -> layout-content
3. Objective (목표)            -> layout-content
4. Approach (접근법)           -> layout-timeline
5-6. Detail (상세 내용)        -> layout-split
7. Expected Results (기대효과) -> layout-metrics
8. Budget/Resources (예산)     -> layout-content
9. Timeline (일정)             -> layout-timeline
10. Next Steps (다음 단계)     -> layout-content
```

### 1.3 한글 콘텐츠 작성 규칙

```
제목: 최대 15자 (한글 기준)
  -- 핵심 키워드 앞에 배치
  -- 숫자가 있으면 강조 효과 활용

부제목: 최대 30자
  -- 제목을 보충하는 한 줄 설명

본문: 한 슬라이드 3-5 포인트
  -- 한 포인트 당 1-2줄
  -- 완전한 문장보다 키워드 중심

숫자: 단위 명시 (원, 건, %, 명)
  -- 1000 이상은 쉼표 (1,234)
  -- 큰 숫자는 억/만 단위 (12.5억)
```

---

## Phase 2: Theme Application

### 2.1 테마 선택 (Mode B)

레퍼런스 이미지가 없을 때 테마 프리셋 제안:

```
프리셋 A: "모던 다크"
  Surface: #0F172A, Text: #F1F5F9, Primary: #3B82F6
  느낌: 테크, 스타트업, 미래지향

프리셋 B: "클린 라이트"
  Surface: #FFFFFF, Text: #1E293B, Primary: #2563EB
  느낌: 비즈니스, 전문적, 깔끔

프리셋 C: "웜 프리미엄"
  Surface: #FFFBF5, Text: #1C1917, Primary: #D97706
  느낌: 고급, 따뜻한, 브랜딩

프리셋 D: "네이처 그린"
  Surface: #F0FDF4, Text: #14532D, Primary: #16A34A
  느낌: 친환경, 건강, 성장

프리셋 E: "바이올렛 크리에이티브"
  Surface: #FAF5FF, Text: #3B0764, Primary: #7C3AED
  느낌: 크리에이티브, 혁신, 대담
```

### 2.2 토큰 적용

Design Cloner 또는 프리셋에서 생성된 tokens.css를
theme/tokens.css에 배치.

---

## Phase 3: HTML Assembly

### 3.1 프로젝트 파일 구조

```
{project-name}/
  index.html                -- 메인 파일
  theme/
    tokens.css              -- 디자인 토큰
    typography.css           -- 타이포그래피
    layout.css              -- 레이아웃
    motion.css              -- 애니메이션
    components.css          -- 컴포넌트
    theme.css               -- 통합 import
  scripts/
    slide-controller.js     -- 슬라이드 네비게이션
    animations.js           -- 애니메이션 트리거
    theme-controller.js     -- 테마 전환 (Light/Dark)
  assets/
    images/                 -- 이미지
    icons/                  -- SVG 아이콘
```

### 3.2 index.html 템플릿

```html
<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{프레젠테이션 제목}</title>

  <!-- Fonts -->
  <link rel="preload"
    href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
    as="style" />
  <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />

  <!-- Theme -->
  <link rel="stylesheet" href="theme/theme.css" />

  <style>
    /* 기본 리셋 */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { font-size: 16px; }
    body {
      font-family: var(--font-body);
      background: var(--color-surface-base);
      color: var(--color-text-body);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  </style>
</head>
<body>

  <div class="slide-deck">

    <!-- Slide 1: Cover -->
    <div class="slide" data-transition="fade">
      <div class="slide-content layout-title">
        <span class="text-overline" data-animate="fade-up">
          {카테고리}
        </span>
        <h1 class="text-display-xl" data-animate="fade-up" data-delay="1">
          {메인 제목}
        </h1>
        <p class="text-body-lg" data-animate="fade-up" data-delay="2"
           style="color: var(--color-text-muted);">
          {부제목 또는 날짜/발표자}
        </p>
      </div>
    </div>

    <!-- Slide 2~N: Content slides here -->

  </div>

  <!-- Slide Controls -->
  <div class="slide-controls">
    <button class="slide-prev" aria-label="이전 슬라이드">&#8592;</button>
    <span class="slide-indicator">1 / {total}</span>
    <button class="slide-next" aria-label="다음 슬라이드">&#8594;</button>
    <button class="slide-fullscreen" aria-label="전체화면">&#x26F6;</button>
  </div>

  <script src="scripts/slide-controller.js"></script>
  <script src="scripts/animations.js"></script>
  <script src="scripts/theme-controller.js"></script>
</body>
</html>
```

### 3.3 슬라이드 유형별 HTML 패턴

#### Content Slide

```html
<div class="slide" data-transition="slide">
  <div class="slide-content layout-content">
    <div class="content-header">
      <span class="text-overline" data-animate="fade-up">{섹션명}</span>
      <h2 class="text-heading-lg" data-animate="fade-up" data-delay="1">
        {제목}
      </h2>
    </div>
    <div class="content-body">
      <p class="text-body-lg" data-animate="fade-up" data-delay="2">
        {본문 내용}
      </p>
      <ul class="text-body" style="display:flex; flex-direction:column; gap:var(--space-3);">
        <li data-animate="fade-up" data-delay="3">{포인트 1}</li>
        <li data-animate="fade-up" data-delay="4">{포인트 2}</li>
        <li data-animate="fade-up" data-delay="5">{포인트 3}</li>
      </ul>
    </div>
  </div>
</div>
```

#### Split Slide

```html
<div class="slide" data-transition="fade">
  <div class="slide-content layout-split">
    <div class="split-left flex-col justify-center" style="gap:var(--content-gap);">
      <span class="text-overline" data-animate="slide-left">{섹션}</span>
      <h2 class="text-heading-lg" data-animate="slide-left" data-delay="1">
        {제목}
      </h2>
      <p class="text-body" data-animate="slide-left" data-delay="2">
        {설명}
      </p>
    </div>
    <div class="split-right" data-animate="slide-right" data-delay="2">
      <img src="assets/images/{image}" class="slide-image" alt="{설명}" />
    </div>
  </div>
</div>
```

#### Metrics Slide

```html
<div class="slide" data-transition="scale">
  <div class="slide-content layout-metrics">
    <div class="content-header text-center">
      <h2 class="text-heading-lg" data-animate="fade-up">{제목}</h2>
    </div>
    <div class="metrics-grid">
      <div class="metric-item" data-animate="scale-up" data-delay="1">
        <span class="metric-value"
              data-count-to="{숫자}" data-suffix="{단위}">0</span>
        <span class="metric-label">{라벨}</span>
      </div>
      <!-- 반복 -->
    </div>
  </div>
</div>
```

#### Cards Grid Slide

```html
<div class="slide" data-transition="fade">
  <div class="slide-content layout-cards">
    <div class="cards-header">
      <h2 class="text-heading-lg" data-animate="fade-up">{제목}</h2>
    </div>
    <div class="cards-grid" data-cols="3">
      <div class="card hover-lift" data-animate="fade-up" data-delay="1"
           style="background:var(--card-bg); border:var(--card-border);
                  border-radius:var(--card-radius); padding:var(--card-padding);
                  box-shadow:var(--card-shadow);">
        <div class="shape-icon-box" style="margin-bottom:var(--space-4);">
          <!-- icon SVG -->
        </div>
        <h3 class="text-heading-sm">{카드 제목}</h3>
        <p class="text-body-sm" style="color:var(--color-text-muted);">
          {카드 설명}
        </p>
      </div>
      <!-- 반복 -->
    </div>
  </div>
</div>
```

---

## Phase 3.5: Chunk-Based Generation (20장 초과 시)

20장을 초과하는 대량 슬라이드는 청크 단위로 나누어 생성한다.
한 번에 전체를 생성하면 후반부 품질이 떨어지므로, 청크 분할이 필수다.

### 청크 분할 규칙

```
슬라이드 수 자동 조정:
  - 최소: 5장
  - 최대: 60장 (초과 시 사용자 확인 후 조정)

청크 크기: 20장 단위
  - 1~20장: 청크 1개 (분할 없음)
  - 21~40장: 청크 2개 (1-20, 21-N)
  - 41~60장: 청크 3개 (1-20, 21-40, 41-N)
```

### 청크별 내러티브 구조

```
각 청크는 독립적 서사 흐름을 유지한다:

청크 내부 구조 (20장 기준):
  1-4장:   문제 제기 / 맥락 설정
  5-10장:  핵심 개념 / 프레임워크
  11-16장: 증거 / 데이터 / 사례
  17-20장: 요약 + 다음 청크 전환

마지막 청크:
  17-19장: 전체 요약 / 핵심 정리
  마지막장: 마무리 (Thank You / CTA / Q&A)
```

### 청크 생성 규칙

```
청크 1 (슬라이드 1~20):
  - 커버(표지) 슬라이드: 1장에만 배치
  - 마무리 슬라이드: 생성 금지
  - 20장에서 다음 청크로의 전환 흐름 유지

청크 2 (슬라이드 21~40):
  - 커버 슬라이드: 생성 금지 (바로 본문 시작)
  - 마무리 슬라이드: 생성 금지 (마지막 청크가 아닌 경우)

청크 3 / 마지막 (슬라이드 41~N):
  - 커버 슬라이드: 생성 금지
  - 마무리 슬라이드: 마지막 장에만 배치
```

### 청크 간 연결

```
각 청크의 마지막 슬라이드는 다음 청크의 첫 슬라이드와
논리적으로 연결되어야 한다:

  청크 1 끝: "지금까지 ~를 살펴봤습니다. 이어서 ~를 알아보겠습니다."
  청크 2 시작: 앞 내용을 자연스럽게 이어받는 제목/구성
```

### 청크 생성 후 자기검증

```
각 청크 생성 완료 후 내부 검증:
  - 슬라이드 수가 정확한가? (예: 20장)
  - 슬라이드 번호가 연속인가? (예: 21-40)
  - 커버/마무리 위치 규칙을 지켰는가?
  - 이전 청크와 내용이 중복되지 않는가?
  - 다음 청크로의 전환이 자연스러운가?
```

CRITICAL: 청크 분할은 생성 과정에서만 적용한다.
최종 출력은 하나의 index.html에 모든 슬라이드가 통합된다.

---

## Phase 3.6: Speaker Script (발표 대본)

각 슬라이드에 발표자가 읽을 구어체 대본을 함께 생성한다.
대본은 HTML의 data 속성에 저장하여 발표자 모드에서 표시한다.

### 대본 작성 규칙

```
형식:
  - 존댓말 구어체 (발표 현장에서 읽는 톤)
  - 슬라이드당 3~5문장
  - 화면 텍스트를 그대로 읽지 않고, 보충 설명

톤 조절:
  "담백하게"   -> 사실 중심, 군더더기 없음
  "친근하게"   -> 질문형, 공감 표현 포함
  "설득적으로" -> 근거 강조, 행동 유도
  "기본"       -> 자연스러운 존댓말
```

### HTML 적용 방식

```html
<div class="slide" data-transition="fade"
     data-speaker-note="여기에 발표 대본이 들어갑니다. 청중 여러분, 이 데이터를 보시면...">
  <div class="slide-content layout-content">
    <!-- 화면 콘텐츠 -->
  </div>
</div>
```

### 발표자 모드 표시

```
슬라이드 컨트롤러에서 'N' 키를 누르면 발표자 노트 패널이 토글된다.
발표자 노트는 화면 하단에 반투명 패널로 표시된다.
청중에게는 보이지 않고, 발표자 화면에서만 확인 가능하다.
```

CRITICAL: 대본은 화면 텍스트의 단순 반복이 아니다.
화면에 없는 맥락, 배경, 전환 멘트를 포함해야 한다.

---

## Phase 4: Animation Assignment

### 슬라이드 유형별 기본 애니메이션

| 슬라이드 유형 | 전환 효과 | 요소 애니메이션 |
|-------------|----------|---------------|
| Cover/Title | fade | TextReveal (제목), fadeUp (부제) |
| Content | slide | fadeUp (순차) |
| Split | fade | slideLeft/Right (좌우 각각) |
| Cards | fade | fadeUp + stagger |
| Metrics | scale | scaleUp + CountUp |
| Timeline | slide | fadeUp + stagger |
| Full Image | zoom | blurIn (텍스트) |
| Thank You | fade | scaleUp |

### 모션 강도 조절

```
사용자 요청에 따라:
  "심플하게" -> data-animate 최소화, fade만
  "화려하게" -> 다양한 효과, stagger, 긴 duration
  "기본"     -> 위 기본 테이블 따름
```

---

## Conversation Flow

### 사용자와 대화 패턴

```
[시작]
"어떤 주제의 발표를 만드시나요?"

[내용 확인]
"10장 구성으로 정리했습니다:
1. 표지: {제목}
2. 목차
3-7. {핵심 내용}
8. 데이터
9. 다음 단계
10. 마무리

이 구성으로 진행할까요? 수정하고 싶은 부분이 있으면 말씀해주세요."

[테마 확인 (레퍼런스 없을 때)]
"테마를 선택해주세요:
A. 모던 다크 (테크 느낌)
B. 클린 라이트 (깔끔 비즈니스)
C. 웜 프리미엄 (고급스러운)
D. 추천해주세요 (주제에 맞게)"

[생성]
"슬라이드를 생성합니다..."

[완료]
"{프로젝트명}/ 폴더에 생성 완료.
index.html을 브라우저에서 열면 확인할 수 있습니다.
방향키(← →)로 슬라이드를 넘기고, F키로 전체화면입니다."
```

---

## Quality Checklist

- [ ] 슬라이드 장수가 요청과 일치
- [ ] 모든 텍스트가 한글 정합성 유지 (word-break: keep-all)
- [ ] 모든 색상/간격이 토큰 참조
- [ ] 핵심 문장이 3초 안에 보이고 강조되어 있음
- [ ] 텍스트-heavy 장표를 그래프/플로우차트/카드/상태 패널/이미지 플레이스홀더로 구조화함
- [ ] 실제 화면 캡처가 필요한 곳은 `[IMAGE PLACEHOLDER]`와 캡처 목적/크롭/블러 지시를 명시함
- [ ] 슬라이드 전환 동작
- [ ] 키보드/터치 네비게이션 동작
- [ ] 전체화면 모드 동작
- [ ] 모바일 반응형 확인
- [ ] 폰트 로딩 확인
- [ ] Telegram/iPhone 검토용 PDF와 UTF-8 TXT fallback을 함께 생성함

## Don't Do This

- 한 슬라이드에 텍스트 과다 (5포인트 초과)
- 모든 슬라이드를 같은 레이아웃으로 (다양성 필요)
- 하드코딩된 스타일
- 한글 제목 20자 초과
- 애니메이션 없이 정적 HTML만 출력
- 사용자 확인 없이 내용 임의 변경
