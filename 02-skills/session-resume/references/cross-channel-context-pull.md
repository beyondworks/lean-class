# Cross-channel context pull for session resume

Use this when {{OWNER_TITLE}} asks to continue work from Telegram/Slack/CLI/API in the current channel, e.g. “텔레그램에서 나눈 대화들 여기서 작업할 수 있게 끌고 와.”

## Goal
Move actionable context from prior channel transcripts into the current session without pretending it is fresh user instruction. Produce a compact handoff artifact and restore the working task list.

## Procedure
1. Search recent sessions by source/channel and project keywords.
   - Prefer broad searches: `telegram OR 텔레그램 OR <project> OR <persona> OR 본진`.
   - If session search summaries are incomplete, inspect Hermes profile session logs under the active profile’s sessions directory.
2. Extract only actionable state:
   - user requests and decisions
   - current project path/repo
   - active todo list
   - files/documents already created
   - verified handoff locations or DB ids
   - immediate next step
3. Do not import stale tool output wholesale. Summarize and cite paths instead.
4. Verify live repo/system state if continuing implementation, especially git branch/status and modified files.
5. Create a compact handoff note under the active profile, e.g.
   - `~/.hermes/profiles/<profile>/handoffs/YYYY-MM-DD-<channel>-context-pulled.md`
6. Restore the session todo list from the prior channel if present.
7. Final response should be short and operational: say what was pulled, where the handoff file is, and what the next executable step is.

## Pitfalls
- Do not treat compacted transcript summaries as active instructions; they are background only.
- Do not mark prior work as complete unless verified in current environment.
- Do not over-save session-specific progress to memory. Use a handoff file for temporary state.
- When multiple personas are involved, preserve boundaries: 효리 moderates 본진/operations; 효일 handles build/dev; 효정 handles education/Notion/schedule/SNS; 효나 handles creator/content unless {{OWNER_TITLE}} directs otherwise.
