---
description: 배포 일반 규칙 (스택별 상세는 프로젝트 CLAUDE.md)
globs: ["vercel.json", "*.service", "Dockerfile", "docker-compose*.yml"]
---

# 배포

## 공통
- 원격 24/7 데몬: systemd user service + linger. `Restart=always`, `RestartSec=10`
- 배포 직후 엔드포인트 `curl` 응답 검증 필수 (빌드 통과 ≠ 동작)

## Vercel (사용 프로젝트만)
- Webhook 사용 시 Deployment Protection 비활성화 (인증 페이지가 webhook을 차단함)
- Slack 통합은 공개 엔드포인트 필요
