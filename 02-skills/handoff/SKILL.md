---
name: handoff
description: Document session work and prepare handover for next session or a a named agent persona
---

# Session Handoff

세션 종료 전 작업 내용을 정리하고 다음 세션을 위한 핸드오버 문서를 준비한다.

## Persona-targeted handoff

The representative requests a persona-targeted handoff to a specific a named agent persona (e.g. a recurring team persona), in addition to the standard session handoff. Detailed patterns are in.

## Recurring cron work-status handoff

주기성 a named agent persona cron이 “handoff-level work-status note”를 요구하면, 진행이 없어도 새 상태 노트와 `log.md` append가 산출물이다. 세부 패턴과 최종 응답 형식은를 따른다.

- 반복 status note 본문은 `templates/cron-work-status-note.md`를 복사해 persona/role/responsibility/lint 상태만 채우면 된다. 특히 “진행 없음” 주기에도 현재 포커스, 마지막 액션, 결정/가정, 블로커, 다음 3시간 계획, 파일/아티팩트, 다른 에이전트가 알아야 할 것을 모두 남긴다.
- A recurring team persona's regular work-status cron should follow the persona-specific wording and readiness plan in the corresponding `references/` file for that persona. When existing vault lint is in FAIL state and no new instructions are given, proceed safely by writing only the new handoff note, and treat post-lint repeated failures as expected verification.
- Pre/post lint가 같은 기존 failure/warning class로 실패하고, post-lint 이후 패치는 `append 완료`/`post-lint FAIL` 같은 wording-only 확정뿐이면 세 번째 lint를 돌리지 않는다. note read-back + `log.md` exact 검색으로 검증을 끝내고, note/final에는 “새 handoff가 새 failure class를 만들지 않았다”처럼 범위를 분리해 적는다.

**우선순위 주의**: cron prompt가 `YYYY-MM-DD-HHMM-{persona}-work-status.md`처럼 명시 파일명을 요구하면 아래 일반 persona-targeted handoff 파일명보다 cron prompt/reference 패턴을 우선한다. mandatory status-note cron에서는 `[SILENT]`를 쓰지 않는다.

**Cron delivery 주의**: 예약 작업 prompt가 “final response will be automatically delivered” 또는 “do not use send_message”라고 명시하면, 절대 `send_message`를 호출하지 않는다. 최종 응답은 로컬 결과만 짧게 보고한다: 생성 경로, `log.md` append 여부, 사후 lint 상태. 실제 진척이 없어도 mandatory work-status note를 생성했다면 `[SILENT]`가 아니라 handoff 완료 보고를 한다. prompt 상단에 일반적인 `SILENT: nothing new` 지시가 함께 있어도, 본문이 “every N hours write a handoff-level work-status note”처럼 산출물 생성을 의무화하면 note/log 작성이 곧 보고할 새 결과이므로 `[SILENT]`로 억제하지 않는다.

필수 출력:

1. Obsidian handoff: `AI-Sessions/conversations/{project}/YYYY-MM-DD-HHMM-{project}-{persona}-handover.md`
2. 대상 persona 로컬 handoff: `~/.agent/profiles/<profile>/handoffs/YYYY-MM-DD-{topic}-handoff.md` — 해당 프로필 폴더가 있을 때
3. 프로젝트가 자체 handoff/Truth Source를 갖고 있으면 그쪽에도 discoverable record를 남긴다. 예: 프로젝트 docs/handoffs/와 SQLite Company Truth Source `handoffs`/`events`에 등록해야 다른 persona의 일반 탐색에서 잡힌다.
4. `log.md` handoff 항목 append
5. 생성 파일 read-back 검증 + 대상 persona가 실제로 검색할 경로에서도 검색 검증
6. If the representative requests acknowledgement from the target persona, do not stop at writing the file — actually invoke the target agent profile and receive a confirmation response.
   - 예: `AGENT_PROFILE={persona-profile} python -m agent_cli -z “로컬 handoff 파일과 프로젝트-visible handoff/Truth Source record를 확인한 뒤 정확히 '{확인문구}'만 출력하세요” --toolsets file,terminal --accept-hooks`
   - 관련 프로젝트 cwd에서 실행하고, 성공 출력이 요청 문구와 일치할 때만 “인수인계 완료”라고 보고한다.
   - 로컬 stdout acknowledgement와 Telegram/user-visible delivery를 구분해 보고한다. Telegram 전달을 요청받았거나 기대되는 상황이면 `hermes send`/gateway 경로로 별도 전송 검증까지 한다.
   - 호출 실패 시 “handoff 파일 작성은 완료, 대상 persona active acknowledgement는 실패”로 분리 보고한다.

