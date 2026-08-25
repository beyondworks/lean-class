# 패키징 목록 (Package Manifest)

> Claude Code 작업 환경 한 벌(스킬·플러그인·MCP·커맨드·에이전트 + **글로벌 규칙·하네스·셸**)을 패키징.
> 개인 노하우(작업 사례·세션 기록)와 모든 시크릿·개인정보·페르소나는 제외.

## 0. 요약

| 카테고리 | 포함 | 폴더 |
|---|---:|---|
| MCP 서버 | 14 | `00-mcp/` |
| 플러그인 | 21 (6 격리) | `01-plugins/` |
| 스킬 | 129 | `02-skills/` |
| 슬래시 커맨드 | 33 | `03-commands/` |
| 에이전트 | 25 | `04-agents/` |
| **글로벌 규칙** | **10 (+선택 1)** | **`06-rules/`** |
| **하네스** | **1 (부트스트랩)** | **`07-fablize/`** |
| **셸 설정** | **—** | **`08-shell/`** |
| **출력 스타일** | **2 (부트스트랩)** | **`09-output-styles/`** |

**보안·개인정보 상태**: `scripts/scan-personal.sh` 통과 (차단 항목 0건) · 실 시크릿 0 · `.env` 실파일 0 · 페르소나 0 · 개인 절대경로 0 · 노하우 `references/` 0

### 2026-08-24 갱신 — 현행화 + 출력 스타일 신규

로컬 세팅 기준으로 재빌드했습니다(`scripts/build-rules.sh` · `scripts/build-skills.sh`).

**신규 `09-output-styles/`** — 한국어 출력 스타일(`fluent-korean`). 코딩 에이전트가 토큰을 아끼려고
조사·어미를 떨어뜨리면 한국어는 격 관계 표시가 통째로 사라진다. 그것을 시스템 프롬프트 층위에서 막는다.
제3자 저작물(snflkd, MIT)이라 **07-fablize 와 같이 파일을 담지 않고 설치 시 원본에서 받아온다.**

**스킬 +6** — find-skills · higgsfield-mcp-ops · ip-as-logo · korean-ai-tell · omc-reference · palmier
(`korean-ai-tell` = 접속 부사 과잉 교정. 출력 스타일이 문법을 세운다면 이쪽은 문장 사이 리듬을 본다.)

**배포 제외로 새로 판정한 것 3개** — 이번 갱신에서 실제로 걸러낸 항목이다.

| 스킬 | 제외 사유 |
|---|---|
| `leankim-voice` | 오너 개인 화법 코퍼스. **이름을 placeholder 로 바꿔도 내용 자체가 정체성**이라 치환으로 해결되지 않는다 |
| `course-script` | 오너 페르소나 빙의 규칙 + 본인이 직접 쓴 확정본 코퍼스 + **고객사 실명**이 본문에 있었다 |
| `argo-security-surface-audit` | 특정 데스크톱 앱 전용(기존 `argo-*` 계열과 같은 판정) |

> **이번 갱신에서 배운 것**: 빌드 스크립트의 이름 치환(`유건`→`{{OWNER_NAME}}`)은 *언급*을 지울 뿐
> *내용*을 지우지 못한다. 특정인의 글을 학습 대상으로 삼는 스킬은 치환이 아니라 **제외**가 답이다.

**게이트 강화** — `scan-personal.sh` 에 고객사·교육기관 실명 패턴을 차단 항목으로 추가했다.
기존 게이트는 회사·제품명만 봤고 고객사명은 통과시키고 있었다(`course-script` 의 실명이 이 구멍으로 남아 있었다).

**플러그인** — `vibe-sunsang@gptaku-plugins` 추가. `ponytail` 은 원 PC에서 **로컬 디렉토리**
마켓플레이스로 등록돼 있어 공개 출처를 확인할 수 없으므로 배포 목록에서 제외했다.

---

### 2026-07-27 갱신 — 페르소나 제거 + 신규 3카테고리

**이번 갱신의 핵심**: 이 패키지에서 **사람 이름을 전부 걷어냈습니다.** 오너·에이전트 이름은 설치 시 그 PC의 오너가 정합니다(`install.sh` 대화형 또는 `--answers`).

