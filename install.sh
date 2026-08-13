#!/usr/bin/env bash
# ==============================================================
#  Claude AI Kit 설치
#
#  사용법:
#    bash install.sh                       # 대화형 (오너 정보를 물어봄)
#    bash install.sh --answers owner.conf  # 비대화형 (파일에서 읽음)
#    bash install.sh --defaults            # 비대화형 (전부 기본값)
#
#  설치 대상:
#    스킬 · 커맨드 · 에이전트 · 글로벌 규칙 · 플러그인 · MCP · 하네스 · 셸
#
#  안전:
#    · rm -rf 없음. 기존 파일은 .bak-<타임스탬프> 로 백업 후 교체.
#    · 시크릿 미포함. 키가 필요한 MCP 는 안내만 하고 값은 직접 넣게 함.
#    · 어느 단계가 실패해도 나머지는 계속 진행.
# ==============================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
TS="$(date +%Y%m%d-%H%M%S)"
MODE="interactive"; ANSWERS=""

while [ $# -gt 0 ]; do
  case "$1" in
    --answers) MODE="file"; ANSWERS="${2:-}"; shift 2 ;;
    --defaults) MODE="defaults"; shift ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    *) echo "알 수 없는 옵션: $1"; exit 1 ;;
  esac
done

echo "=================================================="
echo "  Claude AI Kit 설치"
echo "  소스 : $SCRIPT_DIR"
echo "  대상 : $CLAUDE_DIR"
echo "=================================================="

# ---------- 0) 오너 정보 ----------
# 이 패키지에는 사람 이름이 들어 있지 않다. 여기서 오너가 정한다.
OWNER_NAME="오너"; OWNER_TITLE="오너님"; OWNER_HANDLE=""; OWNER_EMAIL=""; GITHUB_ORG=""
PROJECTS_ROOT="$HOME/projects"; CODE_ROOT="$HOME/Code"; VAULT_ROOT="$HOME/Documents/Vault"
MODERATOR="조율자"; AGENT_MODERATOR="조율"; AGENT_DEV="개발"; AGENT_CORE="코어개발"
AGENT_DESIGN="디자인"; AGENT_MARKETING="마케팅"; AGENT_CONTENT="콘텐츠"
AGENT_EDU="교육"; AGENT_SALES="영업재무"; AGENT_PLANNING="기획"; AGENT_RESEARCH="리서치"

case "$MODE" in
  file)
    [ -f "$ANSWERS" ] || { echo "answers 파일 없음: $ANSWERS"; exit 1; }
    # KEY=VALUE 만 취한다 (임의 코드 실행 방지 — source 하지 않음)
    while IFS='=' read -r k v; do
      k="${k%%#*}"; k="$(echo "$k" | tr -d '[:space:]')"
      [ -z "$k" ] && continue
      v="${v%%#*}"; v="$(echo "$v" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
      [ -z "$v" ] && continue
      v="${v//\$HOME/$HOME}"
      case "$k" in
        OWNER_NAME|OWNER_TITLE|OWNER_HANDLE|OWNER_EMAIL|GITHUB_ORG|PROJECTS_ROOT|\
        CODE_ROOT|VAULT_ROOT|MODERATOR|AGENT_*) printf -v "$k" '%s' "$v" ;;
      esac
    done < "$ANSWERS"
    echo "  오너 정보: $ANSWERS 에서 읽음"
    ;;
  interactive)
    echo ""
    echo "  이 킷에는 사람 이름이 들어 있지 않습니다. 아래를 정해 주세요."
    echo "  (엔터만 치면 괄호 안 기본값이 들어갑니다. 나중에 바꿔도 됩니다.)"
    echo ""
    read -r -p "  이름 (오너): " _t;            [ -n "$_t" ] && OWNER_NAME="$_t"
    read -r -p "  에이전트가 부를 호칭 (${OWNER_NAME}님): " _t
    OWNER_TITLE="${_t:-${OWNER_NAME}님}"
    read -r -p "  GitHub 계정 (건너뛰려면 엔터): " _t; [ -n "$_t" ] && OWNER_HANDLE="$_t"
    read -r -p "  GitHub 조직 (${OWNER_HANDLE:-없음}): " _t
    GITHUB_ORG="${_t:-$OWNER_HANDLE}"
    read -r -p "  작업 루트 ($PROJECTS_ROOT): " _t; [ -n "$_t" ] && PROJECTS_ROOT="$_t"
    read -r -p "  지식 볼트 경로 (안 쓰면 엔터): " _t; [ -n "$_t" ] && VAULT_ROOT="$_t"
    echo ""
    read -r -p "  에이전트에 이름을 붙일까요? (y/N): " _t
    if [[ "$_t" =~ ^[Yy] ]]; then
      read -r -p "    조율 담당 ($AGENT_MODERATOR): " _x; [ -n "$_x" ] && { AGENT_MODERATOR="$_x"; MODERATOR="$_x"; }
      read -r -p "    개발 ($AGENT_DEV): "        _x; [ -n "$_x" ] && AGENT_DEV="$_x"
      read -r -p "    디자인 ($AGENT_DESIGN): "   _x; [ -n "$_x" ] && AGENT_DESIGN="$_x"
      echo "    (나머지는 기본 직무명 — ~/.claude/CLAUDE.md 에서 언제든 수정)"
    fi
    ;;
  defaults) echo "  오너 정보: 전부 기본값" ;;
