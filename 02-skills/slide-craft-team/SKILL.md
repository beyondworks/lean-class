---
name: slide-craft-team
description: "PPT 레퍼런스 이미지 기반 디자인 클로닝 + 대화 기반 슬라이드 생성이 가능한 프로급 HTML 프레젠테이션 에이전트 팀. 디자인 시스템, 토큰 시스템, 한글 최적화 타이포, 애니메이션/인터랙션까지 현존 최고 수준의 슬라이드 제작."
---

# Slide Craft Team

프로급 HTML 프레젠테이션 제작 에이전트 팀 오케스트레이터

## Overview

```
"PPT 이미지 하나면 그 디자인 그대로, 대화 한마디면 새로운 디자인으로"
```

6명의 전문 에이전트가 협업하여 프로덕션급 HTML 슬라이드를 제작합니다.

### 강점

- 현존 최고 수준의 디자인 클로닝 (이미지 -> 토큰 -> HTML)
- 디자인 시스템 + CSS 토큰 기반 일관된 테마
- 한글 타이포그래피 최적화
- 슬라이드 전환/요소 애니메이션/인터랙션
- 16:9 캔버스 + 반응형 + 전체화면 프레젠테이션 모드

### 기능

| 기능 | 설명 |
|------|------|
| 디자인 클로닝 | PPT 캡처 이미지로 디자인 복제 |
| 대화 생성 | 에이전트와 대화하며 슬라이드 생성 |
| 한글 최적화 | 한글 폰트, 줄바꿈, 자간, 강조 표현 |
| 디자인 편집 | 폰트, 색상, 그리드, 여백, 도형, 이미지 |
| 애니메이션 | 슬라이드 전환, 요소 진입, 카운터, 타이핑 |
| 테마 시스템 | CSS 변수 기반, 토큰 하나로 전체 테마 변경 |

---

## Agent Team

```
                    ┌─────────────────────┐
                    │    Orchestrator     │
                    │   (이 SKILL.md)     │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         v                     v                     v
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │Design Cloner │   │   Slide      │   │  QA Reviewer │
  │(시각 역설계) │   │  Composer    │   │ (품질 검증)  │
  └──────┬───────┘   │(내용+조립)  │   └──────────────┘
         │           └──────┬───────┘
    ┌────┴────┐             │
    │         │             │
    v         v             v
┌────────┐ ┌────────┐ ┌────────────┐
│Typo    │ │Layout  │ │  Motion    │
│Expert  │ │Engineer│ │ Director   │
│(한글)  │ │(그리드)│ │(애니메이션)│
└────────┘ └────────┘ └────────────┘
```

| 에이전트 | 역할 | 스킬 참조 |
|---------|------|----------|
| **Design Cloner** | PPT 이미지 역설계 -> 토큰 추출 | design-cloning/ |
| **Slide Composer** | 대화 기반 슬라이드 내용 구성 + HTML 조립 | slide-generation/ |
| **Typography Expert** | 한글 폰트 선택, 타이포 스케일, 줄바꿈 | typography-system/ |
| **Layout Engineer** | 16:9 그리드, 레이아웃 템플릿, 도형/이미지 | layout-system/ |
| **Motion Director** | 전환 효과, 요소 애니메이션, 인터랙션 | motion-system/ |
| **QA Reviewer** | 원본 대비 시각 검증, 기능/접근성 테스트 | -- |

---

## Execution Routes

### Route 0: Notion 커리큘럼/강의 페이지 기반 자료화

사용자가 Notion 커리큘럼 URL을 주고 강의 슬라이드/교재/워크북 제작을 요청하면, 바로 슬라이드를 만들지 말고 먼저 전체 페이지를 재귀 추출해 강의 구조를 확인한다. 세부 절차는를 따른다.

필수:
- 페이지 제목/부제/과정 개요/회차별 커리큘럼/실습 과제/옵션 과정/가격·상품 정보를 모두 확인한다.
- Notion 테이블과 child block을 누락하지 않는다.
- 슬라이드화 전, 개념 레이어·실습 레이어·코칭 레이어로 구조를 분석한다.
- 과정 시간/가격/상품 구성 등 소스 내부 불일치는 정리 필요 지점으로 표시한다.
- 첫 응답에서는 production-critical 질문만 짧게 묻는다: 자료 용도, 상품 기준, 대상 수준, 메인 데모 도구, 디자인 톤, 최종 산출물 형식.

### Route A: 레퍼런스 이미지로 디자인 클로닝

