---
name: gemini-code
description: Gemini로 프론트엔드 코드 생성 (텍스트/이미지 → 코드)
---

# Gemini 코드 생성

Gemini 3.1 Pro를 활용하여 프론트엔드 코드를 생성한다.

## 실행 절차

1. `gemini_auth_status`로 인증 상태를 확인한다. 미인증 시 `/gemini-login`을 먼저 실행하라고 안내한다.

2. 사용자의 입력 유형에 따라 도구를 선택한다:

### 이미지 → 코드 (`gemini_image_to_code`)
디자인 이미지(스크린샷, 목업, 와이어프레임)를 코드로 변환할 때 사용한다.
- `image_paths`: 변환할 디자인 이미지 경로 (필수)
- `tech_stack`: 기술 스택 (react, nextjs, vue, html_css, tailwind)
- `requirements`: 추가 요구사항 (선택)

### 텍스트 → 코드 (`gemini_generate_frontend`)
텍스트 설명을 기반으로 프론트엔드 코드를 생성할 때 사용한다.
- `description`: 구현할 UI/컴포넌트 설명
- `tech_stack`: 기술 스택 (react, nextjs, vue, html_css, tailwind)
- `requirements`: 추가 요구사항 (선택)

3. 생성된 코드를 적절한 파일로 저장한다:
   - React/Next.js: `.tsx` 파일
   - Vue: `.vue` 파일
   - HTML/CSS: `.html` 파일
   - Tailwind: `.tsx` 또는 `.html` 파일

4. 코드에 대한 간단한 설명과 함께 사용자에게 제공한다.

## 활용 시나리오

- 디자인 시안 스크린샷을 React 컴포넌트로 변환
- Figma 캡처를 Next.js 페이지로 변환
- 텍스트 설명 기반 반응형 레이아웃 구현
- 인터랙션 및 애니메이션 코드 생성
- shadcn/ui 기반 컴포넌트 구현
- Tailwind CSS 유틸리티 클래스 적용
