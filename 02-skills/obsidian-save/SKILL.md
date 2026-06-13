---
name: obsidian-save
description: 사용자가 "옵시디언에 저장해줘", "vault에 저장", "save to obsidian", "이거 저장해" 같은 자연어로 요청하면 발동. 현재 컨텍스트(질문/답변/검색결과/대화 요약/파일 분석 등)를 AI-Sessions-Vault의 Karpathy LLM Wiki 구조에 맞게 자동 분류·파일명 생성·frontmatter 부착하여 저장하고, index.md/log.md를 갱신한 뒤 vault-lint.sh로 정합 검증까지 수행한다. vault AGENTS.md의 강제 self-check 체크리스트(사전점검·save vs ingest 구분·projects 명명 차단·사후 lint)를 반드시 따른다. 사용자가 vault 구조를 몰라도 이 스킬이 모든 의사결정을 자동 처리한다.
triggers: ["옵시디언에 저장", "옵시디언 저장", "옵시디언에 보관", "vault에 저장", "vault 저장", "obsidian save", "save to obsidian", "save to vault", "이거 저장해", "이 답변 저장", "방금 답변 저장", "이거 wiki에 저장", "wiki에 저장"]
---

# obsidian-save

자연어 한 마디로 vault에 저장하는 스킬. 사용자는 카파시 패턴을 몰라도 됨. **단, 본 스킬은 vault 의 [`AGENTS.md`](AGENTS.md) 강제 self-check 체크리스트를 따른다 — 사전점검·lint 게이트·사후검증 모두 의무**.

## 발동 조건

사용자 메시지가 다음 중 하나를 포함:
- "옵시디언에 저장", "옵시디언 저장", "옵시디언에 보관"
- "vault에 저장", "wiki에 저장"
- "obsidian save", "save to obsidian", "save to vault"
- "이거 저장해", "이 답변 저장", "방금 답변 저장"

발동 시 사용자에게 "어떤 카테고리로 저장할까요?" 같은 되묻기 **없이** 자동 결정 후 진행. 결과가 마음에 안 들면 사용자가 사후에 수정 요청한다.

## 🚨 사전점검 (0단계, 건너뛰기 금지)

**저장 작업 시작 전 반드시 다음을 수행한다. 빠지면 카파시 설계가 무너진다.**

1. **vault `AGENTS.md` 읽기** — `~/Documents/AI-Sessions-Vault/AGENTS.md`. 작업 종류별(save/ingest/lint/handoff/destructive) 체크리스트 확인
2. **vault `index.md` 읽기** — 같은 슬러그가 이미 있는지, 카테고리 정리 큐가 있는지 확인
3. **`bash scripts/vault-lint.sh --quiet` 실행** — vault 루트에서. exit 0 이 아니면:
   - 명명 위반·broken link 등 fail 항목이 있으면 → 사용자에게 "vault lint 실패 상태. 저장 진행 전 정리 권장. 그래도 진행?" 1회 확인
   - 사용자가 "진행", "맞아", "반영해서 기록", "계속"처럼 진행 의사를 확인하면 새 저장을 진행하고, 같은 lint 실패로 다시 묻지 않는다. 사후 보고서에는 기존 fail과 이번 저장 관련 fail을 분리해 명시한다.
   - 기존 fail이 projects 명명 위반처럼 이번 save와 무관하면, 새 페이지/index/log의 생성·등재·cross-link 검증을 별도로 수행해 "저장 자체는 성공, 기존 lint fail 잔존"으로 보고한다.
4. **save vs ingest 구분** (CLAUDE.md 의 비교표):
   - 외부 1차 자료(웹 아티클·논문·영상 transcript)는 save 가 아니라 **ingest** 절차로 우회. 사용자에게 "이건 외부 자료라 raw/ 에 두고 ingest 하는 게 카파시 룰입니다. raw 로 복사할까요, 아니면 save 로 강행할까요?" 1회 확인
   - 사용자의 합성 결과물·의사결정·playbook 은 save 진행

## 대상 vault

```
~/Documents/AI-Sessions-Vault/
├── CLAUDE.md       (운영 규약 — 따른다)
├── index.md        (저장 후 갱신 대상)
├── log.md          (저장 후 append 대상)
└── AI-Sessions/
    ├── raw/inbox/  (분류 모호할 때 fallback)
    └── wiki/{sources,concepts,decisions,playbooks,projects,entities,errors,synthesis}/
```

