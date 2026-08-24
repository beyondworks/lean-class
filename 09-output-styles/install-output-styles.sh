#!/usr/bin/env bash
# ==============================================================
#  09-output-styles — 한국어 출력 스타일 부트스트랩
#
#  사용법:  bash 09-output-styles/install-output-styles.sh
#
#  왜 파일을 안 담고 받아오나:
#    fluent-korean 은 제3자(snflkd, MIT)의 저작물이다. 07-fablize 와 같은 이유로
#    파일을 복사해 넣지 않고 원본 레포에서 직접 받아온다.
#
#  하는 일:
#    1) snflkd/fluent-korean 을 받아 output-style md 2종을 ~/.claude/output-styles/ 에 둔다
#    2) 이 킷의 운용 조항 2개를 말미에 덧붙인다 (원저자 README 가 제공하는 블록)
#    3) settings.json 의 outputStyle 기본값을 fluent-korean 으로 설정
#
#  안전: 실패해도 exit 0 — 상위 install.sh 를 멈추지 않는다. settings.json 은 백업한다.
# ==============================================================
set -uo pipefail

SRC_DIR="${FLUENT_KOREAN_DIR:-$HOME/Code/fluent-korean}"
REPO="https://github.com/snflkd/fluent-korean.git"
DEST="$HOME/.claude/output-styles"

echo "── 한국어 출력 스타일 ──────────────────────────"

if ! command -v git >/dev/null 2>&1; then
  echo "   git 미설치 — 건너뜁니다. 나중에: $REPO"
  exit 0
fi

if [ -d "$SRC_DIR/.git" ]; then
  git -C "$SRC_DIR" pull --ff-only -q 2>/dev/null || true
else
  git clone -q --depth 1 "$REPO" "$SRC_DIR" 2>/dev/null || {
    echo "   내려받기 실패 — 건너뜁니다."; exit 0; }
fi

STYLES="$SRC_DIR/plugins/fluent-korean/output-styles"
[ -d "$STYLES" ] || { echo "   원본 구조가 바뀐 듯합니다 — 건너뜁니다."; exit 0; }

mkdir -p "$DEST"
cp "$STYLES/fluent-korean.md" "$STYLES/fluent-korean-not-coding.md" "$DEST/" 2>/dev/null || {
  echo "   복사 실패 — 건너뜁니다."; exit 0; }

# 이 킷의 운용 조항 — 원저자 README 가 '세부 동작' 블록으로 제공하는 문장이다.
#  · 1행: 화법·대본처럼 전용 지침이 있는 산출물에서 스타일이 충돌하지 않게 한다
#  · 2행: 저빈도 어휘 남용을 막는다
for f in "$DEST/fluent-korean.md" "$DEST/fluent-korean-not-coding.md"; do
  grep -q '구체적인 지침이 따로 존재하는 산출물' "$f" 2>/dev/null && continue
  cat >> "$f" <<'ADD'

- 구체적인 지침이 따로 존재하는 산출물 유형에는 이 지침을 적용하지 않습니다. 적용 여부가 애매하다면 사용자에게 확인합니다.
- 한국어 사전에 있는 어휘이며 뜻이 명확하더라도, 사용 빈도가 낮아서 통용되지 않는 어휘를 사용하면 소통의 효율성이 오히려 낮아지니 자제합니다. 대신 의미가 명확하며 실제로 통용되는 어휘를 우선적으로 선택합니다.
ADD
done

python3 - <<'PY' 2>/dev/null || echo "   기본값 설정 건너뜀(수동: /config → output-style)"
import json, pathlib, time
p = pathlib.Path.home()/".claude/settings.json"
d = json.loads(p.read_text()) if p.exists() else {}
if p.exists():
    (p.parent/f"settings.json.bak.{int(time.time())}").write_text(p.read_text())
d["outputStyle"] = "fluent-korean"
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("   기본 출력 스타일: fluent-korean")
PY

echo "   설치 완료 — 새 세션 또는 /clear 후 적용됩니다."
echo "   코드를 직접 고치지 않는 작업에는 fluent-korean-not-coding 으로 바꾸세요."
exit 0
