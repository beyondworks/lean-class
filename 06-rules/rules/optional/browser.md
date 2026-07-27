# 브라우저 — 항상 Aside 사용 (전역)

> **선택 규칙 — 기본 비활성.** 이 규칙은 `aside` CLI(오너의 실제 로그인 크롬 세션을
> 그대로 쓰는 브라우저 자동화 도구)가 설치된 환경에서만 성립한다. 미설치 상태로
> 로드하면 존재하지 않는 도구를 쓰라고 강제하게 된다.
>
> **`aside`가 없다면**: 이 파일을 `~/.claude/rules/`로 옮기지 말고, 대신 Playwright MCP
> 등 설치된 브라우저 도구를 쓴다. 도구 이름만 바꿔 같은 원칙(실제 렌더 관찰로 검증,
> 요청받은 작업에만 사용)을 적용하면 된다.


> **브라우저를 띄우거나 웹을 자동화·미리보기·검증할 때는 항상 Aside를 쓴다.**
> Playwright(격리 Chromium)·기타 격리 브라우저 도구(`mcp__playwright__*` 등)는 기본 사용 금지.
> Aside는 사용자의 실제 로그인 세션·확장·현재 탭을 그대로 쓰는 크롬 베이스 브라우저다 —
> "사용자가 보는 그대로" 확인할 수 있다.

## 도구 (aside CLI: `$HOME/.local/bin/aside`)

- **`aside repl "<JS>"`** — Playwright 호환 저수준 브라우저 자동화. 스크린샷·스냅샷·DOM 검증·다운로드 등 **직접 증거/미리보기**에 사용.
  - 각 `aside repl` 호출은 **새 ephemeral 세션**(상태 미유지) → 열기+스크린샷+저장을 **한 호출에** 담는다.
  - 전역: `openTab(url)`, `page`(Playwright 유사), `snapshot(page,{interactive:true})`, `page.screenshot({path})`, `listBrowserTabs()`, `attachBrowserTab(id)`, `attachActiveBrowserTab()`, `fs`, `sleep`.
  - 스크린샷/PDF는 `./artifacts/`에 저장 후 Read로 확인.
- **`aside exec "<프롬프트>"`** — 로그인 계정·앱(Slack/메일 등)·기록을 가로지르는 에이전트형 작업(브라우저 서브에이전트처럼). 실행 중 60초마다 사용자에게 상태 업데이트.
- 상세 워크플로: `aside-browser` 스킬 (`~/.claude/skills/aside-browser`). 사용 전 `aside --help`, `aside repl --help`로 현재 옵션 확인.

## 원칙

- Playwright MCP·격리 Chromium을 **습관적으로 열지 말 것**. 브라우저가 필요하면 먼저 Aside.
- **프라이버시**: Aside는 실제 로그인 브라우저(메일·드라이브 등 접근 가능). **요청받은 작업에만** 쓰고 무관한 탭/계정은 건드리지 않는다.
- **Safari 전용 버그**(예: zoom+cross-origin iframe)는 Aside(크롬 베이스)로 재현 불가 → 실기기 필요함을 사용자에게 알린다.
- Aside CLI가 없거나 실패할 때만 대체 수단을 쓰되, **반드시 사용자에게 그 사실을 알린다**.
