# 🔒 보안 절대 규칙 (최우선)

**시크릿 평문 기입 금지** — 핸드오버/세션요약/README/CLAUDE.md/MEMORY.md/커밋메시지/코드주석/PR/이슈/채팅/메일 **어디에도** API 키·토큰·DB 접속문자열·비밀번호·OAuth secret·JWT secret·webhook secret 평문 절대 금지.

- 대신: **환경변수 이름 + 저장 위치**만 기록 (예: `DATABASE_URL (Vercel / Production)`)
- 접두사 노출 최소화 (`re_***`, `npg_***` 형태만 허용)
- `.env*` 파일은 읽어서 출력 금지, 편집 시에도 값 복붙 금지
- `git add .` / `git add -A` 금지 — 파일 명시적 추가
- 커밋 전 `git diff --cached`에서 `password|secret|key|token|api_key|DATABASE_URL` 검증
- 상세 규칙 및 유출 시 대응: `~/.claude/rules/security.md`

# 🎯 정합성 절대 규칙 (보안 다음 최우선)

**기획 = 설계 = 구현은 항상 같은 목적지.** 텍스트로 합의한 목적이 코드에서 변질되면 그 방향으로 더 가지 말고 즉시 멈춰 재정렬한다.

- 작업 시작 시 **North Star(사용자 결과 한 문장)**를 최상단에 박는다
- 표류 감지 시 **한 걸음도 더 가지 말고 정지 → 재정렬** (잘못된 방향 누적 금지)
- "완료" 전 완성물 ↔ 기획 텍스트 **역대조**. 빌드 통과 ≠ 목적 달성

# 🌐 브라우저 절대 규칙 (전역)

**브라우저를 띄우거나 웹 자동화·미리보기·검증 시 항상 Aside를 쓴다.** Playwright(격리 Chromium)·기타 격리 브라우저 도구(`mcp__playwright__*` 등) 기본 사용 금지. Aside = 사용자 실제 로그인 세션·확장·현재 탭 그대로의 크롬 베이스 브라우저.

- 미리보기·시각검증·스크린샷 → `aside repl "<JS>"` (한 호출에 openTab+screenshot+저장; `./artifacts/`에 저장 후 Read)
- 로그인 계정·앱 가로지르는 작업 → `aside exec "<프롬프트>"`
- 프라이버시: 요청받은 작업에만 사용, 무관한 탭/계정 금지. Aside 불가 시에만 대체하고 사용자에게 알림.
- 상세: `~/.claude/rules/browser.md` · 워크플로 `aside-browser` 스킬.

## Workflow Orchestration

### 1. Subagent Strategy

- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution

---

### 2. Self-Improvement Loop

- After ANY correction from the user: append one line to `~/.claude/lessons.md` (global, cross-domain) or the project's MEMORY.md Lessons section — per `~/.claude/rules/learning-loop.md`
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review `~/.claude/lessons.md` and the project MEMORY.md at session start

---

### 3. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

---

### 4. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests -- then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

<aside>

### Task Management

1. **Plan First:** Track the plan with TodoWrite, North Star pinned at top
2. **Track Progress:** Mark items complete as you go
3. **Explain Changes:** High-level summary at each step
4. **Document Results:** Write a retro summary and record it in the project's MEMORY.md
5. **Capture Lessons:** Append to `~/.claude/lessons.md` / MEMORY.md Lessons after corrections
</aside>

<aside>

### Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing bugs.
</aside>

