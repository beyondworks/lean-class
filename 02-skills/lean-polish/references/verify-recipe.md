# 앱 안 브라우저 검증 절차

{{OWNER_TITLE}}이 실제로 보는 화면과 같은 렌더러에서 확인하기 위한 절차다. 맥 미리보기(qlmanage), 헤드리스 크롬 같은 다른 렌더러는 글꼴 크기 계산이 달라서 "맞아 보이는데 브라우저에서는 어긋나는" 일이 생긴다(2026-10-20 실제로 글자가 칸 중앙에서 3~4px 벗어났다).

## 1. 서버 띄우기

```bash
bash ~/.claude/skills/lean-polish/scripts/serve.sh start <결과물 폴더> 8765
```

- 앱 안 브라우저는 `file://` 주소를 정적 스냅샷으로만 보여 주고 캡처할 수 없다("page tools can't act on it here"). 그래서 로컬 서버가 필요하다.
- 서버는 127.0.0.1에만 열린다. 확인이 끝나면 반드시 `serve.sh stop`.

## 2. 열고 보기

1. `mcp__Claude_Browser__navigate` 에 `http://127.0.0.1:8765/<파일명>` (한글 파일명도 된다).
2. SVG처럼 도면 폭이 뷰포트(약 800px)보다 크면 잘린다. `mcp__Claude_Browser__javascript_tool` 로 폭을 맞춘다.
   ```js
   const s = document.documentElement; const vb = s.viewBox.baseVal;
   s.setAttribute('width', 800); s.setAttribute('height', Math.round(800 * vb.height / vb.width)); 'ok'
   ```
3. `mcp__Claude_Browser__computer` 의 `screenshot` 으로 본다. 글자 중앙이나 겹침은 `zoom` (`region: [x0, y0, x1, y1]`)으로 확대해 본다.
4. 여러 장은 `mcp__Claude_Browser__browser_batch` 로 "navigate, javascript, screenshot" 세 개를 한 세트로 묶으면 빠르다. 이미지가 장마다 돌아온다.
5. `file://` 로 열린 탭에서는 다른 주소로 이동할 수 없어 새 탭이 만들어진다. 응답에 나온 새 `tabId` 를 이후 호출에 지정한다.

## 3. 브라우저가 그려지지 않을 때

증상: `screenshot failed: ... the Browser pane is not displayed`

- 원인: 이 세션이 어떤 창에도 열려 있지 않거나(사용자가 다른 세션을 보는 중), 브라우저 창이 숨겨진 상태.
- 시도: `mcp__Claude_Browser__tabs_select` 로 탭을 앞으로 → `mcp__ccd_view__show_pane` (`pane: "preview"`).
- 그래도 안 되면(`This session isn't open in any window right now`): **확인을 보류한다.** 다른 렌더러로 대신 확인하고 "확인했다"고 보고하지 않는다. 보고에 "앱 안 브라우저가 그려지지 않아 N장 확인 안 함, 세션 창을 열면 이어서 확인"이라고 쓴다.

## 4. 확인 순서

1. 처음 만든 직후: 전 장을 한 장씩 본다.
2. 결함을 고치면: **고친 장을 다시 열어 다시 본다.** 고친 것이 다른 곳을 깨뜨리는 일이 흔하다(번호표 위치를 옮기자 글자를 가린 경우 등).
3. 마지막에 전 장을 한 번 더 훑는다.
4. 장 수를 센다: "N/M장 확인". 일부만 다시 보고 전부 확인했다고 쓰지 않는다.

## 5. 최종 산출물이 다른 렌더러를 거칠 때

PDF, EPUB, 모바일 앱 화면처럼 최종 렌더러가 따로 있으면, 앱 안 브라우저 확인은 "원본 그림 확인"일 뿐이다. 그 렌더러에서 쪽 크기, 글자 크기, 글꼴 대체가 맞는지 별도로 확인하고, 하지 못했으면 "확인 안 함"으로 적는다.

## 6. 끝내기

```bash
bash ~/.claude/skills/lean-polish/scripts/serve.sh stop
```

작업 중 만든 미리보기 이미지·임시 파일은 번호 표(번호, 경로, 크기, 무엇인지)로 보고하고 정리한다.
