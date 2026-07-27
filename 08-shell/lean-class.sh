# ==============================================================
#  lean-class 셸 스니펫
#  셸 프로파일(.zshrc / .bashrc)에서 source 됩니다.
#  install-shell.sh 가 자동으로 연결합니다.
# ==============================================================

# ---------- PATH: 사용자 설치 CLI ----------
# uv tool / pipx / 로컬 스크립트가 설치되는 곳. 없으면 CLI 도구가 안 잡힙니다.
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac

# npm 전역 prefix 를 홈으로 바꿔 쓰는 경우(sudo 없이 -g 설치)
if [ -d "$HOME/.npm-global/bin" ]; then
  case ":$PATH:" in
    *":$HOME/.npm-global/bin:"*) ;;
    *) export PATH="$HOME/.npm-global/bin:$PATH" ;;
  esac
fi

# ---------- Claude Code ----------
# cc — 권한 확인 프롬프트 없이 실행.
#
#   ⚠️  경고: 파일 쓰기·삭제·셸 실행 전에 묻지 않습니다.
#      · 본인이 신뢰하는 저장소에서만 쓰세요.
#      · 남의 코드, 방금 clone 한 저장소, 출처 불명 파일이 섞인 폴더에서는
#        그냥 `claude` 로 실행해 확인 프롬프트를 받으세요.
#      · 이 alias 가 부담스러우면 아래 줄을 지우면 됩니다. 나머지는 그대로 동작합니다.
alias cc='claude --dangerously-skip-permissions'
