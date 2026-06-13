---
name: visual-asset-generator
description: |
  나노바나나 3.0 Pro (Gemini API)를 사용해 상세페이지용 비주얼 에셋을 생성합니다.
  히어로 배너, 섹션 배너, 제품 이미지, 아이콘을 자동 생성하고 base64로 변환하여
  HTML에 바로 삽입 가능한 코드를 제공합니다.
allowed-tools: []
---

# Visual Asset Generator

나노바나나 3.0 Pro (Gemini API)를 활용한 상세페이지 비주얼 에셋 자동 생성

## 개요

```
[brief.md + design-tokens]
        │
        ▼
┌─────────────────────────┐
│   Prompt Generator      │
│   (템플릿 기반 프롬프트)  │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│   Gemini API            │
│   (이미지 생성)          │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│   Image Processor       │
│   (리사이징 + base64)    │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│   Code Generator        │
│   (HTML/CSS 코드 출력)   │
└─────────────────────────┘
```

## 생성 가능한 에셋

### 1. 히어로 배너 (Hero Banner)
- 용도: 상세페이지 최상단 메인 비주얼
- 크기: 860x500px (쿠팡/스마트스토어), 1010x600px (마켓컬리), 1200x600px (카페24)
- 스타일: 제품 중심, 브랜드 컬러 배경, 감성적 분위기

### 2. 섹션 배너 (Section Banner)
- 용도: 각 섹션 구분 비주얼
- 크기: 플랫폼별 전체 너비 x 300px
- 스타일: 추상적 그라데이션, 텍스처, 패턴

### 3. 제품 이미지 (Product Shot)
- 용도: 제품 상세 컷
- 크기: 800x800px (정사각형)
- 스타일: 클린 배경, 제품 포커스

### 4. 특징 아이콘 (Feature Icon)
- 용도: 혜택/특징 강조
- 크기: 120x120px
- 스타일: 플랫/3D 아이콘

## 워크플로우

### Phase 1: 프롬프트 생성

```bash
# brief.md와 design-tokens에서 정보 추출
python scripts/generate_prompts.py \
    --brief outputs/brief.md \
    --tokens outputs/design-tokens/tokens.css \
    --output outputs/visuals/prompts.json
```

**프롬프트 템플릿 활용**:
- `templates/hero-banner.md` - 히어로 배너용
- `templates/section-banner.md` - 섹션 배너용
- `templates/product-shot.md` - 제품 이미지용
- `templates/feature-icon.md` - 아이콘용

### Phase 2: 이미지 생성

```bash
# Gemini API로 이미지 생성
python scripts/generate_image.py \
    --prompt "프롬프트 내용" \
    --size 860x500 \
    --output outputs/visuals/hero-banner.png
```

**API 설정**:
```python
# .env 파일
GEMINI_API_KEY=your_api_key_here
```

### Phase 3: 이미지 처리 및 코드 변환

```bash
# 이미지를 base64로 변환하여 HTML 코드 생성
python scripts/image_to_code.py \
    --input outputs/visuals/hero-banner.png \
    --format html \
    --output outputs/visuals/hero-banner-code.html
```

**출력 형식**:
- `html` - `<img src="data:image/png;base64,...">` 태그
- `css` - `background-image: url(data:image/png;base64,...);`
- `json` - `{"base64": "...", "width": 860, "height": 500}`

## 프롬프트 작성 규칙

### 기본 구조

```
[스타일] + [주제] + [배경] + [조명] + [분위기] + [기술적 요구사항]
```

### 카테고리별 가이드

**식품**:
- 따뜻한 톤 (Warm, Cozy)
- 자연광, 주방/식탁 배경
- 신선함, 맛있어 보이는 연출

**뷰티**:
- 깨끗하고 고급스러운 톤
- 대리석, 꽃, 물방울 소품
- 광택, 투명감 강조

**가전**:
- 모던하고 기술적인 톤
- 화이트/그레이 배경
- 제품 기능 강조

**패션**:
- 스타일리시하고 트렌디한 톤
- 스튜디오/라이프스타일 배경
- 착용감, 핏 강조

