# AGENTS.md — Claude Code(AI) 설치 지시

이 저장소는 **Claude AI Kit**(강사의 범용 툴 셋: MCP·플러그인·스킬·커맨드·에이전트)입니다.

## 사용자가 "이 저장소를 설치해줘"라고 하면

아래를 순서대로 실행하세요:

1. 저장소가 로컬에 없으면 clone:
   ```bash
   git clone https://github.com/beyondworks/lean-class.git
   ```
   - private 저장소라 clone 이 인증 오류로 실패하면, 사용자에게 먼저 `gh auth login`(GitHub 로그인)을 안내하세요. 초대받은 계정으로 로그인돼 있어야 합니다.

2. 설치 스크립트 실행:
   ```bash
   bash lean-class/install.sh
   ```

3. 완료 후 사용자에게 안내:
   - Claude Code 재시작
   - 키가 필요한 MCP 설정은 `00-mcp/README.md` 참고 (수강생이 본인 키 입력)
   - OMC 셋업은 `05-omc/README.md` 참고

## install.sh 가 하는 일 (안전)
- 스킬/커맨드/에이전트를 `~/.claude/` 로 복사 (기존 동명 파일은 `.bak` 으로 백업, 덮어쓰지 않음)
- 플러그인 일괄 설치 + 키 불필요한 MCP 자동 등록 (`claude` CLI 있을 때)
- `rm -rf` 등 파괴적 명령 없음. 시크릿 미포함 — 키 필요한 MCP는 사용자가 직접 입력.

## 주의
- 이것은 **배포 패키지**입니다. `02-skills/` 등의 내용을 임의로 수정·재배포하지 마세요.
- 시크릿·환경변수·개인정보는 들어있지 않습니다. 사용자에게 키 입력을 요구하는 부분은 placeholder(`<YOUR_...>`)입니다.
