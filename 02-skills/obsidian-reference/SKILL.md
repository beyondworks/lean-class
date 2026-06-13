---
name: obsidian-reference
description: Use when the user asks to reference, search, or learn newly reflected rules from the AI-Sessions-Vault / Obsidian vault, including prior handoffs, project wiki pages, lint status, and review queues.
triggers: ["옵시디언 참조", "옵시디언 참고", "옵시디언 봐", "옵시디언에서 찾아", "옵시디언에서 검색", "옵시디언 노트 가져와", "옵시디언 볼트에 반영된 규칙 숙지", "새 규칙 숙지", "vault 규칙 숙지", "obsidian reference", "obsidian ref", "obsidian search", "vault 참조", "vault 참고", "vault 검색", "wiki 참조", "wiki 검색", "이전 작업 참조", "이전 세션 참조", "이전 핸드오버", "지난번 어디까지"]
---

# obsidian-reference

자연어 한 마디로 vault에서 현재 프로젝트 관련 노트를 끌어오는 스킬. obsidian-save와 짝을 이룸. **읽기 전용이지만 vault 의 [`AGENTS.md`](AGENTS.md) 사전점검 룰은 동일하게 적용** — 사용자에게 stale·broken·정리 큐 정보를 함께 노출해야 카파시 wiki 가 살아 움직인다.

## 발동 조건

사용자 메시지가 다음 중 하나를 포함:
- "옵시디언 참조" / "옵시디언 참고" / "옵시디언 봐" / "옵시디언에서 찾아" / "옵시디언 노트 가져와"
- "옵시디언 볼트에 반영된 규칙 숙지" / "새 규칙 숙지" / "vault 규칙 숙지"
- "vault 참조" / "vault 참고" / "vault 검색"
- "wiki 참조" / "wiki 검색"
- "obsidian reference" / "obsidian ref" / "obsidian search"
- "이전 작업 참조" / "이전 세션 참조" / "이전 핸드오버" / "지난번 어디까지"

## 🚨 사전점검 (0단계, 건너뛰기 금지)

**참조 작업 시작 전 반드시 다음을 수행한다.**

1. **vault `AGENTS.md` 읽기** — 작업 종류별 체크리스트 확인
2. **vault `index.md` 읽기** — 정리 큐(`_REVIEW-*.md`)와 알려진 문제(orphan/명명 위반) 파악. 이 정보는 사용자 보고에 포함되어야 함
3. **`bash scripts/vault-lint.sh --quiet 2>&1 | tail -10` 실행** — exit code 와 fail 항목 헤더 캡처. 사용자에게 lint 현황 1줄 노출 (참조는 read-only 라 fail 이어도 진행)
4. `_REVIEW-*.md` dry-run 보고서가 있으면 → 현재 참조 대상 프로젝트와 관련된 항목을 추출해 사용자에게 함께 안내

## 대상 vault

```
~/Documents/AI-Sessions-Vault/
├── CLAUDE.md         (운영 규약 — 정규화 매핑 표 + save/ingest 구분표)
├── AGENTS.md         (강제 self-check 체크리스트)
├── index.md          (콘텐츠 카탈로그 + 정리 큐)
├── log.md            (operation 타임라인)
├── scripts/
│   └── vault-lint.sh (정합 자동 검증 게이트)
└── AI-Sessions/
    ├── conversations/{프로젝트}/    (핸드오버 노트 — 1순위 참조)
    └── wiki/
        ├── projects/{프로젝트}.md   (정식 프로젝트 페이지 — 2순위)
        ├── decisions/, playbooks/, errors/, concepts/  (관련 노트 — 3순위)
        ├── synthesis/_REVIEW-*.md   (정리 큐 dry-run 보고서 — 참조 시 함께 노출)
        └── sources/legacy/          (구조 정비 전 산재 노트 — 4순위, distill 대기)
```

## 절차 (5단계)

### 0.5. Source-of-truth / contamination guardrail

When referencing or updating Vault context for a project with a designated owner/handoff, do not treat the latest note as automatically authoritative. Before summarizing or distilling:

1. Identify the source hierarchy explicitly:
   - user direct instruction
   - reference-product / external evidence
   - designated agent handoff or UI/UX artifact
   - current repo/runtime state
   - general heuristics or assistant interpretation
