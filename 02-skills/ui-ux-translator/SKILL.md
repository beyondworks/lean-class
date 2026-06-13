---
name: ui-ux-translator
description: >
  비전문 언어나 스크린샷을 UI/UX 전문 용어로 번역하는 스킬.
  Claude Code에서 UI 수정 시 정확한 컴포넌트명, CSS 속성, 디자인 용어로 변환.
  트리거: (1) "이거 고쳐줘" + 스크린샷, (2) "~부분 ~하게 해줘" 식의 비전문 요청,
  (3) "UI 수정", "디자인 바꿔줘", "버튼/메뉴/글자 고쳐줘" 포함 요청.
  키워드: 버튼, 메뉴, 글자, 간격, 색깔, 크기, 정렬, 테두리, 그림자, 팝업, 탭, 카드
---

# UI/UX Translator Skill

비전문 언어 → UI/UX 전문 프롬프트 변환기
Claude Code에서 바로 사용할 수 있는 정확한 기술 지시문을 생성합니다.

---

## 스킬 작동 방식

### 입력 유형

1. **텍스트만** — "상단 메뉴 글자 간격 벌려줘"
2. **스크린샷만** — 이미지 첨부, 별도 설명 없음
3. **텍스트 + 스크린샷** — 이미지 + "이 버튼 더 둥글게"

### 출력 형식

```
[분석] 어떤 컴포넌트/영역인지 파악한 내용
[번역된 프롬프트] Claude Code에 그대로 붙여넣을 수 있는 전문 지시문
[참고] 관련 CSS 속성 또는 컴포넌트명 (선택)
```

---

## 핵심 번역 규칙

### 1. 컴포넌트 식별 우선

사용자의 비전문 표현을 아래 컴포넌트 중 하나로 매핑 후 번역:

| 비전문 표현 | 컴포넌트명 | 설명 |
|---|---|---|
| 상단 메뉴 | Navigation Bar / Header | 페이지 최상단 탐색 영역 |
| 햄버거 버튼 | Hamburger Menu / Mobile Menu Toggle | ≡ 형태의 메뉴 트리거 |
| 드롭다운 | Dropdown Menu / Select | 클릭 시 목록 펼쳐지는 컴포넌트 |
| 팝업 / 뜨는 창 | Modal / Dialog | 화면 위에 레이어로 뜨는 창 |
| 알림 메시지 | Toast / Snackbar / Alert | 일시적 상태 알림 |
| 탭 | Tabs | 같은 영역 내 콘텐츠 전환 UI |
| 카드 | Card | 단일 개체(상품/게시글)를 담는 컨테이너 |
| 버튼 | Button (Primary/Secondary/Ghost/Icon) | 액션 트리거 |
| 입력창 | Input / Text Field | 텍스트 입력 요소 |
| 체크박스 | Checkbox | 다중 선택 컨트롤 |
| 토글/스위치 | Toggle / Switch | 온/오프 상태 전환 |
| 검색창 | Search Field / Search Bar | 검색 입력 UI |
| 페이지 넘김 | Pagination | 다중 페이지 탐색 컨트롤 |
| 로딩 | Spinner / Skeleton / Progress Bar | 대기 상태 표시 |
| 툴팁 | Tooltip | 호버 시 나타나는 보조 설명 |
| 배지 / 숫자 표시 | Badge | 상태·수량을 나타내는 소형 레이블 |
| 아코디언 / 펼치기 | Accordion / Disclosure | 클릭으로 펼쳐지는 컨텐츠 섹션 |
| 사이드 패널 | Drawer / Sidebar | 화면 측면에서 슬라이드 인/아웃 |
| 슬라이더 | Slider / Carousel | 콘텐츠를 슬라이드하는 UI |
| 진행바 | Progress Bar / Stepper | 진행 상태를 시각화 |
| 아바타 | Avatar | 사용자 프로필 이미지/이니셜 |
| 브레드크럼 | Breadcrumbs | 현재 위치 계층 표시 탐색 |
| 태그 | Tag / Chip / Label | 속성·분류를 나타내는 소형 UI |
| 별점 | Rating | 별 모양 평점 선택 UI |
| 구분선 | Divider / Separator | 영역 구분용 수평선 |
| 테이블 | Table / Data Table | 행·열 형태의 데이터 표시 |
| 달력 | Calendar / Date Picker | 날짜 선택 UI |
| 목록 | List / List Item | 연관 항목의 세로 나열 |
| 도넛/막대 차트 영역 | Chart / Data Visualization | 데이터 시각화 컴포넌트 |
| 푸터 | Footer | 페이지 최하단 영역 |
| 히어로 영역 | Hero Section / Banner | 상단 대형 이미지+텍스트 영역 |
| 빈 화면 | Empty State | 데이터 없을 때 보여주는 UI |

---

### 2. 속성·스타일 번역 매핑

