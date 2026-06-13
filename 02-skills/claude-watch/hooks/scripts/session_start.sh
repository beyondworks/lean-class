#!/usr/bin/env bash
# Print a one-line claude-watch status only when remediation is needed.
# Silent on `ready`.
set -e
RAW=$(python3 "${CLAUDE_PLUGIN_DIR:-$(dirname "$0")/../..}/scripts/setup.py" --check --json 2>/dev/null || true)
[ -z "$RAW" ] && exit 0
STATUS=$(printf '%s' "$RAW" | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])' 2>/dev/null || echo "")
case "$STATUS" in
  ready|"") exit 0 ;;
  needs_install) echo "[claude-watch] Run /claude-watch — setup will install ffmpeg/yt-dlp on first run." ;;
  needs_key) echo "[claude-watch] Whisper key missing. Set GROQ_API_KEY or OPENAI_API_KEY in ~/.config/claude-watch/.env (or use --no-whisper)." ;;
  needs_install_and_key) echo "[claude-watch] Setup incomplete: run /claude-watch and Claude will walk you through install + API key." ;;
esac
