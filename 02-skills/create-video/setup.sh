#!/bin/bash
set -e

echo "=== Video Pipeline 의존성 설치 ==="
echo ""

# 1. Homebrew 확인
if ! command -v brew &>/dev/null; then
  echo "[!] Homebrew가 설치되어 있지 않습니다."
  echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  exit 1
fi
echo "[✓] Homebrew"

# 2. ffmpeg
if ! command -v ffmpeg &>/dev/null; then
  echo "[i] ffmpeg 설치 중..."
  brew install ffmpeg
else
  echo "[✓] ffmpeg ($(ffmpeg -version 2>&1 | head -1 | awk '{print $3}'))"
fi

# 3. Node.js
if ! command -v node &>/dev/null; then
  echo "[i] Node.js 설치 중..."
  brew install node
else
  echo "[✓] Node.js ($(node -v))"
fi

# 4. Python 3
if ! command -v python3 &>/dev/null; then
  echo "[i] Python 3 설치 중..."
  brew install python@3
else
  echo "[✓] Python 3 ($(python3 --version 2>&1 | awk '{print $2}'))"
fi

# 5. Playwright
if ! npx playwright --version &>/dev/null 2>&1; then
  echo "[i] Playwright 설치 중..."
  npm install -g playwright
  npx playwright install chromium
else
  echo "[✓] Playwright ($(npx playwright --version 2>/dev/null))"
fi

# 6. Python requests
if ! python3 -c "import requests" &>/dev/null 2>&1; then
  echo "[i] Python requests 설치 중..."
  python3 -m pip install requests
else
  echo "[✓] Python requests"
fi

# 7. 스크립트 존재 확인
SCRIPTS_DIR="$(pwd)/scripts"
if [ ! -f "$SCRIPTS_DIR/capcut-project-gen.py" ]; then
  echo "[!] scripts/capcut-project-gen.py 없음 — 프로젝트 루트에서 실행하세요"
else
  echo "[✓] capcut-project-gen.py"
fi

if [ ! -f "$SCRIPTS_DIR/tts-generate.py" ]; then
  echo "[!] scripts/tts-generate.py 없음"
else
  echo "[✓] tts-generate.py"
fi

# 8. Voicebox 앱 확인
if [ -d "/Users/$USER/Projects/Voicebox.app" ] || mdfind "kMDItemFSName == 'Voicebox.app'" 2>/dev/null | grep -q Voicebox; then
  echo "[✓] Voicebox 앱"
else
  echo "[!] Voicebox 앱이 설치되어 있지 않습니다. https://voicebox.sh 에서 다운로드하세요."
fi

# 9. CapCut 앱 확인
if [ -d "/Applications/CapCut.app" ]; then
  echo "[✓] CapCut 앱"
else
  echo "[!] CapCut 앱이 설치되어 있지 않습니다. App Store에서 다운로드하세요."
fi

# 10. vb-clean alias 확인
if grep -q "vb-clean" ~/.zshrc 2>/dev/null; then
  echo "[✓] vb-clean alias"
else
  echo "[i] vb-clean alias 등록 중..."
  echo '' >> ~/.zshrc
  echo '# Voicebox 일괄 정리' >> ~/.zshrc
  echo 'alias vb-clean='"'"'sqlite3 "$HOME/Library/Application Support/sh.voicebox.app/voicebox.db" "DELETE FROM generation_versions; DELETE FROM generations; DELETE FROM story_items; DELETE FROM stories;" && rm -f "$HOME/Library/Application Support/sh.voicebox.app/generations/"*.wav && rm -rf "$HOME/Library/Caches/sh.voicebox.app/"* && osascript -e "tell application \"Voicebox\" to quit" 2>/dev/null; sleep 1; open -a Voicebox && echo "Voicebox 정리 + 재시작 완료"'"'" >> ~/.zshrc
  echo "[✓] vb-clean alias 등록 완료 (새 터미널에서 사용)"
fi

echo ""
echo "=== 설치 완료 ==="
echo ""
echo "사용법:"
echo "  1. /create-video — 전체 파이프라인 실행"
echo "  2. /ttstudio-voice — TTS 음성 생성"
echo "  3. /capcut-project — CapCut 프로젝트 생성"
echo "  4. /video-capture — HTML → MP4 캡처"
echo "  5. vb-clean — Voicebox 정리 + 재시작"
