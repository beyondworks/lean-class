# 패키징 목록 (Package Manifest)

> 강사가 실제로 쓰는 **범용 툴 셋**(스킬·플러그인·MCP·커맨드·에이전트)을 패키징. 강사 개인 노하우(작업 사례·세션 기록)와 모든 시크릿·개인정보는 제외.

## 0. 요약

| 카테고리 | 포함 | 제외 | 폴더 |
|---|---:|---:|---|
| MCP 서버 | 18 | 3 | `00-mcp/` |
| 플러그인 | 27 | 0 | `01-plugins/` |
| 스킬 | 111 | 7 | `02-skills/` |
| 슬래시 커맨드 | 29 | 2 | `03-commands/` |
| 에이전트 | 22 | (보관 레거시 97) | `04-agents/` |

**보안·개인정보 상태**: 실 시크릿 0 · `.env` 실파일 0 · 개인 식별자 0 · 개인 절대경로 0 · 깨진 링크 0 · **노하우 references 0**

### 2026-07-07 갱신
- 마켓플레이스 +2: **gptaku-plugins**(`fivetaku/gptaku_plugins`) · **pixelrag-plugins**(`StarTrail-org/PixelRAG`)
- 플러그인 +2: **insane-search ★**(차단 사이트 적응형 접근·WAF 우회) · **pixelbrowse**
- 스킬 +3: **script-to-slides**(대본→16:9 캐러셀 슬라이드) · **model-ab-test**(모델 비교 관찰·로그) · **video-content-visuals**(영상 비주얼 일관 생산)
- 커맨드 +2: **easy**(비전문가용 쉬운 설명) · **creator-persona-clone**
- 개인 볼트 인프라 의존분(wiki-autolink·skill-proposal)은 공개 킷 정책상 제외

> **핵심 방침**: 각 스킬은 사용설명서(`SKILL.md`) + 구동 자산(`data`/`scripts`/`resources`)만 남기고, 강사가 세션에서 축적한 노하우 폴더(`references/`)는 전부 제거했습니다.

---

## 1. MCP 서버 (`00-mcp/`)

### 포함 — 키 없이 즉시 동작 (8)
context7 · sequential-thinking · playwright · shadcn-ui · ui-expert · design-systems(HTTP) · stitch · linear(OAuth)

### 포함 — API 키 필요 (4)
| MCP | 키 |
|---|---|
| hyperbrowser | `HYPERBROWSER_API_KEY` |
| magic | `TWENTYFIRST_API_KEY` |
| testsprite | `API_KEY` |
| notion | Notion Integration Token |

### 포함 — 로컬 의존(직접 설치, 템플릿 분리) (6)
code-review-graph · mcp-obsidian · n8n-mcp · ui-inspector · octo-browser · pencil

### 제외 — 개인·회사 전용 (3)
회사 워크스페이스 연동 에이전트 · 강사 본인 서비스 연동 MCP · 강사 커스텀 브리지 MCP

---

## 2. 플러그인 (`01-plugins/`) — 25개

**마켓플레이스(7)**: claude-plugins-official · claude-code-plugins · bkit-marketplace · omc ★ · harness-marketplace · hyperframes · openai-codex

**공식(20)**: context7 · claude-md-management · claude-code-setup · code-review · firecrawl · firebase · figma · github · frontend-design · huggingface-skills · Notion · ralph-loop · playwright · security-guidance · slack · vercel · superpowers · swift-lsp · telegram · discord

**서드파티(5)**: **oh-my-claudecode ★** · bkit · harness · hyperframes · codex

> 플러그인은 자신의 번들 스킬·에이전트·MCP·커맨드를 함께 가져옵니다.

---

## 3. 독립 스킬 (`02-skills/`) — 108개

### UI·디자인 (37)
adapt · animate · arrange · audit · bolder · clarify · colorize · critique · delight · distill · extract · harden · normalize · onboard · optimize · overdrive · polish · quieter · typeset · frontend-design · taste-brutalist · taste-minimalist · taste-output · taste-redesign · taste-skill · taste-soft · taste-stitch · design-masters-reference · ui-ux-pro-max · ui-ux-translator · ui-inspector · gemini-design-expert · aidu-design-system · aidu-web-cloner · web-design-guidelines · designer-skill-builder · teach-impeccable

### 영상·이미지 콘텐츠 (19)
create-video · capcut-project · video-capture · ttstudio-voice · virtual-influencer-script · virtual-influencer-fashion-tryon · virtual-influencer-reference-remake · ducktape-character-sheet · strict-shortform-production-rules · codex-gptimage-heygen-video-wrapper · codex-gptimage2-heygen-media-generation · card-news · claude-watch · screenstudio-cut · analyze-bug-video · kling-image-to-video · grok-imagine · youtube-content-expander · yt-competitive-analysis

