---
allowed-tools: Bash, Read, Write, Edit
argument-hint: "<bundle-path-or-name> [--language ko|en|auto] [--silence-min 1.8] [--whisper-model small|medium|large]"
description: Cut-edit a Screen Studio (.screenstudio) bundle by removing silences, false starts, and stutters using Whisper word timestamps.
---

Use the `screenstudio-cut` skill to handle this request.

User input: $ARGUMENTS

Follow the skill exactly:
1. Resolve the bundle path (search `~/Screen Studio Projects/` if a name was given).
2. Run pre-flight checks. If Screen Studio is running, refuse and ask the user to Quit.
3. Back up the bundle as `<name>.backup-<UTC-timestamp>.screenstudio`.
4. Extract microphone audio to 16 kHz mono WAV in a `.work-screenstudio-cut-<TS>` directory next to the bundle.
5. Run Whisper with `--word_timestamps True` using the Bash tool's own `run_in_background: true` (NEVER `nohup … &`).
6. After Whisper completes, run `scripts/analyze.py` to produce candidate cuts.
7. Read the full transcript and add sentence-level repetition cuts that the analyzer cannot detect.
8. Validate every cut: word boundaries, zoom overlap, breath margin (0.4s for silences, 0s for false starts).
9. Show the cut table to the user. If they did not pre-authorize automatic apply, wait for confirmation.
10. Run `scripts/apply_cuts.py` to write `project.json`. Report per the skill's template (§ 10).

Honor every guardrail in `SKILL.md` § 5 and watch for the common mistakes in § 6 — especially Mistake A (partial cut leaves first false-start audible) and Mistake B (output-time vs source-time confusion).