| 비전문 표현 | 전문 용어 / CSS 속성 |
|---|---|
| 글자 간격 벌려줘 | `letter-spacing` 증가 (예: `letter-spacing: 0.05em`) |
| 줄 간격 넓혀줘 | `line-height` 증가 (예: `line-height: 1.8`) |
| 글자 더 크게/작게 | `font-size` 조정 (px 또는 rem 단위) |
| 글자 굵게 | `font-weight: 600` 또는 `700` (Semibold / Bold) |
| 글자 색 바꿔줘 | `color` 속성 변경 (HEX/RGB/CSS 변수) |
| 배경색 바꿔줘 | `background-color` 속성 변경 |
| 더 둥글게 | `border-radius` 증가 (예: `border-radius: 8px` → `12px`) |
| 완전 원형으로 | `border-radius: 50%` 또는 `border-radius: 9999px` |
| 테두리 없애줘 | `border: none` |
| 테두리 추가해줘 | `border: 1px solid {color}` |
| 그림자 넣어줘 | `box-shadow: 0 4px 12px rgba(0,0,0,0.1)` |
| 그림자 없애줘 | `box-shadow: none` |
| 간격 넓혀줘 (내부) | `padding` 증가 |
| 간격 넓혀줘 (외부) | `margin` 증가 |
| 가운데 정렬 | `text-align: center` / `justify-content: center` / `align-items: center` |
| 오른쪽 정렬 | `text-align: right` / `justify-content: flex-end` |
| 세로 가운데 | `align-items: center` (flex/grid context) |
| 꽉 채워줘 (너비) | `width: 100%` |
| 크기 고정해줘 | `width: {n}px; height: {n}px` |
| 투명하게 | `opacity` 조정 또는 `rgba` alpha 채널 |
| 흐리게 | `opacity: 0.5` 또는 `filter: blur()` |
| 위치 올려줘 | `margin-top` 감소 또는 `top` 값 조정 |
| 겹치게 보여줘 | `position: absolute` / `z-index` 조정 |
| 숨겨줘 | `display: none` 또는 `visibility: hidden` |
| 애니메이션 넣어줘 | `transition` / `animation` 속성 |
| 호버 효과 | `:hover` pseudo-class 스타일 |
| 클릭하면 색 바뀌게 | `:active` / `:focus` pseudo-class |
| 반응형으로 | Media query + breakpoint 적용 |
| 모바일에서 숨겨줘 | `@media (max-width: 768px) { display: none }` |

---

### 3. 레이아웃 번역 매핑

| 비전문 표현 | 전문 용어 |
|---|---|
| 옆으로 나란히 배치 | `display: flex; flex-direction: row` |
| 위아래로 쌓기 | `display: flex; flex-direction: column` |
| 격자 형태로 | `display: grid; grid-template-columns: repeat(n, 1fr)` |
| 양쪽 끝에 붙여줘 | `justify-content: space-between` |
| 균등하게 배치 | `justify-content: space-evenly` |
| 오른쪽 끝에 붙여줘 | `margin-left: auto` 또는 `justify-content: flex-end` |
| 화면 꽉 차게 | `width: 100vw; height: 100vh` |
| 항상 위에 떠있게 | `position: sticky; top: 0` 또는 `position: fixed` |
| 스크롤해도 안 움직이게 | `position: sticky` 또는 `position: fixed` |
| 뒤에 반투명 배경 | `backdrop-filter: blur()` 또는 overlay `rgba` layer |

---

## 스크린샷 분석 규칙

이미지가 첨부된 경우 다음 순서로 분석:

1. **영역 식별** — Header / Hero / Content / Sidebar / Footer 중 어느 영역인가
2. **컴포넌트 식별** — 어떤 컴포넌트가 보이는가 (위 컴포넌트 목록 참조)
3. **현재 상태 묘사** — 지금 어떻게 보이는가 (색상, 간격, 크기 추정)
4. **의도 파악** — 사용자가 어떻게 바꾸고 싶은가
5. **번역** — 정확한 CSS/컴포넌트 속성으로 변환

---

## 출력 템플릿

### 텍스트 요청 시

```
[분석]
- 대상 컴포넌트: {컴포넌트명}
- 대상 속성: {CSS 속성 또는 스타일 항목}
- 파악된 의도: {사용자가 원하는 결과}

[Claude Code용 프롬프트]
{파일경로 또는 컴포넌트명}의 {컴포넌트/요소}에서
{CSS 속성}을 {현재값}에서 {목표값}으로 변경해주세요.
{추가 조건이 있다면 명시}

[참고]
- CSS: `{속성}: {값}`
- 적용 범위: {전체/특정 breakpoint/특정 상태}
```

### 스크린샷 요청 시

```
[이미지 분석]
- 식별된 영역: {Header/Content/Footer 등}
- 주요 컴포넌트: {컴포넌트명 목록}
- 현재 스타일 추정: {색상/간격/크기 등 관찰 내용}

[번역된 프롬프트]
{구체적인 Claude Code 지시문}

[추가 확인 사항] (필요 시)
- 프레임워크가 무엇인지 알려주시면 더 정확한 코드를 드릴 수 있어요. (React/Vue/HTML 등)
```

---

## 번역 예시 (Quick Reference)

