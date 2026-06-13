---
name: motion-system
description: "HTML 슬라이드 전용 애니메이션/전환 시스템. 슬라이드 전환, 요소 진입/퇴장, 순차 등장, 숫자 카운터, 타이핑 효과 등. CSS Animations + Web Animations API. GPU 가속 원칙 준수."
---

# Motion System

HTML 슬라이드 전용 애니메이션 및 인터랙션 시스템

## Core Purpose

**정적 PPT에 생명을 불어넣되, 목적 있는 움직임만**

```
원칙 1: 목적 있는 움직임 -- 장식이 아닌 의미 전달
원칙 2: 일관된 이징 -- 브랜드 성격에 맞는 곡선
원칙 3: 계층적 타이밍 -- 중요도 순 시차 진입
원칙 4: 성능 우선 -- transform/opacity만 애니메이트
```

---

## Easing System

### 브랜드 톤별 이징 프리셋

```css
/* theme/motion.css */

:root {
  /* ===== Easing Curves ===== */

  /* Standard -- 범용 */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* Expressive -- 프리미엄/고급 */
  --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);

  /* Bouncy -- 활기/에너지 */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Sharp -- 비즈니스/전문적 */
  --ease-sharp: cubic-bezier(0.25, 0.1, 0.25, 1);

  /* Gentle -- 미니멀/차분 */
  --ease-gentle: cubic-bezier(0.4, 0, 0, 1);

  /* Spring -- 탄성 */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* ===== Duration ===== */
  --duration-instant: 100ms;
  --duration-fast: 200ms;
  --duration-normal: 400ms;
  --duration-slow: 600ms;
  --duration-dramatic: 800ms;
  --duration-slide-transition: 700ms;

  /* ===== Stagger Delay ===== */
  --stagger-fast: 50ms;
  --stagger-normal: 80ms;
  --stagger-slow: 120ms;

  /* ===== Active Easing (Design Cloner가 설정) ===== */
  --ease-brand: var(--ease-smooth);
  --duration-brand: var(--duration-normal);
}
```

---

## Slide Transitions

### 슬라이드 간 전환 효과

```css
/* ===== Slide Transition Keyframes ===== */

/* Fade */
@keyframes slide-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes slide-fade-out {
  from { opacity: 1; }
  to   { opacity: 0; }
}

/* Slide Left */
@keyframes slide-left-in {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
@keyframes slide-left-out {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(-100%); opacity: 0; }
}

/* Slide Up */
@keyframes slide-up-in {
  from { transform: translateY(100%); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}

/* Scale */
@keyframes slide-scale-in {
  from { transform: scale(0.9); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}

/* Zoom */
@keyframes slide-zoom-in {
  from { transform: scale(1.1); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}

/* Blur */
@keyframes slide-blur-in {
  from { filter: blur(20px); opacity: 0; }
  to   { filter: blur(0); opacity: 1; }
}

/* 슬라이드 전환 적용 */
.slide[data-transition="fade"]  { animation: slide-fade-in var(--duration-slide-transition) var(--ease-brand); }
.slide[data-transition="slide"] { animation: slide-left-in var(--duration-slide-transition) var(--ease-brand); }
.slide[data-transition="scale"] { animation: slide-scale-in var(--duration-slide-transition) var(--ease-brand); }
.slide[data-transition="zoom"]  { animation: slide-zoom-in var(--duration-slide-transition) var(--ease-brand); }
.slide[data-transition="blur"]  { animation: slide-blur-in var(--duration-slide-transition) var(--ease-brand); }
```

---

## Element Animations

### 요소 진입 효과

