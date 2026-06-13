---
name: typography-system
description: "한글 최적화 타이포그래피 시스템. Pretendard/Noto Sans KR 웹폰트 로딩, 한/영 혼합 줄바꿈 제어, 타이포 스케일, font-display 최적화, 슬라이드 가독성 극대화."
---

# Typography System

한글 강력 지원 HTML 슬라이드 전용 타이포그래피 시스템

## Core Purpose

**한글이 아름답게 보이는 프레젠테이션 타이포그래피**

한글은 영문과 다른 특성을 가진다:
- 글자 폭이 균일 (고정폭에 가까움)
- 자간(letter-spacing)이 좁으면 답답, 넓으면 산만
- 줄간격(line-height)이 영문보다 넓어야 가독성 확보
- 단어 단위가 아닌 음절 단위 줄바꿈 가능

---

## Font Stack

### 한글 웹폰트 우선순위

| 순위 | 폰트 | 특징 | 용도 |
|-----|------|------|------|
| 1 | Pretendard | 가변폰트, Apple SF 호환, 깔끔 | 범용 (제목+본문) |
| 2 | Noto Sans KR | Google, 넓은 웨이트 지원 | 범용 대안 |
| 3 | Spoqa Han Sans Neo | 부드러운, 가독성 좋음 | 본문 특화 |
| 4 | SUIT | Pretendard 계열, 경량 | 경량 대안 |

### 영문 보조 폰트

| 폰트 | 특징 | 용도 |
|------|------|------|
| Inter | Geometric, 숫자 가독성 | 데이터 슬라이드 |
| Plus Jakarta Sans | 모던, 깔끔 | 제목 강조 |
| DM Sans | Geometric, 심플 | 미니멀 테마 |
| Space Grotesk | 테크, 모던 | 테크 테마 |
| Playfair Display | Serif, 우아 | 프리미엄 테마 |

### 디스플레이 한글 폰트 (특수용)

| 폰트 | 특징 | 용도 |
|------|------|------|
| Black Han Sans | 매우 굵음, 임팩트 | 히어로 제목 |
| Do Hyeon | 복고풍, 개성 | 특수 테마 |
| Gmarket Sans | 상업적, 깔끔 | 비즈니스 |

---

## Font Loading Strategy

### CRITICAL: font-display: swap + preload

```html
<!-- index.html <head> -->

<!-- Pretendard 가변폰트 (Primary) -->
<link rel="preload"
      href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
      as="style" />
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />

<!-- Noto Sans KR (Fallback) -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" />
```

### CSS Font Stack 선언

```css
/* theme/typography.css */

:root {
  /* Font Family Tokens */
  --font-display: 'Pretendard Variable', 'Pretendard',
                  -apple-system, BlinkMacSystemFont,
                  system-ui, 'Noto Sans KR', sans-serif;

  --font-heading: var(--font-display);

  --font-body: 'Pretendard Variable', 'Pretendard',
               -apple-system, BlinkMacSystemFont,
               system-ui, 'Noto Sans KR', sans-serif;

  --font-mono: 'JetBrains Mono', 'Fira Code',
               'SF Mono', 'Consolas', monospace;

  /* Design Cloner Override Point */
  /* 클로닝 시 원본 폰트로 대체 */
  --font-display-override: ;
  --font-body-override: ;
}
```

---

## Type Scale

### 슬라이드 전용 스케일 (16:9 화면 최적화)

PPT 슬라이드는 일반 웹보다 큰 타이포가 필요하다.
프로젝터/대형 화면 기준으로 최소 가독 크기가 다름.

```css
:root {
  /* ===== Type Scale ===== */

  /* Display -- 히어로, 커버 슬라이드 */
  --text-display-xl: clamp(3rem, 5vw, 5rem);         /* 48-80px */
  --text-display-lg: clamp(2.5rem, 4vw, 4rem);       /* 40-64px */
  --text-display-md: clamp(2rem, 3.5vw, 3rem);       /* 32-48px */

  /* Heading -- 섹션 제목 */
  --text-heading-lg: clamp(1.75rem, 2.5vw, 2.5rem);  /* 28-40px */
  --text-heading-md: clamp(1.5rem, 2vw, 2rem);       /* 24-32px */
  --text-heading-sm: clamp(1.25rem, 1.5vw, 1.5rem);  /* 20-24px */

  /* Body -- 본문 */
  --text-body-lg: clamp(1.125rem, 1.25vw, 1.25rem);  /* 18-20px */
  --text-body-md: clamp(1rem, 1.1vw, 1.125rem);      /* 16-18px */
  --text-body-sm: clamp(0.875rem, 1vw, 1rem);        /* 14-16px */

  /* Caption/Label */
  --text-caption: clamp(0.75rem, 0.9vw, 0.875rem);   /* 12-14px */
  --text-label: clamp(0.8125rem, 0.95vw, 0.9375rem); /* 13-15px */
  --text-overline: clamp(0.6875rem, 0.8vw, 0.75rem); /* 11-12px */
}
```

