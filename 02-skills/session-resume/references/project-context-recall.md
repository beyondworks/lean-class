# Project context recall pattern

Use this when the user asks to “remember” a prior project discussion, especially when the exact phrase may not appear in the current chat.

## Pattern
1. Start with session retrieval for the user's keywords and likely synonyms.
   - Example shapes: `사내 시스템 ERP 오픈소스 템플릿`, then narrower/broader variants such as `사내 시스템`, `ERP`, `template`, `오픈소스`.
2. Treat session-search hits as pointers, not final truth. Compaction summaries and cron reports can be stale or noisy.
3. Cross-check durable project stores before answering confidently:
   - project wiki note / context digest
   - handoff files under the relevant conversation/project folder
   - repo-local plans, PRDs, handoffs, or design docs when paths are known
4. If broad searches overhit, narrow by project folder/path and concrete candidate names.
5. Report what was verified vs. what was not found.
   - Good: “정본 문서에는 X로 남아 있고, Y 후보 비교 원문은 아직 못 찾았습니다.”
   - Bad: inventing a remembered candidate list from a vague recollection.

## Output shape
- `확인한 정본:` durable files or DB/session sources actually checked.
- `기억/맥락 복원:` concise reconstruction.
- `불확실:` missing original research, stale handoff, or unresolved candidate list.
- `다음 액션:` re-run research, inspect repo, or ask user only if the missing source is not retrievable.

## Pitfalls
- Do not answer from memory just because the project name is familiar.
- Do not treat the newest handoff as authority if project wiki/source-of-truth says otherwise.
- Do not let broad keyword search results from unrelated cron jobs become the answer.
