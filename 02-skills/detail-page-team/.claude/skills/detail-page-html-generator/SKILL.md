---
name: detail-page-html-generator
description: |
  플랫폼별 상세페이지 HTML을 자동 생성합니다.
  마크다운 콘텐츠 + 디자인 토큰 + base64 이미지를 조합하여
  쿠팡, 스마트스토어, 마켓컬리, 카페24용 완성 HTML을 출력합니다.
allowed-tools: []
---

# Detail Page HTML Generator

콘텐츠 + 디자인 + 이미지를 조합한 상세페이지 HTML 자동 생성

## 개요

```
[콘텐츠]              [디자인]              [이미지]
content.md    +    design-tokens/    +    visuals/
     │                  │                    │
     └──────────────────┼────────────────────┘
                        ▼
              ┌─────────────────┐
              │  HTML Assembler │
              │  (템플릿 조합)   │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │  Platform HTML  │
              │  (최종 출력)     │
              └─────────────────┘
```

## 워크플로우

### Phase 1: 입력 수집

```bash
# 필요한 입력 파일
outputs/
├── {platform}/
│   ├── content.md        # 플랫폼별 콘텐츠
│   └── sections.json     # 섹션 구조
├── design-tokens/
│   ├── colors.json       # 컬러 토큰
│   ├── typography.json   # 타이포 토큰
│   └── tokens.css        # CSS 변수
└── visuals/
    ├── hero-banner-code.html    # base64 이미지
    ├── section-*-code.html
    └── manifest.json
```

### Phase 2: HTML 조립

```bash
python scripts/assemble_html.py \
    --content outputs/coupang/content.md \
    --tokens outputs/design-tokens/ \
    --visuals outputs/visuals/ \
    --template templates/coupang.html \
    --output outputs/coupang/index.html
```

### Phase 3: 검증 및 미리보기

```bash
# 로컬 미리보기 서버
python -m http.server 8000 --directory outputs/coupang/
```

## 플랫폼별 HTML 스펙

### 쿠팡 (Coupang)

```html
<!-- 너비: 860px 고정 -->
<div class="coupang-detail" style="width: 860px; margin: 0 auto;">
  <!-- 모든 이미지 860px -->
  <!-- 인라인 스타일 필수 (외부 CSS 불가) -->
  <!-- JavaScript 불가 -->
</div>
```

**제약사항**:
- 이미지 너비: 정확히 860px
- 외부 CSS/JS: 불가
- 폰트: 시스템 폰트만 (웹폰트 불가)
- 인라인 스타일: 필수

### 스마트스토어 (Naver Smartstore)

```html
<!-- 너비: 860px 고정 -->
<div class="smartstore-detail" style="width: 860px; margin: 0 auto;">
  <!-- 네이버 쇼핑 최적화 -->
  <!-- 인라인 스타일 권장 -->
</div>
```

**제약사항**:
- 이미지 너비: 860px
- 일부 CSS 속성 제한
- 웹폰트: 제한적

### 마켓컬리 (Market Kurly)

```html
<!-- 너비: 1010px 고정 -->
<div class="kurly-detail" style="width: 1010px; margin: 0 auto;">
  <!-- 프리미엄 감성 디자인 -->
  <!-- 여백 넉넉하게 -->
</div>
```

**제약사항**:
- 이미지 너비: 1010px
- 프리미엄 톤 유지
- 브랜드 가이드라인 준수

### 카페24 (Cafe24)

```html
<!-- 너비: 최대 1200px, 반응형 -->
<div class="cafe24-detail" style="max-width: 1200px; margin: 0 auto;">
  <!-- 반응형 가능 -->
  <!-- 외부 CSS/JS 가능 (자사몰) -->
</div>

<style>
@media (max-width: 768px) {
  .cafe24-detail { padding: 0 16px; }
  .cafe24-detail img { width: 100%; height: auto; }
}
</style>
```

**특징**:
- 반응형 지원
- 자유로운 스타일링
- 브랜드 커스터마이징 가능

## 섹션 템플릿

### 히어로 섹션

```html
<section class="hero-section" style="width: {platform_width}px;">
  {hero_banner_image}
  <div class="hero-content">
    <h1 style="font-size: 32px; font-weight: 700;">{headline}</h1>
    <p style="font-size: 18px; color: #666;">{subheadline}</p>
  </div>
</section>
```