### Weight Scale

```css
:root {
  --weight-light: 300;
  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-extrabold: 800;
  --weight-black: 900;
}
```

### Line Height (한글 최적화)

```css
:root {
  /* 한글은 영문보다 줄간격이 넓어야 가독성 확보 */
  --leading-none: 1;
  --leading-tight: 1.15;      /* 대형 Display 제목 */
  --leading-snug: 1.3;        /* Heading */
  --leading-normal: 1.6;      /* 한글 본문 (영문 1.5보다 넓게) */
  --leading-relaxed: 1.75;    /* 긴 본문 */
  --leading-loose: 2;         /* 매우 여유로운 */
}
```

### Letter Spacing (한글 최적화)

```css
:root {
  /* 한글 자간 -- 영문보다 좁은 범위 사용 */
  --tracking-tighter: -0.04em;  /* 대형 제목만 */
  --tracking-tight: -0.02em;    /* 제목 */
  --tracking-normal: -0.01em;   /* 한글 기본 (0보다 약간 좁게) */
  --tracking-wide: 0.02em;      /* 영문 대문자, 라벨 */
  --tracking-wider: 0.04em;     /* 오버라인 */
}
```

---

## Text Style Presets

### Semantic Utility Classes

```css
/* 슬라이드 제목 유형별 프리셋 */

.text-display-xl {
  font-family: var(--font-display);
  font-size: var(--text-display-xl);
  font-weight: var(--weight-extrabold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tighter);
  color: var(--color-text-heading);
  word-break: keep-all;          /* 한글 단어 단위 줄바꿈 */
  overflow-wrap: break-word;
}

.text-display-lg {
  font-family: var(--font-display);
  font-size: var(--text-display-lg);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--color-text-heading);
  word-break: keep-all;
}

.text-display-md {
  font-family: var(--font-display);
  font-size: var(--text-display-md);
  font-weight: var(--weight-bold);
  line-height: var(--leading-snug);
  letter-spacing: var(--tracking-tight);
  color: var(--color-text-heading);
  word-break: keep-all;
}

.text-heading-lg {
  font-family: var(--font-heading);
  font-size: var(--text-heading-lg);
  font-weight: var(--weight-bold);
  line-height: var(--leading-snug);
  letter-spacing: var(--tracking-tight);
  color: var(--color-text-heading);
  word-break: keep-all;
}

.text-heading-md {
  font-family: var(--font-heading);
  font-size: var(--text-heading-md);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
  color: var(--color-text-heading);
  word-break: keep-all;
}

.text-heading-sm {
  font-family: var(--font-heading);
  font-size: var(--text-heading-sm);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
  color: var(--color-text-heading);
}

.text-body-lg {
  font-family: var(--font-body);
  font-size: var(--text-body-lg);
  font-weight: var(--weight-regular);
  line-height: var(--leading-normal);
  color: var(--color-text-body);
  word-break: keep-all;
}

.text-body {
  font-family: var(--font-body);
  font-size: var(--text-body-md);
  font-weight: var(--weight-regular);
  line-height: var(--leading-normal);
  color: var(--color-text-body);
  word-break: keep-all;
}

.text-body-sm {
  font-family: var(--font-body);
  font-size: var(--text-body-sm);
  font-weight: var(--weight-regular);
  line-height: var(--leading-normal);
  color: var(--color-text-muted);
}

.text-caption {
  font-family: var(--font-body);
  font-size: var(--text-caption);
  font-weight: var(--weight-medium);
  line-height: var(--leading-snug);
  color: var(--color-text-muted);
}

.text-label {
  font-family: var(--font-body);
  font-size: var(--text-label);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
  letter-spacing: var(--tracking-wide);
  color: var(--color-text-body);
  text-transform: none;  /* 한글에 uppercase 적용하지 않음 */
}

.text-overline {
  font-family: var(--font-body);
  font-size: var(--text-overline);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-snug);
  letter-spacing: var(--tracking-wider);
  color: var(--color-text-accent);
  text-transform: uppercase; /* 영문 오버라인만 */
}
```

