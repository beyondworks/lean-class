---
name: design-harness
description: 디자인 작업 전 vault Design Harness(정제수 12토픽 + 품질 게이트)를 로드해 적용하는 스킬. 트리거 — "디자인 하네스", "디자인 기준 로드", "정제수 로드해서 디자인", UI/화면/랜딩/대시보드 등 디자인 산출물 작업 시작 시, 레퍼런스 채택 판단 시, 디자인 QA/검수 시. 효리 design-radar 119건(2026-05-30~06-20)을 정제한 지식을 세션에 주입한다.
---

# design-harness — Design Harness 로더 (vault 정제수 소비)

> 정본: `{{VAULT_ROOT}}/AI-Sessions/wiki/harnesses/design.md` (v0.2, 2026-07-06).
> 이 스킬은 그 하네스의 **Claude Code 소비 진입점**이다. 지식 본문을 여기 복사하지 않는다 — vault가 단일 진실.

## 절차

### 1. 정제수 로드 (디자인 작업 시작 시, 총 ~27KB)

```
VAULT={{VAULT_ROOT}}/AI-Sessions/wiki/knowledge/design
```

읽는 순서:
1. `$VAULT/_quality-rubric.md` — 3중 게이트(실무성/anti-slop/시니어 깊이) + 산출물 검증 체크리스트
2. `$VAULT/reference/` — components · typography · layout-grid · design-tokens · color-palette (객관 자산)
3. `$VAULT/judgment/` — mood-effects · interaction-patterns · spacing-rules · anti-slop-tells · work-surface-evidence · reference-adoption · visual-fidelity-scoring (판단 노하우)

### 2. 게이트 적용 (작업 종류별)

| 작업 | 적용 게이트 |
|---|---|
| 레퍼런스 채택 | `reference-adoption` — 필수 메타 5필드(product/platform, flow/screen/element, recording/annotation, source/date, applied component) 없으면 mood-only로 기각 |
| AI/SaaS 화면 설계 | `work-surface-evidence` — 7종 증거 중 4+ 게이트, launch layer/operation layer 분리 |
| 산출물 완료 판정 | `_quality-rubric` — 실제 렌더 관찰(browser) 필수, build PASS ≠ 합격. 검증은 구현자와 다른 컨텍스트의 평가 에이전트가 |
| 재현·품질 채점 | `visual-fidelity-scoring` — 10점 정의 + 점수 cap 판정표(passthrough 2점 실격, generic 7.5, mood-only 8.3, grid break 8.5, px imbalance 9) |

### 3. 원수 재탐색 (정제수에 없는 세부)

효리 design-radar 원수 119건에서 검색:
```bash
grep -l "<키워드>" {{VAULT_ROOT}}/AI-Sessions/wiki/sources/*hyori-design-radar*.md
```

### 4. 자가학습 환류

새 관찰이 루브릭 3중 게이트를 통과하면 → 해당 정제수 topic 갱신(`updated` bump) → 하네스 version bump → index/log 갱신 + `vault-lint.sh` 통과 + 커밋. vault 쓰기는 반드시 vault `AGENTS.md` 체크리스트를 따른다 (환각 0%, 근거 링크 필수).

## 주의

- vault 쓰기 전 `git -C {{VAULT_ROOT}} status`로 타계열 미커밋 확인 — 공유파일 일괄 add 금지, 자기 파일만 명시 add.
- 이 스킬은 로더다. 스타일 생성 자체는 frontend-design·ui-ux-pro-max 등 기존 스킬과 병용하되, **게이트 판정은 항상 이 하네스 기준이 우선**.
