# Claude AI Kit — 강사의 AI 작업 환경 패키지

강사가 Claude Code 에서 실제로 쓰는 **범용 툴 셋**(MCP·플러그인·스킬·커맨드·에이전트)을 한 번에 설치하는 패키지입니다. 시크릿·개인정보는 모두 제외했습니다.

---

## 설치 (수강생용)

### 가장 쉬운 방법 — Claude Code 에게 맡기기
Claude Code 에 아래처럼 말하면 자동 설치됩니다:

> `https://github.com/beyondworks/lean-class.git 이 저장소 설치해줘`

Claude 가 clone → `install.sh` 실행까지 알아서 합니다. (동작 지시는 `AGENTS.md` 에 정의돼 있음)

### 직접 실행
```bash
git clone https://github.com/beyondworks/lean-class.git
bash lean-class/install.sh
```

> **저장소가 private 인 경우**: clone 전에 GitHub 로그인이 필요합니다.
> ```bash
> gh auth login        # 초대받은 GitHub 계정으로 로그인
> ```
> 로그인 후 위 clone 명령을 실행하세요.

설치가 끝나면 **Claude Code 를 재시작**하세요.

---

## install.sh 가 하는 일

| 단계 | 내용 |
|---|---|
| 1 | `02-skills/` → `~/.claude/skills/` 복사 (기존 동명은 `.bak` 백업) |
| 2 | `03-commands/` → `~/.claude/commands/` |
| 3 | `04-agents/` → `~/.claude/agents/` |
| 4 | 플러그인 27개 일괄 설치 (`claude` CLI 있을 때) |
| 5 | 키 불필요한 MCP 자동 등록 + 키 필요한 MCP 안내 |

안전: 기존 파일은 덮어쓰지 않고 백업합니다. `rm -rf` 없음. 시크릿 미포함.

---

## 설치 후 추가 설정

- **MCP 키**: 일부 MCP(hyperbrowser·magic·testsprite·notion)는 본인 키가 필요합니다 → `00-mcp/README.md`
- **OMC(oh-my-claudecode)**: 멀티에이전트 오케스트레이션 → `05-omc/README.md`

---

## 폴더 구조

```
lean-class/
├── README.md              ← 지금 이 파일
├── AGENTS.md              ← Claude Code 자동 설치 지시
├── install.sh             ← 원샷 설치 스크립트
├── PACKAGE_MANIFEST.md    ← 전체 패키징 목록 표
├── 00-mcp/                ← MCP 설정 템플릿 + 가이드
├── 01-plugins/            ← 플러그인 설치 스크립트 + 가이드
├── 02-skills/             ← 스킬 111개 (사용설명서 + 구동 자산)
├── 03-commands/           ← 슬래시 커맨드 29개
├── 04-agents/             ← 전문 에이전트 22개
└── 05-omc/                ← oh-my-claudecode 안내
```

## 구성 요약

| 카테고리 | 개수 |
|---|---:|
| MCP 서버 | 18 |
| 플러그인 | 27 |
| 스킬 | 111 |
| 슬래시 커맨드 | 29 |
| 에이전트 | 22 |

전체 목록은 `PACKAGE_MANIFEST.md` 를 보세요.

## 안전·범위 고지
- API 키·토큰·DB 접속정보·개인 경로·이메일이 **하나도 없습니다.** MCP 키 자리는 모두 `<YOUR_...>` placeholder 입니다.
- 강사 노하우(`references/` 의 작업 사례·세션 기록)는 제외했습니다. 이 킷은 "강사가 쓰는 범용 툴 셋"이지 노하우 모음이 아닙니다.
- 일부 MCP·스킬은 로컬 설치/자체 서버에 의존합니다 — 각 README 의 "로컬 의존" 표기를 확인하세요.
