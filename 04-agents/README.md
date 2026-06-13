# Agent Teams

OMC 빌트인 에이전트(30+종)가 기본. 이 폴더의 에이전트는 **사용자 스택에 특화된 도메인 지식 보완** 역할.

## 폴더 구조

| 폴더 | 역할 | 에이전트 | OMC 보완 대상 |
|------|------|---------|-------------|
| **01-core** | 핵심 개발 | typescript-pro, react-specialist, fullstack-developer, electron-pro | executor, deep-executor |
| **02-platform** | 플랫폼/인프라 | deployment-engineer, mcp-developer, devops-engineer | build-fixer |
| **03-integration** | 외부 서비스 통합 | slack-expert, api-designer | dependency-expert |
| **04-quality** | 품질/보안/테스트 | security-engineer, performance-engineer, test-automator | review-lane (6종) |
| **05-product** | 제품/디자인 | ui-designer, seo-specialist | product-lane (4종) |
| **06-data** | 데이터/AI/프롬프트 | ai-engineer, data-analyst, prompt-engineer | scientist |
| **archive** | 미사용 보관 | 97개 | - |

## 선택 기준

1. 먼저 OMC 빌트인 에이전트(executor, architect, debugger 등) 사용
2. 도메인 전문성이 필요할 때만 이 폴더의 에이전트 호출
3. archive에서 필요한 에이전트를 해당 팀 폴더로 복원 가능
