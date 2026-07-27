# 06-rules — 글로벌 운영 규칙

Claude Code가 **모든 프로젝트에서 항상 지키는 규칙** 묶음입니다. 스킬·플러그인이 "무엇을 할 수 있나"라면, 이쪽은 "어떻게 일하나"입니다.

설치되면 이렇게 놓입니다.

```
~/.claude/CLAUDE.md      ← CLAUDE.template.md (치환 후)
~/.claude/rules/*.md     ← rules/ (12개)
```

`CLAUDE.md`가 `rules/`를 참조하는 구조라, 규칙 하나를 고칠 때 본체를 건드리지 않습니다.

---

## 담긴 규칙 (12)

| 파일 | 내용 |
|---|---|
| `security.md` | **시크릿 평문 금지** — 문서·커밋·로그 어디에도. 환경변수는 이름·위치만 |
| `alignment.md` | 기획=설계=구현 정합성. North Star 고정, 표류 감지 시 즉시 정지 |
| `principles.md` | 정직성·근본원인·추측 금지·YAGNI. 확신도 표기 |
| `communication.md` | 열린 선택형 질문 금지(판단 후 승인만 받기), 자가 인증 배지 금지 |
| `workflow.md` | 세션 시작·종료 절차, UI 변경 검증 플로우, 계획 우선 기준 |
| `learning-loop.md` | 교정받을 때마다 lessons에 한 줄 축적 → 같은 실수 반복 방지 |
| `intent-bridge.md` | 자연어 요청 → 내부 스펙 변환, Metric Lock |
| `git.md` | 브랜치·커밋 규칙, **레포 경계**(오너가 채울 표) |
| `deployment.md` | 배포 후 실제 응답 검증 필수 |
| `mcp.md` · `macos.md` | 도구·OS 함정 모음 |
| `emil-skills.md` | UI 애니메이션 스킬 사용 전 가이드 로드 |

### 선택 규칙 (`rules/optional/`)

특정 도구가 있어야만 성립하는 규칙입니다. **기본 설치에서 빠집니다.**

- `browser.md` — `aside` CLI(실제 로그인 크롬 세션 자동화) 전용. 없으면 Playwright MCP 등으로 대체하고 이 파일은 두지 마세요.

### 배포에서 뺀 것

- 개인 ERP 연동 규칙 · 개인 모델 비교 로그 규칙 — 원 소유자 환경 전용이라 제외했습니다.

---

## 치환 변수 — 오너가 정하는 값

이 패키지에는 **어떤 사람 이름도 들어 있지 않습니다.** 설치할 때 `install.sh`가 물어보고 채웁니다.

| 변수 | 뜻 | 예 |
|---|---|---|
| `{{OWNER_NAME}}` | 오너 이름 | `홍길동` |
| `{{OWNER_TITLE}}` | 호칭 (에이전트가 부를 말) | `길동님`, `대표님` |
| `{{OWNER_HANDLE}}` | GitHub 계정 | `gildong` |
| `{{OWNER_EMAIL}}` | 이메일 | |
| `{{GITHUB_ORG}}` | GitHub 조직 | `my-org` |
| `{{PROJECTS_ROOT}}` | 작업 루트 | `~/projects` |
| `{{CODE_ROOT}}` | 도구·엔진 루트 | `~/Code` |
| `{{VAULT_ROOT}}` | 지식 볼트(옵시디언 등) | `~/Documents/Vault` |
| `{{MODERATOR}}` | 조율자 역할 이름 | 오너가 정함 |
| `{{AGENT_*}}` | 직무별 에이전트 이름 | `AGENT_DEV`·`AGENT_DESIGN` 등 |

에이전트 이름은 **안 정해도 됩니다.** 비워두면 설치기가 직무명(`개발`·`디자인`)을 그대로 넣습니다. 나중에 `~/.claude/CLAUDE.md`에서 바꾸면 됩니다.

---

## 수동 설치

```bash
cp 06-rules/CLAUDE.template.md ~/.claude/CLAUDE.md   # 치환 후
mkdir -p ~/.claude/rules && cp 06-rules/rules/*.md ~/.claude/rules/
```

기존 파일이 있으면 `install.sh`가 `.bak-<타임스탬프>`로 백업합니다. 덮어쓰지 않습니다.

## 다시 뽑기 (원 소유자용)

로컬 규칙을 고친 뒤 패키지에 반영할 때:

```bash
bash scripts/build-rules.sh && bash scripts/scan-personal.sh 06-rules
```

`~/.claude/`에서 읽어 개인정보를 치환하고 다시 씁니다. 스캐너가 통과해야 커밋할 수 있습니다.
