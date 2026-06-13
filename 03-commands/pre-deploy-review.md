# Pre-Deploy Review Team

배포 전 코드베이스 전체를 6개 관점에서 병렬 리뷰하는 에이전트 팀.

$ARGUMENTS

---

@.skills/pre-deploy-review/README.md

---

## 실행 프로토콜

### Step 0: 정찰 (Scout)

대상 프로젝트 경로가 `$ARGUMENTS`에 없으면 현재 작업 디렉토리를 사용한다.
Explore 에이전트를 사용하여 프로젝트를 빠르게 파악한다:

- 프레임워크 & 기술 스택 (package.json, tsconfig, 설정 파일)
- 디렉토리 구조 & 라우트 맵
- 주요 진입점 (pages, app, routes)
- 환경변수 사용 현황 (.env.example)
- 테스트 커버리지 현황

결과를 `review-context.md`로 프로젝트 루트에 저장한다.

### Step 1: 병렬 리뷰 (6개 에이전트 동시)

review-context.md 내용을 각 에이전트에 전달하여 **반드시 6개를 동시에** 실행한다.
각 에이전트는 `run_in_background: true`가 아닌 **하나의 메시지에서 6개 Agent 호출을 병렬로** 실행한다.

#### 1-1. code-quality (코드 품질)
- **에이전트**: `oh-my-claudecode:code-reviewer` (model: opus)
- **점검 항목**:
  - 로직 결함 & 엣지 케이스 누락
  - Anti-patterns & code smells
  - SOLID 원칙 위반
  - 타입 안전성 (any, as, non-null assertion 남용)
  - 에러 핸들링 부재 (catch 없는 async, unhandled promise)
  - 불필요한 복잡도 (중첩 3단계+, 함수 50줄+)
  - 중복 코드 (DRY 위반)
- **산출물**: `review-code-quality.md` (프로젝트 루트)

#### 1-2. security (보안)
- **에이전트**: `security-reviewer`
- **점검 항목**:
  - OWASP Top 10 (XSS, SQLi, CSRF, SSRF 등)
  - 하드코딩된 시크릿/API 키/토큰
  - 인증/인가 누락 또는 우회 가능 경로
  - 입력 검증 부재 (사용자 입력 → DB/API 직접 전달)
  - 의존성 취약점 (알려진 CVE)
  - CORS 설정 문제
  - 민감 데이터 노출 (로그, 에러 메시지)
- **산출물**: `review-security.md` (프로젝트 루트)

#### 1-3. ux-audit (UX 감사)
- **에이전트**: `oh-my-claudecode:designer` (model: sonnet)
- **점검 항목**:
  - 사용자 흐름 일관성 (네비게이션, 뒤로가기, 상태 전이)
  - 로딩/에러/빈 상태 처리 여부
  - 폼 유효성 검사 & 에러 메시지 품질
  - 반응형 대응 (모바일/태블릿/데스크톱)
  - 시각적 일관성 (간격, 색상, 타이포그래피)
  - 사용자 피드백 (버튼 클릭 후 상태 변화, 토스트 등)
  - 다크모드 지원 상태 (있다면 깨진 부분)
- **산출물**: `review-ux.md` (프로젝트 루트)

#### 1-4. dead-feature (빈 기능 탐지)
- **에이전트**: `oh-my-claudecode:verifier`
- **점검 항목**:
  - UI는 있지만 핸들러가 미연결인 버튼/링크/폼
  - onClick/onSubmit이 빈 함수이거나 console.log만 있는 경우
  - TODO/FIXME/HACK/TEMP 주석이 있는 미완성 코드
  - 하드코딩된 mock 데이터가 실제 API 호출을 대체하는 경우
  - 라우트는 정의됐으나 페이지가 "Coming Soon" 또는 빈 컴포넌트인 경우
  - import 되었으나 사용되지 않는 모듈
  - 설정에 정의됐으나 실제 사용되지 않는 환경변수
  - disabled 상태로 하드코딩된 기능 플래그
- **산출물**: `review-dead-features.md` (프로젝트 루트)

#### 1-5. architecture (아키텍처)
- **에이전트**: `oh-my-claudecode:architect` (model: opus)
- **점검 항목**:
  - 모듈 간 의존성 방향 (순환 참조 여부)
  - 관심사 분리 (비즈니스 로직 ↔ UI ↔ 데이터)
  - API 경계 설계 (REST 규칙, 응답 일관성)
  - 에러 경계 & 장애 전파 범위
  - 확장성 병목 (N+1 쿼리, 동기 블로킹)
  - 상태 관리 복잡도 (props drilling, 전역 상태 남용)
  - 배포 환경 적합성 (환경변수, 빌드 설정)
- **산출물**: `review-architecture.md` (프로젝트 루트)

#### 1-6. a11y (접근성)
- **에이전트**: `accessibility-tester`
- **점검 항목**:
  - WCAG 2.1 AA 기준 준수
  - 시맨틱 HTML 사용 (div 남용 vs 적절한 태그)
  - 키보드 탐색 가능 여부 (Tab, Enter, Escape)
  - 스크린리더 호환 (aria-label, role, alt 텍스트)
  - 색상 대비 비율 (4.5:1 이상)
  - 포커스 표시기 가시성
  - 동적 콘텐츠 알림 (aria-live)
- **산출물**: `review-a11y.md` (프로젝트 루트)

### Step 2: 종합 (Synthesizer)

6개 리포트가 모두 완료되면 직접 통합 리포트를 작성한다:

1. 6개 리포트를 모두 읽는다
2. 심각도별로 정렬한다 (CRITICAL → HIGH → MEDIUM → LOW)
3. 중복 이슈를 제거하고 교차 관점 연결을 표시한다
4. 통계 요약을 작성한다 (관점별 이슈 수, 심각도별 분포)
5. 수정 우선순위 액션 플랜을 작성한다

최종 리포트 형식:

```markdown
# Pre-Deploy Review Report

## 요약
- 총 이슈: N개 (Critical: X, High: Y, Medium: Z, Low: W)
- 배포 판정: GO / NO-GO (Critical이 1개라도 있으면 NO-GO)

## Critical Issues (배포 차단)
...

## High Issues (배포 전 수정 권장)
...

## Medium Issues (조기 수정 권장)
...

## Low Issues (개선 사항)
...

## 교차 관점 인사이트
(여러 관점에서 동시에 지적된 영역)

## 액션 플랜
1. [즉시] ...
2. [배포 전] ...
3. [배포 후 1주 내] ...
4. [백로그] ...
```

`review-report.md`로 프로젝트 루트에 저장한다.

### 완료 후

사용자에게 다음을 보고한다:
- 배포 판정 (GO / NO-GO)
- Critical/High 이슈 요약 (3줄 이내)
- 전체 리포트 위치 안내
