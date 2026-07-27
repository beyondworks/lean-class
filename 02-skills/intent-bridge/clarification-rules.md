# Clarification Rules

## Principles
- Questions must be answerable by non-technical users
- Maximum 2 questions per interaction
- Each question has maximum 3 options + "recommend for me"
- Option text should be around 18 characters

## Forbidden Terms (never expose to user)
- OAuth2, PKCE
- SSR, CSR
- hydration
- RESTful resource modeling
- optimistic mutation
- stale cache invalidation

## Plain Language Replacement Table
| Technical Term | Plain Language |
|---|---|
| SSR | 처음부터 빠르게 보이기 |
| CSR | 브라우저에서 더 동적으로 처리 |
| OAuth/social auth | 구글/카카오 같은 외부 로그인 |
| credentials auth | 이메일/비밀번호 로그인 |
| REST | 일반 API |
| GraphQL | 필요한 데이터만 받는 API |
| optimistic update | 먼저 화면에 반영하고 나중에 저장 확인 |
| cache invalidation | 이전 데이터 새로고침 규칙 |

## Question Format

```
이 부분만 정하면 바로 진행할 수 있어요.

1) [선택지 A]
2) [선택지 B]
3) 잘 모르겠어요. 추천해줘
```
