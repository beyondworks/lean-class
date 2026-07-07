---
name: script-to-slides
description: 모듈/섹션 구조의 markdown 대본을 미니멀한 '슬라이드형 웹사이트'(16:9 캐러셀 HTML)로 변환한다. 다크+그린 디자인 시스템, 한글 타이포 정밀, 텍스트↔시각화 비충돌 그리드, SVG 다이어그램, 발표자/청중 동기화 + 발표자 노트 + 전체화면 포함. "대본을 슬라이드로", "웹 슬라이드 만들어줘", "이 내용 발표자료로", "발표자료 웹으로", "캐러셀 슬라이드" 류 요청에 사용. 골든 레퍼런스 = webinar-agent-intro/web (브라우저 렌더 검증본).
user-invocable: true
argument-hint: "[대본 파일.md 또는 붙여넣은 콘텐츠]"
license: Proprietary
---

# script-to-slides — 대본 → 슬라이드형 웹사이트

markdown 대본을 **16:9 캐러셀로 슬라이드되는 웹사이트**로 만든다. reveal.js류가 아니라 **순수 vanilla HTML/CSS/JS**다(의존성 0, 정적 서버로 바로 뜸).

> 골든 레퍼런스: 이 스킬의 모든 규칙은 검증된 웨비나 슬라이드 1건에서 추출했고, `references/assets/`(theme.css·carousel.js·presenter.*)에 검증본을 박제했다 — 별도 경로 없이 이 폴더만으로 자립한다.

## 산출물 구조 (고정)
```
<out>/
├── index.html      ← 슬라이드 트랙(.stage>.viewport>.track>.slide 다수)
├── style.css       ← references/assets/theme.css 복사 후 토큰만 커스터마이즈
├── carousel.js     ← references/assets/carousel.js 그대로 (동기화·풀스크린·스와이프)
├── notes.js        ← 발표자 노트(슬라이드별 구어체 스크립트) — 선택
├── presenter.html/.css/.js  ← 발표자 모드 — 선택(references/assets/ 그대로)
└── img/            ← 이미지 배경 쓸 때만
```

## 절차 (이 순서를 지킨다)

### 0. 준비 — 디자인 컨텍스트 로드 (필수)
- gstack 디자인 스킬이 있으면 `/frontend-design`(원칙·안티슬롭·Context Gathering)을 먼저 읽는다. `/design-review`는 마지막 검증에 쓴다.
- ui 스킬(`/shadcn-ui`·`/ui-expert`)은 그리드·컴포넌트 비율 판단에 참조(레이아웃 일관·여백).
- 없으면 이 SKILL의 규칙만으로 충분하다.

### 1. 대본 파싱 → 슬라이드 맵
- 대본의 **모듈/섹션**을 슬라이드 단위로 쪼갠다. 한 슬라이드 = 한 메시지.
- 각 슬라이드에 **패턴**을 배정한다(`references/slide-patterns.md` 카탈로그):
  표지 · 개념예고(pills) · 다이어그램(split) · Before/After(cmp) · 3·4-up 카드 · 정리(maplist) · 상세페이지(detail) · CTA.
- North Star 한 줄(청중 결과)을 맨 위에 박고, 슬라이드마다 "이게 그 결과에 기여하나" 자문.

### 2. 골든 자산 복사
```bash
cp references/assets/{theme.css,carousel.js} <out>/   # theme.css→style.css 로 저장
cp references/assets/presenter.* <out>/               # 발표자 모드 쓸 때
```
- `style.css` 상단 `:root` 토큰만 프로젝트에 맞게: `--bg`·`--green`(액센트)·`--font`. 나머지 레이아웃·컴포넌트는 건드리지 않는다(검증본).

### 3. index.html 작성
- `references/index-template.html` 골격을 복사 → 슬라이드 맵대로 `<section class="slide">` 채운다.
- 다이어그램은 `references/svg-diagrams.md` 패턴(U자·흐름·박스맵·비교)을 viewBox째 가져와 라벨만 교체.
- 카운터/도트/진행바/풀스크린·발표자 버튼은 템플릿에 이미 있다(건드리지 않음).

