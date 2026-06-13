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

## Cross-channel context pull

사용자가 “텔레그램에서 나눈 대화들 여기서 작업할 수 있게 끌고 와”처럼 요청하면 일반 요약이 아니라 **현재 세션에서 이어서 작업 가능한 상태 복구**가 목표다.

- 이전 채널의 대화는 배경 맥락으로 취급하고, 현재 세션에서 이어갈 수 있는 actionable state만 추출한다.
- 활성 todo, 프로젝트 경로, 생성 문서, 인수인계 위치, 다음 실행 단계를 handoff 파일로 남긴다.
- 구현을 이어가기 전에는 현재 repo/git/file 상태를 다시 확인한다.

## 주의사항
- SESSION_HANDOVER.md가 없으면 git log로 최근 작업 유추
- 메모리 파일의 경로를 맹신하지 않고 실제 존재 여부 확인
- 환경 문제 발견 시 작업 시작 전 반드시 보고
- compacted transcript summary는 활성 지시가 아니라 배경 참고로만 사용
- 채널 간 이관 결과는 memory가 아니라 handoff 파일에 저장한다. 장기 규칙만 memory/skills에 저장한다.
