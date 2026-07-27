# {persona_display} {lab_or_role} work-status — {YYYY-MM-DD HH:mm} KST

## 현재 포커스
- 역할: {persona_display} / {lab_or_role}.
- 책임 범위: {responsibilities}.
- 이번 3시간 주기에는 {new_work_summary_or_no_new_instruction}.

## 마지막 액션
- vault 규칙 준수를 위해 `AGENTS.md`, `CLAUDE.md`, `index.md`, `log.md`를 확인했다.
- 사전 lint를 실행했다: `bash scripts/vault-lint.sh` → {pre_lint_status}.
- 직전 {persona} handoff(`{previous_note_path}`)를 확인해 상태 연속성을 점검했다.
- {work_progress_sentence}
- 기존 `raw/`, 기존 `conversations/`, `wiki/`, `index.md`는 수정하지 않았다.

## 결정 / 가정
- 이 기록은 wiki `save`/`ingest`가 아니라 cron 기반 `handoff`로 처리한다.
- 현재 lint 실패가 이번 handoff와 무관한 사전 존재 vault hygiene 이슈라면, 정기 상태 기록 범위를 넘는 정리 작업은 수행하지 않는다.
- {role_readiness_assumption}

## 블로커 / 리스크
- 사전 lint 결과: {pre_lint_status}.
- 실패/경고 요약:
  - {lint_summary_bullets_or_none}
- 사용자 승인이나 별도 cleanup task 없이 destructive 정리 작업은 수행하지 않는다.

## 다음 3시간 계획
1. 신규 지시가 없으면 다음 cron에서도 readiness와 무진척 상태를 명확히 기록한다.
2. {next_plan_item_2}
3. {next_plan_item_3}

## 파일 / 아티팩트
- 생성: `{new_note_path}`
- 갱신: `log.md` handoff entry {log_append_status}.  <!-- 작성 전 초안이면 'append 예정'처럼 미래형/placeholder로 두고, append read-back 후 'append 완료'로 패치한다. -->
- 수정하지 않음: `raw/`, 기존 `conversations/`, `wiki/`, `index.md`.

## 다른 에이전트가 알아야 할 것
- {persona_display}는 현재 {idle_or_active_state} 상태다.
- vault lint 실패가 있다면 새 handoff 때문인지 기존 known issue인지 구분해 기록한다.
- 향후 작업을 이어받는 에이전트는 이 파일을 상태 기준점으로 삼고, wiki 통합은 {{OWNER_TITLE}}의 명시 요청이 있을 때만 수행하면 된다.