```css
/* ===== Element Entry Keyframes ===== */

/* Fade Up */
@keyframes fade-up {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Fade Down */
@keyframes fade-down {
  from { opacity: 0; transform: translateY(-40px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Slide In Left */
@keyframes slide-in-left {
  from { opacity: 0; transform: translateX(-60px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Slide In Right */
@keyframes slide-in-right {
  from { opacity: 0; transform: translateX(60px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Scale Up */
@keyframes scale-up {
  from { opacity: 0; transform: scale(0.8); }
  to   { opacity: 1; transform: scale(1); }
}

/* Scale Down (줌 아웃) */
@keyframes scale-down {
  from { opacity: 0; transform: scale(1.15); }
  to   { opacity: 1; transform: scale(1); }
}

/* Blur In */
@keyframes blur-in {
  from { opacity: 0; filter: blur(12px); }
  to   { opacity: 1; filter: blur(0); }
}

/* Rotate In */
@keyframes rotate-in {
  from { opacity: 0; transform: rotate(-5deg) scale(0.95); }
  to   { opacity: 1; transform: rotate(0) scale(1); }
}

/* Clip Reveal (좌->우 드러남) */
@keyframes clip-reveal-right {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0 0 0); }
}

/* Clip Reveal (아래->위) */
@keyframes clip-reveal-up {
  from { clip-path: inset(100% 0 0 0); }
  to   { clip-path: inset(0 0 0 0); }
}

/* Draw Line */
@keyframes draw-line {
  from { stroke-dashoffset: var(--line-length, 1000); }
  to   { stroke-dashoffset: 0; }
}

/* Counter (숫자 카운트업 -- CSS만으로는 한계, JS 보조) */
@keyframes pulse-number {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Typewriter cursor */
@keyframes blink-cursor {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
```

### Animation Utility Classes

```css
/* ===== Animation Utilities ===== */

/* 기본 (모든 애니메이션 요소에 적용) */
[data-animate] {
  opacity: 0;
  will-change: transform, opacity;
}

[data-animate].is-visible {
  animation-fill-mode: forwards;
  animation-timing-function: var(--ease-brand);
  animation-duration: var(--duration-brand);
}

/* 애니메이션 타입 */
[data-animate="fade-up"].is-visible    { animation-name: fade-up; }
[data-animate="fade-down"].is-visible  { animation-name: fade-down; }
[data-animate="slide-left"].is-visible { animation-name: slide-in-left; }
[data-animate="slide-right"].is-visible { animation-name: slide-in-right; }
[data-animate="scale-up"].is-visible   { animation-name: scale-up; }
[data-animate="scale-down"].is-visible { animation-name: scale-down; }
[data-animate="blur-in"].is-visible    { animation-name: blur-in; }
[data-animate="rotate-in"].is-visible  { animation-name: rotate-in; }
[data-animate="clip-right"].is-visible { animation-name: clip-reveal-right; }
[data-animate="clip-up"].is-visible    { animation-name: clip-reveal-up; }

/* 딜레이 (stagger용) */
[data-delay="1"] { animation-delay: calc(var(--stagger-normal) * 1); }
[data-delay="2"] { animation-delay: calc(var(--stagger-normal) * 2); }
[data-delay="3"] { animation-delay: calc(var(--stagger-normal) * 3); }
[data-delay="4"] { animation-delay: calc(var(--stagger-normal) * 4); }
[data-delay="5"] { animation-delay: calc(var(--stagger-normal) * 5); }
[data-delay="6"] { animation-delay: calc(var(--stagger-normal) * 6); }
[data-delay="7"] { animation-delay: calc(var(--stagger-normal) * 7); }
[data-delay="8"] { animation-delay: calc(var(--stagger-normal) * 8); }

/* 속도 변형 */
[data-speed="fast"]     { animation-duration: var(--duration-fast); }
[data-speed="slow"]     { animation-duration: var(--duration-slow); }
[data-speed="dramatic"] { animation-duration: var(--duration-dramatic); }
```

---

## Slide Controller (JavaScript)

### 슬라이드 네비게이션 + 애니메이션 트리거