| 사용자 요청 | Claude Code 프롬프트 |
|---|---|
| "상단 메뉴 글자 간격 벌려줘" | `Header` 컴포넌트 내 `nav` 링크 텍스트의 `letter-spacing`을 `0.08em`으로 설정하고, 각 메뉴 아이템 간 `gap`을 `8px` 늘려주세요. |
| "버튼 더 둥글게" | 해당 `Button` 컴포넌트의 `border-radius`를 `8px`에서 `24px`로 증가시켜 Pill 형태로 변경해주세요. |
| "카드 그림자 없애줘" | `Card` 컴포넌트의 `box-shadow`를 `none`으로 제거하고, 대신 `border: 1px solid #e5e7eb`로 구분선을 추가해주세요. |
| "팝업 배경 더 어둡게" | `Modal` 오버레이의 `background-color`를 `rgba(0, 0, 0, 0.3)`에서 `rgba(0, 0, 0, 0.6)`으로 변경해주세요. |
| "탭 밑줄만 남기고 배경 없애줘" | `Tabs` 컴포넌트의 활성 탭 스타일에서 `background-color`를 제거하고, `border-bottom: 2px solid {primary-color}`만 유지하는 Underline 스타일로 변경해주세요. |
| "로딩 스피너 가운데로" | Spinner를 감싸는 컨테이너에 `display: flex; justify-content: center; align-items: center; min-height: 200px`를 적용해주세요. |
| "글자 너무 붙어있어, 여백 줘" | 해당 텍스트 요소의 `line-height`를 `1.6` 이상으로, `paragraph`인 경우 `margin-bottom: 1rem`을 추가해주세요. |
| "드롭다운 폰트 작게" | `Dropdown Menu` 내 아이템 텍스트의 `font-size`를 `14px`로 줄이고, `padding`도 비례하여 조정해주세요. |
| "헤더 스크롤해도 고정" | `Header`/`Navbar` 컴포넌트에 `position: sticky; top: 0; z-index: 100`을 적용하고, 스크롤 시 `box-shadow` 효과를 추가하는 것을 권장합니다. |
| "빈 화면에 안내 문구 넣어줘" | Empty State 컴포넌트를 추가하여 아이콘 + 제목 + 설명 텍스트 구조로 구성해주세요. |

---

## CRITICAL 규칙

### 절대 하지 않을 것

- 전문 용어를 설명 없이 사용자에게 되물어봄
- "CSS를 직접 알려주세요" 요구
- 컴포넌트가 무엇인지 불확실할 때 임의로 추정
- 스크린샷 없이 위치를 단정

### 반드시 할 것

- 비전문 표현을 가장 가능성 높은 컴포넌트로 매핑
- 여러 해석이 가능하면 2개 번역 제시 후 확인 요청
- Claude Code에서 그대로 복사-붙여넣기 가능한 형태로 출력
- 스크린샷 있을 때: 영역→컴포넌트→속성 순으로 분석
- 프레임워크 불명확 시: React 기준으로 번역 후 괄호로 (Tailwind/CSS-in-JS 버전도 필요하면 요청하세요) 안내

### 모호한 요청 처리

요청이 2가지 이상으로 해석 가능할 경우:
- 가장 일반적인 해석으로 먼저 번역
- 하단에 "[혹시 이런 의미였나요?]" 섹션으로 대안 번역 제시

---

## 디자인 시스템 용어 사전 (빠른 참조)

### 간격 시스템
- **Spacing Scale**: 4, 8, 12, 16, 24, 32, 48, 64px 단위 체계
- **Padding**: 요소 내부 여백
- **Margin**: 요소 외부 여백
- **Gap**: Flex/Grid 자식 요소 간격

### 타이포그래피
- **Font Weight**: Thin(100), Light(300), Regular(400), Medium(500), Semibold(600), Bold(700), ExtraBold(800)
- **Letter Spacing**: 자간 (em 단위 권장)
- **Line Height**: 행간 (1.4~1.8 일반적)
- **Text Transform**: uppercase / lowercase / capitalize

### 색상
- **Primary**: 브랜드 주 색상
- **Secondary**: 보조 색상
- **Destructive / Danger**: 삭제·경고 빨간 계열
- **Muted**: 흐린 배경·보조 텍스트
- **Foreground**: 텍스트 색상
- **Border**: 테두리 색상

### 상태
- **Default**: 기본 상태
- **Hover**: 마우스 올렸을 때
- **Active / Pressed**: 클릭 중
- **Focus**: 키보드 포커스
- **Disabled**: 비활성화
- **Loading**: 로딩 중
- **Error**: 오류 상태
- **Success**: 성공 상태

### 크기 변형
- **xs / sm / md / lg / xl**: 컴포넌트 크기 variant
- **Compact**: 여백 최소화된 밀집 형태
- **Comfortable**: 기본 여백
- **Spacious**: 여유 있는 여백

### 레이아웃
- **Container**: 최대 너비를 제한하는 래퍼
- **Grid**: 행·열 기반 배치 시스템
- **Flex**: 유연한 1차원 배치
- **Breakpoint**: 반응형 분기점 (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)
- **Z-index**: 레이어 쌓임 순서
