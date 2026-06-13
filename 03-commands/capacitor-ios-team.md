# Capacitor iOS Team

Next.js 웹앱에 Capacitor iOS 네이티브 앱을 추가하는 전문 에이전트 팀.

$ARGUMENTS

---

@.skills/capacitor-ios-team/README.md

---

## 실행 프로토콜

### Step 0: 정찰 (Scout)

대상 프로젝트 경로가 `$ARGUMENTS`에 없으면 현재 작업 디렉토리를 사용한다.
Explore 에이전트로 프로젝트를 파악한다:

- package.json: 프레임워크, 의존성, 기존 스크립트
- next.config: output 설정, 이미지 최적화, 리다이렉트 등
- src/app/ 구조: 라우트, 레이아웃, 서버 컴포넌트 사용 현황
- 'use server', 'use client' 디렉티브 분포
- 서버 액션, Route Handler, 미들웨어 사용 여부
- 환경변수 중 NEXT_PUBLIC_ 접두사 없이 서버에서만 쓰는 것
- 인증 방식 (Supabase Auth, Clerk, NextAuth 등)
- 이미 Capacitor 관련 설정이 있는지 (패키지, config, ios/ 폴더)

결과를 `native-context.md`로 프로젝트 루트에 저장한다.

**SSR 호환성 위험도를 3단계로 평가:**
- LOW: 대부분 클라이언트 컴포넌트, 서버 액션 적음 → 바로 진행
- MEDIUM: 일부 SSR/서버 액션 사용 → 분기 처리 필요한 파일 목록 작성
- HIGH: SSR 의존도 높음 → 사용자에게 전략 변경 제안 (SSG 전환 범위 확인)

### Step 1: Capacitor 셋업

native-context.md를 기반으로 executor 에이전트(model: opus)가 순차 실행:

#### 1-1. 패키지 설치
```bash
npm install @capacitor/core @capacitor/cli @capacitor/ios
npm install @capacitor/status-bar @capacitor/splash-screen @capacitor/haptics @capacitor/keyboard
```
- 추가 플러그인은 native-context.md에서 파악한 기능 기반으로 판단
  - 클립보드 사용 → @capacitor/clipboard
  - 공유 기능 → @capacitor/share
  - 카메라 → @capacitor/camera
  - 푸시 알림 → @capacitor/push-notifications

#### 1-2. capacitor.config.ts 생성
```typescript
import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: '번들ID (ARGUMENTS에서 추출 또는 com.앱이름.app)',
  appName: '앱이름 (ARGUMENTS에서 추출)',
  webDir: 'out',
  server: {
    // 개발 시에만 사용, 프로덕션 빌드에서는 제거
    // url: 'http://localhost:3000',
    // cleartext: true,
  },
  ios: {
    contentInset: 'automatic',
    scheme: '앱이름',
  },
};

export default config;
```

#### 1-3. next.config 빌드 분기
- `CAPACITOR_BUILD=true`일 때 `output: 'export'` 추가
- `images.unoptimized: true` 추가 (정적 export에서 next/image 호환)
- 기존 웹 빌드에는 영향 없도록 조건부 적용

#### 1-4. 플랫폼 분기 구조 생성

**src/lib/platform.ts:**
```typescript
import { Capacitor } from '@capacitor/core';

export const isNative = Capacitor.isNativePlatform();
export const isIOS = Capacitor.getPlatform() === 'ios';
export const isAndroid = Capacitor.getPlatform() === 'android';
export const isWeb = !isNative;
```

**src/styles/native.css:**
```css
.native-app {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  overscroll-behavior: none;
  -webkit-user-select: none;
  user-select: none;
}

.native-app * {
  -webkit-tap-highlight-color: transparent;
}

/* 네이티브에서 pull-to-refresh 방지 */
.native-app body {
  overflow: hidden;
}

.native-app #__next {
  height: 100vh;
  height: 100dvh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
```

**layout.tsx 수정:**
- html 태그에 `className={isNative ? 'native-app' : ''}` 추가
- native.css import 추가
- StatusBar 플러그인 초기화 (isNative일 때만)

#### 1-5. native/ 폴더 컨벤션 설정
- `src/components/native/` 디렉토리 생성
- `src/hooks/native/` 디렉토리 생성
- `src/lib/native/` 디렉토리 생성
- 각 폴더에 빈 .gitkeep 또는 index.ts 배치

#### 1-6. .gitignore 업데이트
```
# Capacitor iOS
ios/App/Pods/
ios/App/DerivedData/
ios/App/build/
ios/App/App/public/
```

