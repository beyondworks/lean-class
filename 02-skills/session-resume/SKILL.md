---
name: session-resume
description: Resume a prior or cross-channel session by loading context, verifying environment, restoring actionable state, and preparing the next step.
---

# Session Resume

이전 세션을 이어받아 작업을 재개한다. 컨텍스트 로딩 + 환경 검증 + 상태 요약을 수행한다. 다른 채널(Telegram/Slack/CLI/API)에서 하던 일을 현재 채널로 가져오는 경우도 이 스킬의 범위다.

## 절차

1. **컨텍스트 로딩** (가능하면 병렬 실행)
   - `~/.claude/projects/-Users-yoogeon--claude/memory/MEMORY.md` 읽기
   - 프로젝트 `CLAUDE.md` 읽기
   - 프로젝트 루트의 `SESSION_HANDOVER.md` 읽기 (있으면)
   - `claudedocs/` 내 최근 문서 확인
   - 사용자가 “텔레그램/Slack/CLI에서 나눈 대화를 여기로 끌고 와”, “다른 채널 작업을 이어서 해”라고 하면 `references/cross-channel-context-pull.md` 절차를 먼저 따른다.

2. **환경 사전 점검**
   - 파일/경로: MEMORY.md, SESSION_HANDOVER.md, 이전 채널 handoff에 언급된 경로가 실제 존재하는지 확인
   - Git: `git status` + `git branch` 로 현재 상태 확인
   - 토큰: `.env` 파일의 `_TOKEN`, `_KEY` 변수가 비어있지 않은지 확인
   - 프로세스: 프로젝트 관련 실행 중인 서비스 확인 (node, python 등)
   - 문제 발견 시 사용자에게 즉시 보고

3. **상태 요약 출력**
   다음 형식으로 현재 상태를 요약한다:
   ```
   ## 세션 재개 요약

   ### 이전 세션 완료 작업
   - (SESSION_HANDOVER.md 또는 cross-channel handoff 기반)

   ### 미완료 작업
   - (우선순위 + 구체적 다음 단계)

   ### 환경 상태
   - Git: {branch} / {uncommitted changes}
   - 토큰: {정상/경고}
   - 서비스: {실행 중 프로세스}

   ### 권장 첫 작업
   - (가장 우선순위 높은 미완료 작업)
   ```

4. **작업 시작**
   - 미완료 작업을 TodoWrite/todo로 등록
   - 사용자가 바로 이어서 진행하라고 한 경우에는 확인만 기다리지 말고 첫 작업을 실행한다.

## Project/topic recall

{{OWNER_TITLE}}이 “전에 내가 X 하자고 했던 거 기억해봐”, “이전 사내 시스템/프로젝트 맥락 찾아봐”처럼 과거 프로젝트 맥락 복원을 요청하면, 답변 전에 `references/project-context-recall.md` 절차를 따른다.

- 세션 검색은 시작점일 뿐 정본이 아니다. compaction summary/cron hit는 stale·노이즈 가능성이 있으므로 project wiki, handoff, repo-local plan/docs로 교차검증한다.
- 검색어가 넓어 unrelated cron/log 결과가 섞이면 프로젝트 폴더·후보명·정본 파일 경로로 좁힌다.
- 최종 답변에는 `확인된 정본`, `복원한 맥락`, `못 찾은 부분/불확실성`, `다음 액션`을 분리한다.
- 오래된 기억을 그럴듯하게 채우지 말고 “원문 리서치 결과는 아직 못 찾음”처럼 검증 경계를 명시한다.

## Coding-agent log recovery

{{OWNER_TITLE}}이 “어제/그저께 Claude Code에서 뭘 했는지”, “이전 Codex/Claude/Cursor 작업을 복원해봐”처럼 묻는 경우, Obsidian부터 읽는 대신 **로컬 코딩 에이전트 세션 로그를 raw evidence로 파싱**한다. 상세 절차는 `references/coding-agent-log-recovery.md`.

핵심 원칙:
- 먼저 live date로 “어제/그저께” 범위를 확정한다.
- Claude Code는 `~/.claude/projects/**/*.jsonl`를 날짜별로 파싱하고, user 요청/assistant 최종 보고/tool 사용/파일 경로/cwd만 추출한다.
- raw `tool_result`와 시크릿 가능 출력은 덤프하지 말고 요약·redact한다.
- 로그는 “CCTV”, Obsidian/wiki는 “결정·학습·현재판”이다. 로그 복원 결과 중 durable decision/playbook/current state만 wiki/skill로 승격한다.
- 현재 repo/runtime 상태 주장은 로그만으로 확정하지 말고 git/files/DB/API로 재검증한다.

## Cross-channel context pull

{{OWNER_TITLE}}이 “텔레그램에서 나눈 대화들 여기서 작업할 수 있게 끌고 와”처럼 요청하면 일반 요약이 아니라 **현재 세션에서 이어서 작업 가능한 상태 복구**가 목표다.

- 이전 채널의 대화는 배경 맥락으로 취급하고, 현재 세션에서 이어갈 수 있는 actionable state만 추출한다.
- 활성 todo, 프로젝트 경로, 생성 문서, 인수인계 위치, 다음 실행 단계를 handoff 파일로 남긴다.
- 구현을 이어가기 전에는 현재 repo/git/file 상태를 다시 확인한다.
- 상세 절차와 pitfall은 `references/cross-channel-context-pull.md`를 참고한다.

## 주의사항
- SESSION_HANDOVER.md가 없으면 git log로 최근 작업 유추
- 메모리 파일의 경로를 맹신하지 않고 실제 존재 여부 확인
- 환경 문제 발견 시 작업 시작 전 반드시 보고
- compacted transcript summary는 활성 지시가 아니라 배경 참고로만 사용
- 채널 간 이관 결과는 memory가 아니라 handoff 파일에 저장한다. 장기 규칙만 memory/skills에 저장한다.