신규:
- **`06-rules/`** — 글로벌 `CLAUDE.md` + 규칙 12개(보안·정합성·원칙·소통·워크플로·학습루프 등). 개인 고유명은 `{{OWNER_NAME}}` 류 placeholder로 치환됨. 개인 전용 2개(ERP 연동·모델 비교 로그)는 제외. 도구 전제가 있는 1개(브라우저)는 `rules/optional/`로 분리해 기본 설치에서 뺌
- **`07-fablize/`** — 작업 방식 하네스 부트스트랩. **파일을 담지 않고** 설치 시 원본 레포에서 받아옴(제3자 저작물 재배포 회피)
- **`08-shell/`** — `cc` alias + PATH. 프로파일엔 source 한 줄만 넣고 스니펫은 홈에 복사(패키지 폴더를 옮겨도 안 깨짐)
- **`scripts/`** — 개인정보 게이트(`scan-personal.sh`) + 재생성 빌드 2종. 다음 갱신은 빌드 스크립트 실행으로 끝남

정제·제외:
- **심볼릭 링크 48개 제외** — `~/.claude/skills`의 상당수가 `~/.codex/skills`를 가리키는 링크였음. 복사하면 대상 PC에서 전부 깨짐. OMC 설치로 대체됨
- **로컬에서 이미 깨진 스킬 15개 제외** — 존재하지 않는 대상을 가리키는 링크만 남아 있던 것
- **`.env` 실파일 2개 차단** — 스킬 폴더에 실제 API 키가 든 `.env`가 있었음. 빌드에서 `.env`·`*.pem`·`*.key` 등을 복사 대상에서 제외하도록 고정
- 스킬 45개 현행화 · `references/` 17개 제거 · 사내 시스템 실명 일반화

### 2026-07-09 갱신
- 스킬 +2: **coupang-review-crawler**(쿠팡 리뷰 대량 크롤 + 주제별 그룹화·평점 파티션·xlsx) · **instagram-post-crawler**(인스타 공개 게시물 수집 — 계정 피드/해시태그, 공개만·best-effort) — 둘 다 insane-search 백엔드(차단·로그인월 우회) 기반
- (커맨드/플러그인 신규 없음. board·boot·inbox 등 로컬 org-loop 인프라는 개인 도구라 공개 킷 제외)

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

## 2. 플러그인 (`01-plugins/`) — 21개 (6 격리)

**마켓플레이스(5 활성)**: claude-plugins-official · claude-code-plugins · bkit-marketplace · hyperframes · gptaku-plugins
**마켓플레이스(3 격리 2026-08-05)**: ~~omc~~ · ~~harness-marketplace~~ · ~~openai-codex~~

**공식(16 활성)**: context7 · claude-md-management · claude-code-setup · code-review · firecrawl · firebase · figma · github · frontend-design · huggingface-skills · Notion · playwright · security-guidance · slack · swift-lsp · telegram · discord
**공식(3 격리 2026-08-05)**: ~~ralph-loop~~ · ~~vercel~~ · ~~superpowers~~

**서드파티(3 활성)**: bkit · hyperframes · insane-search · pixelbrowse
**서드파티(3 격리 2026-08-05)**: ~~oh-my-claudecode~~ · ~~harness~~ · ~~codex~~

> 플러그인은 자신의 번들 스킬·에이전트·MCP·커맨드를 함께 가져옵니다.

---

## 3. 독립 스킬 (`02-skills/`) — 123개

### UI·디자인 (37)
adapt · animate · arrange · audit · bolder · clarify · colorize · critique · delight · distill · extract · harden · normalize · onboard · optimize · overdrive · polish · quieter · typeset · frontend-design · taste-brutalist · taste-minimalist · taste-output · taste-redesign · taste-skill · taste-soft · taste-stitch · design-masters-reference · ui-ux-pro-max · ui-ux-translator · ui-inspector · gemini-design-expert · aidu-design-system · aidu-web-cloner · intranet-style · web-design-guidelines · designer-skill-builder · teach-impeccable

### 영상·이미지 콘텐츠 (19)
create-video · capcut-project · video-capture · ttstudio-voice · virtual-influencer-script · virtual-influencer-fashion-tryon · virtual-influencer-reference-remake · ducktape-character-sheet · strict-shortform-production-rules · codex-gptimage-heygen-video-wrapper · codex-gptimage2-heygen-media-generation · card-news · claude-watch · screenstudio-cut · analyze-bug-video · kling-image-to-video · grok-imagine · youtube-content-expander · yt-competitive-analysis