### 4. 검증 (자기승인 금지 — 빌드≠동작)
정적 서버 띄우고 **실제 브라우저 렌더로 시각 확인**한다:
```bash
cd <out> && python3 -m http.server 4601 &   # 또는 npx serve
# headless 캡처 → 이미지로 직접 확인 (슬라이드별 #N 딥링크)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --window-size=1920,1080 --hide-scrollbars --virtual-time-budget=3500 \
  --screenshot=/tmp/s_N.png "http://localhost:4601/#N"
```
- 또는 playwright `browser_navigate` + `browser_evaluate`로 오버플로우/겹침 측정.
- 체크: ① 텍스트↔다이어그램 **겹침 0** ② SVG 라벨이 박스 밖으로 안 넘침 ③ 한글 줄바꿈이 단어 중간에서 안 깨짐 ④ 콘텐츠가 도트(하단)·버튼(우하단)과 안 겹침 ⑤ 카운터 N/total 정확.
- 정렬 검수는 **구현과 분리된 컨텍스트**(가능하면 code-reviewer/design-review 서브에이전트)로. 자기 세션 자기승인 금지.

## ★ 박제 규칙 (v3에서 검증된 것 — 반드시 적용)

1. **한글 가독성**: 모든 텍스트 요소에 `word-break:keep-all; overflow-wrap:break-word`(theme.css 13행에 전역 박제됨). 제목 `line-height` 1.15~1.25, `letter-spacing:-0.02em`. 영어가 아니라 **한글 기준**으로 줄바꿈·자간을 본다. `<br>`로 의미 단위 균형 줄바꿈.
2. **그리드 비충돌(shadcn식)**: 텍스트와 시각화(카드·그래프)는 `.overlay.split`(좌 텍스트/우 비주얼) 또는 상하 분리로 **절대 겹치지 않게**. 여백·정렬 토큰 일관(`padding:0 8.5cqw`, `gap` 일정).
3. **SVG 정밀**: `viewBox` 기준 좌표로 정렬·균형. 선이 박스를 관통하지 않게 **가장자리에서 끊는다**(노드 edge 좌표로). 화살표 marker는 작게(`markerWidth 6` 내외). 라벨이 박스를 넘으면 `font-size` 축소 또는 문구 단축. 텍스트는 `class="l"/"s"`로 통일.
4. **이미지 위 가독성**(이미지 배경 쓸 때): 균일 스크림(`.scrim.full`) + 글라스 패널(`backdrop-filter:blur`)로 washed-out 방지. 단, **상세/전환 슬라이드는 사진 빼고 플랫 다크**(`.slide.detail`)로 정보 밀도↑.
5. **단위는 컨테이너 쿼리(cqw/cqh)**: `.stage{container-type:size}` 안에서 모든 폰트·간격을 `cqw`로 → 16:9 어디서나 동일 비율. px 직접 쓰지 않는다(다이어그램 viewBox 내부 제외).
6. **검증 = 시각**: 코드/수치부터 만지지 말고 렌더를 보고(headless 캡처→Read) 판단한 뒤 수치화. "디자인은 눈으로 보고 그걸 수치화하는 것."

## 슬라이드 패턴 & theme 변수
- 패턴 카탈로그: `references/slide-patterns.md` (HTML 스니펫).
- SVG 다이어그램: `references/svg-diagrams.md`.
- theme 토큰·컴포넌트 클래스: `references/assets/theme.css` 주석 참조.
  - 핵심 클래스: `.title/.head/.eyebrow/.lead` · `.pills/.pill` · `.cmp .pan.good/.bad` · `.cards3/.cards4 .c` · `.maplist` · `.gcard` · `.takeaway` · `.flow6` · `.faq` · `.dg`(다이어그램) · `.slide.detail`(상세 포맷).

## 기능(템플릿에 포함, 무료)
- **캐러셀**: 화살표 없이 도트·키보드(←→ Home End)·스와이프·진행바·카운터·해시 딥링크(#N).
- **전체화면**: `F` 키 / 우하단 버튼(webkit 프리픽스 폴백 포함).
- **발표자/청중 동기화**: `S` 키로 `presenter.html` 팝업. BroadcastChannel+localStorage로 양방향 동기화(같은 브라우저 창·탭 간). 크로스기기는 별도 동기 서버 필요(미포함).
- **발표자 노트**: `notes.js`의 `DEFAULT_NOTES[]`(슬라이드별 구어체 스크립트) → 발표자 모드에서 자동저장·글자크기 조절.

## status
- **seed** — 이 스킬은 골든 레퍼런스 1건(webinar-agent-intro)에서 추출했다. 실사용 2건+ / 품질 채점 / 유건 승인 후 **active** 승격.
- design 도메인 → 볼트 `wiki/harnesses/design.md` 의 `provenance.fed_by` 후보로 연결 가능.
