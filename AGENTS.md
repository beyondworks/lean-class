# AGENTS.md — Claude Code(AI) 설치 지시

이 저장소는 **Claude AI Kit**입니다. 스킬·플러그인·MCP·커맨드·에이전트에 더해 **글로벌 규칙과 작업 하네스**까지 포함한 작업 환경 한 벌입니다.

## 사용자가 "이 저장소를 설치해줘"라고 하면

1. 저장소가 로컬에 없으면 clone:
   ```bash
   git clone https://github.com/beyondworks/lean-class.git
   ```
   private이라 인증 오류가 나면 `gh auth login`을 먼저 안내하세요.

2. **설치 전에 사용자에게 물어보세요.** 이 킷에는 사람 이름이 없고, 설치 시 오너가 정합니다:
   - 이름과 호칭 (에이전트가 부를 말)
   - 작업 루트 경로
   - 에이전트에 이름을 붙일지 (선택)

   답을 받았으면 `owner.conf`를 만들어 비대화형으로 돌리는 편이 확실합니다:
   ```bash
   cp lean-class/owner.example.conf lean-class/owner.conf
   # 받은 답으로 값을 채운 뒤
   bash lean-class/install.sh --answers lean-class/owner.conf
   ```
   사용자가 "알아서 해줘"라고 하면 `bash lean-class/install.sh --defaults`로 기본값 설치하고, 나중에 `~/.claude/CLAUDE.md`에서 바꿀 수 있다고 알려주세요.

3. 완료 후 안내:
   - **Claude Code 재시작** + **새 터미널** (셸 설정 적용)
   - 키가 필요한 MCP는 `00-mcp/README.md`
   - **`cc` alias 경고** — `--dangerously-skip-permissions`라 확인 프롬프트가 없습니다. 신뢰하는 저장소에서만 쓰라고 반드시 전하세요.

## install.sh가 하는 일 (안전)

- 스킬·커맨드·에이전트·규칙을 `~/.claude/`로 복사. **기존 파일은 `.bak-<타임스탬프>`로 백업**하고 덮어쓰지 않음
- 플러그인 일괄 설치 + 키 불필요한 MCP 등록 (`claude` CLI 있을 때)
- fablize 하네스를 원본 레포에서 받아와 `CLAUDE.md`에 블록 주입
- 셸 프로파일에 source 한 줄 추가 (마커로 감싸 제거 가능)
- `rm -rf` 등 파괴적 명령 없음. 어느 단계가 실패해도 나머지는 계속 진행

## 설치 순서를 바꾸지 마세요

`06-rules`(CLAUDE.md 생성) → `07-fablize`(그 뒤에 블록 append) 순서입니다. 거꾸로 하면 규칙 설치가 하네스 블록을 지웁니다. `install.sh`는 이 순서를 지키므로, 수동으로 단계를 재배열하지 마세요.

## 주의

- 이것은 **배포 패키지**입니다. `02-skills/` 등의 내용을 임의로 수정·재배포하지 마세요.
- 시크릿·개인정보가 들어 있지 않습니다. 키 자리는 전부 `<YOUR_...>` placeholder입니다.
- **패키지에 개인정보를 추가하지 마세요.** 커밋 전 반드시 `bash scripts/scan-personal.sh`를 돌리고, 통과(exit 0)해야 커밋합니다.