2. If a later handoff contradicts an earlier owner handoff, mark the later item as `contested` or `needs review` instead of promoting it as final truth.
3. Never apply lean-native / Claude Desktop internal UI rules to an independent benchmark or external-reference product unless the user or design owner explicitly requested that style.
4. For cross-agent context packs, write provenance labels directly into the note so downstream agents can distinguish "팀 페르소나 판단" / "사용자 지시" / "reference observation" / "팀 페르소나 implementation note" / "assumption".
5. If contamination is discovered, fix in this order: shared context pack → project wiki → offending handoff warning → index/log → Company Truth Source DB correction event if runtime state was affected.

Session-specific detail:.

### 1. 현재 프로젝트 식별

**우선순위 (위에서 아래로)**:

1. 사용자 발화에 프로젝트명 명시 (예: "옵시디언 참조 myproject", "myproject 옵시디언 참조")
   → 그대로 사용
2. 현재 프로젝트 `CLAUDE.md`에 `vault_folder: <name>` 메타가 있으면
   → 그 값 사용
3. `Bash` 도구로 `basename "$PWD"` 실행 가능하면 (Claude Code 환경)
   → 결과를 vault `CLAUDE.md`의 정규화 매핑 표에 통과시켜 정규화
4. Bash 도구 미가용 (Claude Desktop Cowork 등)
   → mcp-obsidian으로 `conversations/` 폴더 listing 후 사용자에게 후보 제시
   → 또는 사용자에게 "어떤 프로젝트?" 한 번 확인

**정규화 매핑 (vault CLAUDE.md와 동일)**:
- `MyProject`, `MyProject-UI`, `My-Project` → `myproject`
- `TTStudio_v2` → `ttstudio-v2`
- `Cardnews/Creator/Deckster/Image-gen/Mole/Openclaw/RelayAX/Skills` → 모두 lowercase
- 그 외 PascalCase/공백/언더스코어 → kebab-case lowercase로 변환

### 2. 모드 결정

| 사용자 발화 | 모드 |
|---|---|
| 트리거 키워드만 단독 | **Listing** — 관련 노트 인덱스 + 최근 핸드오버 요약 |
| 트리거 + 질문 (예: "옵시디언 참조: 지난번 어디까지?") | **Query** — 검색 + 합성 답변 + citations |
| 트리거 + 작업 지시 (예: "옵시디언 참조 후 X 작업해줘") | **Context inject** — 노트 로드 후 X 작업 진행 |

### 3. 참조 범위 수집

프로젝트명 식별 후 다음 자료를 수집한다 (병렬):

**Claude Code 환경** (`Bash`, `Glob`, `Grep`, `Read` 사용):
```bash
VAULT="~/Documents/AI-Sessions-Vault/AI-Sessions"
PROJECT="myproject"  # 식별된 프로젝트명

# 1순위: 핸드오버 폴더
ls -t "$VAULT/conversations/$PROJECT/"*.md 2>/dev/null

# 2순위: 정식 프로젝트 페이지
ls "$VAULT/wiki/projects/$PROJECT.md" 2>/dev/null

# 3순위: wiki 전체에서 frontmatter related/tags 매칭
grep -lr "$PROJECT" "$VAULT/wiki/" 2>/dev/null

# 4순위: legacy 노트
grep -lri "$PROJECT" "$VAULT/wiki/sources/legacy/" 2>/dev/null
```

**Claude Desktop / Cowork 환경** (`mcp-obsidian` 사용):
- `mcp__mcp-obsidian__obsidian_list_files_in_dir` — `AI-Sessions/conversations/{프로젝트}/`
- `mcp__mcp-obsidian__obsidian_get_file_contents` — 정식 프로젝트 페이지
- `mcp__mcp-obsidian__obsidian_simple_search` 또는 `obsidian_complex_search` — 프로젝트명으로 vault 전체 검색
- `mcp__mcp-obsidian__obsidian_batch_get_file_contents` — 여러 노트 일괄 로드

### 4. 콘텐츠 로드 정책

토큰 절약을 위해 단계적 로드:

**Listing 모드** (가벼움):
- 1순위: 핸드오버 폴더 파일명만 (날짜 정렬, 최근 5개의 frontmatter `title`만 read)
- 2순위 정식 페이지: 한 줄 요약(첫 줄)만
- 3·4순위: 매칭된 파일명 목록만

**Query 모드** (선별 로드):
- 1순위: 가장 최근 핸드오버 1~3개 본문 read
- 2순위 정식 페이지: 전체 read (있으면)
- 3·4순위: 질문 키워드와 가장 매칭되는 1~2개만 read
- 합성 후 citations로 `[[file-stem]]` 명시

