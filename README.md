# Claude AI Kit — 강사의 AI 작업 환경 패키지

이 폴더 하나로 강사가 Claude Code 에서 **실제로 쓰는 MCP · 플러그인 · 스킬 · 커맨드 · 에이전트**를 본인 환경에 재현할 수 있습니다. 최근 3개월간 유지해온 환경을 통째로 미러링하되, **개인·회사 전용 항목과 모든 시크릿·개인정보는 제거**했습니다.

> 🔒 **안전**: 이 킷에는 API 키·토큰·DB 접속정보·개인 경로·이메일이 **하나도 없습니다.** MCP 키 자리는 모두 `<YOUR_...>` placeholder 입니다. 본인 키를 직접 넣어 쓰세요.

## 폴더 구조

```
claude-ai-kit/
├── README.md              ← 지금 이 파일
├── PACKAGE_MANIFEST.md    ← 전체 패키징 목록 표 (무엇이 들어있나)
├── 00-mcp/                ← MCP 서버 설정 템플릿 + 설치 가이드
├── 01-plugins/            ← 플러그인 일괄 설치 스크립트 + 가이드
├── 02-skills/             ← 독립 스킬 108개 (복사형)
├── 03-commands/           ← 슬래시 커맨드 27개
├── 04-agents/             ← 전문 에이전트 22개
└── 05-omc/                ← oh-my-claudecode (핵심 오케스트레이션 레이어) ★
```

## 빠른 시작 (순서대로)

### 1단계 — 플러그인 설치 (가장 먼저)
```bash
cd 01-plugins && bash install-plugins.sh
```
플러그인을 설치하면 **그 플러그인의 번들 스킬·에이전트·MCP·커맨드가 자동으로 따라옵니다.** (`superpowers`, `oh-my-claudecode`, `vercel`, `figma` 등)

### 2단계 — MCP 연결
`00-mcp/README.md` 를 따라 `mcp.template.json` 에 본인 키를 넣고 `.mcp.json` 으로 병합. 키 없이 바로 되는 MCP(context7, playwright, sequential-thinking 등)부터 시작하세요.

### 3단계 — 독립 스킬·커맨드·에이전트 배치
플러그인에 속하지 않은 자산입니다. 본인 환경에 복사하세요.
```bash
# 글로벌(모든 프로젝트)에서 쓰려면:
cp -R 02-skills/*   ~/.claude/skills/
cp -R 03-commands/* ~/.claude/commands/
cp -R 04-agents/*   ~/.claude/agents/
# 또는 특정 프로젝트에서만: 프로젝트의 .claude/ 하위로 복사
```
Claude Code 재시작 후 `/`(커맨드)·Skill 호출·에이전트 호출로 사용.

### 4단계 — OMC 설정 (강력 추천)
`05-omc/README.md` 참고. `setup omc` 또는 `/oh-my-claudecode:omc-setup`.

## 사용법 요약

| 자산 | 호출 방법 |
|------|-----------|
| 스킬 | 트리거 키워드 입력 또는 Skill 도구로 호출 (각 `SKILL.md` 의 description 참고) |
| 커맨드 | Claude Code 에서 `/커맨드명` |
| 에이전트 | "○○ 에이전트로 ~해줘" 또는 Task/Agent 호출 |
| MCP | 설정 후 자동 노출 (`/mcp` 로 상태 확인) |

## 알아두기
- 스킬·커맨드·에이전트 본문은 강사 작업 사례의 **개인 식별정보를 일반 예시로 치환**했습니다. 일부 문장이 일반화되어 있을 수 있습니다.
- 강사 노하우(`references/` 의 작업 사례·세션 기록·기법 노트)는 **전부 제거**했습니다 — 이 킷은 "강사가 쓰는 범용 툴 셋"이지 노하우 모음이 아닙니다. 각 스킬의 사용설명서(`SKILL.md`)와 구동 자산(`data`/`scripts`)은 유지됩니다.
- 무엇을 넣고 뺐는지는 **`PACKAGE_MANIFEST.md`** 에 모두 투명하게 기록돼 있습니다.
- 일부 MCP·스킬은 강사의 로컬 인프라(로컬 빌드, 자체 서버)에 의존합니다 — 각 README 의 "로컬 의존" 표기를 확인하세요.