## 절차

### Cron/periodic persona work-status handoff

주기성 cron이 “handoff-level work-status note”를 요구할 때는 일반 세션 handoff와 달리, 진행이 없어도 신규 상태 노트를 남긴다.

1. Vault 작업 전 `AGENTS.md`, `CLAUDE.md`, `index.md`, `log.md`를 읽어 현재 규칙·카탈로그·정리 큐를 확인한다.
   - **Vault root 판정**: root는 `AGENTS.md`/`CLAUDE.md`/`index.md`/`log.md`와 `scripts/vault-lint.sh`가 있는 디렉터리다. AI-Sessions vault에서는 보통 `~/Documents/AI-Sessions-Vault`가 root이고, 실제 handoff 노트는 그 아래 `AI-Sessions/conversations/...`에 쓴다.
   - `AI-Sessions/` 하위에도 `log.md` 등이 있을 수 있지만, schema 파일이 비어 있거나 lint script가 없으면 잘못된 root로 본다. 이때 상위 vault root로 올라가 다시 읽고 lint를 실행한다.
2. 가능하면 vault root에서 `bash scripts/vault-lint.sh`를 사전 실행한다.
   - 기존 lint FAIL이 destructive cleanup 대상이면 raw/와 기존 conversations 파일은 건드리지 말고, 새 handoff 파일 생성만 계속한다.
   - 결과 요약은 handoff 본문과 최종 보고에 남긴다.
3. 파일 위치는 `{vault_root}/AI-Sessions/conversations/{persona}/YYYY-MM-DD-HHMM-{persona}-work-status.md`를 사용한다. 예: `AI-Sessions/conversations/hyori/2026-05-19-0542-hyori-work-status.md`.
   - 가능하면 같은 `{persona}` 폴더의 최신 `*-work-status.md`를 1개 read-back해 직전 상태를 이어받는다. 신규 실작업이 없으면 직전 노트 이후에도 “진행 없음”이라고 명확히 쓰고, 직전 노트 경로를 마지막 액션에 남긴다.
   - **직전 handoff 확인 pitfall**: 최신 파일을 `search_files(target="files")` 등으로 찾았고 read-back까지 했다면, 새 노트에 “이전 handoff를 찾지 못함” 같은 이전 템플릿 문구를 복사하지 않는다. 반드시 확인한 직전 note의 정확한 vault-relative path를 `지난 3시간 / 마지막 액션` 또는 `결정 / 가정`에 남긴다.
   - 사전 lint가 기존 이슈로 실패해도 destructive cleanup이 필요한 항목이면 신규 handoff 작성만 계속할 수 있다. 이때 노트와 최종 보고에는 정확한 failure class(예: projects 명명 위반 N건, orphan warning N건, raw/sources warning, `_unsorted` N건)를 짧게 적는다.
   - **Lint 요약 정확도 pitfall**: 직전 handoff나 오래된 `log.md` 항목의 lint 문구를 그대로 복사하지 않는다. 이번 실행의 `vault-lint.sh` stdout에서 실제로 나온 failure/warning class만 적고, 이번 출력에 없는 `broken wikilink`, `frontmatter`, `index 불일치` 같은 항목은 쓰지 않는다. 이전 노트가 과장/오래된 요약을 담고 있으면 이번 note에서 최신 lint 결과로 바로잡는다.
   - **PASS-with-warnings 구분**: `vault-lint.sh`가 `✅ vault-lint: PASS`로 끝나면 warning이 있어도 note/log/final에는 `PASS`로 기록한다. `raw 0/sources`, `_unsorted`, `conversations→wiki distillation coverage` 같은 warning queue는 `FAIL`로 승격하지 않는다. 직전 handoff가 pre-existing FAIL을 말하더라도 현재 출력이 PASS이면 `기존 lint fail 상태`라고 쓰지 말고 `PASS; warning: ...` 형태로 최신 상태를 남긴다.
