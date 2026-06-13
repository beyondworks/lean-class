#!/usr/bin/env bash
# ==============================================================
#  Claude AI Kit 설치 스크립트
#  사용법:
#    git clone https://github.com/beyondworks/lean-class.git
#    bash lean-class/install.sh
#
#  하는 일:
#    - 스킬/커맨드/에이전트를 ~/.claude/ 로 복사 (기존 동명은 .bak 백업)
#    - 플러그인 일괄 설치 (claude CLI 있을 때)
#    - 키 불필요한 MCP 자동 등록 (claude CLI 있을 때)
#    - 키 필요한 MCP 는 안내만 (수강생이 본인 키 입력)
#  안전: rm -rf 없음. 기존 파일은 덮어쓰지 않고 .bak 으로 백업.
# ==============================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
TS="$(date +%Y%m%d-%H%M%S)"

echo "=================================================="
echo "  Claude AI Kit 설치"
echo "  소스 : $SCRIPT_DIR"
echo "  대상 : $CLAUDE_DIR"
echo "=================================================="

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/commands" "$CLAUDE_DIR/agents"

# ---------- 1) 스킬 ----------
echo ""
echo "[1/5] 스킬 설치 (02-skills -> ~/.claude/skills)"
sc=0; bk=0
for d in "$SCRIPT_DIR"/02-skills/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  dest="$CLAUDE_DIR/skills/$name"
  if [ -e "$dest" ]; then mv "$dest" "${dest}.bak-${TS}"; bk=$((bk+1)); fi
  cp -R "$d" "$dest"
  sc=$((sc+1))
done
echo "      설치 ${sc}개 / 기존 백업 ${bk}개"

# ---------- 2) 커맨드 ----------
echo "[2/5] 커맨드 설치 (03-commands -> ~/.claude/commands)"
cp -R "$SCRIPT_DIR"/03-commands/. "$CLAUDE_DIR/commands/" 2>/dev/null
echo "      완료"

# ---------- 3) 에이전트 ----------
echo "[3/5] 에이전트 설치 (04-agents -> ~/.claude/agents)"
cp -R "$SCRIPT_DIR"/04-agents/. "$CLAUDE_DIR/agents/" 2>/dev/null
echo "      완료"

# ---------- 4) 플러그인 ----------
echo "[4/5] 플러그인 설치"
if command -v claude >/dev/null 2>&1; then
  bash "$SCRIPT_DIR/01-plugins/install-plugins.sh" || echo "      일부 플러그인 실패 — /plugin 으로 수동 확인"
else
  echo "      claude CLI 미발견 -> 01-plugins/install-plugins.sh 를 나중에 실행하세요"
fi

# ---------- 5) MCP (키 불필요한 것만 자동) ----------
echo "[5/5] MCP 등록 (키 불필요한 것)"
if command -v claude >/dev/null 2>&1; then
  claude mcp add context7            -- npx -y @upstash/context7-mcp@latest 2>/dev/null || true
  claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking 2>/dev/null || true
  claude mcp add playwright          -- npx @playwright/mcp@latest 2>/dev/null || true
  claude mcp add shadcn-ui           -- npx -y @jpisnice/shadcn-ui-mcp-server 2>/dev/null || true
  claude mcp add ui-expert           -- npx -y @johndoe20012/ui-expert-mcp 2>/dev/null || true
  echo "      키 불필요 MCP 등록 완료"
  echo "      키 필요 MCP(hyperbrowser/magic/testsprite/notion)는 00-mcp/README.md 참고"
else
  echo "      claude CLI 미발견 -> 00-mcp/README.md 참고"
fi

echo ""
echo "=================================================="
echo "  설치 완료"
echo "  - Claude Code 를 재시작하세요."
echo "  - 기존 동명 스킬은 .bak-${TS} 로 백업했습니다."
echo "  - MCP 키 설정: 00-mcp/README.md"
echo "  - OMC 셋업: 05-omc/README.md"
echo "=================================================="