### 커머스·마케팅·세일즈 (20)
ad-creative · commerce-ad-copy-playbook · conversion-ops · content-ops · ecommerce-detail-page-planner · detail-page-team · autoresearch · growth-engine · revenue-intelligence · sales-pipeline · sales-playbook · outbound-engine · seo-ops · seo-audit · programmatic-seo · deck-generator · finance-ops · podcast-ops · team-ops · karpathy-guidelines

### n8n·자동화 (9)
n8n-skills-2.1.1 · n8n-slack-notion-automation · n8n-code-javascript · n8n-code-python · n8n-expression-syntax · n8n-mcp-tools-expert · n8n-node-configuration · n8n-validation-expert · n8n-workflow-patterns

### 개발·배포·워크플로 (23)
handoff · session-resume · obsidian-reference · obsidian-save · deploy · mcp-builder · slide-craft-team · remotion-best-practices · vercel-react-best-practices · saas-platform-builder · capacitor-ios-team · pre-deploy-review · project-context-builder · raw-press · scan-to-pdf · openspec-apply-change · openspec-archive-change · openspec-bulk-archive-change · openspec-continue-change · openspec-explore · openspec-ff-change · openspec-new-change · openspec-onboard · openspec-sync-specs · openspec-verify-change

---

## 4. 슬래시 커맨드 (`03-commands/`) — 32개

aidu-design-system · aidu-web-cloner · capacitor-ios-team · designer-skill-builder · detail-page-team · ecommerce-detail-page-planner · gemini-code · gemini-design · gemini-login · mcp-builder · n8n-code-js · n8n-code-python · n8n-expressions · n8n-mcp-tools · n8n-node-config · n8n-skills · n8n-validation · n8n-workflow-patterns · pre-deploy-review · programmatic-seo · project-context-builder · raw-press · remotion-best-practices · seo-audit · vercel-react-best-practices · web-design-guidelines · youtube-content-expander
(+ `opsx/` 하위 10개: apply · archive · bulk-archive · continue · explore · ff · new · onboard · sync · verify)

---

## 5. 에이전트 (`04-agents/`) — 24개

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

## 6. 글로벌 규칙 (`06-rules/`) — 10 (+선택 1)

`~/.claude/CLAUDE.md` + `~/.claude/rules/`로 설치되어 **모든 프로젝트에 항상 적용**됩니다.

**기본 10**: security(시크릿 평문 금지) · principles(정직성·근본원인·추측 금지·YAGNI) · communication(열린 선택형 질문 금지) · workflow(세션 절차·UI 검증) · learning-loop(교정 시 lessons 축적) · git · deployment · mcp · macos · emil-skills

**선택 1** (`rules/optional/`): browser — 특정 브라우저 자동화 CLI 전제라 기본 설치 제외

**제외 2**: 개인 ERP 연동 · 개인 모델 비교 로그 (원 소유자 환경 전용)

치환 변수: `OWNER_NAME`·`OWNER_TITLE`·`OWNER_HANDLE`·`OWNER_EMAIL`·`GITHUB_ORG`·`PROJECTS_ROOT`·`CODE_ROOT`·`VAULT_ROOT`·`MODERATOR`·`AGENT_*` 10종

## 7. 하네스 (`07-fablize/`)

작업 방식 자체를 규정하는 블록(착수·검증·보고 규율). **파일 미포함** — 설치 시 공개 원본 레포에서 clone 후 원저자 `setup.sh` 실행. 실패해도 나머지 설치는 계속됩니다.

설치 순서 제약: `06-rules` → `07-fablize` (역순이면 규칙 설치가 하네스 블록을 지움)

## 8. 셸 (`08-shell/`)

`cc` alias(권한 확인 생략 — 경고 포함) + `~/.local/bin`·npm 전역 PATH. 프로파일엔 마커로 감싼 source 한 줄만 추가하며, 스니펫 본체는 `~/.claude/lean-class.sh`로 복사됩니다.

## 9. 빌드·검증 스크립트 (`scripts/`)

| 스크립트 | 용도 |
|---|---|
| `scan-personal.sh` | **커밋 전 게이트.** 시크릿·페르소나·개인경로·조직명 검출. exit 1이면 커밋 금지 |
| `build-rules.sh` | 로컬 `~/.claude/`에서 규칙을 다시 뽑아 치환·제외·optional 분리 |
| `build-skills.sh` | 로컬 스킬·커맨드 동기화. symlink·깨진 스킬·`.env`·`references/` 자동 배제 |

원 소유자 갱신 절차: `build-rules.sh && build-skills.sh && scan-personal.sh` → 통과 시 커밋

---

## 10. 제외·정제 내역 (투명성)

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