```javascript
// scripts/slide-controller.js

class SlideController {
  constructor(deckSelector = '.slide-deck') {
    this.deck = document.querySelector(deckSelector);
    this.slides = [...this.deck.querySelectorAll('.slide')];
    this.currentIndex = 0;
    this.isTransitioning = false;

    this.init();
  }

  init() {
    // 모든 슬라이드 숨기기 (첫 번째 제외)
    this.slides.forEach((slide, i) => {
      if (i !== 0) slide.style.display = 'none';
    });

    // 첫 슬라이드 애니메이션 트리거
    this.triggerAnimations(this.slides[0]);

    // 키보드 이벤트
    document.addEventListener('keydown', (e) => this.handleKey(e));

    // 터치 스와이프
    this.setupTouch();

    // 슬라이드 인디케이터
    this.updateIndicator();
  }

  handleKey(e) {
    if (this.isTransitioning) return;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case ' ':
        e.preventDefault();
        this.next();
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        this.prev();
        break;
      case 'f':
      case 'F':
        this.toggleFullscreen();
        break;
      case 'Escape':
        this.exitFullscreen();
        break;
    }
  }

  async next() {
    if (this.currentIndex >= this.slides.length - 1) return;
    await this.goTo(this.currentIndex + 1);
  }

  async prev() {
    if (this.currentIndex <= 0) return;
    await this.goTo(this.currentIndex - 1);
  }

  async goTo(index) {
    if (this.isTransitioning || index === this.currentIndex) return;
    this.isTransitioning = true;

    const current = this.slides[this.currentIndex];
    const target = this.slides[index];
    const transition = target.dataset.transition || 'fade';

    // 현재 슬라이드 퇴장
    current.style.display = 'none';
    this.resetAnimations(current);

    // 다음 슬라이드 진입
    target.style.display = '';
    target.setAttribute('data-transition', transition);

    // 진입 애니메이션 완료 대기
    await this.waitForAnimation(target);

    // 요소 애니메이션 트리거
    this.triggerAnimations(target);

    this.currentIndex = index;
    this.updateIndicator();
    this.isTransitioning = false;
  }

  triggerAnimations(slide) {
    const elements = slide.querySelectorAll('[data-animate]');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, { threshold: 0.1 });

    // 약간의 딜레이 후 트리거 (슬라이드 전환 후)
    setTimeout(() => {
      elements.forEach((el) => {
        el.classList.add('is-visible');
      });

      // 특수 효과 트리거
      initCounters(slide);
      initTypewriters(slide);
    }, 100);
  }

  resetAnimations(slide) {
    const elements = slide.querySelectorAll('[data-animate]');
    elements.forEach((el) => {
      el.classList.remove('is-visible');
    });
  }

  waitForAnimation(el) {
    return new Promise((resolve) => {
      const handler = () => {
        el.removeEventListener('animationend', handler);
        resolve();
      };
      el.addEventListener('animationend', handler);

      // Fallback timeout
      setTimeout(resolve, 1000);
    });
  }

  setupTouch() {
    let startX = 0;
    this.deck.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    }, { passive: true });

    this.deck.addEventListener('touchend', (e) => {
      const diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) {
        diff > 0 ? this.next() : this.prev();
      }
    }, { passive: true });
  }

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      this.deck.requestFullscreen();
      this.deck.classList.add('presentation-mode');
    } else {
      this.exitFullscreen();
    }
  }

  exitFullscreen() {
    if (document.fullscreenElement) {
      document.exitFullscreen();
      this.deck.classList.remove('presentation-mode');
    }
  }

  updateIndicator() {
    const indicator = document.querySelector('.slide-indicator');
    if (indicator) {
      indicator.textContent =
        `${this.currentIndex + 1} / ${this.slides.length}`;
    }
  }
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.slideController = new SlideController();
});
```

---

## Special Effects (JavaScript)

### CountUp (숫자 카운트업)

```javascript
// scripts/animations.js

function countUp(element, target, duration = 2000) {
  const start = 0;
  const startTime = performance.now();
  const suffix = element.dataset.suffix || '';
  const prefix = element.dataset.prefix || '';
  const decimals = parseInt(element.dataset.decimals || '0');

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // easeOutExpo
    const eased = progress === 1
      ? 1
      : 1 - Math.pow(2, -10 * progress);
    const current = start + (target - start) * eased;

    element.textContent = prefix + current.toFixed(decimals)
      .replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// data-count-to 속성이 있는 요소 자동 감지
function initCounters(slide) {
  const counters = slide.querySelectorAll('[data-count-to]');
  counters.forEach((el) => {
    const target = parseFloat(el.dataset.countTo);
    const duration = parseInt(el.dataset.countDuration || '2000');
    countUp(el, target, duration);
  });
}
```

### Typewriter (타이핑 효과)

```javascript
function typewriter(element, speed = 50) {
  const text = element.textContent;
  element.textContent = '';
  element.style.visibility = 'visible';

  let i = 0;
  function type() {
    if (i < text.length) {
      element.textContent += text[i];
      i++;
      setTimeout(type, speed);
    }
  }
  type();
}

// data-typewriter 속성 요소 자동 감지
function initTypewriters(slide) {
  const elements = slide.querySelectorAll('[data-typewriter]');
  elements.forEach((el) => {
    const speed = parseInt(el.dataset.typewriterSpeed || '50');
    typewriter(el, speed);
  });
}
```

