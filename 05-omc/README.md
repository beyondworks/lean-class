# 05 · oh-my-claudecode (OMC) ★

**OMC 는 이 킷의 핵심**입니다. Claude Code 위에 올라가는 **멀티에이전트 오케스트레이션 레이어**로, 전문 에이전트·스킬·툴·상태관리를 묶어 복잡한 작업을 자동 조율합니다.

## 설치

```bash
# 방법 A — 마켓플레이스 + 플러그인
claude plugin marketplace add Yeachan-Heo/oh-my-claudecode
claude plugin install oh-my-claudecode@omc

# 방법 B — npm CLI (설치 후 omc 명령 사용 가능)
npm install -g oh-my-claudecode   # 또는 레포 README 참고
```

설치 후 Claude Code 안에서:
```
setup omc            # 또는
/oh-my-claudecode:omc-setup
```

## Tier-0 워크플로 (가장 자주 쓰는 것)

| 명령 | 역할 |
|------|------|
| `/oh-my-claudecode:autopilot` | 아이디어 → 동작 코드까지 완전 자율 실행 |
| `/oh-my-claudecode:ultrawork` | 고강도 자율 작업 루프 |
| `/oh-my-claudecode:ralph` | 작업 완료까지 자기참조 반복(검증 리뷰어 포함) |
| `/oh-my-claudecode:team` | N개 에이전트가 공유 작업목록을 협업 |
| `/oh-my-claudecode:ralplan` | 모호한 요청을 실행 전 합의 계획으로 게이트 |

## 키워드 트리거 (자동 감지)

`autopilot` → autopilot · `ralph` → ralph · `ulw` → ultrawork · `ccg` → ccg ·
`ralplan` → ralplan · `deep interview` → deep-interview · `deslop`/`anti-slop` → ai-slop-cleaner ·
`deep-analyze` → 분석 모드 · `tdd` → TDD · `deepsearch` → 코드베이스 검색 ·
`ultrathink` → 심층 추론 · `cancelomc` → 취소

## 주요 전문 에이전트

`planner`(전략 계획) · `architect`(아키텍처·디버깅, 읽기전용) · `executor`(구현) ·
`explore`(코드 검색) · `designer`(UI/UX) · `code-reviewer` · `security-reviewer` ·
`verifier`(검증) · `debugger` · `tracer`(인과 추적) · `critic`(다관점 리뷰) ·
`document-specialist`(외부 문서) · `writer`(문서 작성)

> 전체 카탈로그는 설치 후 `/oh-my-claudecode:omc-reference` 스킬에서 확인.

## 핵심 운영 원칙 (이 킷이 따르는 방식)

- **위임**: 다중 파일 변경·리팩터·디버깅·리뷰·계획·리서치는 전문 에이전트에 위임
- **검증 분리**: 구현과 리뷰는 다른 컨텍스트에서 (자기 승인 금지)
- **모델 라우팅**: `haiku`(빠른 조회) / `sonnet`(표준) / `opus`(아키텍처·심층)
- **상태 관리**: `.omc/state/`, `.omc/notepad.md` 등에 작업 상태 영속화

## 취소
```
/oh-my-claudecode:cancel
```
실행 모드(autopilot/ralph/ultrawork/team 등)를 종료합니다.

---
> ⚠ OMC 는 빠르게 업데이트됩니다. 설치 후 `omc update` 로 최신화하세요. 이 킷 작성 시점 기준 v4.14.x.
