# 01 · 플러그인 설치 가이드

Claude Code 플러그인은 **마켓플레이스(GitHub 레포)** 에서 설치합니다.
이 폴더의 `install-plugins.sh` 가 마켓플레이스 등록 + 플러그인 설치를 한 번에 해줍니다.

## 설치 방법

### 방법 A — 스크립트 일괄 설치
```bash
bash install-plugins.sh
```

### 방법 B — 대화형 설치 (`/plugin`)
Claude Code 안에서 `/plugin` 입력 → marketplace 추가 → 플러그인 선택 설치.
스크립트가 막힐 때(버전별 CLI 차이) 이 방법이 가장 안전합니다.

## 마켓플레이스 (9개)

| 마켓플레이스 | GitHub 레포 |
|---|---|
| claude-plugins-official | `anthropics/claude-plugins-official` |
| claude-code-plugins | `anthropics/claude-code` |
| bkit-marketplace | `popup-studio-ai/bkit-claude-code` |
| omc ★ | `Yeachan-Heo/oh-my-claudecode` |
| harness-marketplace | `revfactory/harness` |
| hyperframes | `heygen-com/hyperframes` |
| openai-codex | `openai/codex-plugin-cc` |
| gptaku-plugins ★ | `fivetaku/gptaku_plugins` |
| pixelrag-plugins | `StarTrail-org/PixelRAG` |

## 설치되는 플러그인 (27개)

### 공식 (anthropics)
| 플러그인 | 역할 |
|---|---|
| context7 | 라이브러리 최신 공식 문서 조회 |
| claude-md-management | CLAUDE.md 작성·개선 |
| claude-code-setup | Claude Code 설정·자동화 추천 |
| code-review | 변경 diff 코드 리뷰 (`/code-review`, ultra 모드) |
| firecrawl | 웹 검색·스크래핑·크롤 |
| firebase | Firebase 연동 |
| figma | Figma 디자인 → 코드 |
| github | GitHub PR·이슈 작업 |
| frontend-design | 고품질 프론트엔드 디자인 생성 |
| huggingface-skills | HuggingFace 도구 모음 |
| Notion | Notion 워크스페이스 연동 |
| ralph-loop | 작업 완료까지 자율 반복(Ralph) |
| playwright | 브라우저 자동화 |
| security-guidance | 보안 가이드·리뷰 |
| slack | Slack 메시징·검색 |
| vercel | Vercel 배포·AI SDK·Next.js |
| superpowers | 스킬 시스템(브레인스토밍·TDD·디버깅 등) |
| swift-lsp | Swift 언어 서버 |
| telegram | 텔레그램 채널 연동 |
| discord | 디스코드 채널 연동 |

### 서드파티
| 플러그인 | 역할 |
|---|---|
| **oh-my-claudecode ★** | 멀티에이전트 오케스트레이션 (자세히는 `../05-omc/`) |
| bkit | bkit 개발 툴킷 |
| harness | 도메인별 하네스(전문 에이전트+스킬) 구성 |
| hyperframes | HeyGen 영상 프레임 워크플로 |
| codex | OpenAI Codex 연동(2차 구현/진단 패스) |
| **insane-search ★** | 차단 사이트 적응형 접근 — WAF 우회·yt-dlp·Jina·curl_cffi 체인 (X/Reddit/YouTube/네이버/쿠팡 등) |
| pixelbrowse | 픽셀 기반 브라우즈·스크린샷 |

## 참고
- 플러그인은 설치 시 **자신의 스킬·에이전트·MCP·커맨드를 함께 가져옵니다.** 즉 이 폴더의 플러그인을 설치하면 `02-skills`/`04-agents` 에 수동 복사하지 않아도 해당 플러그인 번들 스킬이 자동으로 따라옵니다.
- `02-skills`/`03-commands`/`04-agents` 폴더의 파일은 **플러그인에 속하지 않은, 강사가 직접 만들거나 수집한 독립 자산**입니다. (설치형이 아니라 복사형)
