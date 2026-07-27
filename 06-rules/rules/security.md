# 보안 (절대 규칙)

## 시크릿 평문 금지 (위반 시 즉시 작업 중단)

**핸드오버 문서, 세션 요약, README, CLAUDE.md, MEMORY.md, 커밋 메시지, 코드 주석, PR 설명, 이슈 본문, 채팅/메일 회신, 로그 덤프 — 어디에도 다음 값의 평문을 기입하지 않는다:**

- API 키 (OpenAI, Anthropic, Resend, Stripe, Toss live, Google, AWS, Vercel, Supabase 등)
- DB 접속 문자열 (postgresql://, mongodb://, mysql://, redis://)
- OAuth client secret, refresh token, access token
- JWT secret, 암호화 키, 서명 키
- 비밀번호, DB password, SSH private key
- Webhook secret, signing secret
- 신용카드 번호, 주민번호, 여권번호

## 참조 방식 (반드시 이 형태로만)

평문 대신 **환경변수 이름**과 **위치**만 기록:

```
✅ DATABASE_URL (Vercel auto-video-landing / Production)
✅ RESEND_API_KEY (~/.env.local 참조)
✅ npg_*** (Neon 콘솔에서 재발급)
✅ re_cb***REDACTED***

❌ DATABASE_URL=postgresql://user:<실제_비밀번호>@<host>/<db>
❌ re_<실제_키_전체>
❌ "예시로 <실제_키> 같은 키를..."
```

**접두사 3~4자만 노출하는 것도 최소화**. 키 종류 식별이 필요하면 `re_***` 처럼만.

## 사전 방어 (작업 시작 전 체크)

1. 문서 작성 전: "이 문서에 시크릿 값이 들어갈 가능성이 있는가?" 자문. 있으면 참조 방식으로 전환
2. `.env` 계열 파일(`*.env`, `*.env.*`, `.envrc`)은 **절대 읽어서 출력하지 말 것**. 편집 시에도 값을 복붙/에코하지 말 것
3. 커밋 전 `git diff --cached`에서 `password|secret|key|token|api_key|DATABASE_URL` 패턴 grep 검증
4. `git add .` / `git add -A` 사용 금지 — 파일 단위로 명시적 추가

## 사후 대응 (유출 발생 시)

1. **revoke 먼저, 히스토리 재작성은 보조수단**. history rewrite는 GitHub 캐시·포크·스캐너 때문에 100% 보호 안 됨
2. GitGuardian/GitHub Secret Scanning 알림 오면 즉시 revoke → force push는 그 다음
3. 로그·감사 이력 확인: 이미 악용됐는지 확인

## 환경변수 관리 원칙

- 로컬: `.env.local`만 사용 (`.gitignore`에 반드시 포함)
- 원격: Vercel/Supabase/AWS 대시보드에 저장
- 팀 공유: 1Password, Doppler, Infisical 같은 secret manager — 평문 메일/Slack/Notion 금지
- 개발·스테이징·프로덕션 키 분리

## 관련 사례

2026-04-09: `{{GITHUB_ORG}}/{{OWNER_HANDLE}}.xyz` 레포의 `SESSION_HANDOVER.md`에 Vercel Blob / Resend / Neon Postgres 평문 기재 → 푸시 즉시 GitGuardian 3건 감지. `git filter-repo`로 히스토리 재작성. 원인은 "세션 요약 문서에 env 값 덤프" 습관. **이런 요약 문서에는 환경변수 이름만 쓰고 값은 절대 쓰지 않는다**.