### 커머스·마케팅·세일즈 (20)
ad-creative · commerce-ad-copy-playbook · conversion-ops · content-ops · ecommerce-detail-page-planner · detail-page-team · autoresearch · growth-engine · revenue-intelligence · sales-pipeline · sales-playbook · outbound-engine · seo-ops · seo-audit · programmatic-seo · deck-generator · finance-ops · podcast-ops · team-ops · karpathy-guidelines

### n8n·자동화 (9)
n8n-skills-2.1.1 · n8n-slack-notion-automation · n8n-code-javascript · n8n-code-python · n8n-expression-syntax · n8n-mcp-tools-expert · n8n-node-configuration · n8n-validation-expert · n8n-workflow-patterns

### 개발·배포·워크플로 (23)
handoff · session-resume · obsidian-reference · obsidian-save · deploy · mcp-builder · slide-craft-team · remotion-best-practices · vercel-react-best-practices · saas-platform-builder · capacitor-ios-team · pre-deploy-review · project-context-builder · raw-press · scan-to-pdf · openspec-apply-change · openspec-archive-change · openspec-bulk-archive-change · openspec-continue-change · openspec-explore · openspec-ff-change · openspec-new-change · openspec-onboard · openspec-sync-specs · openspec-verify-change

---

## 4. 슬래시 커맨드 (`03-commands/`) — 27개

aidu-design-system · aidu-web-cloner · capacitor-ios-team · designer-skill-builder · detail-page-team · ecommerce-detail-page-planner · gemini-code · gemini-design · gemini-login · mcp-builder · n8n-code-js · n8n-code-python · n8n-expressions · n8n-mcp-tools · n8n-node-config · n8n-skills · n8n-validation · n8n-workflow-patterns · pre-deploy-review · programmatic-seo · project-context-builder · raw-press · remotion-best-practices · seo-audit · vercel-react-best-practices · web-design-guidelines · youtube-content-expander
(+ `opsx/` 하위 10개: apply · archive · bulk-archive · continue · explore · ff · new · onboard · sync · verify)

---

## 5. 에이전트 (`04-agents/`) — 22개

| 카테고리 | 에이전트 |
|---|---|
| 01-core | electron-pro · fullstack-developer · react-specialist · typescript-pro |
| 02-platform | deployment-engineer · devops-engineer · mcp-developer |
| 03-integration | api-designer · slack-expert |
| 04-quality | performance-engineer · security-engineer · test-automator |
| 05-product | seo-specialist · ui-designer |
| 06-data | ai-engineer · data-analyst · prompt-engineer |
| 공통 | ad-copywriter · ad-designer · ad-landing-analyzer · brainstormer · qna-responder |

(+ `ORG_CHART.md`, `README.md` 조직도 문서)

---

## 6. 제외·정제 내역 (투명성)

### 통째로 제외 (개인·회사 전용)
| 유형 | 개수 | 성격 |
|---|---:|---|
| MCP | 3 | 회사 워크스페이스 연동 · 본인 서비스 연동 · 커스텀 브리지 |
| 스킬 | 7 | 회사 자동화 워크플로 레포 · 개인 일정 도우미 · 커스텀 인텐트 브리지 · 페르소나 복제 · 본인 서비스 디자인시스템 · 외부 심볼릭 링크 · 개인 라이프코칭 팀 |
| 커맨드 | 2 | 위 스킬에 대응하는 커맨드 |
| 에이전트 | 97 | 강사가 보관 처리한 미사용 레거시(`archive`) |

### 정제(제거·치환)
- **노하우 references**: 25개 스킬의 `references/` 폴더 **전부 제거** (강사의 작업 사례·세션 기록·기법 노트). 툴 사용설명서(`SKILL.md`)와 구동 자산(`data`/`scripts`/`resources`)은 유지.
- **시크릿**: 모든 MCP 키·토큰 → `<YOUR_...>` placeholder. 실제 `.env` 파일 5개 미복사.
- **개인 식별자**: 강사명·회사명·서비스명·캐릭터/페르소나명 → 일반 표현으로 치환 (영상/인플루언서/슬라이드 등 스킬 본문).
- **경로**: 개인 절대경로 → `~/...` 일반화.
- **깨진 링크**: references 제거로 생긴 링크 154건(64+82+α) 정리.
- **예시 토큰**: 공개 n8n 튜토리얼의 JWT 예시 마스킹.
