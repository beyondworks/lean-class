---
name: card-news
description: 카드뉴스 자동 생성 에이전트 (Threads/Instagram용)
---

# card-news 에이전트 팀 스킬

주제를 입력하면 에이전트 팀이 리서치 → 카피 → 후킹 검증 → 구조 검토 → PNG 렌더링을 자동 수행한다.

## 사용법

```
/card-news "주제"
/card-news "주제" --cards 10 --brand myBrand --tone casual
/card-news template "디자인 이미지 경로" --name "템플릿이름"
```

- `--cards`: 카드 수 (기본 10, 범위 5~10)
- `--brand`: brands/ 폴더의 브랜드 이름 (기본 "default")
- `--tone`: professional | casual | academic
- `template`: 5단계 커스텀 템플릿 생성 모드

## 프로젝트 경로

```
~/Desktop/Appbuild/Agents/Cardnews
```

## 에이전트 팀 파이프라인

```
[사용자: 주제 입력]
       |
       v
  1. researcher ---- 웹 리서치 + 10장 카피 초안
       |
       v
  2. hooking-expert + copy-editor ---- 후킹력 + 카피 품질 채점
       |                                    |
       | (7점 미만)                          | (7점 이상)
       v                                    v
  researcher 재작성 (최대 3회)         3. structure-reviewer ---- 10장 흐름 검토
                                           |
                                           v
                                    4. renderer ---- HTML → PNG (1080x1350)
                                           |
                                           v
                                    [output/ 폴더에 결과물]
```

## Claude 실행 지침

### Phase 0: 환경 준비

```bash
cd ~/Desktop/Appbuild/Agents/Cardnews
mkdir -p working
```

### Phase 1: 리서치 + 카피 (researcher 에이전트)

1. 사용자의 명령에서 **주제(topic)**를 파싱한다.
   - 인자가 없으면 "어떤 주제로 카드뉴스를 만들까요?"라고 물어본다.
2. `template` 서브커맨드면 Phase 5로 직접 이동한다.

**researcher 에이전트를 실행한다:**

에이전트에게 전달할 작업:
- WebSearch로 주제에 대해 5~7회 검색
- 핵심 인사이트 10개 이상 추출 (통계 데이터 최소 2개)
- 10장 카드 카피 초안 작성 (cover 1 + content/data/quote 혼합 8 + cta 1)
- `working/card-draft.json` 파일로 저장

카드 타입 배분 기준:
- content: 60% (5~6장)
- data: 25% (2장, 반드시 수치 포함)
- quote: 15% (1~2장)

카피 규칙:
- 제목(title): 40자 이내, SNS 훅처럼 강렬하게
- 본문(body): 80자 이내, 하나의 메시지
- 데이터(dataValue): 숫자+단위 (예: "76%", "$15.2B")
- 한국어만, 마크다운/특수기호/이모지 금지

### Phase 2: 후킹 팀 토론 (hooking-expert + copy-editor)

**두 에이전트를 병렬로 실행한다:**

**hooking-expert 에이전트:**
- `working/card-draft.json` 읽기
- 각 카드의 "스크롤 멈춤력" 10점 만점 채점
- 커버 카드 가중치 3x, 콘텐츠 2x
- `working/hooking-review.json` 저장

**copy-editor 에이전트:**
- `working/card-draft.json` 읽기
- 문장 품질, 가독성, 정확성, 톤 일관성 10점 만점 채점
- `working/copy-review.json` 저장

**판정:**
- 두 점수의 평균이 7.0점 이상 AND 개별 카드 최저 5.0점 이상 → Phase 3으로
- 미달 → researcher 에이전트에게 재작성 요청:
  - `hooking-review.json`과 `copy-review.json`의 `mustFix` 카드 + 개선안 전달
  - 해당 카드만 수정하여 `card-draft.json` 업데이트
  - Phase 2 재실행 (최대 3회)
- 3회 후에도 미달 → 최고 점수 버전으로 진행하며 사용자에게 알림

### Phase 3: 구조 검토 (structure-reviewer 에이전트)

**structure-reviewer 에이전트를 실행한다:**
- `working/card-draft.json` + 후킹/카피 리뷰 파일 읽기
- 10장 서사 아크 (기승전결) 검토
- 정보 흐름, 카드 타입 배치, 이탈 방지 점검
- `working/structure-review.json` 저장

구조 점수 7점 이상이면 Phase 4로.
미달이면 카드 순서 변경안 반영 후 `card-draft.json` 업데이트.

### Phase 4: PNG 렌더링 (renderer 에이전트)

**renderer 에이전트를 실행한다:**

1. `working/card-draft.json`의 cards를 ResearchResult 형식으로 변환
2. `working/research-for-render.json` 저장
3. 커스텀 템플릿 존재 여부 확인: `templates/custom-*/`
4. orchestrator.ts 실행:

```bash
cd ~/Desktop/Appbuild/Agents/Cardnews
npx tsx src/orchestrator.ts "TOPIC" --cards N --brand BRAND --research working/research-for-render.json
```

5. 생성된 모든 PNG를 Read로 열어서 시각 검증:
   - 텍스트 잘림 없음
   - 폰트 로드 정상
   - 색상 대비 충분
   - 카드 번호 정확

6. 문제 발견 시 사용자에게 보고, 코드 수정 → 재렌더링 제안.

### Phase 5: 템플릿 커스터마이징 (template-designer 에이전트)

`/card-news template` 으로 호출 시만 실행:

**template-designer 에이전트를 실행한다:**
- 사용자가 전달한 디자인 이미지를 Read로 분석
- 색상 팔레트, 타이포그래피, 레이아웃 패턴 추출
- 5종 카드 HTML 템플릿 + theme.json 생성
- `templates/custom-{name}/` 에 저장
- 샘플 데이터로 미리보기 PNG 생성

### Phase 6: 결과 보고

1. 출력 디렉토리 경로 안내
2. 생성된 카드 목록 (파일명 + 타입) 표시
3. 후킹 점수 / 카피 점수 / 구조 점수 요약 표시
4. `caption.md` 읽어서 Instagram/Threads 캡션 출력
5. 재작성 횟수가 있었으면 점수 변화 추이 표시

## 출력 구조

```
output/{timestamp}_{topic}/
  01_cover.png
  02_content.png
  ...
  10_cta.png
  caption.md    ← Instagram / Threads 캡션
  sources.md    ← 출처 목록 (등급 포함)
```

## 중간 산출물

```
working/
  card-draft.json          ← 카드 카피 (v1, v2, v3...)
  hooking-review.json      ← 후킹 점수
  copy-review.json         ← 카피 품질 점수
  structure-review.json    ← 구조 검토
  research-for-render.json ← 렌더링용 리서치 데이터
```

## 오류 처리

- `--cards`가 5~10 범위 밖이면 올바른 범위 안내
- Playwright 미설치 시: `npx playwright install chromium` 안내
- WebSearch 실패 시: 사용자에게 리서치 데이터 직접 전달 요청
- 렌더링 실패 시: 에러 로그 확인 후 원인 보고
- 3회 재작성 후에도 7점 미만 시: 현재 최고 점수 버전으로 진행, 점수 공개