4. 내용은 최소한 현재 포커스, 마지막 액션, 결정/가정, 블로커, 다음 3시간 계획, 파일/아티팩트, 다른 에이전트가 알아야 할 것을 포함한다.
   - 실제 진척이 없으면 “진행 없음”을 명시하고 readiness/context를 기록한다.
6. `log.md`에는 `handoff` operation으로 신규 note path와 1~2줄 요약만 append한다. `index.md`는 handoff만으로 갱신하지 않는다.
   - 신규 handoff 노트 본문에는 `log.md` append 전이라도 최종 상태가 모호하지 않게 쓴다. 단, 실제 append 전 초안에 `log.md handoff entry append 완료`처럼 완료형을 미리 쓰지 않는다. 초안에는 `append 예정`/`append 대기`를 쓰고, append read-back 후에만 `append 완료`로 패치한다. 가능하면 파일 생성 후 log append까지 끝낸 뒤 note를 “갱신:” 상태로 맞춰 read-back한다. `갱신 예정` 같은 미래형이 남아 있으면 최종 검증 전에 현재형으로 패치한다.
6. `log.md` append 직전에는 반드시 `log.md`의 최신 tail을 다시 읽고 그 최신 tail 기준으로 append한다. 여러 persona cron이 같은 분에 동시에 실행될 수 있어, 오래된 `log.md` 스냅샷을 기준으로 patch하면 다른 cron의 append를 덮어쓰거나 tool warning(`modified since you last read`)을 유발할 수 있다.
   - **Append 방식 주의**: `log.md`처럼 append-only 대형 파일은 partial `read_file(offset/limit)` 직후 `patch`로 끝부분을 교체하면 도구가 “partial view before overwriting” 경고를 낼 수 있다. 가능하면 append-only 방식(예: 스크립트/쉘 append)으로 끝에 추가하거나, `patch`를 써야 하면 최신 tail 문맥을 충분히 잡고 작업 후 반드시 full/tail read-back으로 내 항목과 동시 cron 항목이 모두 보존됐는지 확인한다.
   - **Append newline/blank-line guard**: 동시 cron/이전 append 때문에 `log.md` 마지막 항목이 줄바꿈 없이 끝날 수 있다. 스크립트로 append할 때는 마지막 바이트를 확인해 `\n`이 아니면 먼저 개행을 쓴다. 또한 새 `## [...] handoff | ...` heading 앞에는 가능하면 빈 줄 1개를 보장한다. 마지막 항목이 줄바꿈으로 끝나더라도 빈 줄 없이 바로 heading을 붙이면 사람이 읽는 tail에서 항목 경계가 흐려지고 일부 grep/파싱 워크플로가 깨질 수 있다. 단, 기존 항목을 재작성하지 말고 append-only로 separator만 추가한다.
   - **권장 append 검증 패턴**: cron handoff에서는 `execute_code`/스크립트로 `log.md`를 append-only로 열어 항목을 추가한 뒤, `search_files`로 새 note path를 exact 검색해 내 항목이 들어갔는지 확인한다. 대형 `log.md`에서 “내 항목이 마지막 tail에 보인다”를 유일한 성공 조건으로 두지 않는다.
   - **동시 cron pitfall**: 최신 tail을 읽은 직후에도 다른 persona가 먼저 append할 수 있다. 이 경우 내 항목이 log의 마지막 항목이 아니어도 실패가 아니다. append-only로 추가한 뒤 tail read-back에서 (a) 방금 끼어든 타 persona 항목이 보존됐고 (b) 내 항목도 존재하면 정상 완료로 본다.
   - warning이 발생하면 성공 diff만 믿지 말고 read-back으로 내 항목과 타 항목이 모두 보존됐는지 확인한다.