## 프로젝트별 참고 자료


## Handoff / scheduled status note 처리

예약 작업이나 사용자가 “handoff”, “work-status”, “세션 상태 기록”, “3시간 주기 상태 노트”를 요청하면 일반 save/ingest가 아니라 **handoff**로 처리한다.

- 대상 경로는 vault 규칙의 `AI-Sessions/conversations/{agent-or-project}/YYYY-MM-DD-HHMM-{agent-or-project}-work-status.md` 또는 명시된 handover 파일명 패턴을 따른다.
- 쓰기 전 `AGENTS.md`, `CLAUDE.md`, `index.md`, `log.md`를 읽고, 가능하면 `bash scripts/vault-lint.sh`를 사전 실행한다.
- 사전 lint가 기존 wiki/projects 명명 위반·orphan·raw/sources warning 등 이번 handoff와 무관한 이슈로 실패해도, cron/무인 실행에서는 기존 raw·기존 conversations 파일을 건드리지 말고 새 handoff와 `log.md` append만 안전하게 진행한다. 사용자 확인을 기다리지 않는다.
- handoff는 wiki save/ingest가 아니므로 `index.md`를 갱신하지 않는다.
- 노트 내용은 handoff-level이어야 한다: 현재 초점, 마지막 행동, 결정/가정, 블로커, 다음 주기 계획, 파일/아티팩트 상태, 다른 에이전트가 알아야 할 점, lint 요약.
- `log.md`에는 `## [YYYY-MM-DD HH:MM] handoff | AI-Sessions/conversations/...` 형식으로 1~2줄만 append한다.
- 여러 Lab/agent cron이 같은 분 단위에 동시에 append할 수 있다. `log.md`는 append-only로 다루되, 쓰기 직전 최신 tail을 다시 확인하고 가능하면 파일 끝에 새 항목만 추가한다. 외부 writer 경고가 나면 즉시 최신 tail을 재확인해 중복·순서 꼬임 여부만 보정하고, unrelated log 항목은 재작성하지 않는다.
- 사후 lint를 재실행하고, 실패 시 “이번 handoff 때문인지 / 기존 이슈인지”를 분리해 짧게 보고한다.
- **lint 요약은 현재 실행 출력에서만 작성한다.** 이전 handoff의 failure summary를 복붙하지 말고, 이번 lint에서 실제로 나온 항목만 적는다. 예: 현재 출력에 frontmatter/index 정합 실패가 없고 OK라면 “frontmatter/index 불일치”를 넣지 않는다.
- 직전 handoff 파일을 참고할 때는 연속성 확인(직전 경로, 실작업 유무, readiness)용으로만 사용한다. 직전 파일의 lint 문구나 “pending/완료 예정” 문구를 템플릿처럼 재사용하지 않는다. 새 handoff 본문은 현재 pre-lint 출력과 현재 작업 상태로 다시 작성한다.
- 사후 lint 결과를 handoff 파일에 업데이트한 뒤, 가능하면 한 번 더 lint를 실행해 그 업데이트 자체가 새 문제를 만들었는지 확인한다. 단, 동일한 기존 lint 실패가 반복되면 unrelated 파일을 고치거나 무한 재시도하지 말고 “기존 이슈 유지”로 종료한다.
- 사후 lint 반영 전에는 handoff 본문에 `갱신 예정`, `재검증 예정` 같은 미완료 표현이 남지 않게 한다. `log.md` append와 최종 lint를 마친 뒤 해당 노트를 `append 완료`, `사후: PASS/FAIL(exit N)`로 패치하고, 마지막 검증에서 파일 존재와 `log.md` tail의 내 항목 존재를 확인한다.
- 예약 cron handoff의 최종 응답은 **로컬 작업 보고만** 한다: 생성 경로 + `log.md` 갱신 + lint 결과. 사용자가 자동 전달 금지/무음 규칙을 명시한 경우에도, 실제 handoff 파일을 생성했다면 `[SILENT]`로 숨기지 않는다. `[SILENT]`는 정말 아무 변경도 없을 때만 사용한다.
- 동시 실행되는 다른 Lab cron이 같은 분에 `log.md`를 append할 수 있다. handoff 파일 작성 후 `log.md`를 append하기 직전 최신 tail을 다시 확인하고, 이미 다른 항목이 추가되어 있어도 기존 항목을 재작성하지 말고 내 항목만 파일 끝에 append한다. 사후 검증에서는 tail에 내 handoff 항목이 존재하는지만 확인한다.