**Context inject 모드**:
- Listing 결과 + 가장 관련 깊은 1~2개 본문 read → 후속 작업에 컨텍스트로 사용

### 5. 출력 형식

**Listing 모드** 보고:

```
프로젝트: {정규화된 폴더명}
경로: ~/Documents/AI-Sessions-Vault/AI-Sessions/conversations/{프로젝트}/
vault 상태: lint pass / fail (N건) — {fail 한 줄 요약, 있으면}

핸드오버 ({N}개, 최근순):
1. {YYYY-MM-DD-HHMM-...} — {frontmatter title 또는 첫 H1}
2. ...
3. ... (이하 N-3개 더)

정식 프로젝트 페이지:
- wiki/projects/{프로젝트}.md (있으면 한 줄 요약, 없으면 "생성 권장")

관련 wiki 페이지: {N}개
- [[페이지명-1]] (decisions) — 한 줄 요약
- ...

미해결 정리 큐 (해당 프로젝트 관련, _REVIEW-*.md 에서 추출):
- {항목 1줄} — 보고서: [[_REVIEW-YYYY-MM-DD-...]]
- (없으면 이 섹션 생략)

가장 최근 핸드오버 요약:
{최신 핸드오버의 "다음 세션 시작 시" 섹션 내용}

이제 무엇을 도와드릴까요?
```

**Query 모드** 보고:

```
질문: {사용자 질문}

답변:
{vault 내용을 합성한 답변}

근거:
- [[2026-05-03-1430-myproject-handover]] — 인용/참조 위치
- [[wiki/decisions/some-decision]] — ...
- [[wiki/playbooks/some-playbook]] — ...

추가 정보가 필요하면 알려주세요.
```

**Context inject 모드** 보고:

```
참조 완료. {N}개 노트 로드:
- {핵심 1줄}
- {핵심 1줄}
- ...

이제 요청하신 작업을 진행합니다: {사용자 작업 지시 인용}
```

이모지/마케팅 언어 금지(글로벌 communication 규칙).

## Claude Desktop / Cowork 환경 처리

Cowork는 cwd 개념이 다르므로 다음 중 하나로 작동:

1. **사용자 명시 우선**: "옵시디언 참조 myproject", "myproject 옵시디언 참조"
2. **Cowork 컨텍스트 파일 인식**: 작업 폴더에 `.cowork-project` 또는 프로젝트 식별 메타가 있으면 read
3. **mcp-obsidian 폴더 listing**: `conversations/` 하위 폴더 목록을 보여주고 사용자가 선택
4. **vault 전체 검색**: 프로젝트가 모호하면 사용자 발화 키워드로 vault 전체 검색

mcp-obsidian 도구 매핑:
| 작업 | 도구 |
|---|---|
| 폴더 파일 목록 | `mcp__mcp-obsidian__obsidian_list_files_in_dir` |
| 파일 내용 | `mcp__mcp-obsidian__obsidian_get_file_contents` |
| 여러 파일 일괄 | `mcp__mcp-obsidian__obsidian_batch_get_file_contents` |
| 키워드 검색 | `mcp__mcp-obsidian__obsidian_simple_search` |
| 정교한 검색 (frontmatter/tags) | `mcp__mcp-obsidian__obsidian_complex_search` |
| 최근 변경 노트 | `mcp__mcp-obsidian__obsidian_get_recent_changes` |

mcp-obsidian의 경로는 vault 루트(`AI-Sessions-Vault/`) 기준 상대 경로 — 즉 `AI-Sessions/conversations/myproject/`처럼 입력.

## 엣지 케이스

| 상황 | 처리 |
|---|---|
| 프로젝트 폴더가 vault에 없음 | "vault에 `{프로젝트}` 폴더 없음. 핸드오버 첫 실행 시 자동 생성됨" 안내 + 유사 폴더명(편집거리 ≤2) 제안 |
| 핸드오버 0개 + 정식 페이지 0개 | "참조할 vault 노트가 없음. 첫 세션이거나 핸드오버 미실행 상태로 추정" 안내 |
| 프로젝트명 식별 실패 (Cowork에서 cwd 없고 명시 없음) | conversations/ 폴더 목록 보여주고 사용자에게 선택 요청 (1회 한정) |
| 핸드오버 50개 이상 (장기 프로젝트) | 최근 5개 + 사용자가 "전체 보여줘"라고 하면 페이지네이션 |
| 본문이 매우 김 (핸드오버 합쳐서 토큰 폭증) | 본문 read 대신 frontmatter `next_steps` 섹션만 추출 → 요약 |
| 권한 문제로 vault 접근 실패 | 경로 확인 요청 + Obsidian 앱이 vault를 열고 있는지 확인 안내 |
| 시크릿 패턴 검출 (vault에 평문 키 의심) | 사용자에게 즉시 경고 (글로벌 security 규칙) |