## 출력 구조

```
outputs/visuals/
├── prompts.json              # 생성된 프롬프트 목록
├── hero-banner.png           # 히어로 배너 원본
├── hero-banner-code.html     # HTML 코드
├── section-benefits.png      # 섹션 배너
├── section-benefits-code.html
├── product-main.png          # 제품 메인 이미지
├── product-main-code.html
├── icons/
│   ├── icon-delivery.png
│   ├── icon-quality.png
│   └── icons-code.html       # 아이콘 통합 코드
└── manifest.json             # 생성된 에셋 목록
```

## 스크립트

| 스크립트 | 용도 |
|----------|------|
| `scripts/generate_prompts.py` | brief에서 프롬프트 자동 생성 |
| `scripts/generate_image.py` | Gemini API 이미지 생성 |
| `scripts/image_to_code.py` | 이미지→base64 HTML 변환 |
| `scripts/batch_generate.py` | 전체 에셋 일괄 생성 |

## 참조 문서

| 문서 | 용도 |
|------|------|
| | 효과적인 프롬프트 작성법 |
| | 카테고리별 스타일 프리셋 |
| | 플랫폼별 이미지 크기 |

## 템플릿

| 템플릿 | 용도 |
|--------|------|
| `templates/hero-banner.md` | 히어로 배너 프롬프트 |
| `templates/section-banner.md` | 섹션 배너 프롬프트 |
| `templates/product-shot.md` | 제품 이미지 프롬프트 |
| `templates/feature-icon.md` | 특징 아이콘 프롬프트 |

## 의존성

```bash
# Python 패키지
pip install google-generativeai Pillow python-dotenv

# 환경 변수
export GEMINI_API_KEY="your_api_key"
```

## 사용 예시

### 단일 이미지 생성

```python
from scripts.generate_image import generate_image

image_path = generate_image(
    prompt="A premium Korean beef bone soup in a traditional earthenware bowl, steam rising, warm kitchen background, soft natural lighting, appetizing food photography style",
    size=(860, 500),
    output_path="outputs/visuals/hero-banner.png"
)
```

### 이미지를 HTML 코드로 변환

```python
from scripts.image_to_code import image_to_html

html_code = image_to_html(
    image_path="outputs/visuals/hero-banner.png",
    alt_text="프리미엄 한우 곰탕",
    css_class="hero-banner"
)
# 결과: <img class="hero-banner" alt="프리미엄 한우 곰탕" src="data:image/png;base64,iVBORw0KGgo...">
```

### 전체 에셋 일괄 생성

```bash
python scripts/batch_generate.py \
    --brief outputs/brief.md \
    --tokens outputs/design-tokens/ \
    --platform coupang \
    --output outputs/visuals/
```

## CRITICAL 규칙

### 프롬프트 품질

```
❌ "맛있는 음식 사진" (모호함)
✅ "A steaming bowl of Korean bone soup, earthenware pot, wooden table, warm natural lighting, overhead shot, food photography" (구체적)
```

### 이미지 크기 준수

```
❌ 임의의 크기로 생성
✅ 플랫폼별 정확한 크기 사용:
   - 쿠팡/스마트스토어: 860px
   - 마켓컬리: 1010px
   - 카페24: 1200px
```

### base64 최적화

```
❌ 원본 고해상도 이미지 그대로 base64 변환
✅ 웹 최적화 (품질 85%, 적절한 리사이징) 후 변환
```

## 품질 체크리스트

### 프롬프트 생성
- [ ] brief.md에서 제품 특성 반영됨
- [ ] design-tokens에서 브랜드 컬러 반영됨
- [ ] 카테고리별 스타일 가이드 준수

### 이미지 생성
- [ ] 플랫폼별 정확한 크기
- [ ] 브랜드 분위기와 일치
- [ ] 제품이 명확하게 보임

### 코드 변환
- [ ] base64 인코딩 정상
- [ ] alt 텍스트 포함
- [ ] 파일 크기 최적화 (< 500KB)
