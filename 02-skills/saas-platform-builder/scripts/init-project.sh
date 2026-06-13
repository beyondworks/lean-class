#!/bin/bash
# SaaS Platform Builder - 프로젝트 초기화 스크립트
# Usage: bash init-project.sh <project-name> <output-path>

set -e

PROJECT_NAME="${1:?프로젝트 이름을 입력하세요. Usage: bash init-project.sh <project-name> <output-path>}"
OUTPUT_PATH="${2:-.}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_DIR="$OUTPUT_PATH/$PROJECT_NAME"

echo "🚀 SaaS Platform Builder - 프로젝트 초기화"
echo "   프로젝트: $PROJECT_NAME"
echo "   위치: $PROJECT_DIR"
echo ""

# 디렉토리 생성
mkdir -p "$PROJECT_DIR"/{docs,docs/templates,src,tests,.github}

echo "📁 디렉토리 구조 생성 완료"

# 템플릿 복사
if [ -d "$SKILL_DIR/references/templates" ]; then
    cp "$SKILL_DIR/references/templates/prd-template.json" "$PROJECT_DIR/docs/templates/PRD.json"
    cp "$SKILL_DIR/references/templates/trd-template.yaml" "$PROJECT_DIR/docs/templates/TRD.yaml"
    cp "$SKILL_DIR/references/templates/ia-template.json" "$PROJECT_DIR/docs/templates/IA.json"
    cp "$SKILL_DIR/references/templates/userflow-template.csv" "$PROJECT_DIR/docs/templates/UserFlows.csv"
    cp "$SKILL_DIR/references/templates/db-schema-template.sql" "$PROJECT_DIR/docs/templates/schema.sql"
    cp "$SKILL_DIR/references/templates/business-logic-template.txt" "$PROJECT_DIR/docs/templates/BusinessLogic.txt"
    cp "$SKILL_DIR/references/templates/qa-checklist-template.md" "$PROJECT_DIR/docs/templates/QA-Checklist.md"
    echo "📋 산출물 템플릿 복사 완료"
else
    echo "⚠️  템플릿 디렉토리를 찾을 수 없습니다: $SKILL_DIR/references/templates"
fi

# Engineering Rules 복사
if [ -f "$SKILL_DIR/references/engineering-rules.md" ]; then
    cp "$SKILL_DIR/references/engineering-rules.md" "$PROJECT_DIR/docs/Engineering-Rules.md"
    echo "📐 엔지니어링 규칙 복사 완료"
fi

# .env.example 생성
cat > "$PROJECT_DIR/.env.example" << 'ENV'
# ===========================================
# Environment Variables
# ===========================================

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Stripe
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# Auth (OAuth)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=
# GITHUB_CLIENT_ID=
# GITHUB_CLIENT_SECRET=

# External APIs
# OPENAI_API_KEY=
# ANTHROPIC_API_KEY=
ENV

echo "🔑 .env.example 생성 완료"

# .gitignore 생성
cat > "$PROJECT_DIR/.gitignore" << 'GIT'
# Dependencies
node_modules/
.pnp
.pnp.js

# Build
.next/
out/
build/
dist/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Testing
coverage/

# Misc
*.tsbuildinfo
next-env.d.ts
GIT

echo "📝 .gitignore 생성 완료"

# PR 템플릿 생성
cat > "$PROJECT_DIR/.github/pull_request_template.md" << 'PR'
## 동기 (Why)
<!-- 이 변경이 필요한 이유 -->

## 변경점 (What)
<!-- 무엇을 변경했는지 -->

## 리스크
<!-- 이 변경으로 인한 잠재적 위험 -->

## 테스트 증거
<!-- 스크린샷, 테스트 결과 등 -->

## 체크리스트
- [ ] 테스트 코드 작성/업데이트
- [ ] 린트/타입체크 통과
- [ ] 문서 업데이트 (필요시)
PR

echo "📄 PR 템플릿 생성 완료"

echo ""
echo "✅ 프로젝트 '$PROJECT_NAME' 초기화 완료!"
echo ""
echo "📂 구조:"
echo "   $PROJECT_DIR/"
echo "   ├── docs/"
echo "   │   └── templates/     ← 산출물 템플릿"
echo "   ├── src/               ← 소스 코드"
echo "   ├── tests/             ← 테스트 코드"
echo "   ├── .github/           ← PR 템플릿"
echo "   ├── .env.example       ← 환경 변수 예시"
echo "   └── .gitignore"
echo ""
echo "다음 단계:"
echo "   1. docs/templates/ 의 템플릿을 프로젝트에 맞게 작성"
echo "   2. PRD → TRD → IA → DB Schema 순으로 진행"
echo "   3. 코드 작성 시 Engineering-Rules.md 참조"
