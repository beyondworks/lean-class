# 00 · MCP 서버 설치 가이드

MCP(Model Context Protocol) 서버는 Claude Code 에 외부 도구·데이터를 연결합니다.
이 폴더에는 **시크릿이 모두 제거된 설정 템플릿**이 들어 있습니다. 본인 키를 넣어 사용하세요.

## 파일

| 파일 | 용도 |
|------|------|
| `mcp.template.json` | 바로 동작하는 MCP(npx/http 기반) 설정 템플릿. `<YOUR_...>` 를 본인 키로 교체 |
| `.env.example` | 어떤 API 키가 필요한지 + 발급처 목록 |

## 설치 방법 (2가지 중 택1)

### 방법 A — 프로젝트 단위 (`.mcp.json`)
1. `mcp.template.json` 의 `<YOUR_...>` 자리를 본인 키로 교체
2. `mcpServers` 블록을 작업할 프로젝트 루트의 `.mcp.json` 으로 복사 (없으면 새로 생성)
3. Claude Code 재시작 → `/mcp` 로 연결 확인

### 방법 B — 개별 추가 (`claude mcp add`)
```bash
# 키 없는 것 (즉시 동작)
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
claude mcp add playwright -- npx @playwright/mcp@latest
claude mcp add shadcn-ui -- npx -y @jpisnice/shadcn-ui-mcp-server

# 키 필요한 것 (env 로 전달)
claude mcp add hyperbrowser --env HYPERBROWSER_API_KEY=본인키 -- npx -y hyperbrowser-mcp
```

> Claude Code 버전에 따라 `claude mcp add` 문법이 다를 수 있습니다. 막히면 방법 A 를 쓰거나 `claude mcp --help` 를 확인하세요.

## 포함된 MCP — 키 없이 즉시 동작

| MCP | 역할 | 패키지 |
|-----|------|--------|
| context7 | 라이브러리 최신 공식 문서 조회 | `@upstash/context7-mcp` |
| sequential-thinking | 단계적 추론 보조 | `@modelcontextprotocol/server-sequential-thinking` |
| playwright | 브라우저 자동화·E2E | `@playwright/mcp` |
| shadcn-ui | shadcn/ui 컴포넌트 검색·예제 | `@jpisnice/shadcn-ui-mcp-server` |
| ui-expert | UI 분석·컴포넌트 생성 | `@johndoe20012/ui-expert-mcp` |
| design-systems | 디자인 시스템 지식 검색 (HTTP) | `design-systems-mcp.southleft.com` |
| stitch | Google Stitch 디자인 연동 | `@_davideast/stitch-mcp` |
| linear | Linear 이슈 관리 (브라우저 OAuth) | `mcp-remote → mcp.linear.app` |

## 포함된 MCP — API 키 필요

| MCP | 역할 | 필요한 키 | 발급처 |
|-----|------|-----------|--------|
| hyperbrowser | 클라우드 브라우저 자동화 | `HYPERBROWSER_API_KEY` | app.hyperbrowser.ai |
| magic | 21st.dev UI 컴포넌트 생성 | `TWENTYFIRST_API_KEY` | 21st.dev/magic |
| testsprite | 자동 테스트 생성·실행 | `API_KEY` | testsprite.com |
| notion | Notion 워크스페이스 연동 | Notion Integration Token | notion.so/my-integrations |

## 고급 — 로컬 의존 MCP (선택, 직접 설치 필요)

이 MCP들은 강사 환경에서 쓰이지만 **별도 로컬 설치/실행**이 필요해 템플릿에서 분리했습니다.

| MCP | 역할 | 사전 조건 |
|-----|------|-----------|
| code-review-graph | 코드베이스 지식 그래프 기반 리뷰 | `code-review-graph` 패키지 로컬 설치 후 `code-review-graph serve` |
| mcp-obsidian | Obsidian 볼트 읽기/쓰기 | Obsidian + Local REST API 플러그인 + `uvx mcp-obsidian` |
| n8n-mcp | n8n 워크플로 자동화 | 본인 n8n 인스턴스 + `N8N_API_URL`/`N8N_API_KEY` |
| ui-inspector | 라이브 프리뷰 UI 인스펙터 | 강사 커스텀 — 별도 빌드 필요(범용 대체: 본 킷의 `ui-inspector` 스킬 참고) |
| octo-browser | 안티디텍트 브라우저 제어 | Octo Browser 앱 + 로컬 브리지 |
| pencil | 디자인 도구 연동 | VS Code Pencil 확장 |

> 로컬 의존 MCP는 "강사가 이렇게 확장했다"는 참고용입니다. 수강생 환경에서 그대로 동작하지 않을 수 있으니, 위 사전 조건을 갖춘 뒤 직접 설정하세요.
