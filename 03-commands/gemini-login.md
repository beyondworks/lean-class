---
name: gemini-login
description: Google OAuth로 Gemini API에 로그인
---

# Gemini 로그인

Google OAuth 인증으로 Gemini API에 연결한다.

## 실행 절차

1. `gemini_auth_status` 도구로 현재 인증 상태를 확인한다.
2. 이미 인증된 경우 "이미 Gemini에 연결되어 있습니다" 메시지를 표시하고 종료한다.
3. 인증되지 않은 경우 `gemini_login` 도구를 호출한다.
4. 브라우저에서 Google 로그인 페이지가 열린다. 사용자에게 로그인을 완료하라고 안내한다.
5. 로그인 완료 후 인증 성공 메시지를 표시한다.

## 주의사항

- 환경 변수 `GOOGLE_CLIENT_ID`와 `GOOGLE_CLIENT_SECRET`이 설정되어 있어야 한다.
- 설정되지 않은 경우 Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하는 방법을 안내한다.
- 토큰은 `~/.gemini-design-agent/tokens.json`에 캐시되어 재로그인 없이 재사용된다.