7. 작성 후 파일 read-back 검증과 사후 `vault-lint`를 실행한다. 기존 FAIL은 고치지 말고 정확한 failure summary만 보고한다.
   - 노트 본문에 `사후 lint 결과는 최종 응답에 보고` 같은 미래형 문구를 남겼다면, 사후 lint 직후 `사전/사후 FAIL` 또는 `PASS`처럼 최종 상태로 패치하고 해당 줄만 read-back한다. 이 wording-only 패치 때문에 동일한 lint를 다시 반복 실행하지 않는다.
8. 예약 작업 final response는 로컬 결과만 짧게: 생성 경로 + lint 결과. delivery는 scheduler가 처리하므로 `send_message`를 쓰지 않는다.
   - 도메인 실작업이 없어도 mandatory work-status note를 생성했다면 `[SILENT]`를 쓰지 않는다. 생성된 note + log append가 산출물이다.
   - `log.md` append가 사후 lint 전에 일어나면 log 항목에는 `pre FAIL/PASS`만 적어도 된다. 사후 lint 결과는 final response에서 `pre/post` 또는 최종 상태로 보고하고, 같은 내용을 반영하려고 append-only log를 되돌려 패치하지 않는다.
   - note read-back + log tail read-back + post-lint 1회면 충분하다. post-lint가 사전 lint와 동일한 기존 failure를 반복하면 retry하지 말고 기존 이슈로 요약한다.
   - 도구가 동일한 `vault-lint` 실패에 대해 repeated/loop warning을 붙여도, 정기 handoff의 사전·사후 lint 2회 실행은 의도된 검증이다. 세 번째 lint를 실행하거나 unrelated cleanup을 시작하지 말고, 기존 failure class만 최종 보고한다. `repeated_exact_failure_warning` 같은 tool-loop 경고가 붙어도 stdout에 post-lint 결과가 있으면 post-lint 캡처는 완료된 것으로 본다.
   - post-lint 뒤에는 노트 안의 미래형 placeholder(`사후 lint 실행 예정`, `append 예정`)만 현재형으로 패치하고, 그 wording-only 패치 때문에 lint를 다시 돌리지 않는다. read-back과 log exact 검색으로 검증을 끝낸다.
   - placeholder가 여러 개 남아 있으면 가능하면 한 번의 targeted patch로 `append 완료`와 `Post-lint: FAIL/PASS...`를 함께 확정한다. 여러 번 나눠 패치해도 무방하지만, cron handoff에서는 edit 횟수를 줄여 동시 실행 중인 다른 persona 작업과의 충돌면을 줄이는 것이 좋다.
   - `log.md` target은 항상 note의 정확한 vault-relative path를 쓴다: `AI-Sessions/conversations/{persona}/YYYY-MM-DD-HHMM-{persona}-work-status.md`. `conversations/...`처럼 root prefix를 줄이거나 `.md` 확장자를 생략하지 않는다. 여러 cron이 섞인 tail에서는 축약 entry가 있더라도 새 entry는 정규형으로 append한다.
   - **검증 중복 방지**: post-lint 후에는 note read-back 1회, `log.md` exact 검색 1회, 필요 시 tail read-back 1회면 충분하다. 같은 exact 검색이나 같은 lint 명령을 이미 성공/실패 캡처한 뒤 반복하지 않는다. `idempotent_no_progress_warning`/`repeated_exact_failure_warning`이 떠도 이미 캡처한 결과가 있으면 정상 검증으로 간주하고, 추가 재시도 대신 최종 요약에 반영한다.
   - **부분 실패 복구**: pre-lint 실행은 성공적으로 끝났지만 같은 automation block 안의 후속 discovery/read-back 단계가 helper 오류 등으로 중단되면, 이미 캡처한 pre-lint 결과를 버리거나 pre-lint를 반복하지 않는다. 후속 단계만 직접 `search_files`/`read_file`/작은 스크립트로 재시도하고, 사후 lint 1회 + note/log exact 검증으로 마무리한다.
   - **검증 호출 분리 권장**: cron handoff에서는 `execute_code` 한 블록 안에 pre-lint, 최신 노트 검색, log tail 읽기까지 과도하게 묶지 않는다. 후속 helper/tool 호출이 실패하면 pre-lint 결과까지 실패처럼 보일 수 있다. 가능하면 pre-lint는 독립 `terminal` 호출로 캡처하고, 최신 note/log 검증은 별도 `search_files`/`read_file` 호출로 분리한다.