```
사용자: [PPT 이미지 첨부] + "이 디자인으로 발표자료 만들어줘"
       (선택) [원고/리포트 첨부] 또는 텍스트 붙여넣기

Step 1: Design Cloner
  - 이미지 시각 분석
  - 분석 보고서 생성
  - tokens.css 생성
  -> 사용자에게 분석 결과 공유

Step 2: Typography Expert + Layout Engineer (병렬)
  - [Typo] 폰트 매핑, typography.css 생성
  - [Layout] 레이아웃 유형 판별, layout.css 생성

Step 3: Slide Composer
  - 원고/리포트가 있으면:
    -> 원고 자동 파싱 (핵심 메시지 추출, 슬라이드 분배)
    -> 구조안 제시 후 사용자 확인 (질문 최소화)
  - 원고가 없으면:
    -> 사용자와 대화하며 내용 구조화
  - 슬라이드 HTML 조립

Step 4: Motion Director
  - 브랜드 톤에 맞는 모션 설계
  - motion.css + animations.js 생성
  - data-animate 속성 배정

Step 5: QA Reviewer
  - 원본 이미지 vs HTML 시각 비교
  - 체크리스트 검증
  - 수정 피드백 -> 해당 에이전트 재작업

Step 6: 최종 출력
  - 프로젝트 폴더 완성
  - 사용 방법 안내
```

### Route B: 대화로 처음부터 생성

```
사용자: "투자자 피칭 15장 만들어줘"

Step 1: Slide Composer
  - 주제, 청중, 분량 확인 (최대 3질문)
  - 슬라이드 구조안 제시

Step 2: 테마 선택
  - 5개 프리셋 제안 (모던다크/클린라이트/웜프리미엄/...)
  - 또는 "추천해주세요"

Step 3: Typography Expert + Layout Engineer (병렬)
  - 선택된 테마 기반 CSS 생성

Step 4: Slide Composer
  - HTML 슬라이드 조립

Step 5: Motion Director
  - 모션 효과 배정

Step 6: 최종 출력
```

### Route C: 기존 슬라이드 수정

```
사용자: "3번 슬라이드 색상 바꿔줘" / "레이아웃 변경" / "애니메이션 추가"

-> 해당 전문 에이전트 직접 호출
  색상 -> Design Cloner (tokens.css 수정)
  폰트 -> Typography Expert
  레이아웃 -> Layout Engineer
  애니메이션 -> Motion Director
  내용 -> Slide Composer
```

---

## Course Slide Rules

For AI Native / course-deck work, load and apply before generating HTML/PDF slides.

Non-negotiables:
- Prioritize visibility/readability; avoid text-heavy generic lecture decks.
- Emphasize key points with semantic visual treatment, not only body text.
- Use graphs, graphic elements, flowcharts, system maps, status panels, and real-image placeholders to aid understanding.
- Preferred direction: compact, operational, high-signal — not oversized hero marketing.
- For Telegram/iPhone review, deliver `.pdf` and UTF-8 `.txt` alongside source `.md`; raw Markdown alone may render poorly on iPhone.

### Design Collaboration Preview

When the user asks to collaborate with a design persona or requests design screenshots before a full deck is built, follow:
- Treat the design persona as the art-direction lane, while this agent keeps curriculum/teaching structure ownership.
- Ask for or create a small visual proof first: cover, architecture/stack, and workflow/pipeline slides.
- Deliver PNG screenshots and a contact sheet, and clearly label them as direction-confirmation previews rather than the completed deck.

### Freeform Direction Prototype

When the user explicitly asks to ignore previously agreed design rules and produce the agent's own best-fit slide sample for later direction, follow:
- Do not over-ask; create a small 6–10 slide visual proof immediately.
- Label it as a prototype/style sample, not the final house style.
- Include representative slide types and practical setup-class elements: progress map, prompt box, folder tree, recovery flow, architecture map.
- Deliver artifact-first with PNG contact sheet/screenshots and source HTML; include PDF when practical.
- If macOS Chrome Keychain warnings appear during rendering, tell the user to click 취소, avoid 기본값으로 재설정, and use isolated-profile/mock-keychain Chrome flags on subsequent renders.

### Korean PPT Reference Curation

When the user asks to find or show Korean PPT design references, especially “한글 PPT”, “국문 발표자료”, “사진/캡처로 보여줘”, follow:
- Prioritize Korean-native sources first (디자인킵, PPT BIZCAM, FreePPT, 미리캔버스, 예스폼/국문 제안서) and use Slidesgo/Canva as supplemental layout references.
- If the user asks to see images, produce a PNG contact sheet with 8-14 cards instead of only listing links.
- Keep the reply short and artifact-first: send `MEDIA:/absolute/path.png`, then a compact source summary.

### Korean PPT Reference Research