#### 1-7. CLAUDE.md 업데이트
네이티브 앱 규칙 섹션 추가:
```markdown
# 네이티브 앱 규칙
- 플랫폼 분기: src/lib/platform.ts의 isNative/isWeb 사용
- 네이티브 전용 코드: src/**/native/ 폴더에 배치
- ios/ 폴더: 직접 수정 금지, cap sync로만 변경
- 빌드: 웹은 `npm run build`, 네이티브는 `npm run build:native`
- CSS: 네이티브 전용 스타일은 .native-app 클래스 스코프 안에서
- 기능 추가 시: 웹에서 먼저 동작 확인 → cap:sync → iOS 확인
- 커밋: 웹 변경과 ios/ 변경은 별도 커밋으로 분리
- 서버 전용 코드(서버 액션, Route Handler)는 네이티브에서 동작 안 함 → isWeb 분기 필수
```

#### 1-8. iOS 프로젝트 생성
```bash
npm run build:native
npx cap add ios
npx cap sync
```

### Step 2: 병렬 검증 (4개 에이전트 동시)

**반드시 4개를 하나의 메시지에서 병렬 Agent 호출로 실행한다.**

#### 2-1. web-build (웹 빌드 검증)
- **에이전트**: `oh-my-claudecode:verifier`
- **점검**:
  - `npm run build` 성공 여부 (기존 웹 빌드 깨짐 없는지)
  - `npm run type-check` 통과 여부
  - platform.ts import로 인한 Capacitor 런타임 에러 없는지 (웹에서)
- **산출물**: 검증 결과를 `native-setup-report.md`의 "웹 빌드" 섹션에 기록

#### 2-2. native-build (네이티브 빌드 검증)
- **에이전트**: `oh-my-claudecode:verifier`
- **점검**:
  - `npm run build:native` 성공 (output: 'export' 정상 동작)
  - `out/` 디렉토리에 정적 파일 생성 확인
  - `npx cap sync` 성공
  - 동적 라우트가 정적 export에서 에러 나는지 (generateStaticParams 누락 등)
- **산출물**: 검증 결과를 `native-setup-report.md`의 "네이티브 빌드" 섹션에 기록

#### 2-3. compat-check (호환성 점검)
- **에이전트**: `oh-my-claudecode:code-reviewer` (model: opus)
- **점검**:
  - `'use server'` 디렉티브가 있는 서버 액션 → 네이티브에서 호출 가능 여부
  - Route Handler (app/api/**/route.ts) → 네이티브에서 접근 경로 (절대 URL 필요)
  - `cookies()`, `headers()` 등 서버 전용 API 사용 위치
  - `NEXT_PUBLIC_` 없는 환경변수가 클라이언트에서 참조되는 경우
  - `next/image` → 정적 export에서 `unoptimized: true` 적용 확인
  - `next/link` → 네이티브에서 라우팅 정상 동작 여부
  - 미들웨어/프록시 → 정적 export에서 무시됨, 대체 필요 여부
- **산출물**: 검증 결과를 `native-setup-report.md`의 "호환성" 섹션에 기록

#### 2-4. mobile-ux (모바일 UX 감사)
- **에이전트**: `oh-my-claudecode:designer`
- **점검**:
  - safe-area 패딩 적용 확인 (노치/다이나믹 아일랜드 영역)
  - 터치 타겟 최소 크기 (44x44px) 준수
  - 스크롤 컨테이너 중첩 여부 (네이티브에서 제스처 충돌)
  - 모달/드롭다운이 키보드와 겹치는 경우
  - 폰트 크기 최소 16px (iOS auto-zoom 방지)
  - position: fixed 요소의 safe-area 대응
  - 가로 스크롤 overflow 방지 (모바일에서 의도치 않은 스와이프)
- **산출물**: 검증 결과를 `native-setup-report.md`의 "모바일 UX" 섹션에 기록

### Step 3: 수정 & 재검증

Step 2에서 발견된 이슈를 심각도순으로 수정한다:

1. `native-setup-report.md`의 4개 섹션을 모두 읽는다
2. 빌드 실패 이슈를 먼저 수정 (CRITICAL)
3. 호환성 이슈 수정 (HIGH) — 서버 코드 분기, 환경변수 정리 등
4. UX 이슈 수정 (MEDIUM) — safe-area, 터치 타겟 등
5. 수정 후 `npm run build` + `npm run build:native` + `npx cap sync` 재실행
6. 모두 통과하면 `native-setup-report.md`에 최종 결과 기록

### 완료 후

사용자에게 보고:
- 셋업 성공/실패 여부
- 수정한 이슈 요약
- 다음 단계 안내:
  - `npx cap open ios` → Xcode에서 시뮬레이터 실행
  - 실기기 테스트 시 Apple Developer 계정 + 코드 서명 필요
  - App Store 배포 시 fastlane 설정 권장