1. **컨텍스트 수집**
   - MEMORY.md 읽기
   - 프로젝트 CLAUDE.md 읽기
   - 기존 SESSION_HANDOVER.md가 있으면 읽기

2. **세션 요약 작성**
   - 이번 세션에서 완료한 작업 목록
   - 변경된 파일 목록 (`git diff --name-only` 활용)
   - 주요 결정 사항과 근거

3. **미완료 작업 정리**
   - 남은 작업 + 구체적 다음 단계
   - 블로커가 있다면 원인과 해결 방향
   - 우선순위 표기

4. **에러/학습 기록**
   - 발생한 에러와 해결 방법
   - 새로 알게 된 패턴이나 주의사항

5. **MEMORY.md 업데이트**
   - 반복 가능한 학습만 추가 (세션 한정 정보 제외)
   - 200줄 제한 이내 유지

6. **SESSION_HANDOVER.md 생성/갱신**
   - 프로젝트 루트에 생성
   - 구조:
     ```
     # Session Handover
     ## 날짜: {today}
     ## 완료
     - (목록)
     ## 미완료
     - (목록 + 다음 단계)
     ## 에러/학습
     - (목록)
     ## 다음 세션 시작 시
     - (구체적 첫 행동)
     ```

7. **Obsidian vault 동기화** (필수, 모든 프로젝트 공통)
   - 베이스 경로: `~/Documents/AI-Sessions-Vault/AI-Sessions/conversations/`
   - 프로젝트 폴더명 결정:
     - 우선순위: 프로젝트 CLAUDE.md에서 명시된 vault 폴더명 → `basename "$PWD"` 결과
     - 폴더가 없으면 `mkdir -p`로 생성
   - 파일명: `YYYY-MM-DD-HHMM-{프로젝트}-handover.md` (kebab-case, 충돌 시 시퀀스 추가)
   - 파일 내용 = YAML frontmatter + SESSION_HANDOVER.md 본문 동일 복제:
     ```yaml
     ---
     date: '{ISO8601 KST 시간}'
     project: '{프로젝트명}'
     type: handover
     trigger: '{handoff | precompact}'
     cwd: '{$PWD}'
     git_branch: '{현재 브랜치 또는 not-a-repo}'
     git_head: '{git rev-parse --short HEAD 결과 또는 빈 문자열}'
     tags:
       - handover
       - claude-code
     title: '[{프로젝트}] {한 줄 요약}'
     ---

     {SESSION_HANDOVER.md 본문 그대로}
     ```
   - 쓰기 방식: `Write` 도구로 절대경로 직접 쓰기 (Obsidian 파일 시스템 워처가 자동 인덱싱). mcp-obsidian MCP가 활성이면 `mcp__mcp-obsidian__obsidian_put_content`도 가능
   - 실패 시: 에러 출력 후 SESSION_HANDOVER.md만 남기고 진행 (작업 중단 금지)

8. **커밋**
   - 변경된 문서 파일만 staging (Obsidian vault 파일은 보통 별도 git이므로 프로젝트 git에는 포함되지 않음)
   - 커밋 메시지: `docs: session handover update`
   - push 하지 않음 (사용자 확인 후)

## PreCompact 자동 트리거

`PreCompact` 훅이 발동하면 이 스킬을 자동으로 호출하도록 글로벌 settings.json에 설정되어 있다. 사용자가 `/compact`를 실행하거나 자동 compact가 임박하면 이 스킬의 모든 단계(특히 7번 옵시디언 동기화 포함)를 완료한 뒤에야 compact가 진행되어야 한다. trigger 필드를 `precompact`로 표기.