## 예시 시나리오

**시나리오 1 — Listing**: 사용자가 `~/Desktop/Appbuild/MyProject/`에서 새 세션 시작 후 "옵시디언 참조"
1. `basename` → `MyProject` → 정규화 → `myproject`
2. `conversations/myproject/` 45개 파일 발견
3. 최근 3개 핸드오버 frontmatter read → 요약
4. `wiki/projects/myproject.md` 없음 → "생성 권장"
5. Listing 출력 + 다음 작업 대기

**시나리오 2 — Query**: 사용자가 "옵시디언 참조: 지난번 인증 어떻게 끝냈어?"
1. 프로젝트 식별 (myproject)
2. `conversations/myproject/` 파일명 + 본문에서 "auth|인증|login" grep
3. 매칭된 핸드오버 2개 read
4. 합성 답변 + citations 제공

**시나리오 3 — Context inject**: 사용자가 "옵시디언 참조 후 SEO 메타 태그 추가해줘"
1. 프로젝트 식별 (myproject)
2. 관련 핸드오버 1~2개 + `wiki/decisions/` 중 SEO 관련 페이지 read
3. "참조 완료. SEO 관련 결정사항: ..." 보고
4. 이어서 SEO 메타 태그 추가 작업 진행

**시나리오 4 — Claude Desktop Cowork**: 사용자가 Desktop에서 "옵시디언 참조 ttstudio"
1. mcp-obsidian으로 `AI-Sessions/conversations/ttstudio/` listing
2. 6개 핸드오버 + `ttstudio-v2/` 12개도 함께 안내 (관련 프로젝트)
3. 가장 최근 1~2개 batch_get_contents
4. 합성 결과 보고

## obsidian-save와의 관계

| 스킬 | 방향 | 용도 |
|---|---|---|
| `obsidian-save` | 쓰기 (LLM → vault) | 현재 답변/분석을 wiki 페이지로 저장 |
| `obsidian-reference` (이 스킬) | 읽기 (vault → LLM) | 과거 노트를 컨텍스트로 끌어옴 |

두 스킬은 자주 짝으로 사용:
1. "옵시디언 참조" → 이전 컨텍스트 로드 + 정리 큐 인지
2. (작업 진행)
3. "옵시디언에 저장해줘" → 결과를 vault 에 저장 (save 스킬이 자동 lint)

## _REVIEW-*.md 보고서 노출 룰

`AI-Sessions/wiki/synthesis/_REVIEW-*.md` 파일은 destructive 정리 작업의 dry-run 보고서다. Listing/Query 모드에서 다음 룰로 사용자에게 노출:

1. 참조 대상 프로젝트와 관련된 항목이 있으면 → `미해결 정리 큐` 섹션으로 노출
2. 사용자가 정리 작업(예: "projects 합치기 진행해줘")을 트리거하면 → 해당 `_REVIEW-` 보고서의 체크박스 항목 1건씩 사용자 승인 받아 진행
3. 보고서 자체가 거대해도(>500줄) 전체 read 금지 — 키워드(프로젝트명)로 grep 후 매칭 섹션만 요약

## 정합성 체크 (작업 후)

응답 직전 다음을 확인:
1. 프로젝트명이 vault 에 존재하는 폴더와 매칭되는가
2. 인용한 `[[file-stem]]` 이 실제 vault 파일과 일치하는가 (정확한 검증: `find AI-Sessions/wiki -name "{stem}.md"`)
3. Query 모드 답변이 vault 내용에 근거하는가 (할루시네이션 금지)
4. 토큰 예산 준수 (Listing 모드는 가볍게, Query 모드는 답변 + citations만)
5. lint 상태 노출 (Listing 모드에서 1줄 필수, Query/Context-inject 모드에서는 fail 시에만)

하나라도 불확실하면 사용자에게 명시적으로 보고 ("이 부분은 vault 에 없어 일반 지식으로 답변").
