# Coding Agent Log Recovery

Use when the user asks what happened in prior Claude Code / Codex / coding-agent sessions, or when reconstructing work across days without relying on Obsidian summaries.

## Core pattern

Treat local coding-agent transcripts as raw evidence/CCTV, not as curated knowledge.

1. Determine the target date range using live time (`date`) before interpreting “yesterday”, “two days ago”, etc.
2. Locate the tool’s local session store:
   - Claude Code: `~/.claude/projects/**/*.jsonl`
   - Codex: `~/.codex/` state/config/session DBs where available
   - Hermes: session DB/profile logs/cron outputs
   - IDE agents: workspace storage / extension logs / app DBs, if accessible
3. Parse by timestamp and group by session file / cwd / project.
4. Extract only decision-grade signals:
   - user requests
   - assistant summaries/final reports
   - tool names/counts
   - touched file paths
   - cwd/project/session id
5. Suppress or redact noisy/sensitive material:
   - do not print raw `.env` values, tokens, API keys, OAuth secrets, DB strings
   - avoid dumping full `tool_result`; summarize shape and evidence instead
6. Cross-check important claims with repo/git/files/DB when the user asks for current state or “what actually changed”.

## Obsidian boundary

- Local logs answer: “what happened?”
- Obsidian/wiki answers: “what was decided, learned, and should be reused?”
- Do not replace Obsidian with raw logs. Promote only durable decisions, current-state summaries, and reusable playbooks into wiki/skills.

## Output shape

Use a compact synthesis, not a log dump:

```md
## 확인 범위
- 날짜:
- sources:
- sessions found:

## 핵심 흐름
- D-1:
- D-2:

## 실제 산출물/경로
- ...

## 미확실/재검증 필요
- ...
```

## Pitfalls

- Same project may have multiple persona/session files; avoid claiming one continuous conversation unless session ids prove it.
- Some logs contain tool output with secrets in command lines or environment dumps; redact aggressively.
- `tool_result` often dominates token volume and should be filtered unless debugging tool behavior.
- Logs are evidence, not truth-source state. For current repo/runtime claims, verify live.