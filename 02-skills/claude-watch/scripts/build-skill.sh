#!/usr/bin/env bash
# Build dist/claude-watch.skill — a zip of SKILL.md + scripts/ for claude.ai upload.
# Strips Claude-Code-only and Codex-only directories.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DIST="$ROOT/dist"
STAGE="$DIST/_stage"
OUT="$DIST/claude-watch.skill"

rm -rf "$DIST"
mkdir -p "$STAGE"

# Files claude.ai sees: SKILL.md + scripts/ (minus build-skill.sh itself)
cp SKILL.md "$STAGE/"
mkdir -p "$STAGE/scripts"
for f in scripts/*.py; do
    cp "$f" "$STAGE/scripts/$(basename "$f")"
done

# (No commands/, hooks/, .claude-plugin/, .codex-plugin/ — those are surface-specific.)

(cd "$STAGE" && zip -qr "$OUT" .)
rm -rf "$STAGE"

echo "Built: $OUT ($(du -h "$OUT" | awk '{print $1}'))"