When the user asks for 한국어/한글/국문 PPT 디자인 레퍼런스, load and apply:
- Prioritize Korean-first sources and Hangul-ready business/education decks before broad global template sites.
- Score references by readability, visual explanation value, and usefulness for actual slide production.
- If the user asks to “보여줘” or “캡처”, produce a visual contact sheet image and deliver it via `MEDIA:` rather than only listing links.
- Group findings by use case: 강의/교육, 제안서/회사소개서, 플로우/프로세스, 비즈니스/IR.

## Chunk-Based Generation (20장 초과)

20장을 초과하는 슬라이드는 Slide Composer가 청크 단위로 분할 생성한다.

```
청크 크기: 20장
분할 예시:
  25장 -> 청크 2개 (1-20, 21-25)
  40장 -> 청크 2개 (1-20, 21-40)
  60장 -> 청크 3개 (1-20, 21-40, 41-60)

규칙:
  - 커버 슬라이드: 1장에만
  - 마무리 슬라이드: 마지막 장에만
  - 청크 간 내러티브 연결 필수
  - 최종 출력은 하나의 index.html로 통합
```

## Speaker Script (발표 대본)

모든 슬라이드에 발표자용 구어체 대본을 포함한다.

```
- data-speaker-note 속성으로 HTML에 저장
- 'N' 키로 발표자 노트 패널 토글
- 화면 텍스트의 반복이 아닌 보충 설명/전환 멘트
- 존댓말 구어체, 슬라이드당 3~5문장
```

---

## Parallel Execution Rules

### 동시 실행 가능

```
Typography Expert + Layout Engineer
  (서로 독립적, 토큰만 공유)
```

### 순차 대기

```
Design Cloner 완료 -> Typography Expert, Layout Engineer
                   -> Slide Composer
Motion Director  <- Slide Composer HTML 완료 후
QA Reviewer      <- 모든 에이전트 완료 후
```

---

## Output Structure

### Mobile / Telegram delivery

When delivering slide drafts, lecture manuscripts, workbooks, or long course artifacts over Telegram, do **not** send only raw `.md`. iPhone/Telegram preview can render Markdown poorly or make Korean text hard to review. Deliver a mobile-review package by default:

- Working source: `.md`
- Mobile review: `.pdf`
- Plain fallback: UTF-8 `.txt`

If the final HTML slide renderer is not ready, generate a mobile-friendly HTML reading view and print it to PDF with Chrome headless. See for the exact pattern, CSS notes, and verification checklist.

## Output Structure

```
{project-name}/
  index.html                 -- 슬라이드 메인 파일
  theme/
    tokens.css               -- 디자인 토큰 (Design Cloner)
    typography.css            -- 타이포그래피 (Typography Expert)
    layout.css               -- 레이아웃 (Layout Engineer)
    motion.css               -- 애니메이션 (Motion Director)
    components.css            -- 컴포넌트 기본 스타일
    theme.css                -- @import 통합
  scripts/
    slide-controller.js      -- 슬라이드 네비게이션
    animations.js            -- 애니메이션 트리거
    theme-controller.js      -- 테마 전환 (Light/Dark)
  assets/
    images/                  -- 이미지 파일
    icons/                   -- SVG 아이콘
```

---

## Theme Presets

레퍼런스 이미지 없이 시작할 때 제공하는 기본 테마:

| 프리셋 | 배경 | 텍스트 | 강조 | 분위기 |
|-------|------|--------|------|--------|
| **모던 다크** | #0F172A | #F1F5F9 | #3B82F6 | 테크, 미래지향 |
| **클린 라이트** | #FFFFFF | #1E293B | #2563EB | 비즈니스, 깔끔 |
| **웜 프리미엄** | #FFFBF5 | #1C1917 | #D97706 | 고급, 따뜻한 |
| **네이처 그린** | #F0FDF4 | #14532D | #16A34A | 친환경, 성장 |
| **바이올렛 크리에이티브** | #FAF5FF | #3B0764 | #7C3AED | 혁신, 대담 |

---

## Slide Controls

### 키보드 단축키

| 키 | 동작 |
|---|------|
| `→` `↓` `Space` | 다음 슬라이드 |
| `←` `↑` | 이전 슬라이드 |
| `F` | 전체화면 토글 |
| `N` | 발표자 노트 토글 |
| `Esc` | 전체화면 종료 |

### 터치 제스처

| 제스처 | 동작 |
|--------|------|
| 좌로 스와이프 | 다음 슬라이드 |
| 우로 스와이프 | 이전 슬라이드 |

---

## Conversation Protocol

### 한글 소통 원칙

```
- 질문은 짧고 구체적으로 (1개씩)
- 선택지는 2-3개로 제한
- 전문 용어 대신 일상어 사용
- "추천해주세요" 옵션 항상 포함
```