## 절차 (5단계)

### 1. 컨텍스트 수집
저장 대상 결정. 우선순위:
1. 사용자가 "이 답변 저장"이라고 하면 → **직전 어시스턴트 응답** 전체
2. 사용자가 "이거 저장해"라고 하면 → **현재 대화 흐름의 마지막 분석/결과물**
3. 명시적 텍스트가 함께 오면 → 그 텍스트
4. 모호하면 → 직전 1~2개 turn의 핵심을 합쳐서 본문 작성

### 2. 카테고리 자동 결정 (decision tree)

| 컨텐츠가 ... 이면 | 카테고리 |
|---|---|
| 외부 아티클·논문·영상·책의 1차 요약 | `wiki/sources/` |
| 이론·패턴·프레임워크·개념 정의 | `wiki/concepts/` |
| "왜 X를 골랐나" 같은 의사결정 (ADR) | `wiki/decisions/` |
| 단계별 절차·체크리스트·반복 가능한 방법론 | `wiki/playbooks/` |
| 특정 프로젝트의 누적 지식·진행상황 | `wiki/projects/` |
| 사람·조직·도구·서비스 정보 | `wiki/entities/` |
| 시행착오 + 해결책 (같은 실수 방지용) | `wiki/errors/` |
| 비교·분석·여러 페이지 가로지르는 통찰·MOC | `wiki/synthesis/` |
| 위 어디에도 명확히 안 맞음 | `raw/inbox/` (사용자 사후 분류) |

**모호할 때 휴리스틱**:
- "이거 저장" 짧은 한 마디 + 직전 답변이 합성된 분석 → `wiki/synthesis/`
- 직전 답변이 외부 자료 요약 + URL 포함 → `wiki/sources/`
- 직전 답변이 단계 목록 + "...해라" 톤 → `wiki/playbooks/`
- "오늘 테스트한 2가지 프로젝트 기록"처럼 같은 umbrella 아래 여러 실험/런을 묶어달라는 요청 → `wiki/projects/` 단일 페이지로 저장하고 각 실험을 H2 섹션으로 분리
- 진짜 모호하면 → `raw/inbox/` + log에 reason 명시

### 3. 파일명 생성

- **sources**: `YYYY-MM-DD-{source_type}-{kebab-slug}.md`
  - `source_type`: article | paper | video | podcast | book | transcript | note
  - 예: `2026-05-04-article-karpathy-llm-wiki.md`
- **decisions**: `YYYY-MM-DD-{kebab-slug}.md` (시점 추적 필요)
- **그 외 (concepts/playbooks/entities/errors/synthesis)**: `{kebab-slug}.md` — **날짜 접두사 금지**
  - 예: `llm-wiki-pattern.md`, `vercel-vs-self-host.md`
- **projects**: **프로젝트명만** (`myproject.md`, `ttstudio.md`, `hermes.md`)
  - **금지 패턴 (lint 가 차단)**: `-session`, `-production`, `-2026-MM-DD`, `*-session-YYYY-MM-DD`
  - 같은 프로젝트의 새 세션은 별도 페이지 만들지 말 것 — 기존 페이지의 `## 세션 로그 YYYY-MM-DD` 섹션으로 append
  - `wiki/projects/{프로젝트}.md` 가 없으면 stub 생성 (frontmatter + 한 문장 요약), 본문 append
- **kebab-slug 생성 규칙**:
  - 본문 첫 H1 또는 핵심 키워드 추출 → lowercase + 한글 음차 또는 영어 키워드
  - 한글 가능 (예: `시각-디자인-원칙.md`) — Obsidian/git 모두 지원
  - 길이 50자 이내
- **충돌 시**: `{slug}-2.md`, `{slug}-3.md` 순으로
- **`_REVIEW-` 접두사 예약**: dry-run 보고서 전용. 일반 save 에서는 사용 금지

### 4. 파일 작성

frontmatter는 카테고리별로 분기:

**source 카테고리**:
```yaml
---
type: source
source_type: article|paper|video|podcast|book|transcript|note
title: '원문 제목'
author: ''
date_published: ''
url: ''
ingested: 'YYYY-MM-DD'
status: ingested
related: []
tags: []
---

> 한 문장 핵심 요약 (frontmatter 직후, 본문 시작)

## 핵심
- ...

## 상세
...

## 출처
- {URL 또는 원본 위치}
```

**그 외 모든 카테고리**:
```yaml
---
type: concept|decision|playbook|project|entity|error|synthesis
title: ''
status: seed
created: 'YYYY-MM-DD'
updated: 'YYYY-MM-DD'
related: []
tags: []
---

> 한 문장 핵심 요약

## 핵심
- ...

## 상세
...

## 관련
- [[관련-페이지-1]] — 이유 (있는 경우만)

## 출처
- 대화 컨텍스트 / 외부 URL (있는 경우만)
```

`Write` 도구로 절대 경로에 저장. 폴더가 없으면 `mkdir -p` 먼저.

### 5. index.md + log.md 갱신

**index.md**: vault 루트의 `~/Documents/AI-Sessions-Vault/index.md`. 해당 카테고리 섹션에 한 줄 추가:
```markdown
- [[file-stem]] — 한 줄 요약 (status)
```
"_(아직 없음...)_" placeholder가 있으면 제거.

상단 메타 갱신:
- `Last updated`: 현재 날짜
- `페이지 총합`: +1

카테고리 분포 표의 해당 카테고리 카운트 +1.

**log.md**: vault 루트의 `~/Documents/AI-Sessions-Vault/log.md`. append-only로 새 항목:
```markdown

## [YYYY-MM-DD HH:MM] save | wiki/{category}/{file-stem}
- 저장 트리거: "{사용자 발화 짧게 인용}"
- 카테고리 자동 결정 근거: {간단 설명}
- 본문 길이: {대략 N줄 / N단어}
```

### 6. 사후 검증 (필수, 건너뛰기 금지)

저장 후 다음을 반드시 수행:

```bash
cd ~/Documents/AI-Sessions-Vault
bash scripts/vault-lint.sh --quiet
echo "exit: $?"
```

**판정**:
- **exit 0** → 사용자에게 "lint pass" 보고
- **exit 1 + 새로 만든 페이지 때문** (예: orphan, 명명 위반, broken link) → **즉시 정정**:
  - orphan → 관련 페이지 1개에 [[link]] 추가
  - 명명 위반 → `projects/` 였다면 파일 rename(또는 기존 페이지로 흡수)
  - broken link → 해당 wikilink 수정
  - 정정 후 lint 재실행. 정정해도 안 되면 사용자에게 보고하고 결정 요청
- **exit 1 + 기존 fail 잔존** (이번 저장과 무관) → 사용자에게 "기존 fail N건 잔존. 저장 자체는 성공" 보고

추가 확인:
1. 저장된 파일이 실제 존재 (`ls`)
2. frontmatter 가 valid YAML
3. index.md 에 새 entry 등재됨 (`grep -F "[[file-stem]]"`)
4. log.md 마지막 항목이 이번 save (`tail -10 log.md`)
5. `related:` 필드에 `wiki/sources/legacy/` 직접 링크 없음

## 사용자 보고 형식 (필수)

저장 완료 후 사용자에게 다음 형식으로 보고:

```
저장 완료.
- 경로: ~/Documents/AI-Sessions-Vault/AI-Sessions/wiki/{category}/{file-name}.md
- 카테고리: {category} (자동 결정 근거: {1줄})
- 링크: [[{file-stem}]]
- 갱신: index.md, log.md
- lint: pass / fail (실패 항목 N건 — 본 저장과 무관/관련)
- 후속 권장: {있으면 1줄. 예: orphan 해소, 관련 페이지 cross-link}
```

이모지/마케팅 언어 금지(글로벌 communication 규칙).

### 진행 설명 언어

사용자에게 진행 과정을 설명할 때는 내부 도구명 대신 한글 의미 중심으로 말한다.

예:
- `skill_view` → `옵시디언 저장 규칙을 확인했어요.`
- `read_file` → `기존 index.md와 log.md를 읽었어요.`
- `write_file` → `새 노트를 작성했어요.`
- `patch` → `index.md를 갱신했어요.`
- `execute_code` → `저장 결과를 검증했어요.`

