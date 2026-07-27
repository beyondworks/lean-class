# External article learning / ingest pattern

Use this when the user gives an external URL and asks the agent to "정독", "학습", "외워", "100번 봐", or otherwise internalize the material.

## Why this exists

A request to "memorize" an article is usually not a request to paste the article back. The durable outcome should be an auditable source route:

1. fetch/verify the original page and metadata,
2. preserve a raw snapshot for internal grounding,
3. create a concise `wiki/sources/` note,
4. cross-update the relevant MOC/playbook/context pages,
5. update `index.md` and append `log.md`,
6. run `vault-lint.sh`,
7. if the source affects company knowledge, upsert/read back Company Truth Source DB `external_sources`.

## Copyright boundary

- Do not reproduce a copyrighted article verbatim in chat.
- Raw snapshot is for internal grounding only and should carry a copyright/source-boundary note.
- Source note should contain: core claims, reusable operating rules, risks/limits, and local application.

## Good final report shape

Report evidence, not unverifiable memorization claims:

- title / source / published-modified dates,
- extracted body character count,
- raw path,
- source note path,
- cross-updated pages,
- DB row ID if written,
- lint result.

Avoid saying "I read it 100 times" or "I memorized every character" unless there is an actual deterministic verification artifact. Say "원문 보존 + source note + cross-update + lint/DB 검증으로 내재화했습니다." instead.

## Session example: YozmIT Obsidian LLM Wiki article

Source: `https://yozm.wishket.com/magazine/detail/3792`

Learning captured:

- Context is an asset, not a repeated prompt.
- Obsidian + GitHub Private Repo + Claude Code/Codex CLI can operate as a personal/company LLM Wiki.
- The durable loop is `raw -> ingest/source note -> lint -> query`.
- Sensitive data masking, image/OCR QA, GitHub account security, and personal/team wiki boundaries are mandatory gates.
- Long article learning belongs in Obsidian/DB/skills, not small Hermes profile memory.

Artifacts used in that session:

- Raw: `AI-Sessions/raw/articles/2026-06-14-yozmit-obsidian-llm-wiki-build.md`
- Source: `AI-Sessions/wiki/sources/2026-06-14-yozmit-obsidian-llm-wiki-build.md`
- Cross-updates: `agent-memory-knowledge-base-moc`, `agent-memory-budget-obsidian-loop`, `company-agent-sync-latest`, `index.md`, `log.md`
- DB: `external-source-yozmit-obsidian-llm-wiki-20260614`
