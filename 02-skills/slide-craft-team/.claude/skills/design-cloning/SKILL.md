---
name: design-cloning
description: "PPT/프레젠테이션 레퍼런스 이미지를 역설계하여 디자인 토큰을 추출하는 전문 스킬. 시각 분석(Visual First) -> 색상/타이포/레이아웃/효과 추출 -> CSS Custom Properties 토큰으로 변환. theme-system 토큰 구조를 반드시 따름."
---

# Design Cloning

PPT 레퍼런스 이미지 -> 디자인 토큰 역설계 전문 스킬

## Core Purpose

**눈으로 본 디자인을 정확한 토큰으로 변환**

```
PPT 이미지 입력
    |
    v
[Step 1] First Impression -- 5초 전체 인상
    |
    v
[Step 2] Color Extraction -- 색상 팔레트 역설계
    |
    v
[Step 3] Typography Analysis -- 폰트/스케일 파악
    |
    v
[Step 4] Layout Deconstruction -- 그리드/간격 측정
    |
    v
[Step 5] Effects & Decoration -- 그림자/radius/그라데이션
    |
    v
[Step 6] Token Generation -- CSS Custom Properties 출력
```

## Input

- PPT 슬라이드 이미지 1장 이상 (PNG/JPG)
- (선택) 브랜드 가이드라인, HEX 값
- (선택) 원본 PPT 파일명 (폰트 추정용)

## Analysis Protocol

### CRITICAL: Visual First, Code Verify

```
1순위: 이미지를 사람 눈으로 분석 (느낌, 인상, 분위기)
2순위: 색상/크기를 시각적으로 추정
3순위: 사용자 제공 정보로 검증/보정
```

---

### Step 1: First Impression (5초 분석)

이미지를 보고 즉각적인 인상을 기록한다.
이것이 전체 디자인 톤을 결정한다.

```markdown
## 첫인상 분석

### 분위기
- 전체 톤: [다크 프리미엄 / 밝고 깨끗 / 화려하고 역동 / 미니멀 / ...]
- 브랜드 느낌: [고급 / 친근 / 전문적 / 크리에이티브 / 테크 / ...]
- 색상 온도: [따뜻한(오렌지/옐로) / 차가운(블루/퍼플) / 중립(그레이)]

### 시각적 특징
- 주요 색상: [눈에 가장 먼저 들어오는 색]
- 배경 처리: [단색 / 그라데이션 / 이미지 / 패턴]
- 여백 수준: [넉넉 / 적당 / 촘촘]
- 장식 요소: [미니멀 / 중간 / 화려]

### 유사 레퍼런스
- "XX의 OO 느낌" (예: "Apple의 발표자료 느낌", "Notion의 깔끔함")
```

---

### Step 2: Color Extraction

#### 2.1 주요 색상 식별

이미지에서 다음 역할별 색상을 찾는다:

| 역할 | 어디서 찾나 | 토큰 매핑 |
|------|-----------|----------|
| Primary | CTA 버튼, 제목 강조, 로고 | --color-primary |
| Secondary | 보조 강조, 아이콘 배경 | --color-secondary |
| Accent | 포인트 장식, 배지 | --color-accent |
| Surface Base | 슬라이드 기본 배경 | --color-surface-base |
| Surface Elevated | 카드/박스 배경 | --color-surface-elevated |
| Text Heading | 제목 텍스트 | --color-text-heading |
| Text Body | 본문 텍스트 | --color-text-body |
| Text Muted | 보조 텍스트 | --color-text-muted |

#### 2.2 시각적 색상 추정 가이드

| 시각적 느낌 | 추정 HEX 범위 |
|-----------|--------------|
| 순백 배경 | #FFFFFF |
| 아이보리/크림 | #FAFAF5 ~ #F5F0E8 |
| 밝은 회색 배경 | #F5F5F5 ~ #F0F0F0 |
| 네이비/다크 배경 | #0F172A ~ #1E293B |
| 순검정 배경 | #000000 ~ #111111 |
| 선명한 파랑 | #2563EB ~ #3B82F6 |
| 선명한 빨강 | #DC2626 ~ #EF4444 |
| 선명한 오렌지 | #EA580C ~ #F97316 |
| 선명한 초록 | #16A34A ~ #22C55E |
| 선명한 보라 | #7C3AED ~ #8B5CF6 |
| 연한 파스텔 | 메인 색상 + opacity 20-30% |

#### 2.3 Light vs Dark 판별

