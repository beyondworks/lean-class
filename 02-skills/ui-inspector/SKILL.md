---
name: ui-inspector
description: >
  라이브 프리뷰에서 UI 요소를 클릭하면 코드 위치, 컴포넌트 이름, 상세 스타일,
  UI/UX 전문 용어를 즉시 확인하고 그 자리에서 수정할 수 있는 인스펙터.
  Agentation 스타일 다중 annotation 지원 — 여러 요소(같은 요소 중복 포함)에
  핀+코멘트를 남기면 annotation_list로 한 번에 읽어 일괄 수정하고
  annotation_resolve로 해결 처리한다(브라우저 핀이 초록색으로 실시간 전환).
  사용자가 "이 부분", "여기", "선택한 요소", "클릭한 거"라고 말하면
  반드시 inspector_get_selection을 먼저 호출해서 컨텍스트를 가져온 뒤 작업한다.
  사용자가 "핀 단 것들", "annotation 반영해줘", "메모한 것들 수정해줘",
  "표시한 부분들 처리해줘"라고 말하면 반드시 annotation_list를 먼저 호출한다.
  트리거: "인스펙터", "프리뷰 띄워줘", "이 부분 수정", "여기 색 바꿔",
  "선택한 요소", "preview_attach", "라이브 프리뷰", "어노테이션", "핀",
  "annotation", "메모 반영".
version: 1.1.0
---

# UI Inspector

라이브 프리뷰 + 요소 인스펙터 MCP. 외부 LLM 호출 없이 순수하게 코드 위치·스타일·UI/UX 용어만 반환하며, 모든 추론·편집은 Claude가 직접 수행한다.

## 핵심 워크플로우 — 양방향 호출

### 사내 운영 콘솔 시각 QA 규칙

사내 인트라넷·운영 콘솔, dashboard, 또는 dense operational UI 작업에서는 코드만 보고 디자인 품질을 판단하지 않는다. 반드시 라이브 프리뷰/ui-inspector 또는 browser vision으로 렌더링을 먼저 확인하고, 수정 후 다시 시각 검증한다.

우선순위는 새 시각 콘셉트가 아니라 시스템 일관성이다: 아이콘 통일성, 레이아웃 리듬, row/card 기준선, spacing, typography scale, 패널 폭 균형, component auto-layout 동작. 사용자가 명시하지 않는 한 기존 톤/색을 유지하고, 그라데이션/장식적 색상 변경을 디자인 개선으로 취급하지 않는다.

실행 루프:
1. ui-inspector/browser로 실제 화면을 연다.
2. 관련 화면(Today/Work/Agents/Runs/Truth/Gateways 등)을 렌더 기준으로 본다.
3. side-panel weight, row height, clipped label, icon size, chip alignment, title truncation, metadata wrapping, inconsistent gap처럼 구체적 불균형을 기록한다.
4. 최소한의 CSS/component rhythm 수정만 한다.
5. 다시 시각 QA를 하고 build/API/console을 검증한 뒤 완료 보고한다.

1. 사용자가 `preview_attach` (외부 dev 서버) 또는 `preview_start` (새 Vite 세션)로 프리뷰 실행
2. 사용자가 `preview_select_element` 의 `enable_inspector` 액션으로 인스펙터 모드 활성화, 또는 브라우저 우하단 토글 클릭
3. 사용자가 브라우저에서 요소 클릭 → WebSocket으로 서버에 `element_selected` 브로드캐스트
4. 사용자가 "이 부분 padding 늘려줘" 같은 자연어 요청
5. **Claude는 즉시 `inspector_get_selection` 호출** → `sourceLocation.file`, `sourceLocation.line`, `tag`, `className`, `computedStyles`, `uiTerm` 확보
6. Read 도구로 해당 파일을 읽고 Edit으로 수정
7. Vite HMR (또는 attach 모드의 원본 dev 서버)이 자동 반영

## 렌더 기준 시각 QA 규칙
사용자가 UI 균형, 디자인 시스템, 오토레이아웃, 아이콘 통일성, 레이아웃 리듬, 카드/행/텍스트 간격을 지적하면 코드만 읽고 판단하지 않는다. 반드시 라이브 프리뷰를 열어 실제 렌더링을 보고, 필요하면 `preview_screenshot` 또는 브라우저/vision QA로 전후를 비교한다.

- 색상/그라데이션/장식 추가가 아니라 **시스템 일관성** 요청이면 기존 톤을 유지한다.
- 우선 확인 축: 아이콘 크기·stroke·baseline, column weight, card/row height, padding/gap scale, meta text wrapping, button/input height, Korean label rhythm.
- 수정 후에는 같은 화면을 다시 시각 검증하고 build/console/API까지 확인한 뒤 완료를 말한다.
- 세부 체크리스트는 `references/visual-rhythm-qa.md`를 따른다.

## 도구 목록 (18)

### 프리뷰 (7)
- `preview_start` — 새 Vite 세션 시작 (초기 파일 맵 제공 가능)
- `preview_attach` — 기존 Next.js/Vite dev 서버에 프록시+인스펙터 주입
- `preview_update` — 파일 업데이트 (HMR 반영)
- `preview_status` — 세션 상태 조회
- `preview_stop` — 세션 종료
- `preview_export` — 프레임워크 변환 후 ZIP으로 내보내기
- `preview_screenshot` — 뷰포트/셀렉터 기준 스크린샷

