# 상세페이지 제작팀 자동화 시스템

레퍼런스 URL을 입력하면 멀티 플랫폼(쿠팡, 스마트스토어, 마켓컬리, 카페24) 상세페이지가 자동 생성되는 AI 에이전트 시스템

## 🎯 개요

```
[레퍼런스 URL + 상품 정보]
         │
         ▼
┌────────────────────────────────────────────────────┐
│  1. planner (기획 에이전트)                         │
│     - 스크린샷 캡처 (Playwright)                   │
│     - 7가지 필수 질문 수집                         │
│     - ecommerce-detail-page-planner 스킬 호출     │
│     - brief.md 작성                               │
└────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────┐
│  2. 병렬 실행                                       │
│                                                    │
│  [디자인 분석]        [플랫폼별 작성]      [비주얼 생성] │
│  design-system-      coupang-writer     Gemini API │
│  extractor           smartstore-writer   이미지 생성 │
│                      kurly-writer       base64 변환 │
│                      cafe24-writer                 │
└────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────┐
│  3. html-assembler (조립 에이전트)                  │
│     - 콘텐츠 + 토큰 + 이미지 조합                   │
│     - 플랫폼별 HTML 생성                           │
└────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────┐
│  4. reviewer (검수 에이전트)                        │
│     - 전환율 최적화 체크                           │
│     - 플랫폼 가이드라인 준수                        │
│     - 100점 만점 품질 평가                         │
└────────────────────────────────────────────────────┘
         │
         ▼
[outputs/ 폴더에 최종 결과물]
```

## 📁 프로젝트 구조

```
detail-page-team/
├── .claude/
│   ├── agents/
│   │   ├── planner.md              # 기획 에이전트
│   │   ├── coupang-writer.md       # 쿠팡 콘텐츠 작성
│   │   ├── smartstore-writer.md    # 스마트스토어 콘텐츠 작성
│   │   ├── kurly-writer.md         # 마켓컬리 콘텐츠 작성
│   │   ├── cafe24-writer.md        # 카페24 콘텐츠 작성
│   │   ├── html-assembler.md       # HTML 조립
│   │   └── reviewer.md             # 품질 검수
│   │
│   └── skills/
│       ├── design-system-extractor/    # 디자인 토큰 추출
│       │   ├── SKILL.md
│       │   ├── references/
│       │   └── scripts/
│       │
│       ├── visual-asset-generator/     # AI 이미지 생성
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   │   ├── generate_image.py   # Gemini API
│       │   │   ├── image_to_code.py    # base64 변환
│       │   │   └── batch_generate.py   # 일괄 생성
│       │   └── templates/
│       │
│       └── detail-page-html-generator/ # HTML 생성
│           ├── SKILL.md
│           ├── scripts/
│           └── templates/
│
├── outputs/                        # 생성 결과물
│   ├── brief.md
│   ├── design-tokens/
│   ├── visuals/
│   ├── coupang/
│   ├── smartstore/
│   ├── kurly/
│   ├── cafe24/
│   └── review-report.md
│
└── README.md
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# Python 의존성 설치
pip install google-generativeai Pillow python-dotenv markdown

# Gemini API 키 설정
export GEMINI_API_KEY="your_api_key_here"
```

### 2. 실행

Claude Code에서:

```
"이 레퍼런스 URL을 참고해서 한우 곰탕 상세페이지 만들어줘"
+ 레퍼런스 URL 첨부
```

또는 구체적으로:

```
상세페이지 제작 시작
- 레퍼런스: https://example.com/reference-page
- 카테고리: 식품
- 가격대: 프리미엄 (3만원대)
- 플랫폼: 쿠팡, 마켓컬리
```

## 🎨 에이전트 상세

### planner (기획 에이전트)

**역할**: 프로젝트 총괄 기획

**7가지 필수 질문**:
1. 상품 카테고리 (식품/뷰티/가전/패션)
2. 가격대 (저가/중가/프리미엄)
3. 판매 상황 (신규/기존)
4. 타겟 고객
5. 판매 플랫폼
6. 핵심 차별점 3가지
7. 브랜드 스토리

**출력**: `outputs/brief.md`

### 플랫폼별 Writer

| 플랫폼 | 심리 트리거 | 콘텐츠 비중 | 강조점 |
|--------|------------|------------|--------|
| 쿠팡 | FOMO (긴급성) | 정보 70% | 로켓배송, 할인 |
| 스마트스토어 | 신뢰 | 균형 50/50 | 리뷰, 적립 |
| 마켓컬리 | Aspiration | 스토리 60% | 프리미엄, 원재료 |
| 카페24 | Loyalty | 스토리 70% | 브랜드 철학 |