```
배경이 밝다 (Lightness > 80%):
  -> Light Theme
  -> --color-surface-base: 밝은 색
  -> --color-text-heading: 어두운 색
  -> --color-text-body: 중간 어두운 색

배경이 어둡다 (Lightness < 30%):
  -> Dark Theme
  -> --color-surface-base: 어두운 색
  -> --color-text-heading: 밝은 색
  -> --color-text-body: 중간 밝은 색
```

#### 2.4 그라데이션 추출

```
그라데이션이 있다면:
  1. 시작 색상, 끝 색상 각각 추정
  2. 방향 추정 (대각선 135도가 가장 흔함)
  3. --gradient-primary: linear-gradient(방향, 시작 %, 끝 %)
  4. 시작 색상을 --color-primary로 설정
```

---

### Step 3: Typography Analysis

#### 3.1 폰트 식별

PPT에서 자주 쓰는 폰트 -> 웹폰트 매핑:

| PPT 폰트 | 웹폰트 대체 | 비고 |
|----------|-----------|------|
| 맑은 고딕 | Pretendard | 상위 호환 |
| 나눔고딕 | Noto Sans KR | 유사 |
| 나눔바른고딕 | Pretendard | 더 세련됨 |
| 함초롬바탕 | Noto Serif KR | 세리프 유지 |
| Calibri | Inter | 유사 |
| Arial | Inter | 유사 |
| Segoe UI | Inter | 유사 |
| Times New Roman | Playfair Display | 세리프 |
| Helvetica | Inter | 유사 |
| Poppins | Plus Jakarta Sans | 유사 |

시각적 식별 불가 시 기본값: **Pretendard** (한글) + **Inter** (영문)

#### 3.2 타이포 스케일 추정

슬라이드 내 텍스트 크기 계층을 측정:

```
이미지 높이 대비 텍스트 크기 비율로 추정:

대형 제목 (화면의 15-25%): -> display-xl (3-5rem)
중형 제목 (화면의 8-15%):  -> display-md ~ heading-lg (2-3rem)
소제목 (화면의 5-8%):      -> heading-md ~ heading-sm (1.5-2rem)
본문 (화면의 3-5%):        -> body-md (1-1.25rem)
캡션 (화면의 2-3%):        -> caption (0.75-0.875rem)
```

#### 3.3 텍스트 굵기 추정

```
매우 두꺼움 (글자가 꽉 차 보임): 800-900 (extrabold/black)
두꺼움 (강조 확실함): 700 (bold)
약간 두꺼움: 600 (semibold)
보통: 400-500 (regular/medium)
가벼움 (얇아 보임): 300 (light)
```

---

### Step 4: Layout Deconstruction

#### 4.1 그리드 추정

```
이미지를 12등분 격자로 나눠 요소 위치 측정:

[1][2][3][4][5][6][7][8][9][10][11][12]
|-- 좌측 콘텐츠 (col 1-5) --|-- 우측 이미지 (col 6-12) --|

-> layout-split-40-60
```

#### 4.2 여백 추정

```
슬라이드 가장자리 ~ 콘텐츠 시작 거리:

좁은 여백 (2-3%): -> --slide-padding-x: var(--space-6)   (24px)
보통 여백 (5-8%): -> --slide-padding-x: var(--space-12)  (48px)
넓은 여백 (10%+): -> --slide-padding-x: var(--space-16)  (64px)
매우 넓은 (15%+): -> --slide-padding-x: var(--space-24)  (96px)
```

#### 4.3 슬라이드 유형 판별

```
[Title]    제목이 화면 중앙에 크게     -> layout-title
[Content]  제목 + 본문 블록             -> layout-content
[Split]    좌우 2분할                   -> layout-split
[Cards]    3-4개 카드 그리드            -> layout-cards
[Metrics]  큰 숫자 나열                 -> layout-metrics
[Timeline] 순서/프로세스 표현           -> layout-timeline
[Image]    전체 이미지 + 오버레이 텍스트 -> layout-fullimage
```

---

### Step 5: Effects & Decoration

#### 5.1 모서리 둥글기

```
각진 (0px): -> --radius-card: var(--radius-none)
약간 둥근 (4-8px): -> --radius-card: var(--radius-md)
둥근 (12-16px): -> --radius-card: var(--radius-xl)
매우 둥근 (20px+): -> --radius-card: var(--radius-2xl)
완전 둥근: -> --radius-card: var(--radius-full)
```

#### 5.2 그림자

```
그림자 없음: -> --shadow-card: var(--shadow-none)
미세한 그림자: -> --shadow-card: var(--shadow-sm)
보통 그림자: -> --shadow-card: var(--shadow-md)
강한 그림자: -> --shadow-card: var(--shadow-xl)
```

#### 5.3 장식 요소