### 인스펙터 양방향 (3)
- `preview_select_element` — `action: enable_inspector | disable_inspector | get_selected`. 세션 단위 조작
- `inspector_get_selection` — **가장 최근 클릭 요소** 반환. 지시대명사("이 부분", "여기", "선택한 거") 처리 전용. `session_id` 생략 시 모든 활성 세션에서 최신 선택 자동 선택
- `inspector_clear_selection` — 선택 해제

### Annotation — Agentation 스타일 다중 핀 (4)
- `annotation_list` — 사용자가 브라우저에서 남긴 모든 annotation(핀+코멘트) 목록. 요소 이름·cssPath·소스 위치·스타일·HTML 스니펫 포함
- `annotation_resolve` — 수정 완료한 annotation을 해결 처리 (`ids` 또는 `all: true`, `note`에 수정 내용 한 줄). 브라우저 핀이 초록 ✓로 실시간 전환. `reopen: true`로 되돌리기
- `annotation_remove` — annotation 삭제
- `annotation_to_prompt` — 전체 annotation을 에이전트용 마크다운 태스크 리스트로 변환 (Codex 등 외부 에이전트 전달용)

### 인스펙터 보조 (2)
- `inspector_highlight` — 브라우저에서 요소를 잠시 하이라이트+스크롤 (selector 또는 data_at). "여기 수정했습니다" 시각 커뮤니케이션
- `preview_errors` — 페이지 런타임 에러(uncaught/rejection/console.error) 조회. 수정 후 정상 동작 확인 루프에 사용

### 디자인 지식 (2)
- `query_ontology` — UI/UX 용어·디자인 토큰·패턴 검색 (로컬 온톨로지 저장소)
- `validate_design` — 대비/터치 타겟/계층/간격 규칙 검증

## Annotation 일괄 처리 워크플로우

1. 사용자가 브라우저 툴바에서 **Annotate** 토글 → 요소 클릭 → 코멘트 입력 (같은 요소에 여러 개 중복 가능, 번호 핀으로 표시). **드래그하면 영역 내 최상위 요소들을 일괄 선택**해 코멘트 하나로 그룹 annotation 생성 (핀 1개, `elements` 배열에 요소 최대 30개 — 각각 셀렉터·소스 위치 포함)
2. 사용자가 "핀 단 것들 반영해줘" → **`annotation_list` 호출**
3. 각 annotation의 `sourceLocation`(있으면) 또는 `cssPath`/`htmlSnippet`/`textContent`로 Grep해서 파일 위치 특정 → Edit. **그룹 annotation(`elements` 배열 존재)이면 배열의 모든 요소에 같은 요청을 적용**
4. 항목 하나 수정 완료할 때마다 **즉시 `annotation_resolve`** (`note`에 수정 내용) — 사용자가 브라우저에서 진행 상황을 실시간으로 봄
5. 전체 완료 후 `preview_errors`로 런타임 에러 확인, 필요 시 `inspector_highlight`로 수정 위치를 시각적으로 보여줌
6. annotation은 서버에 저장되어 새로고침/HMR에도 유지됨

## "이 부분" 처리 규칙
사용자 발화에 다음 단어가 있으면 **무조건 `inspector_get_selection` 먼저 호출**:
- "이 부분", "여기", "이거", "이것"
- "선택한", "클릭한", "지금 보는"
- "이 컴포넌트", "이 버튼", "이 영역"

선택 정보가 없으면 (`selected_element: null`) 사용자에게 이렇게 안내한다:
> 브라우저 인스펙터에서 수정할 요소를 먼저 클릭해주세요.

## 반환 스키마 (inspector_get_selection)
```json
{
  "session_id": "prev_xxxxxx",
  "selected_element": {
    "tag": "button",
    "className": "primary cta",
    "textContent": "구매하기",
    "boundingRect": { "x": 120, "y": 340, "width": 180, "height": 48 },
    "computedStyles": {
      "backgroundColor": "rgb(59, 130, 246)",
      "color": "rgb(255, 255, 255)",
      "fontSize": "16px",
      "padding": "12px 24px",
      "borderRadius": "8px"
    },
    "sourceLocation": { "file": "src/components/CTA.tsx", "line": 18, "column": 4 },
    "parentChain": ["div.hero", "section.landing", "main"],
    "uiTerm": "Call to Action",
    "uiDescription": "사용자의 핵심 행동을 유도하는 강조된 버튼이나 링크 (CTA)",
    "selectedAt": "2026-04-07T12:34:56.789Z"
  }
}
```

`sourceLocation`은 `data-at` 속성(Vite/Babel source plugin)이 주입된 경우에만 채워진다. Next.js/Vite React 프로젝트에서 일반적으로 자동 주입되며, 없으면 `null`이 반환된다. 그 경우 `parentChain`과 `className`으로 파일을 Grep해서 위치를 찾는다.

## 팁
- 인스펙터 모드는 프리뷰 우하단의 "Inspector OFF/ON" 토글로도 전환 가능
- 클릭 시 우측 패널에 실시간으로 Source/Design Term/Styles/Size/Parent Chain이 표시됨
- `preview_attach`는 Next.js HMR을 그대로 유지하므로 원본 프로젝트 파일을 직접 Edit하면 된다
- Hermes 프로필에서 `preview_attach` 같은 MCP 도구가 직접 노출되지 않으면 `references/hermes-next-attach.md`의 MCP client fallback을 사용해 기존 Next.js dev 서버에 프록시를 붙인다.
- WebSocket 연결이 끊겨도 10회까지 자동 재연결 (exponential backoff)