### 혜택 카드 그리드

```html
<section class="benefits-section">
  {section_banner_image}
  <div class="benefits-grid" style="display: flex; flex-wrap: wrap; gap: 16px;">
    {{#each benefits}}
    <div class="benefit-card" style="flex: 1; min-width: 200px; padding: 24px; background: #f9f9f9; border-radius: 8px;">
      {icon_image}
      <h3 style="font-size: 18px; margin: 16px 0 8px;">{{title}}</h3>
      <p style="font-size: 14px; color: #666;">{{description}}</p>
    </div>
    {{/each}}
  </div>
</section>
```

### 비교 테이블

```html
<section class="comparison-section">
  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background: {primary_color}; color: white;">
        <th style="padding: 16px;">비교 항목</th>
        <th>우리 제품</th>
        <th>일반 제품</th>
      </tr>
    </thead>
    <tbody>
      {{#each comparisons}}
      <tr style="border-bottom: 1px solid #eee;">
        <td style="padding: 16px;">{{item}}</td>
        <td style="color: {primary_color}; font-weight: 700;">{{ours}}</td>
        <td style="color: #999;">{{theirs}}</td>
      </tr>
      {{/each}}
    </tbody>
  </table>
</section>
```

### CTA 섹션

```html
<section class="cta-section" style="text-align: center; padding: 48px 24px; background: {primary_color};">
  <h2 style="font-size: 28px; color: white; margin-bottom: 16px;">{cta_headline}</h2>
  <p style="font-size: 16px; color: rgba(255,255,255,0.9); margin-bottom: 24px;">{cta_description}</p>
  <!-- 버튼은 플랫폼 기본 제공 사용 -->
</section>
```

## 스크립트

| 스크립트 | 용도 |
|----------|------|
| `scripts/assemble_html.py` | 콘텐츠+토큰+이미지 조합 |
| `scripts/validate_html.py` | 플랫폼 규격 검증 |
| `scripts/preview_server.py` | 로컬 미리보기 |

## 템플릿

| 템플릿 | 용도 |
|--------|------|
| `templates/coupang.html` | 쿠팡 상세페이지 기본 구조 |
| `templates/smartstore.html` | 스마트스토어 기본 구조 |
| `templates/kurly.html` | 마켓컬리 기본 구조 |
| `templates/cafe24.html` | 카페24 기본 구조 (반응형) |

## 출력 형식

### 완성 HTML

```
outputs/{platform}/
├── index.html          # 최종 상세페이지 HTML
├── preview.html        # 미리보기용 (래퍼 포함)
└── assets.json         # 사용된 에셋 목록
```

### index.html 구조

```html
<!-- 플랫폼 에디터에 복사/붙여넣기 가능한 형태 -->
<div class="{platform}-detail-page" style="width: {width}px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Malgun Gothic', sans-serif;">

  <!-- 1. 히어로 섹션 -->
  <img src="data:image/png;base64,..." alt="..." style="width: 100%;">
  
  <!-- 2. 콘텐츠 섹션들 -->
  ...
  
  <!-- 9. CTA 섹션 -->
  ...
  
</div>
```

## CRITICAL 규칙

### 이미지 임베딩

```
❌ <img src="https://외부URL/image.png">  (외부 호스팅)
✅ <img src="data:image/png;base64,...">  (base64 인라인)
```

### 스타일 적용

```
❌ <link rel="stylesheet" href="style.css">  (외부 CSS)
❌ class="my-style"  (클래스 참조)
✅ style="..."  (인라인 스타일)
```

### 플랫폼 너비

```
❌ width: 100%  (가변)
✅ width: 860px  (쿠팡/스마트스토어 고정)
✅ width: 1010px  (마켓컬리 고정)
✅ max-width: 1200px  (카페24 반응형)
```

## 품질 체크리스트

### 구조 검증
- [ ] 플랫폼별 정확한 너비
- [ ] 모든 이미지 base64 인라인
- [ ] 모든 스타일 인라인
- [ ] 9단계 구조 완성

### 콘텐츠 검증
- [ ] 마크다운→HTML 변환 완료
- [ ] 디자인 토큰 적용
- [ ] 이미지 alt 텍스트 포함

### 기술 검증
- [ ] HTML 문법 오류 없음
- [ ] 이미지 로딩 정상
- [ ] 예상 렌더링 결과 확인