### Progress Bar Fill

```javascript
function fillProgress(element) {
  const target = element.dataset.progress || '100';
  element.style.setProperty('--progress', '0%');

  requestAnimationFrame(() => {
    element.style.transition =
      `--progress var(--duration-dramatic) var(--ease-brand)`;
    element.style.setProperty('--progress', target + '%');
  });
}
```

---

## Hover Interactions

```css
/* ===== Hover Effects ===== */

/* 카드 리프트 */
.hover-lift {
  transition: transform var(--transition-hover),
              box-shadow var(--transition-hover);
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
}

/* 카드 틸트 (미세 기울기) */
.hover-tilt {
  transition: transform var(--transition-hover);
}
.hover-tilt:hover {
  transform: perspective(800px) rotateY(2deg) rotateX(-2deg);
}

/* 스케일업 */
.hover-scale {
  transition: transform var(--transition-hover);
}
.hover-scale:hover {
  transform: scale(1.05);
}

/* 이미지 줌 */
.hover-zoom {
  overflow: hidden;
}
.hover-zoom img {
  transition: transform var(--transition-slow);
}
.hover-zoom:hover img {
  transform: scale(1.1);
}

/* 버튼 glow */
.hover-glow {
  transition: box-shadow var(--transition-hover);
}
.hover-glow:hover {
  box-shadow: var(--shadow-glow);
}

/* 배경색 스위프 */
.hover-fill {
  position: relative;
  overflow: hidden;
  z-index: 0;
}
.hover-fill::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-primary);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-normal) var(--ease-smooth);
  z-index: -1;
}
.hover-fill:hover::before {
  transform: scaleX(1);
}
.hover-fill:hover {
  color: var(--color-primary-contrast);
}
```

---

## Accessibility: Reduced Motion

CRITICAL: 모션 감소 선호 사용자 대응

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  [data-animate] {
    opacity: 1 !important;
    transform: none !important;
    filter: none !important;
  }

  .slide[data-transition] {
    animation: none !important;
  }
}
```

---

## Usage in HTML

```html
<div class="slide" data-transition="fade">
  <div class="slide-content layout-content">

    <!-- 제목: 페이드업 -->
    <h2 class="text-heading-lg" data-animate="fade-up">
      핵심 성과 지표
    </h2>

    <!-- 숫자들: 순차 등장 + 카운트업 -->
    <div class="layout-metrics">
      <div class="metrics-grid">
        <div class="metric-item" data-animate="scale-up" data-delay="1">
          <span class="metric-value"
                data-count-to="1234"
                data-suffix="건">0</span>
          <span class="metric-label">처리 건수</span>
        </div>

        <div class="metric-item" data-animate="scale-up" data-delay="2">
          <span class="metric-value"
                data-count-to="99.7"
                data-suffix="%"
                data-decimals="1">0</span>
          <span class="metric-label">성공률</span>
        </div>

        <div class="metric-item" data-animate="scale-up" data-delay="3">
          <span class="metric-value"
                data-count-to="42"
                data-prefix="$"
                data-suffix="M">0</span>
          <span class="metric-label">매출</span>
        </div>
      </div>
    </div>

  </div>
</div>
```

---

## Quality Checklist

- [ ] 모든 애니메이션이 transform/opacity만 사용
- [ ] will-change 적절히 설정 (과다 사용 금지)
- [ ] prefers-reduced-motion 대응
- [ ] 슬라이드 전환 부드러움
- [ ] stagger 타이밍 자연스러움
- [ ] 60fps 유지 확인
- [ ] 터치 스와이프 동작
- [ ] 키보드 네비게이션 동작

## Don't Do This

- width/height/margin/padding을 애니메이트 (레이아웃 트리거)
- will-change를 모든 요소에 적용 (메모리 낭비)
- 500ms 이상의 의미 없는 딜레이
- 모든 요소에 무차별 bounce 효과
- prefers-reduced-motion 무시
- 중첩 애니메이션으로 성능 저하
- setInterval로 애니메이션 (requestAnimationFrame 사용)