회색 도구 호출 박스는 시스템 생성이라 영어로 보일 수 있다. 하지만 assistant-authored 진행 보고와 최종 요약은 한글 작업 로그로 작성한다.

## 엣지 케이스

| 상황 | 처리 |
|---|---|
| vault가 존재하지 않음 | 사용자에게 vault 경로 확인 요청 후 중단 |
| 같은 slug 파일이 이미 존재 | `-2`, `-3` 접미사 추가, 사용자에게 알림 |
| 본문이 너무 짧음 (≤3줄) | 그래도 저장하되 `status: seed` 명시, "확장 권장" 메모 추가 |
| 본문이 매우 김 (>1000줄) | 그대로 저장. 사용자가 lint 시 분할 검토 |
| 카테고리 진짜 모호 | `raw/inbox/`로 저장 + 사용자에게 "분류 모호하여 inbox에 저장. 사후 이동 권장" |
| 한글 파일명 | 허용. Obsidian/git/macOS 모두 지원 |
| 시크릿 포함 의심 (API 키 패턴) | 저장 직전 grep으로 검출 → 발견 시 사용자에게 confirm 받기 (글로벌 security 규칙) |

## 예시 시나리오

**시나리오 1**: 사용자가 외부 아티클 분석 답변을 받은 직후 "이거 저장해"
→ 카테고리: `wiki/sources/` (URL/외부 출처 있음)
→ 파일명: `2026-05-04-article-{topic-slug}.md`
→ 보고: 경로 + "외부 아티클로 분류"

**시나리오 2**: 사용자가 의사결정 논의 후 "옵시디언에 저장해줘"
→ 카테고리: `wiki/decisions/` (선택 + 근거 패턴)
→ 파일명: `{decision-slug}.md`
→ 보고: 경로 + "의사결정으로 분류"

**시나리오 3**: 사용자가 단계별 워크플로우를 정리 후 "vault에 저장"
→ 카테고리: `wiki/playbooks/` (단계 목록)
→ 파일명: `{playbook-slug}.md`
→ 보고: 경로 + "반복 절차로 분류"

**시나리오 4**: 사용자가 "이 답변 저장" 했는데 답변이 잡담 + 한 줄 팁 혼합
→ 카테고리: `raw/inbox/` (모호)
→ 파일명: `YYYY-MM-DD-inbox-{slug}.md`
→ 보고: 경로 + "분류 모호. 추후 wiki로 distill 권장"

## 단순 save vs full ingest 구분 (vault CLAUDE.md 의 비교표 참조)

| 구분 | save (이 스킬) | ingest |
|---|---|---|
| 트리거 | "저장해", "save to obsidian" | "이거 정리해줘", "wiki 갱신", `raw/` 에 새 파일 |
| 입력 | 현재 대화의 분석·합성 결과물 | `raw/` 또는 `conversations/` 의 1차 자료 |
| 출력 | 카테고리 1개에 단일 페이지 | `wiki/sources/{slug}.md` + 영향 받는 다른 wiki 페이지 10~15개 cross-update |
| 함정 | save를 ingest로 착각하면 raw 없는 sources 생성 → 카파시 원칙 위반 | ingest 요청을 save로 처리하면 cross-update 누락 |

**외부 1차 자료 처리 원칙**: 웹 아티클·논문·영상 transcript 등 외부 자료는 sources 에 직접 save 금지. 반드시 `raw/articles|papers|notes` 에 두고 ingest 절차로 우회. save 트리거로 발동했더라도 이 패턴이면 사용자에게 1회 확인 후 우회.

사용자가 "ingest해줘", "전체 정리해줘", "wiki 갱신해줘"라고 명시적으로 말하면 full ingest로 확장. 그 외에는 save만 수행.

## 절대 금지 (vault-lint.sh 가 자동 차단)

- `wiki/projects/` 에 `-session`, `-production`, `-YYYY-MM-DD` 접미사 박힌 파일 생성
- 외부 자료를 save 로 `wiki/sources/` 에 직접 쓰기 (raw/ → ingest 우회 원칙)
- `related:` 필드에 `wiki/sources/legacy/` 페이지 직접 링크
- frontmatter 없이 wiki 페이지 생성
- orphan 페이지 생성 (최소 1 [[link]] 보장)
- vault-lint.sh fail 상태에서 신규 저장 진행 (1회 사용자 확인 없이)
- index.md 갱신 누락한 채 작업 종료