esac

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/commands" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/rules"

backup() { [ -e "$1" ] && mv "$1" "${1}.bak-${TS}"; }

# ---------- 1) 스킬 ----------
echo ""
echo "[1/7] 스킬"
sc=0; bk=0
for d in "$SCRIPT_DIR"/02-skills/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"; dest="$CLAUDE_DIR/skills/$name"
  [ -e "$dest" ] && { backup "$dest"; bk=$((bk+1)); }
  cp -R "$d" "$dest"; sc=$((sc+1))
done
echo "      설치 ${sc}개 / 기존 백업 ${bk}개"

# ---------- 2) 커맨드 · 에이전트 ----------
echo "[2/7] 커맨드 · 에이전트"
cp -R "$SCRIPT_DIR"/03-commands/. "$CLAUDE_DIR/commands/" 2>/dev/null
cp -R "$SCRIPT_DIR"/04-agents/.   "$CLAUDE_DIR/agents/"   2>/dev/null
echo "      완료"

# ---------- 3) 글로벌 규칙 (치환) ----------
# fablize 보다 먼저 와야 한다. fablize 가 CLAUDE.md 끝에 블록을 덧붙이므로,
# 순서가 뒤집히면 여기서 덮어써서 그 블록이 날아간다.
echo "[3/7] 글로벌 규칙 (오너 정보로 치환)"
if [ -d "$SCRIPT_DIR/06-rules" ]; then
  TMP="$(mktemp -d)"
  cp "$SCRIPT_DIR/06-rules/CLAUDE.template.md" "$TMP/CLAUDE.md"
  cp "$SCRIPT_DIR"/06-rules/rules/*.md "$TMP/" 2>/dev/null

  OWNER_NAME="$OWNER_NAME" OWNER_TITLE="$OWNER_TITLE" OWNER_HANDLE="$OWNER_HANDLE" \
  OWNER_EMAIL="$OWNER_EMAIL" GITHUB_ORG="$GITHUB_ORG" PROJECTS_ROOT="$PROJECTS_ROOT" \
  CODE_ROOT="$CODE_ROOT" VAULT_ROOT="$VAULT_ROOT" MODERATOR="$MODERATOR" \
  AGENT_MODERATOR="$AGENT_MODERATOR" AGENT_DEV="$AGENT_DEV" AGENT_CORE="$AGENT_CORE" \
  AGENT_DESIGN="$AGENT_DESIGN" AGENT_MARKETING="$AGENT_MARKETING" \
  AGENT_CONTENT="$AGENT_CONTENT" AGENT_EDU="$AGENT_EDU" AGENT_SALES="$AGENT_SALES" \
  AGENT_PLANNING="$AGENT_PLANNING" AGENT_RESEARCH="$AGENT_RESEARCH" \
  FABLIZE_DIR="${FABLIZE_DIR:-$HOME/Code/fablize}" \
  python3 - "$TMP" <<'PY'
import os, re, sys, pathlib
keys = ['OWNER_NAME','OWNER_TITLE','OWNER_HANDLE','OWNER_EMAIL','GITHUB_ORG',
        'PROJECTS_ROOT','CODE_ROOT','VAULT_ROOT','MODERATOR','AGENT_MODERATOR',
        'AGENT_DEV','AGENT_CORE','AGENT_DESIGN','AGENT_MARKETING','AGENT_CONTENT',
        'AGENT_EDU','AGENT_SALES','AGENT_PLANNING','AGENT_RESEARCH','FABLIZE_DIR']
vals = {k: os.environ.get(k, '') for k in keys}
for p in pathlib.Path(sys.argv[1]).glob('*.md'):
    t = p.read_text(encoding='utf-8')
    for k, v in vals.items():
        t = t.replace('{{%s}}' % k, v)
    # 값을 안 준 변수는 흔적을 남기지 않는다
    t = re.sub(r'\{\{[A-Z_]+\}\}', '', t)
    p.write_text(t, encoding='utf-8')
PY

  backup "$CLAUDE_DIR/CLAUDE.md"
  mv "$TMP/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
  n=0
  for f in "$TMP"/*.md; do
    [ -f "$f" ] || continue
    backup "$CLAUDE_DIR/rules/$(basename "$f")"
    mv "$f" "$CLAUDE_DIR/rules/"; n=$((n+1))
  done
  rm -rf "$TMP"
  echo "      CLAUDE.md + 규칙 ${n}개 (호칭: ${OWNER_TITLE})"
  echo "      선택 규칙은 06-rules/rules/optional/ — 필요할 때만 직접 복사"
else
  echo "      06-rules 없음 — 건너뜀"
fi

# ---------- 4) 플러그인 ----------
echo "[4/7] 플러그인"
if command -v claude >/dev/null 2>&1; then
  bash "$SCRIPT_DIR/01-plugins/install-plugins.sh" >/dev/null 2>&1 \
    && echo "      완료" \
    || echo "      일부 실패 — /plugin 으로 확인하세요"
else
  echo "      claude CLI 미발견 → 나중에 01-plugins/install-plugins.sh 실행"
fi

# ---------- 5) MCP ----------
echo "[5/7] MCP (키 불필요한 것만 자동)"
if command -v claude >/dev/null 2>&1; then
  claude mcp add context7            -- npx -y @upstash/context7-mcp@latest >/dev/null 2>&1
  claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking >/dev/null 2>&1
  claude mcp add playwright          -- npx @playwright/mcp@latest >/dev/null 2>&1
  claude mcp add shadcn-ui           -- npx -y @jpisnice/shadcn-ui-mcp-server >/dev/null 2>&1
  claude mcp add ui-expert           -- npx -y @johndoe20012/ui-expert-mcp >/dev/null 2>&1
  echo "      등록 완료 — 키 필요한 것은 00-mcp/README.md 참고"
else
  echo "      claude CLI 미발견 → 00-mcp/README.md 참고"
fi

# ---------- 6) 하네스 ----------
echo "[6/7] 작업 방식 하네스 (fablize)"
bash "$SCRIPT_DIR/07-fablize/install-fablize.sh" global 2>&1 | sed 's/^/      /'

# ---------- 7) 셸 ----------
echo "[7/7] 셸 설정"
bash "$SCRIPT_DIR/08-shell/install-shell.sh" 2>&1 | sed 's/^/      /'

echo ""
echo "=================================================="
echo "  설치 완료"
echo ""
echo "  1. Claude Code 를 재시작하세요."
echo "  2. 새 터미널을 열거나: source ~/.zshrc"
echo "  3. 호칭·에이전트 이름 수정: ~/.claude/CLAUDE.md"
echo "  4. 키가 필요한 MCP: 00-mcp/README.md"
echo ""
echo "  기존 파일은 .bak-${TS} 로 백업했습니다."
echo "=================================================="
