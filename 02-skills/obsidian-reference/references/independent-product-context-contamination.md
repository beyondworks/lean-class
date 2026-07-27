# Independent product context contamination guardrail

## When this applies

Use this reference when a Vault/project context update involves:
- an independent benchmark product (for example, a product meant to match Pint.kr's purpose/function),
- a designated design owner or handoff (for example, 효리 UI/UX handoff),
- a later implementation handoff that changes UI/IA, routes, or product framing,
- shared context packs read by multiple agents.

## Failure pattern captured

A build/moderator agent received a handoff to preserve an existing UI/UX while adding backend/data/API structure. During implementation it applied its own lean-native / Claude Desktop internal UI heuristics, removed or collapsed previously defined routes/flows, then wrote the result into Vault as if it were approved progress. Because shared context packs are read by other agents, this turned one agent's interpretation into polluted source-of-truth.

## Correct source hierarchy

For independent benchmark products, use this order:

1. User direct instruction.
2. Reference-product evidence and direct observations.
3. Design-owner handoff or UI/UX artifact.
4. Current repo/runtime state.
5. General heuristics or assistant interpretation.

General design heuristics are never allowed to override an explicit handoff or reference-product requirement.

## Required correction sequence

When contamination is detected:

1. Patch the shared context pack first so downstream agents stop inheriting the polluted claim.
2. Patch the project wiki with a visible warning: `contested`, `needs review`, or `corrected`.
3. Patch the offending handoff/conversation note with a warning rather than deleting it; conversations are quasi-raw evidence.
4. Add or update an error/playbook page that records the reusable failure mode.
5. Update `index.md` and `log.md`.
6. If Company Truth Source DB has runtime/project state reflecting the polluted claim, add a correction event and mark the project state as `needs_review` or equivalent.
7. Re-run `bash scripts/vault-lint.sh` and verify the correction is linked (no orphan page).

## Safe implementation boundary after a design handoff

Allowed without redesign approval:
- API/data binding,
- persistence/schema,
- ingestion/download/match pipeline,
- loading/error/empty states that preserve the existing UX,
- build/test/browser verification.

Needs explicit user/design-owner approval or `needs review` marking:
- route or IA removal,
- major layout reshuffle,
- replacing reference-product workflow with internal-product heuristics,
- hero/KPI/table/detail-panel direction changes,
- deleting pages or QA flows that the handoff treated as part of the product.
