---
name: ui-inspector
description: >
  라이브 프리뷰에서 UI 요소를 클릭하면 코드 위치, 컴포넌트 이름, 상세 스타일,
  UI/UX 전문 용어를 즉시 확인하고 그 자리에서 수정할 수 있는 인스펙터.
  사용자가 "이 부분", "여기", "선택한 요소", "클릭한 거"라고 말하면
  반드시 inspector_get_selection을 먼저 호출해서 컨텍스트를 가져온 뒤 작업한다.
  트리거: "인스펙터", "프리뷰 띄워줘", "이 부분 수정", "여기 색 바꿔",
  "선택한 요소", "preview_attach", "라이브 프리뷰".
version: 1.0.0
---

# UI Inspector

라이브 프리뷰 + 요소 인스펙터 MCP. 외부 LLM 호출 없이 순수하게 코드 위치·스타일·UI/UX 용어만 반환하며, 모든 추론·편집은 Claude가 직접 수행한다.

## 핵심 워크플로우 — 양방향 호출

### control-room/control-room 시각 QA 규칙

control-room, company intranet, control-room, dashboard, 또는 dense operational UI 작업에서는 코드만 보고 디자인 품질을 판단하지 않는다. 반드시 라이브 프리뷰/ui-inspector 또는 browser vision으로 렌더링을 먼저 확인하고, 수정 후 다시 시각 검증한다.

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

## 도구 목록 (12)

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

### 디자인 지식 (2)
- `query_ontology` — UI/UX 용어·디자인 토큰·패턴 검색 (로컬 온톨로지 저장소)
- `validate_design` — 대비/터치 타겟/계층/간격 규칙 검증

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
- WebSocket 연결이 끊겨도 10회까지 자동 재연결 (exponential backoff)
