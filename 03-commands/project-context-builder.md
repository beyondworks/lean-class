# Project Context Builder

프로젝트 컨텍스트 자동 생성 및 세션 학습 스킬. CLAUDE.md(프로젝트 메모리)와 Agent.md(전문 에이전트) 파일을 자동으로 생성하고 업데이트한다.

**트리거 상황:**
- "CLAUDE.md 만들어줘", "프로젝트 컨텍스트 설정해줘"
- "Agent.md 생성해줘", "에이전트 정의해줘"
- "프로젝트 세팅 도와줘", "코딩 규칙 정리해줘"
- "@update-context" - 세션 학습 내용 CLAUDE.md에 반영
- 새 프로젝트 시작 시 초기 설정 요청

**지원 프로젝트:** 웹(React/Next.js/Vue), 백엔드(Node/Python/Go), 풀스택, 노코드(n8n/Make), 모바일, AI/ML 등 모든 유형

## 워크플로우

### Phase 1: 프로젝트 분석

1. **프로젝트 유형 파악**
   - 사용자 설명 또는 기존 코드베이스 분석
   - 기술 스택 식별 (프레임워크, 언어, 도구)
   - 프로젝트 구조 파악

2. **베스트 프랙티스 검색**
   - 웹 검색으로 해당 스택의 최신 베스트 프랙티스 수집
   - 아래 기술 스택별 베스트 프랙티스 참조
   - 공식 문서, 커뮤니티 권장사항 종합

### Phase 2: CLAUDE.md 생성

아래 CLAUDE.md 작성 가이드 참조하여 작성.

**필수 섹션:**
```markdown
# {프로젝트명}

## 기술 스택
- 핵심 기술 나열

## 프로젝트 구조
- 주요 디렉토리 설명

## 코딩 규칙
- 네이밍 컨벤션
- 파일 구조 규칙

## MCP 서버 (있는 경우)
- 사용 가능한 MCP와 용도

## 워크플로우
- 개발 프로세스
- 테스트/배포 방법

---
## 🚨 실수 기록 (반복 금지)
<!-- Claude/Claude Code가 저지른 실수를 기록 -->

---
## 📝 세션 학습 기록
<!-- @update-context 호출 시 여기에 추가됨 -->
```

### Phase 3: Agent.md 생성

아래 Agent.md 작성 가이드 참조하여 작성.

**프로젝트 유형별 추천 에이전트:**

| 프로젝트 유형 | 추천 에이전트 |
|-------------|-------------|
| 웹 프론트엔드 | @ui-reviewer, @a11y-checker, @perf-optimizer |
| 백엔드 API | @api-designer, @security-auditor, @test-writer |
| 풀스택 | @architect, @db-designer, @code-reviewer |
| 노코드/자동화 | @workflow-optimizer, @error-handler |
| AI/ML | @prompt-engineer, @model-evaluator |

### Phase 4: 세션 학습 (@update-context)

사용자가 `@update-context` 또는 "학습 내용 반영해줘" 요청 시:

1. **현재 세션 분석**
   - 성공한 패턴/접근법
   - 발생한 오류와 해결책
   - 사용자 선호 스타일

2. **CLAUDE.md 업데이트**
   ```markdown
   ## 📝 세션 학습 기록

   ### {날짜} 세션
   **✅ 성공 패턴:**
   - {패턴 설명}

   **⚠️ 주의사항:**
   - {실수 방지 사항}

   **🎯 사용자 스타일:**
   - {선호 사항}
   ```

### Phase 5: 실수 기록 및 반복 방지

Claude/Claude Code가 저지른 **모든 실수를 명시적으로 기록**하고, 향후 세션에서 동일한 실수를 반복하지 않도록 한다.

#### 실수 감지 시점
- 사용자가 "그거 아니야", "다시 해줘", "잘못됐어" 등 피드백 시
- 코드 실행 에러 발생 시
- 테스트 실패 시
- 사용자가 수동으로 수정한 경우

#### 실수 기록 형식
```markdown
## 🚨 실수 기록 (반복 금지)

### [{날짜}] {실수 카테고리}
**상황:** {무엇을 하려고 했는지}
**실수:** {무엇이 잘못되었는지}
**원인:** {왜 발생했는지}
**해결:** {어떻게 수정했는지}
**교훈:** {다음에 어떻게 해야 하는지}
```

