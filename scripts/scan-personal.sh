#!/usr/bin/env bash
# ==============================================================
#  배포 전 게이트 — 개인정보·페르소나·시크릿 검출
#
#  사용법:
#    bash scripts/scan-personal.sh          # 전체 스캔
#    bash scripts/scan-personal.sh 06-rules # 특정 폴더만
#
#  exit 0 = 깨끗함 / exit 1 = 검출됨 (커밋 금지)
#
#  설계 노트: "광고 효율 / 토큰 효율 / 효율적" 같은 일반 단어와
#  인명(효율님·김효율)을 구분한다. 단순 단어 매칭은 오탐이 많다.
# ==============================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-.}"
cd "$ROOT" || exit 2

RED=$'\033[31m'; YEL=$'\033[33m'; GRN=$'\033[32m'; OFF=$'\033[0m'
FOUND=0

# 스캔 제외 경로
EXCLUDES=(--exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv
          --exclude=*.png --exclude=*.jpg --exclude=*.pdf --exclude=*.zip
          --exclude=.DS_Store --exclude=scan-personal.sh)

# 정당한 참조 — 이 패턴에 걸리는 줄은 무시한다.
#  · 레포 URL, 치환 placeholder, 문서용 더미 키(your-api-key-here 류)
#  · 빌드 스크립트 자신의 "제외 목록/치환 표"는 개인정보가 아니라 정책 선언이다
ALLOW='github\.com/[A-Za-z0-9_-]+/lean-class|\{\{[A-Z_]+\}\}|OWNER_HANDLE|GITHUB_ORG|placeholder|your[-_]|YOUR_|<[A-Za-z_]+>|api[-_]key[-_]here|example\.(com|org)|xxxx|^\./scripts/build-[a-z]+\.sh:|EXCLUDE=\(|건너뜀'

report() {          # report <라벨> <정규식> <심각도>
  local label="$1" pattern="$2" sev="$3" hits
  hits="$(grep -rInE "$pattern" "$TARGET" "${EXCLUDES[@]}" 2>/dev/null \
          | grep -vE "$ALLOW" || true)"
  if [ -n "$hits" ]; then
    local n; n="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
    if [ "$sev" = "block" ]; then
      printf '%s[검출-차단]%s %s — %s건\n' "$RED" "$OFF" "$label" "$n"
      FOUND=1
    else
      printf '%s[검출-확인]%s %s — %s건\n' "$YEL" "$OFF" "$label" "$n"
    fi
    printf '%s\n' "$hits" | head -12 | sed 's/^/    /'
    [ "$n" -gt 12 ] && printf '    … 외 %s건\n' "$((n-12))"
    echo
  fi
}

echo "=================================================="
echo "  개인정보·페르소나·시크릿 스캔"
echo "  대상: $ROOT/$TARGET"
echo "=================================================="
echo

# ---------- 1) 시크릿 (최우선 차단) ----------
# 토큰 접두사는 반드시 "값 위치"(줄 시작·따옴표·=·공백 뒤)에서만 인정한다.
# 그러지 않으면 temperature_distribution 의 re_ 같은 단어 내부가 걸린다.
SEP='(^|[^A-Za-z0-9_])'
report "시크릿 토큰 형태" \
  "${SEP}(sk-[A-Za-z0-9]{16}|re_[A-Za-z0-9]{12}|npg_[A-Za-z0-9]{8}|ghp_[A-Za-z0-9]{20}|github_pat_[A-Za-z0-9_]{20}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10}|AIza[0-9A-Za-z_-]{30})" \
  block

report "DB 접속 문자열" \
  '(postgresql|postgres|mysql|mongodb(\+srv)?|redis|rediss)://[^ "'"'"'`]*:[^ "'"'"'`]*@' \
  block

report "환경변수에 값이 박힌 형태" \
  '(API_KEY|SECRET|TOKEN|PASSWORD|PASSWD|CLIENT_SECRET)[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9_/+-]{16}' \
  block

# ---------- 2) 페르소나 (인명 패턴만 — 일반 단어 제외) ----------
# "효율"은 인명 형태(효율님/효율이/효율용/김효율)만 잡는다.
# "광고 효율·토큰 효율·효율적·효율성·비효율·효율화"는 통과시킨다.
report "오너·인물 페르소나" \
  '유건|김효율|효율님|효율이[[:space:]가는]|효율용|효율씨' \
  block

# 에이전트 이름 — 조사/문맥이 붙는 형태로 좁혀 오탐을 줄인다
report "에이전트 페르소나 이름" \
  '페퍼|슈리|카맥|에드나|비스트|월터|요다|울프|다빈치|파인만|데밍|시원(이|님|은|이가|에게)' \
  block

report "개인 계정·핸들" \
  'leankim|beyondworks\.br|kimyoogeons' \
  block

# ---------- 3) 개인 절대경로·개인 인프라 ----------
report "개인 절대경로" \
  '/Users/[a-z]+/|~/lean-projects|~/Documents/AI-Sessions|AI-Sessions-Vault|company-bus' \
  block

# "AI-Native UI"는 디자인 스타일 이름이라 통과시키고, 우리 레포/제품만 잡는다.
report "고객사·교육기관 실명" \
  '패스트캠퍼스|패캠|세무회계태양|taeyangtax|이중희|조성환|황한별|우강마케팅|어센트원|성일렌트카' \
  block

report "개인 조직·고객사 고유명" \
  '우강마케팅|성일렌트카|어센트원|ascent-?one|LeanAX|leanax|lean-org|agent-org|lean-crew|AI-Native[ /](인트라넷|앱|프로젝트|인프라)|AI-Native/' \
  block

# ---------- 4) 치환 누락 (템플릿 무결성) ----------
report "치환되지 않은 채 남은 한글 인명 조사형" \
  '님이 지시|님 지시|님께 보고|대표님' \
  warn

echo "=================================================="
if [ "$FOUND" -eq 0 ]; then
  printf '%s통과%s — 차단 항목 0건. 배포 가능합니다.\n' "$GRN" "$OFF"
  echo "=================================================="
  exit 0
else
  printf '%s실패%s — 차단 항목이 남아 있습니다. 커밋하지 마세요.\n' "$RED" "$OFF"
  echo "  조치: 해당 줄을 placeholder({{OWNER_NAME}} 등)로 바꾸거나 파일을 제외하세요."
  echo "=================================================="
  exit 1
fi
