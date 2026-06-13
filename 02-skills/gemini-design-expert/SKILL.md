---
name: gemini-design-expert
description: >
  This skill should be used when the user asks to "review a design with Gemini",
  "generate frontend code with Gemini", "get design consultation from Gemini",
  "build a design system with Gemini", "analyze a screenshot with Gemini",
  "convert a design image to code", "audit accessibility", "check responsive design",
  or needs Gemini 3.1 Pro's expertise for UI/UX design, web/app design,
  or frontend development tasks.
  Trigger phrases include: "Gemini로 디자인 리뷰해줘", "Gemini한테 코드 짜달라고 해",
  "디자인 시스템 만들어줘 Gemini로", "프론트엔드 코드 Gemini로 생성",
  "스크린샷 분석해줘", "이미지를 코드로 변환해줘", "접근성 검사해줘",
  "반응형 검사해줘", "디자인 반복 수정해줘", "테마 생성해줘".
version: 0.2.0
---

# Gemini Design Expert

Gemini 3.1 Pro를 활용한 UI/UX 디자인 및 프론트엔드 개발 전문 에이전트.
이미지 분석(비전), 구조화된 JSON 출력, 멀티턴 대화를 지원한다.

## 사용 가능한 MCP 도구 (14개)

### 인증 (2)
| 도구 | 용도 |
|------|------|
| `gemini_login` | Google OAuth 로그인 |
| `gemini_auth_status` | 인증 상태 확인 |

### 비전 · 이미지 분석 (4)
| 도구 | 용도 |
|------|------|
| `gemini_analyze_image` | 스크린샷/목업 시각 분석 (레이아웃, 색상, 타이포, UX 이슈) |
| `gemini_image_to_code` | 디자인 이미지 → React/HTML/Vue 코드 변환 |
| `gemini_compare_designs` | 두 디자인 비교 분석 (Before/After, A/B) |
| `gemini_extract_tokens` | 디자인 이미지에서 토큰 추출 (색상, 폰트, 간격 → JSON) |

### 디자인 리뷰 · 컨설팅 (2)
| 도구 | 용도 |
|------|------|
| `gemini_design_review` | 디자인 리뷰 10점 척도 평가 (이미지 첨부 가능) |
| `gemini_design_consult` | UX 전략, IA, 유저플로우, 접근성 자문 |

### 코드 생성 (1)
| 도구 | 용도 |
|------|------|
| `gemini_generate_frontend` | 프론트엔드 코드 생성 (React/Next.js/Vue/HTML) |

### 디자인 시스템 (1)
| 도구 | 용도 |
|------|------|
| `gemini_design_system` | 디자인 토큰, 컴포넌트 API, 테마 구조 설계 |

### 전문 감사 (2)
| 도구 | 용도 |
|------|------|
| `gemini_a11y_audit` | WCAG 2.2 접근성 감사 (위반 목록 + 수정 코드) |
| `gemini_responsive_audit` | 반응형 감사 (브레이크포인트별 레이아웃 검증) |

### 반복 · 테마 (2)
| 도구 | 용도 |
|------|------|
| `gemini_iterate` | 멀티턴 디자인 반복 수정 (대화 히스토리 유지) |
| `gemini_generate_theme` | 브랜드 기반 테마/색상 팔레트 생성 (JSON) |

## 워크플로우

### 1. 인증 확인
모든 Gemini 도구 사용 전 `gemini_auth_status`로 인증 상태를 확인한다.
인증되지 않은 경우 `gemini_login`으로 Google OAuth 로그인을 안내한다.

### 2. 도구 선택 기준

**이미지가 있는 경우 → 비전 도구 우선:**
- 스크린샷/목업 피드백 → `gemini_analyze_image`
- 이미지를 코드로 → `gemini_image_to_code`
- 두 버전 비교 → `gemini_compare_designs`
- 토큰 추출 → `gemini_extract_tokens`
- 이미지 + 점수 평가 → `gemini_design_review` (image_paths 파라미터 사용)

**텍스트만 있는 경우:**
- 디자인 점수 평가 → `gemini_design_review`
- 코드 생성 → `gemini_generate_frontend`
- UX/IA 자문 → `gemini_design_consult`
- 시스템 설계 → `gemini_design_system`

**특수 워크플로우:**
- WCAG 검사 → `gemini_a11y_audit`
- 반응형 검사 → `gemini_responsive_audit`
- 반복 수정 (멀티턴) → `gemini_iterate` (session_id로 대화 유지)
- 테마/팔레트 생성 → `gemini_generate_theme`

### 3. 멀티턴 반복 수정

`gemini_iterate` 도구는 session_id를 통해 이전 대화 맥락을 유지한다:
1. 첫 요청: session_id 없이 호출 → 응답에서 session_id 반환
2. 후속 수정: 반환된 session_id와 수정 요청 전달
3. 최대 20턴까지 대화 유지

### 4. 결과 활용
- 코드 결과 → `.tsx`, `.vue`, `.html` 파일로 저장
- 리뷰/감사 결과 → 구조화된 마크다운으로 정리
- 토큰/테마 → JSON 파일로 저장
- 비교 분석 → 마크다운 테이블로 정리

## 참고 자료
