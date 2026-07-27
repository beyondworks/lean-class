# lean-native Agent Truth Source Notes

Use this reference when saving or classifying lean-native company-agent synchronization rules, agent memory boundaries, or artifact schemas into the {{VAULT_ROOT}}.

## Central rule

Company Truth Source is the shared company memory. Persona/profile memory is role-local support memory. Do not claim full real-time automatic synchronization unless the implementation and health checks prove it.

Accurate phrasing:
- "Company Truth Source 기반 동기화 규약을 정의했다."
- "구조 설계 가능, 일부 진실원 존재, 완전 동기화는 구현/검증 필요."

Avoid:
- "모든 에이전트 장기기억과 스킬이 이미 자동 동기화 중이다."

## Shared categories

Promote shared information to one of these truth-source categories:
- work status / 진행 상황
- decision
- handoff
- artifact
- learning
- agent capability
- skill/plugin catalog

Keep out of shared memory unless explicitly promoted:
- profile-internal long-term memory dumps
- temporary session reasoning
- unverified claims
- runtime-specific skill loading state

## Agent role split from the session

- 효리: 본진 운영, 프로필 경계, 공통 진실원 동기화
- 효일: 구현, 상태 검증, 회의 정리, 작업 라우팅, 최소 스키마 정리
- 효삼: 코드, 리서치, 심층 분석, capabilities/skills registry analysis
- 효나: 콘텐츠/영상 artifacts
- 효정: 강의/유튜브 planning artifacts

## 효나 content/video artifact types

Types:
- script
- cutlist
- edit-brief
- subtitle-pack
- reference-pack
- qa-report
- final-artifact
- handoff

Minimum fields:
- project_id
- content_id
- platform
- status
- owner_agent=hyona
- version
- source_links
- artifact_path
- decision_refs
- next_action
- updated_at
- verification_status

Rule: individual video progress stays in truth-source artifacts/handoffs/status, not personal memory. Reusable editing principles may become learning.

## 효정 lecture/YouTube artifact types

Types:
- lecture-plan: goal, audience, difficulty, module structure, practice flow
- curriculum: course structure, lesson topics, learning outputs, assignments
- youtube-brief: topic, target viewer, core message, positioning, references
- script: hook, body structure, CTA, version
- title-thumbnail-pack: title candidates, thumbnail copy, click angle, banned wording
- recording-flow: recording order, screen composition, demo sequence, talking points, preparation
- teaching-principle: reusable teaching tone, examples, metaphors, banned patterns
- review-note: structure review, logic flow, audience comprehension, improvements

Rule: temporary drafts may remain in working context, but reusable principles, confirmed briefs, real deliverables, and cross-agent handoffs should be promoted to learning/artifact/decision/handoff/status.

## Vault classification hint

When asked to save these rules to Obsidian:
- If it is lean-native project state and schema: update/create `wiki/projects/lean-native-company-truth-source-background-workers-memory-loop.md` or a lean-native project page section.
- If it is a reusable synchronization method across agents: `wiki/playbooks/`.
- If it is a confirmed architecture decision: `wiki/decisions/`.
- If it is a cross-cutting comparison or map of categories: `wiki/synthesis/`.

Always obey the vault AGENTS/CLAUDE/index/lint workflow before writing.