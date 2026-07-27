# AgentSpec Examples

## Example 1: Login Feature

User says: "로그인 기능 만들어줘"

Internal AgentSpec (hidden from user):
```json
{
  "version": "1.0",
  "meta": {
    "sessionId": "sess-001",
    "projectRoot": "/project",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "riskLevel": "medium"
  },
  "intent": {
    "rawUserRequest": "로그인 기능 만들어줘",
    "normalizedGoal": "Implement user authentication with login functionality",
    "taskType": "feature",
    "userVisibleOutput": "Users can log in to the application"
  },
  "clarification": {
    "needed": true,
    "reason": "Authentication method not specified",
    "questions": [
      {
        "id": "q1",
        "plainLanguage": "어떤 로그인 방식을 원하시나요?",
        "options": [
          "구글/카카오 같은 외부 로그인",
          "이메일/비밀번호 로그인",
          "잘 모르겠어요. 추천해줘"
        ],
        "allowRecommendForMe": true
      }
    ]
  }
}
```

## Example 2: Performance Improvement

User says: "이 페이지 좀 빨라지게 해줘"

Clarification question (if needed):
```
이 부분만 정하면 바로 진행할 수 있어요.

1) 처음부터 빨리 보이게
2) 브라우저에서 더 동적으로
3) 잘 모르겠어요. 추천해줘
```

## Example 3: Test Addition

User says: "테스트 붙여줘"

No clarification needed if test runner is detected.
Proceed with proposed assumptions.

## Example 4: Dangerous Operation

User says: "필요 없는 파일 싹 지워줘"

danger_check returns: high risk
Action: Force confirmation before proceeding.
