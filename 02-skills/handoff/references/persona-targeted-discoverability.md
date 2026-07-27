# Persona-targeted handoff discoverability

## Lesson

A persona handoff is not complete just because a file exists somewhere or a target profile can answer in a one-shot run. The receiving persona must be able to discover the handoff through the paths it normally searches.

## Required discoverability checks

When handing work from one Hermes persona to another:

1. Write the standard Obsidian conversation handoff.
2. Write the target profile-local handoff when the profile directory exists.
3. If the project has its own visible handoff directory, write a repo-visible handoff there too.
   - lean-native example: `$HOME/lean-native/docs/handoffs/{topic}-from-{sender}.md`
4. If the project has a Company Truth Source / ledger, register the handoff there as well.
   - lean-native example: SQLite `claude_web_ui/data/lean-native.db`, `handoffs` row + `events` row with `type='handoff.created'`.
5. Verify from the receiving persona's expected search surface, not only from the sender's filesystem.
6. If the user expects a visible reply in Telegram, distinguish:
   - local stdout acknowledgement from `HERMES_PROFILE=... hermes -z ...`
   - actual Telegram delivery via `hermes send` or gateway routing

## Pitfall from session

효리 created:
- Obsidian handoff under `conversations/lean-native/`
- hyoil profile-local handoff under `.hermes/profiles/hyoil/handoffs/`

효일 later reported no handoff because it searched:
- latest `conversations/hyori/` work-status
- Company Truth Source DB
- `$HOME/lean-native/docs/handoffs/`

The fix was to add a repo-visible handoff and Company Truth Source record, then rerun the hyoil profile acknowledgement with those exact paths.