```
- 아이콘 스타일: [Line/Filled/Duo-tone] -> lucide 아이콘 매핑
- 구분선: [없음/얇은선/굵은선/그라데이션]
- 배경 장식: [없음/도형/패턴/노이즈]
- 강조 표시: [밑줄/마커/배경색/볼드]
```

#### 5.4 모션 톤 결정

```
PPT 분위기에 따른 모션 이징 선택:

고급/프리미엄 -> --ease-brand: var(--ease-smooth)
활기/에너지   -> --ease-brand: var(--ease-bounce)
비즈니스/전문 -> --ease-brand: var(--ease-sharp)
미니멀/차분   -> --ease-brand: var(--ease-gentle)
```

---

### Step 6: Token Generation

#### CRITICAL: theme-system 토큰 구조를 반드시 따른다

분석 결과를 theme-system의 CSS Custom Properties에 맞춰 출력:

```css
/* === 분석 결과: tokens.css === */

:root {
  /* Brand Colors */
  --color-primary: #3B82F6;
  --color-primary-light: #60A5FA;
  --color-primary-dark: #2563EB;
  --color-primary-contrast: #FFFFFF;
  --color-primary-rgb: 59, 130, 246;

  --color-secondary: #8B5CF6;
  --color-secondary-light: #A78BFA;
  --color-secondary-dark: #7C3AED;
  --color-secondary-contrast: #FFFFFF;

  --color-accent: #F59E0B;

  /* Surface */
  --color-surface-base: #FFFFFF;
  --color-surface-elevated: #F8FAFC;
  --color-surface-overlay: rgba(0, 0, 0, 0.5);
  --color-surface-inverse: #0F172A;

  /* Text */
  --color-text-heading: #0F172A;
  --color-text-body: #334155;
  --color-text-muted: #94A3B8;
  --color-text-inverse: #F8FAFC;
  --color-text-accent: #3B82F6;
  --color-text-link: #2563EB;

  /* Border */
  --color-border-default: #E2E8F0;
  --color-border-subtle: #F1F5F9;
  --color-border-strong: #CBD5E1;

  /* Gradient */
  --gradient-primary: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  --gradient-subtle: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
  --gradient-overlay: linear-gradient(to bottom, transparent 40%, rgba(0,0,0,0.7) 100%);
  --gradient-hero: linear-gradient(135deg, #0F172A 0%, #1E3A5F 100%);

  /* Typography */
  --font-display: 'Pretendard Variable', 'Pretendard', sans-serif;
  --font-heading: var(--font-display);
  --font-body: var(--font-display);

  /* Spacing overrides */
  --slide-padding-x: var(--space-16);
  --slide-padding-y: var(--space-12);

  /* Radius */
  --radius-card: var(--radius-xl);
  --radius-button: var(--radius-lg);
  --radius-image: var(--radius-lg);

  /* Shadow */
  --shadow-card: var(--shadow-md);

  /* Motion */
  --ease-brand: var(--ease-smooth);
  --duration-brand: var(--duration-normal);
}
```

---

## Multi-Slide Analysis

여러 슬라이드를 분석할 경우:

```
1. 모든 슬라이드에서 공통 요소 추출 (색상, 폰트, 여백)
2. 슬라이드별 고유 레이아웃 유형 판별
3. 공통 요소 -> 토큰
4. 고유 레이아웃 -> 슬라이드별 layout 클래스 매핑
5. 교차 검증: 색상이 2장 이상에서 동일하면 확신도 높음
```

---

## Output Format

분석 완료 시 다음 2개를 출력:

### 1. 분석 보고서 (마크다운)

사용자에게 보여주는 시각 분석 결과. 느낌 위주로 작성.

### 2. tokens.css

theme-system 구조에 맞는 CSS 변수 파일. 바로 적용 가능.

---

## Quality Checklist

- [ ] 색상 추출 완료 (primary, secondary, surface, text)
- [ ] 타이포 스케일 정의 완료
- [ ] 레이아웃 유형 판별 완료
- [ ] radius/shadow/gradient 정의 완료
- [ ] 모션 톤 선택 완료
- [ ] theme-system 토큰 구조 준수
- [ ] Light/Dark 테마 판별 정확
- [ ] 접근성: 텍스트/배경 대비 4.5:1 확인

## Don't Do This

- 코드 값 없이 "대략 파란색" 같은 모호한 결론
- theme-system 토큰 구조와 다른 변수명 생성
- 이미지 없이 추측으로 토큰 생성
- 사용자 확인 없이 대폭 다른 색상 적용
- 한 슬라이드만 보고 전체 테마 확정 (가능하면 2장 이상 교차 검증)
