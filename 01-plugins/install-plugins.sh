#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  Claude Code 플러그인 일괄 설치 스크립트
#  실행: bash install-plugins.sh
#  ⚠ Claude Code 버전에 따라 plugin CLI 문법이 다를 수 있습니다.
#    막히면 README.md 의 '대화형 설치(/plugin)' 방법을 쓰세요.
# ──────────────────────────────────────────────────────────────
set -uo pipefail

echo "▶ 1/2 마켓플레이스 등록"
markets=(
  "anthropics/claude-plugins-official"   # 공식 플러그인 모음
  "anthropics/claude-code"               # claude-code-plugins
  "popup-studio-ai/bkit-claude-code"     # bkit
  "Yeachan-Heo/oh-my-claudecode"         # OMC ★
  "revfactory/harness"                   # harness
  "heygen-com/hyperframes"               # hyperframes
  "openai/codex-plugin-cc"               # codex
  "fivetaku/gptaku_plugins"              # gptaku — insane-search 등 ★
  "StarTrail-org/PixelRAG"               # pixelrag — pixelbrowse
)
for m in "${markets[@]}"; do
  echo "  + marketplace: $m"
  claude plugin marketplace add "$m" || echo "    (이미 등록됨/실패 — 건너뜀)"
done

echo "▶ 2/2 플러그인 설치"
plugins=(
  # 공식 마켓플레이스(claude-plugins-official)
  "context7@claude-plugins-official"
  "claude-md-management@claude-plugins-official"
  "claude-code-setup@claude-plugins-official"
  "code-review@claude-plugins-official"
  "firecrawl@claude-plugins-official"
  "firebase@claude-plugins-official"
  "figma@claude-plugins-official"
  "github@claude-plugins-official"
  "frontend-design@claude-plugins-official"
  "huggingface-skills@claude-plugins-official"
  "Notion@claude-plugins-official"
  "ralph-loop@claude-plugins-official"
  "playwright@claude-plugins-official"
  "security-guidance@claude-plugins-official"
  "slack@claude-plugins-official"
  "vercel@claude-plugins-official"
  "superpowers@claude-plugins-official"
  "swift-lsp@claude-plugins-official"
  "telegram@claude-plugins-official"
  "discord@claude-plugins-official"
  # 서드파티 마켓플레이스
  "bkit@bkit-marketplace"
  "oh-my-claudecode@omc"                 # ★ 멀티에이전트 오케스트레이션
  "harness@harness-marketplace"
  "hyperframes@hyperframes"
  "codex@openai-codex"
  "insane-search@gptaku-plugins"         # ★ 차단 사이트 적응형 접근 (WAF 우회)
  "pixelbrowse@pixelrag-plugins"         # 픽셀 기반 브라우즈/스크린샷
)
for p in "${plugins[@]}"; do
  echo "  + install: $p"
  claude plugin install "$p" || echo "    (실패 — 건너뜀: $p)"
done

echo "✓ 완료. Claude Code 재시작 후 /plugin 으로 설치 상태를 확인하세요."
