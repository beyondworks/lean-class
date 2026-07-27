# Cron work-status handoff pattern for {{VAULT_ROOT}}

Use this reference for recurring Hermes persona jobs that must write periodic Obsidian handoff-level status notes even when no practical work progressed.

## Durable pattern

1. Load/read vault rules before writing:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `index.md`
   - `log.md` tail
2. Run pre-write `bash scripts/vault-lint.sh` from the vault root when available.
   - Keep prerequisite probes resilient: avoid bundling lint, latest-note lookup, and log-tail retrieval into one `execute_code` script if a single helper failure would abort the whole collection. Prefer direct/parallel tool calls for independent reads after lint, then continue with the successful evidence.
3. If lint fails from known pre-existing vault hygiene issues, continue only with append-only/new-file handoff work:
   - create a new file under `AI-Sessions/conversations/{persona}/`
   - append one concise `handoff` entry to `log.md`
   - do not rewrite old `raw/`, `conversations/`, or unrelated `wiki/` files
   - treat this as an explicit exception for mandatory scheduled status-note jobs: even when vault rules say “no new writes on lint fail,” the recurring handoff requirement is satisfied by safe append-only/new-file writes plus exact lint reporting, not by stopping silently
4. Read the newest previous `{persona}` work-status note when possible and explicitly state whether any new assigned work progressed since then.
5. For the new note, include at least:
   - current focus / persona responsibility
   - last actions
   - decisions and assumptions
   - blockers
   - next 3-hour plan
   - files/artifacts touched
   - what another agent needs to know
6. Append to `log.md` using append-only mechanics after re-reading its latest tail. Avoid patching a stale tail in concurrent cron windows.
   - If the cron prompt orders `log.md` append before post-write lint, the log entry should accurately say `lint: pre FAIL/PASS ...` (or omit post status). Do not claim `pre/post` in the log until post-lint has actually run; the final scheduler response can report the post-lint result separately.
   - Preferred concrete pattern: use a tiny Python append script (`Path.open('a', encoding='utf-8')`) or shell append so only new bytes are added; do not use a partial tail + replace patch for large append-only logs.
   - **Quoting pitfall**: avoid one-line `python3 -c "... entry='\n...' ..."` through `terminal` when the entry contains embedded newlines, backticks, Korean text, or long Unicode punctuation; shell/Python escaping can produce `SyntaxError` and waste a cron turn. Use `execute_code` for the append script, or write a short temp script/file-backed append if `execute_code` is unavailable.
   - Ensure there is a blank line between the previous entry and the new `## [...] handoff` heading. If the append script only guarantees a single newline and the prior entry has no trailing blank line, read back the tail and patch the separator before finalizing.
   - Preserve any entries from other personas that appeared in the latest tail; do not reorder or rewrite concurrent cron entries just because timestamps are close.
   - If the tail shows pre-existing malformed separators (for example, two `## [...]` headings adjacent with no blank line), do **not** normalize unrelated old log content during a mandatory status-note cron. Append the new entry with its own leading blank line(s), read back to verify preservation, and report only your new note/log append plus lint state.
7. Read back the newly written note and the appended log entry. Confirm the note text is final-state accurate; if it still says `갱신 예정` for a completed append, patch it to `갱신` before reporting.
   - Preferred wording in the note before `log.md` append is either neutral (`이번 실행에서 log.md handoff 항목 append`) or immediately verified after append. Do not leave a note that says the log was already appended unless the append has actually succeeded and was read back in the same run.
   - Avoid leaving future-tense placeholders such as `사후 lint 재실행 대상` in the note. For cron status notes, either (a) omit the post-lint subsection and put the post-lint result only in the final cron response, or (b) run post-lint once after the note/log writes, then patch the note with the final result and **do not rerun the identical lint command just to re-verify the wording patch** unless the patch touched wiki/index/raw rules. This prevents repeated identical lint-failure loops on known pre-existing vault hygiene issues.
   - It is acceptable for the note body to record only the pre-write lint state when the final scheduler response reports the post-write lint. Do not do an extra wording-only patch just to duplicate the same known lint failure inside the note; read-back verification of the created note + log append is enough.
   - Same-minute concurrent persona entries can appear between the tail read and your append. Treat this as normal if append-only mechanics preserved both entries; do not reorder, rewrite timestamps, or try to make your entry the final log item.
8. Run post-write `vault-lint` once after the handoff note and `log.md` append, then report its exact status.
   - Tool-loop warning pitfall: scheduled handoff jobs intentionally run the same lint command twice (pre-write and post-write). If the post-write run returns the same pre-existing failure summary and the tool emits a repeated-failure/loop warning, treat it as expected verification evidence, not a reason to retry. Do not run a third identical lint; summarize the stable pre-existing issues in the final response.

## Final response shape for cron jobs

Keep final output short and local-only because the scheduler handles delivery. Include:

```text
handoff 완료.
- 생성: `AI-Sessions/conversations/{persona}/YYYY-MM-DD-HHMM-{persona}-work-status.md`
- 갱신: `log.md` handoff 항목 append
- lint: PASS
```

If lint fails from existing issues, report a compact failure summary instead of attempting destructive cleanup:

```text
- lint: FAIL — 기존 이슈 유지
  - `wiki/projects/` 명명 위반 N건
  - orphan warning N건
  - raw 0 / sources N warning
  - `_unsorted` conversations N건 warning
```

Do not use `send_message` in scheduled jobs whose prompt says delivery is automatic.
Do not respond `[SILENT]` after creating a required handoff note; `[SILENT]` is only for genuinely no-report watchdog tasks, not mandatory status-note jobs.
