# Capacitor iOS Team

Next.js 웹앱에 Capacitor iOS 네이티브 앱을 추가하는 전문 에이전트 팀.
셋업부터 빌드 검증까지 병렬 에이전트가 역할 분담하여 진행합니다.

## 워크플로우

```
[프로젝트 경로 + 앱 설정 입력]
         │
         ▼
┌─────────────────────────────────────────────┐
│  0. scout (정찰 에이전트)                      │
│     - 프로젝트 구조 파악                       │
│     - SSR/동적 기능 사용 현황 분석              │
│     - 정적 export 호환성 사전 점검              │
│     - native-context.md 작성                  │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  1. 순차 셋업 (executor 에이전트)              │
│     - Capacitor 패키지 설치                   │
│     - capacitor.config.ts 생성               │
│     - next.config 빌드 분기 추가              │
│     - 플랫폼 분기 구조 생성                    │
│       (platform.ts, native/, native.css)     │
│     - .gitignore & CLAUDE.md 업데이트         │
│     - cap add ios                            │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  2. 병렬 검증 (4개 에이전트 동시)              │
│                                              │
│  [web-build]        [native-build]           │
│  npm run build      npm run build:native     │
│  기존 웹 깨짐 없는지  정적 export 성공 여부     │
│  SSR 기능 정상 여부   cap sync 성공 여부       │
│                                              │
│  [compat-check]     [mobile-ux]              │
│  SSR 전용 코드 탐지   safe-area 적용 확인      │
│  서버 액션 분기 필요   터치 타겟 크기 (44px+)   │
│  환경변수 노출 체크    스크롤/제스처 충돌        │
│  인증 flow 호환성     상태바 영역 겹침          │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  3. fix-and-verify (수정 에이전트)             │
│     - 2단계에서 발견된 이슈 자동 수정           │
│     - 웹 빌드 + 네이티브 빌드 재검증            │
│     - 최종 상태 보고                          │
└─────────────────────────────────────────────┘
         │
         ▼
[iOS 시뮬레이터 실행 가능 상태]
```

## 에이전트 역할표

| 단계 | 에이전트 | 모델 | 역할 |
|------|---------|------|------|
| 0 | Explore | - | 프로젝트 정찰, SSR 분석 |
| 1 | oh-my-claudecode:executor | opus | Capacitor 셋업 전체 |
| 2-1 | oh-my-claudecode:verifier | sonnet | 웹 빌드 검증 |
| 2-2 | oh-my-claudecode:verifier | sonnet | 네이티브 빌드 검증 |
| 2-3 | oh-my-claudecode:code-reviewer | opus | SSR/서버 코드 호환성 점검 |
| 2-4 | oh-my-claudecode:designer | sonnet | 모바일 UX 적합성 감사 |
| 3 | oh-my-claudecode:executor | sonnet | 이슈 수정 + 재검증 |

## 산출물

| 파일 | 내용 |
|------|------|
| `native-context.md` | 프로젝트 분석 결과 & SSR 사용 현황 |
| `src/lib/platform.ts` | 플랫폼 감지 유틸 |
| `src/styles/native.css` | iOS 전용 스타일 |
| `capacitor.config.ts` | Capacitor 설정 |
| `ios/` | Xcode 프로젝트 |
| `native-setup-report.md` | 최종 셋업 보고서 (이슈 & 해결 내역) |