**출력**: `outputs/{platform}/content.md`

### html-assembler (조립 에이전트)

**입력**:
- 플랫폼별 `content.md`
- `design-tokens/` (컬러, 타이포, 간격)
- `visuals/` (base64 이미지)

**출력**:
- `outputs/{platform}/index.html` (플랫폼 에디터용)
- `outputs/{platform}/preview.html` (미리보기용)

### reviewer (검수 에이전트)

**검수 항목** (100점 만점):
- 전환율 최적화 (CRO): 30점
- 플랫폼 가이드라인: 25점
- 콘텐츠 품질: 25점
- 디자인 일관성: 10점
- 기술 품질: 10점

**출력**: `outputs/review-report.md`

## 🖼️ 비주얼 에셋 생성

### Gemini API (나노바나나 3.0 Pro)

```python
from scripts.generate_image import GeminiImageGenerator

generator = GeminiImageGenerator()

# 히어로 배너 생성
generator.generate_for_platform(
    prompt="Premium Korean beef bone soup, steaming...",
    platform="coupang",
    asset_type="hero",
    output_path="outputs/visuals/hero-banner.png"
)
```

### base64 HTML 변환

```python
from scripts.image_to_code import ImageToCodeConverter

converter = ImageToCodeConverter()

# 이미지 → HTML 코드
html = converter.to_html_img(
    "outputs/visuals/hero-banner.png",
    alt="프리미엄 한우 곰탕",
    css_class="hero-banner"
)
# 결과: <img src="data:image/png;base64,..." ...>
```

### 일괄 생성

```bash
python .claude/skills/visual-asset-generator/scripts/batch_generate.py \
    --brief outputs/brief.md \
    --platform coupang \
    --output outputs/visuals/
```

## 📐 디자인 시스템

### 추출되는 토큰

```json
// colors.json
{
  "primary": { "main": "#E85A4F", "light": "#FF8A80", "dark": "#B71C1C" },
  "secondary": { "main": "#8E8D8A" },
  "neutral": { "50": "#FAFAFA", "900": "#212121" },
  "background": { "default": "#FFFFFF", "paper": "#F5F5F5" }
}

// typography.json
{
  "fontFamily": { "primary": "Pretendard", "secondary": "Noto Sans KR" },
  "fontSize": { "h1": "32px", "body1": "16px", "caption": "12px" }
}

// spacing.json
{
  "base": 8,
  "scale": { "xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32 }
}
```

## 📄 출력물 예시

### brief.md

```markdown
# 프리미엄 한우 곰탕 상세페이지 기획

## 프로젝트 개요
- 제품: 프리미엄 한우 곰탕
- 카테고리: 식품 > 국/탕/찌개
- 가격대: 프리미엄 (32,000원)

## 타겟 고객
- 30-50대 주부
- 건강한 집밥을 원하는 맞벌이 가정
- 부모님 선물용

## 핵심 차별점
1. 국내산 한우 사골 100%
2. 48시간 저온 추출
3. 무첨가 (MSG, 화학조미료 0%)
...
```

### index.html (플랫폼용)

```html
<div class="coupang-detail-page" style="width: 860px; margin: 0 auto;">
  <!-- 히어로 섹션 -->
  <img src="data:image/png;base64,iVBORw0KGgo..." alt="프리미엄 한우 곰탕" style="width: 100%;">
  
  <!-- 혜택 섹션 -->
  <section style="padding: 32px 24px;">
    <h2 style="font-size: 24px;">왜 이 곰탕인가요?</h2>
    ...
  </section>
  ...
</div>
```

## ⚠️ 신규 상품 처리

**❌ 절대 금지**:
- 허위 리뷰/판매량/통계
- 가상의 고객 후기
- 검증되지 않은 수치

**✅ 대안 전략**:
- 브랜드 스토리 강화
- 인증/품질 보증 강조
- 출시 기념 혜택
- 빠른 배송 약속
- 교환/반품 정책

## 🔧 커스터마이징

### 새 플랫폼 추가

1. `.claude/agents/`에 새 writer 추가
2. `PLATFORM_SPECS`에 스펙 추가
3. 템플릿 작성

### 새 에셋 타입 추가

1. `visual-asset-generator/templates/`에 프롬프트 템플릿 추가
2. `DEFAULT_ASSETS`에 에셋 정의 추가

## 📚 참조 문서

- [Claude Code Sub-agents 가이드](https://code.claude.com/docs/ko/sub-agents)
- [Claude Code Skills 가이드](https://code.claude.com/docs/ko/skills)
- [ecommerce-detail-page-planner 스킬](/mnt/skills/user/ecommerce-detail-page-planner/)

## 📜 라이선스

내부 사용 목적