#### 실수 카테고리
| 카테고리 | 예시 |
|---------|------|
| `문법 오류` | 잘못된 import, 오타, 구문 에러 |
| `로직 오류` | 조건문 실수, 무한 루프, off-by-one |
| `타입 오류` | TypeScript 타입 불일치, any 남용 |
| `구조 오류` | 잘못된 디렉토리, 파일명 규칙 위반 |
| `API 오류` | 잘못된 엔드포인트, 파라미터 누락 |
| `환경 오류` | 환경 변수 누락, 설정 실수 |
| `이해 오류` | 사용자 의도 오해, 요구사항 누락 |

#### 세션 시작 시 동작
1. CLAUDE.md의 `🚨 실수 기록` 섹션을 **먼저 읽는다**
2. 기록된 실수 패턴을 **메모리에 로드**한다
3. 작업 수행 전 "이전에 이런 실수를 했는지" **자가 점검**한다
4. 유사한 상황에서 **같은 실수를 반복하지 않는다**

## 출력 위치

- **CLAUDE.md**: 프로젝트 루트 (`/project-root/CLAUDE.md`)
- **Agent.md**: `.claude/agents/` 디렉토리 또는 `~/.claude/agents/`

---

## CLAUDE.md 템플릿

```markdown
# {프로젝트명}

{한 줄 프로젝트 설명}

## 기술 스택

- **프레임워크**: {예: Next.js 15}
- **언어**: {예: TypeScript 5.x}
- **스타일링**: {예: Tailwind CSS}
- **DB**: {예: Supabase}
- **배포**: {예: Vercel}

## 프로젝트 구조

{루트}/
├── {폴더1}/         # {설명}
├── {폴더2}/         # {설명}
├── {폴더3}/         # {설명}
└── {폴더4}/         # {설명}

## 코딩 규칙

### 네이밍 컨벤션
- 컴포넌트: {예: PascalCase}
- 파일: {예: kebab-case}
- 변수/함수: {예: camelCase}
- 상수: {예: SCREAMING_SNAKE}

### 컴포넌트 구조
- {규칙 1}
- {규칙 2}
- {규칙 3}

### 금지 사항
- {피해야 할 패턴 1}
- {피해야 할 패턴 2}

## MCP 서버

### {MCP명}
- **용도**: {설명}
- **권한**: {Read-only / Read-Write}
- **주요 명령**: {명령어들}

## 워크플로우

### 새 기능 개발
1. {단계 1}
2. {단계 2}
3. {단계 3}

### 테스트
- 단위 테스트: `{명령어}`
- 통합 테스트: `{명령어}`

### 배포
- 개발: `{명령어}`
- 프로덕션: `{명령어}`

## 환경 변수

# 필수
{VAR_NAME_1}=
{VAR_NAME_2}=

# 선택
{VAR_NAME_3}=

## 사용 가능한 에이전트

- `@{에이전트1}`: {설명}
- `@{에이전트2}`: {설명}

---

## 🚨 실수 기록 (반복 금지)

<!--
형식:
### [{날짜}] {카테고리}
**상황:** 무엇을 하려고 했는지
**실수:** 무엇이 잘못되었는지
**원인:** 왜 발생했는지
**해결:** 어떻게 수정했는지
**교훈:** 다음에 어떻게 해야 하는지
-->

---

## 📝 세션 학습 기록

<!-- @update-context 호출 시 아래에 추가됨 -->
```

---

## Agent.md 템플릿

```markdown
---
name: {에이전트명}
description: {한 줄 역할 설명}
tools: {Read, Write, Edit, Bash, Grep, Glob 중 필요한 것만}
model: {sonnet|haiku|opus}
---

# 역할

{에이전트의 역할과 책임을 명확히 기술}

## 작업 범위

- {수행하는 작업 1}
- {수행하는 작업 2}
- {수행하는 작업 3}

## 규칙

1. **{규칙 카테고리 1}**
   - {세부 규칙}
   - {세부 규칙}

2. **{규칙 카테고리 2}**
   - {세부 규칙}
   - {세부 규칙}

## 출력 형식

🔴 Critical: {즉시 조치 필요}
🟡 Warning: {개선 권장}
✅ Good: {모범 사례}

## 참조

- 프로젝트 CLAUDE.md를 먼저 읽고 규칙 준수
- {추가 참조 사항}
```

---

## CLAUDE.md 작성 가이드

