#!/usr/bin/env bash
# ==============================================================
#  셸 스니펫 연결 — 프로파일에 source 한 줄만 추가 (멱등)
#
#  사용법:  bash 08-shell/install-shell.sh
#
#  설계: 프로파일에 내용을 복사해 넣지 않고 source 한 줄만 넣는다.
#        그래야 패키지를 갱신하면 셸도 같이 갱신되고,
#        되돌릴 때 마커 블록만 지우면 된다.
# ==============================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BEGIN="# >>> lean-class >>>"
END="# <<< lean-class <<<"

# 스니펫을 홈으로 복사해 두고 그쪽을 source 한다.
# 패키지 폴더를 옮기거나 지워도 셸이 깨지지 않게 하려는 것.
SNIPPET="$HOME/.claude/lean-class.sh"

echo "── 셸 설정 ────────────────────────────────────"

mkdir -p "$HOME/.claude"
if ! cp "$SCRIPT_DIR/lean-class.sh" "$SNIPPET" 2>/dev/null; then
  echo "   스니펫 복사 실패 — 건너뜁니다."
  exit 0
fi

# ---------- 프로파일 판별 ----------
case "$(basename "${SHELL:-/bin/zsh}")" in
  zsh)  PROFILE="$HOME/.zshrc" ;;
  bash) PROFILE="$HOME/.bashrc"; [ -f "$HOME/.bash_profile" ] && PROFILE="$HOME/.bash_profile" ;;
  *)    echo "   지원하지 않는 셸: ${SHELL:-unknown} — 건너뜁니다."
        echo "   수동: 프로파일에 'source $SNIPPET' 추가"
        exit 0 ;;
esac

touch "$PROFILE"

# ---------- 이미 있으면 갱신 ----------
if grep -qF "$BEGIN" "$PROFILE" 2>/dev/null; then
  echo "   이미 연결됨: $PROFILE — 경로만 갱신합니다."
  python3 - "$PROFILE" "$SNIPPET" "$BEGIN" "$END" <<'PY'
import sys, re, pathlib
prof, snip, b, e = sys.argv[1:5]
p = pathlib.Path(prof)
new = f"{b}\n[ -f \"{snip}\" ] && source \"{snip}\"\n{e}"
txt = re.sub(re.escape(b) + r".*?" + re.escape(e), new, p.read_text(encoding='utf-8'), flags=re.S)
p.write_text(txt, encoding='utf-8')
PY
else
  cp "$PROFILE" "$PROFILE.bak-$(date +%Y%m%d-%H%M%S)"
  {
    echo ""
    echo "$BEGIN"
    echo "[ -f \"$SNIPPET\" ] && source \"$SNIPPET\""
    echo "$END"
  } >> "$PROFILE"
  echo "   연결 완료: $PROFILE (기존 파일은 .bak 으로 백업)"
fi

echo
echo "   적용: 새 터미널을 열거나  source $PROFILE"
echo "   해제: $PROFILE 에서 '$BEGIN' ~ '$END' 블록 삭제"
echo "   내용: cc alias(권한 스킵 — 경고 읽어보세요) + ~/.local/bin PATH"
echo "   수정: $SNIPPET  (패키지 폴더와 무관하게 홈에 복사됨)"
echo "──────────────────────────────────────────────"
exit 0
