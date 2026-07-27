#!/usr/bin/env bash
# ==============================================================
#  fablize 하네스 부트스트랩
#
#  사용법:  bash 07-fablize/install-fablize.sh [global|local]
#           (기본 global — 모든 프로젝트에 적용)
#
#  왜 파일을 안 담고 받아오나:
#    fablize 는 제3자(fivetaku)의 저작물이다. 이 패키지에 파일을 복사해 넣으면
#    남의 저작물 재배포가 된다. 그래서 원본 레포에서 직접 받아온다.
#    받아온 뒤 실행되는 setup.sh 도 원저자 것을 그대로 쓴다.
#
#  안전: 실패해도 exit 0 — 상위 install.sh 전체를 멈추지 않는다.
#        setup.sh 가 CLAUDE.md 를 자체 백업한다(.fablize-bak.<ts>).
# ==============================================================
set -uo pipefail

SCOPE="${1:-global}"
FABLIZE_DIR="${FABLIZE_DIR:-$HOME/Code/fablize}"
PUBLIC_REPO="https://github.com/fivetaku/fablize.git"

echo "── fablize 하네스 ──────────────────────────────"

if ! command -v git >/dev/null 2>&1; then
  echo "   git 미설치 — 건너뜁니다."
  echo "   나중에: $PUBLIC_REPO 를 clone 후 setup/setup.sh $SCOPE"
  exit 0
fi

# ---------- 1) 소스 확보 (clone 또는 update) ----------
if [ -d "$FABLIZE_DIR/.git" ]; then
  echo "   기존 설치 발견 → 업데이트: $FABLIZE_DIR"
  git -C "$FABLIZE_DIR" pull --rebase --quiet 2>/dev/null \
    || echo "   업데이트 실패(로컬 변경 있음?) — 기존 버전으로 진행"
else
  echo "   내려받는 중: $PUBLIC_REPO"
  mkdir -p "$(dirname "$FABLIZE_DIR")"
  if ! git clone --depth 1 --quiet "$PUBLIC_REPO" "$FABLIZE_DIR" 2>/dev/null; then
    echo "   내려받기 실패 — 건너뜁니다 (네트워크 또는 접근권 문제)."
    echo "   수동 설치: git clone $PUBLIC_REPO ~/Code/fablize"
    echo "              bash ~/Code/fablize/setup/setup.sh $SCOPE"
    exit 0
  fi
fi

# ---------- 2) setup 실행 ----------
SETUP="$FABLIZE_DIR/setup/setup.sh"
if [ ! -f "$SETUP" ]; then
  echo "   setup.sh 없음 — 레포 구조가 바뀐 듯합니다. 건너뜁니다."
  echo "   확인: $FABLIZE_DIR"
  exit 0
fi

echo "   운영 블록 주입 (scope=$SCOPE)"
if bash "$SETUP" "$SCOPE" >/dev/null 2>&1; then
  echo "   완료 — CLAUDE.md 에 FABLIZE 블록이 들어갔습니다."
else
  echo "   주입 실패 — 수동 실행: bash $SETUP $SCOPE"
fi

echo
echo "   되돌리기: bash $FABLIZE_DIR/setup/uninstall.sh $SCOPE"
echo "──────────────────────────────────────────────"
exit 0
