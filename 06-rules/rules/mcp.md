# MCP 주의

- Notion: `parent`는 JSON 객체 필수. 직렬화 2회 실패 → curl 전환
- `claude mcp add`는 세션 내 사용 금지 — 변경사항 문서화 후 재시작 시 적용
- MCP 서버 소스 수정 → Claude Code 재시작 필수 (런타임 중 반영 안 됨)