### 핵심 원칙
1. **간결함 유지** - 컨텍스트 윈도우는 공유 자원, 토큰 절약 필수. Claude가 이미 아는 일반적인 내용 생략. 프로젝트 고유 정보만 포함.
2. **명령형 문체** - "~합니다" 대신 "~한다" 또는 "~할 것"
3. **구조화된 정보** - 명확한 헤더 계층, 코드 블록으로 예시, 불필요한 설명 없이 바로 규칙 제시

### 안티패턴
- ❌ 너무 장황한 설명
- ❌ Claude가 이미 아는 일반 지식
- ✅ 간결하고 프로젝트 고유 정보만

---

## Agent.md 작성 가이드

### 파일 위치
| 위치 | 용도 |
|-----|-----|
| `~/.claude/agents/` | 전역 에이전트 (모든 프로젝트에서 사용) |
| `.claude/agents/` | 프로젝트 전용 에이전트 |

### Frontmatter 필드
- **name** (필수): 호출명 (`@name`으로 사용)
- **description** (필수): 에이전트 역할 설명
- **tools** (선택): 허용 도구 제한 (보안용)
- **model** (선택): haiku(빠른), sonnet(균형, 기본), opus(복잡한 추론)

### 프로젝트 유형별 에이전트 예시

**웹 프론트엔드**: @ui-reviewer (UI/UX 품질 검토), @a11y-checker (WCAG 2.1 AA 접근성 검사)
**백엔드 API**: @api-designer (RESTful API 설계), @security-auditor (OWASP Top 10 보안 검사)
**풀스택**: @architect (시스템 아키텍처 설계), @test-writer (TDD 기반 테스트 작성)
**노코드/자동화**: @workflow-optimizer (n8n/Make 워크플로우 최적화)
**AI/ML**: @prompt-engineer (LLM 프롬프트 최적화)

### 모범 사례
- ✅ 도구 권한 최소화 (필요한 것만)
- ✅ 명확한 출력 형식 정의
- ✅ CLAUDE.md 참조 명시
- ✅ 작업 범위 명확히 제한
- ❌ 과도한 도구 권한 부여
- ❌ 모호한 역할 정의
- ❌ 너무 긴 시스템 프롬프트

---

## 기술 스택별 베스트 프랙티스

### 웹 프론트엔드

**Next.js 14+**: App Router 사용, Server Components 기본, 'use client' 필요시만, 서버 액션으로 폼 처리, Suspense + loading.tsx, error.tsx 에러 바운더리

**React 18+**: 함수형 컴포넌트만, Hooks 규칙 준수, memo/useMemo/useCallback 적절히. 상태관리: 로컬(useState), 전역(Zustand), 서버(TanStack Query)

**Vue 3**: Composition API (<script setup>), ref vs reactive 구분, Pinia 스토어

**Tailwind CSS**: 유틸리티 클래스 순서(레이아웃→크기→색상→기타), @apply 최소화, 반응형(sm:640/md:768/lg:1024/xl:1280)

### 백엔드

**Node.js (Express/Fastify)**: async/await 사용, 에러는 next(error), 환경변수 dotenv, 입력 검증(Zod/Joi)

**Python (FastAPI)**: 타입 힌트 필수, Pydantic 검증, async def 활용, DI 패턴

**Go**: 에러는 반환값으로, 인터페이스는 사용측에서 정의, context.Context 전파, defer 리소스 정리

### 풀스택

**Supabase**: RLS 필수, 테이블 생성 직후 RLS 정책, 클라이언트: anon key만, 서버: service_role key

**Prisma**: schema.prisma 모델 정의, 마이그레이션, 트랜잭션 prisma.$transaction()

### 노코드/로우코드

**n8n**: 에러 핸들링 노드 필수, 민감정보 Credentials, 웹훅 URL 노출 주의

**Make**: 시나리오 명명 규칙, 에러 핸들러 모듈, Iterator/Aggregator/Router 패턴

### 모바일

**React Native**: Expo 권장, StyleSheet.create(), React Navigation, Zustand + MMKV

**Flutter**: 위젯 분리, const 생성자, StatelessWidget 기본, Riverpod/Bloc

### AI/ML

**LangChain**: 체인 조합, 프롬프트 템플릿 분리, RAG(문서→청킹→임베딩→검색), Agent(도구→계획→실행)

**OpenAI API**: API 키 환경변수, 토큰 제한, 스트리밍 응답, JSON 모드

### 검색 쿼리 템플릿
- `{기술명} best practices 2026`
- `{기술명} project structure recommended`
- `{기술명} common mistakes to avoid`
- `{기술명} production checklist`