### 시작 대화

```
"안녕하세요! 프레젠테이션을 만들어 드리겠습니다.

어떻게 시작할까요?
A. 참고할 PPT/디자인 이미지가 있어요 (이미지 첨부)
   - 원고나 리포트도 함께 첨부하면 자동으로 슬라이드 내용을 구성해드려요
B. 처음부터 새로 만들고 싶어요
C. 기존 슬라이드를 수정하고 싶어요"
```

### 진행 보고

```
"[진행 상황]
1/5 디자인 분석 완료
2/5 레이아웃 설계 중...
"
```

### 완료 안내

```
"{프로젝트명}/ 폴더에 10장의 슬라이드가 준비되었습니다.

시작하기:
  브라우저에서 index.html을 열어주세요.
  → ← 방향키로 슬라이드 전환
  F키로 전체화면 프레젠테이션

수정이 필요하면 말씀해주세요."
```

---

## Agent Delegation Rules

### 에이전트 호출 방법

```
각 에이전트는 .claude/agents/ 디렉토리의 정의를 따르고,
.claude/skills/ 디렉토리의 전문 스킬을 참조합니다.

에이전트 호출 시:
1. 에이전트 정의 파일 읽기 (agents/*.md)
2. 해당 스킬 파일 읽기 (skills/*/SKILL.md)
3. 입력 데이터 전달
4. 출력 확인
```

### 에이전트 간 데이터 전달

```
Design Cloner -> (tokens.css) -> 모든 에이전트
Design Cloner -> (분석 보고서) -> Slide Composer, QA Reviewer
Typography Expert -> (typography.css) -> Slide Composer
Layout Engineer -> (layout.css, 레이아웃 매핑) -> Slide Composer
Slide Composer -> (HTML 슬라이드) -> Motion Director
Motion Director -> (motion.css, animations.js) -> 최종 출력
QA Reviewer -> (수정 피드백) -> 해당 에이전트
```

---

## Quality Gate

### 최종 출력 전 반드시 확인

```
필수:
- [ ] index.html이 브라우저에서 열림
- [ ] 슬라이드 전환 동작 (키보드/터치)
- [ ] 전체화면 모드 동작
- [ ] 모든 스타일이 토큰 참조 (하드코딩 없음)
- [ ] 한글 줄바꿈 정상 (word-break: keep-all)
- [ ] 폰트 로딩 정상

권장:
- [ ] prefers-reduced-motion 대응
- [ ] 색상 대비 4.5:1 이상
- [ ] 모바일 반응형 확인
- [ ] 원본 이미지 대비 시각 검증 (Route A)
```

---

## Don't Do This

- 사용자 확인 없이 슬라이드 내용 임의 작성
- 하드코딩된 스타일 (모든 값은 CSS 변수)
- 한 슬라이드에 정보 과다
- 모든 슬라이드를 같은 레이아웃으로 (다양성 필요)
- 애니메이션 없이 정적 HTML만 출력
- 한글에 italic 적용
- PPT 레이아웃을 position: absolute로 복사
- 에이전트 순서 무시 (토큰 없이 HTML 생성 등)

---

## Dependencies

이 팀은 외부 라이브러리 없이 순수 HTML/CSS/JS로 동작합니다.

```
필수:
- 웹폰트 CDN (Pretendard, Google Fonts)
- 모던 브라우저 (Chrome, Safari, Firefox, Edge)

선택:
- lucide-icons CDN (SVG 아이콘)
- PDF 내보내기: 브라우저 인쇄 기능 (Ctrl+P)
```

---

## File References

| 파일 | 용도 |
|------|------|
| `.claude/agents/design-cloner.md` | 디자인 역설계 에이전트 |
| `.claude/agents/slide-composer.md` | 슬라이드 구성 에이전트 |
| `.claude/agents/typography-expert.md` | 한글 타이포 에이전트 |
| `.claude/agents/layout-engineer.md` | 레이아웃 에이전트 |
| `.claude/agents/motion-director.md` | 모션 에이전트 |
| `.claude/agents/qa-reviewer.md` | QA 검증 에이전트 |
| `.claude/skills/theme-system/SKILL.md` | 디자인 토큰 시스템 |
| `.claude/skills/typography-system/SKILL.md` | 한글 타이포 시스템 |
| `.claude/skills/layout-system/SKILL.md` | 그리드/레이아웃 시스템 |
| `.claude/skills/design-cloning/SKILL.md` | 이미지 역설계 프로토콜 |
| `.claude/skills/motion-system/SKILL.md` | 애니메이션 시스템 |
| `.claude/skills/slide-generation/SKILL.md` | 슬라이드 생성 프로토콜 |