---

## Korean-Specific Rules

### CRITICAL: word-break & overflow

```css
/* 한글 줄바꿈 규칙 */
.ko-text {
  word-break: keep-all;        /* 단어 단위 줄바꿈 (어절 유지) */
  overflow-wrap: break-word;    /* 길 경우 강제 줄바꿈 */
  word-spacing: 0.02em;        /* 한글 단어 간격 미세 조정 */
}

/* 제목: 절대 중간에 끊기지 않게 */
.ko-heading {
  word-break: keep-all;
  overflow-wrap: break-word;
  /* 줄바꿈 위치 제어 -- <wbr> 태그로 수동 지정 가능 */
}

/* 숫자+단위 조합 줄바꿈 방지 */
.ko-metric {
  white-space: nowrap;         /* "123,456건" 이 잘리지 않게 */
}
```

### 한/영 혼합 간격 보정

```css
/* 한글 사이에 영어/숫자가 올 때 미세 간격 */
.text-mixed {
  font-feature-settings: 'calt' 1;  /* 커닝 활성화 */
  text-rendering: optimizeLegibility;
}
```

### 강조 표현 (한글)

```css
/* 한글에서 italic은 부적절 -- 대신 색상/굵기로 강조 */
.text-emphasis {
  color: var(--color-text-accent);
  font-weight: var(--weight-bold);
  /* font-style: italic 사용 금지 (한글) */
}

/* 밑줄 강조 (형광펜 효과) */
.text-highlight {
  background: linear-gradient(
    transparent 60%,
    var(--color-primary-light) 60%
  );
  padding: 0 0.1em;
}

/* 마커 강조 (블록) */
.text-marker {
  background-color: var(--color-primary);
  color: var(--color-primary-contrast);
  padding: 0.1em 0.3em;
  border-radius: var(--radius-sm);
}
```

---

## Responsive Typography

### 슬라이드 뷰포트에 따른 조정

```css
/* 16:9 프레젠테이션 모드 (전체화면) */
@media (min-aspect-ratio: 16/9) and (min-width: 1280px) {
  :root {
    --text-display-xl: 5rem;
    --text-body-md: 1.125rem;
  }
}

/* 일반 브라우저 뷰 */
@media (max-width: 768px) {
  :root {
    --text-display-xl: 2.5rem;
    --text-display-lg: 2rem;
    --text-heading-lg: 1.5rem;
    --text-body-md: 1rem;
    --slide-padding-x: var(--space-6);
  }
}
```

---

## Font Pairing Rules

### 한글+영문 조합 가이드

```
Pretendard + Inter
  -> 가장 안전한 조합. 모던, 깔끔.

Pretendard + Space Grotesk
  -> 테크/스타트업 느낌. 숫자 가독성 좋음.

Noto Sans KR + Plus Jakarta Sans
  -> 부드럽고 모던. SaaS/서비스 적합.

Pretendard + Playfair Display
  -> 한글 산세리프 + 영문 세리프. 고급스러운 대비.
```

### Design Cloner 연동

```
원본 PPT에서 폰트 식별 -> 웹폰트 매핑
  "맑은 고딕" -> Pretendard (상위 호환)
  "나눔고딕" -> Noto Sans KR (유사)
  "함초롬바탕" -> Noto Serif KR (세리프 유지)
  "Arial" -> Inter
  "Calibri" -> Inter
  "Times New Roman" -> Playfair Display
```

---

## Quality Checklist

- [ ] 한글 폰트 로딩 확인 (FOUT 없음)
- [ ] word-break: keep-all 적용 확인
- [ ] 한/영 혼합 텍스트 간격 자연스러움
- [ ] 제목 타이포 계층 명확
- [ ] 본문 가독성 (줄간격, 자간)
- [ ] 숫자+단위 줄바꿈 방지
- [ ] 강조 표현 한글 적합성 (italic 미사용)
- [ ] clamp() 반응형 동작 확인

## Don't Do This

- 한글 텍스트에 font-style: italic 적용
- word-break: break-all 사용 (한글 음절 파괴)
- letter-spacing 0.1em 이상 (한글에서 산만)
- text-transform: uppercase를 한글에 적용
- 본문에 line-height 1.5 미만 사용 (한글 가독성 저하)
- 제목에 12px 미만 폰트 사용 (슬라이드 가독성)
