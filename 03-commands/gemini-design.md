---
name: gemini-design
description: Gemini로 디자인 리뷰, 컨설팅, 감사, 비교, 시스템 설계
---

# Gemini 디자인

Gemini 3.1 Pro를 활용하여 디자인 관련 작업을 수행한다.

## 실행 절차

1. `gemini_auth_status`로 인증 상태를 확인한다. 미인증 시 `/gemini-login`을 먼저 실행하라고 안내한다.

2. 사용자의 요청과 입력(이미지 유무)을 분석하여 적절한 도구를 선택한다:

### 이미지 분석 (`gemini_analyze_image`)
스크린샷, 목업, 와이어프레임 이미지를 분석할 때 사용한다.
- `image_paths`: 분석할 이미지 파일 경로 배열 (필수)
- `analysis_focus`: 분석 초점 (layout, color, typography, ux_issues, all)
- `context`: 프로젝트 배경 정보 (선택)

### 디자인 비교 (`gemini_compare_designs`)
두 디자인(Before/After, A/B)을 비교할 때 사용한다.
- `image_paths_a`: 첫 번째 디자인 이미지 (필수)
- `image_paths_b`: 두 번째 디자인 이미지 (필수)
- `comparison_focus`: 비교 초점 (visual, usability, consistency, all)

### 토큰 추출 (`gemini_extract_tokens`)
디자인 이미지에서 디자인 토큰(색상, 폰트, 간격)을 추출할 때 사용한다.
- `image_paths`: 분석할 이미지 파일 경로 (필수)
- `token_types`: 추출할 토큰 유형 (colors, typography, spacing, all)

### 디자인 리뷰 (`gemini_design_review`)
디자인 품질을 10점 척도로 평가할 때 사용한다.
- `design_description`: 디자인 설명 또는 HTML/CSS 코드
- `review_focus`: 리뷰 초점 (visual_design, usability, accessibility, consistency, responsive, all)
- `image_paths`: 리뷰할 디자인 이미지 (선택)
- `context`: 프로젝트 배경 정보 (선택)

### 접근성 감사 (`gemini_a11y_audit`)
WCAG 2.2 기준으로 접근성을 검사할 때 사용한다.
- `target`: 검사 대상 (HTML 코드 또는 디자인 설명)
- `image_paths`: 검사 대상 이미지 (선택)
- `wcag_level`: 검사 수준 (A, AA, AAA)

### 반응형 감사 (`gemini_responsive_audit`)
반응형 디자인 품질을 검증할 때 사용한다.
- `target`: 검사 대상 (HTML/CSS 코드)
- `image_paths`: 각 브레이크포인트 스크린샷 (선택)
- `breakpoints`: 커스텀 브레이크포인트 (선택)

### 디자인 컨설팅 (`gemini_design_consult`)
UX 전략, IA, 유저 플로우, 접근성 가이드를 요청할 때 사용한다.
- `question`: 컨설팅 질문
- `domain`: 영역 (ux_strategy, information_architecture, user_flow, accessibility, design_principles, all)
- `context`: 프로젝트 배경 정보 (선택)

### 디자인 시스템 (`gemini_design_system`)
디자인 토큰, 컴포넌트 API, 테마 구조를 설계할 때 사용한다.
- `requirements`: 디자인 시스템 요구사항
- `scope`: 범위 (tokens, components, theme, full_system)
- `existing_system`: 기존 시스템 정보 (선택)

### 테마 생성 (`gemini_generate_theme`)
브랜드 기반 테마와 색상 팔레트를 생성할 때 사용한다.
- `brand_description`: 브랜드 설명 (분위기, 타겟 등)
- `base_color`: 기준 색상 (선택)
- `style`: 스타일 (modern, playful, corporate, minimal, bold)

### 반복 수정 (`gemini_iterate`)
이전 대화 맥락을 유지하며 디자인을 반복 수정할 때 사용한다.
- `message`: 수정 요청 내용
- `session_id`: 이전 대화 세션 ID (후속 요청 시 필수)
- `image_paths`: 참고 이미지 (선택)

3. 결과를 구조화된 마크다운으로 정리하여 사용자에게 제공한다.
4. 토큰/테마 결과가 포함된 경우 JSON 파일로도 저장한다.
