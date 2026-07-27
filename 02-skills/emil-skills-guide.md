# Emil Kowalski Skills — 공식 사용 가이드 (필독)

> 이 문서는 emilkowalski/skills 4종(emil-design-eng, review-animations, animation-vocabulary, apple-design)을 사용하기 전에 **반드시 먼저 읽어야 하는** 가이드다.
> 출처: 레포 README(원문 대조), 저자 블로그 "Agents with Taste" (emilkowal.ski/ui/agents-with-taste, WebFetch 요약 — 2차 보고), 각 SKILL.md 원문.

## 저자의 핵심 철학

- **"Agents don't have great taste."** — 에이전트는 동작하는 코드는 만들지만 "느낌이 맞는" 선택을 못 한다. 대표 실수: enter 애니메이션에 `ease-in` 사용(정답은 `ease-out`), 반투명 shadow 대신 solid border 사용. 이런 작은 어긋남이 누적되어 인터페이스 품질을 가른다.
- **"If you know what great feels like, describe the rules, then give them to your agents so they can follow them."** — 스킬은 규칙의 집합이다. 규칙은 **엄격하게(strict)** 따라야 하며, 일반적인 기본값(generic defaults)으로 임의 대체하지 않는다.
- 스킬은 전문성(domain expertise)의 부산물이다. 스킬이 전문성을 대체하는 게 아니라 증폭한다.

## 4개 스킬의 역할 분담 (섞어 쓰지 말 것)

| 스킬 | 역할 | 호출 시점 |
|---|---|---|
| **emil-design-eng** | 메인 스킬. UI 폴리시, 컴포넌트 설계, 애니메이션 결정, 디테일 철학 | UI/애니메이션을 **만들거나 다듬을 때** 기본 호출 |
| **review-animations** | 애니메이션 코드 **검수 전용**. 기본 태도 = 지적(flagging), 승인은 획득하는 것 | 이미 작성된 모션 코드를 리뷰할 때. `disable-model-invocation: true`이므로 **사용자가 명시 요청할 때만** |
| **animation-vocabulary** | 모호한 묘사 → 정확한 용어 역조회 사전 | "그 통통 튀는 거" 같은 묘사를 정확한 용어로 바꿔 프롬프트 품질을 올릴 때. **이름 찾기 전용** — 설계·구현 금지 |
| **apple-design** | Apple WWDC 디자인 원칙(유체적 모션, 스프링, 제스처)의 웹 번역판 | 제스처 기반 UI, 스프링 애니메이션, 시트/드래그/스와이프, 관성·중단 가능 전환, reduced-motion 작업 시 |

## 저자가 정한 사용 규칙 (반드시 준수)

1. **규칙 우선**: 각 SKILL.md의 easing 결정 플로차트, duration 표(요소 유형별 100–300ms 범위), 스프링 설정값을 **그대로** 적용한다. 내 기억 속 일반 관행으로 덮어쓰지 않는다.
2. **review-animations 사용 시**: 정밀 수치·근거가 필요한 지적마다 같은 폴더의 **STANDARDS.md를 반드시 로드**한다(스킬 본문이 명시). 모션 외 코드 리뷰 요청은 거절하고 일반 리뷰로 넘긴다.
3. **emil-design-eng 최초 호출 시**: 구체적 질문 없이 호출되면 스킬이 지정한 준비 멘트만 출력하고 대기한다(스킬 본문 "Initial Response" 규정).
4. **동작 ≠ 통과**: "작동하지만 느낌이 어긋난" 모션(둔한 속도, 잘못된 origin, 과도한 발화, 프레임 드랍)은 회귀(regression)로 취급한다.
5. **워크플로 예시(저자 시연)**: "improve a dialog animation using my animation skill" → 스킬 규칙 기반의 명확한 이슈 목록을 먼저 받고, 그 목록대로 수정한다. 즉 **진단 목록 → 수정** 순서.
6. **용어 먼저**: 원하는 모션을 말로 설명하기 어려우면 animation-vocabulary로 정확한 용어를 먼저 확정한 뒤, 그 용어로 emil-design-eng/apple-design에 작업을 지시한다.
7. **검증**: 모션 변경 후에는 실제 렌더러에서 눈으로 확인한다(전역 verification-grounding 규칙과 동일). 빌드 통과는 증거가 아니다.

## 심화 자료 (저자 공식)

- 코스: animations.dev
- 글: emilkowal.ski/ui/7-practical-animation-tips (easing 선택 근거), emilkowal.ski/ui/agents-with-taste (스킬 사용 철학)
- 업데이트: `npx skills@latest add emilkowalski/skills` (재설치 시 이 가이드 삽입 라인이 SKILL.md에서 지워질 수 있음 — `~/.claude/rules/emil-skills.md` 참조해 복구)
