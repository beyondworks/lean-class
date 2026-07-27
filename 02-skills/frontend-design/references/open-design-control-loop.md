# Claude Design / Open Design Control Loop

Use this reference when a user wants Claude Design official-demo-level web output from an AI design generator such as Open Design, Claude Design, or a local CLI-backed artifact builder.

## Control structure

1. **Verify the actual model path**
   - UI labels are not enough. Confirm the running agent process or log contains the chosen model and reasoning flags.
   - Example success shape: `codex exec ... --model gpt-5.5 ... model_reasoning_effort="xhigh"`.
   - If UI/localStorage model settings do not match the spawned CLI flags, trust the process command and fix the source of the spawned flags before drawing conclusions.

2. **Increase inactivity watchdog for long high-fidelity generations when needed**
   - Open Design daemon defaults chat-run inactivity failure to 120s of no agent output (`resolveChatRunInactivityTimeoutMs` in `apps/daemon/src/server.ts`).
   - Start/restart the dev server with a larger environment value when using high-reasoning models or large self-contained HTML artifacts:
     ```bash
     export OD_CHAT_RUN_INACTIVITY_TIMEOUT_MS=600000  # 10 minutes
     corepack pnpm tools-dev start web --daemon-port 7456 --web-port 5173
     ```
   - Verify it actually reached the daemon process:
     ```bash
     ps eww -p <daemon-pid> | tr ' ' '\n' | grep '^OD_CHAT_RUN_INACTIVITY_TIMEOUT_MS='
     ```
   - This is not a substitute for prompt design: still ask the agent to emit progress before long generation steps and to write the artifact early.

3. **Use a brief gate before generation**
   Capture or force answers for:
   - Platform: responsive / desktop / mobile / fixed canvas
   - Audience
   - Reference distance: close study vs same warmth but original vs loose inspiration
   - Motif: the structural metaphor that makes the page memorable
   - Motion policy: static, subtle reveals, precise micro-interactions, one hero moment
   - Copy density
   - Anti-patterns and replacement aesthetic

4. **Lock the visual system before code**
   Ask the agent to state the design surface in concrete terms:
   - Base surface and panel surface
   - One action/accent color and neutral tint
   - Typography roles: display, UI, mono labels
   - Motif primitives: marks, grids, ticks, traces, proof sheets, instruments, etc.
   - Page rhythm: section-by-section composition intent
   - Motion boundaries and reduced-motion behavior

5. **Generate as an artifact, not a generic page**
   Require self-contained code when appropriate, semantic HTML, responsive ranges, focus states, and `prefers-reduced-motion`.

6. **Screenshot QA loop**
   After generation, open the artifact in a browser and capture desktop plus mobile/tablet screenshots. Score:
   - Design quality: coherent color, type, layout, detail
   - Originality: does it avoid obvious AI/SaaS templates?
   - Craft: spacing, hierarchy, contrast, responsiveness, motion restraint
   - Functionality: can a user understand the product and primary action?
   - Anti-slop: absence of purple/blue gradients, glass cards, repeated cards, oversized hero copy, vague AI claims

7. **Refinement prompts must be surgical**
   Do not say “make it better.” Reference visual evidence and name the failed dimension:
   - “Hero is still generic SaaS; replace card grid with an instrument/proof-sheet composition.”
   - “Typography is too large for a control-room product; reduce hero scale and increase information density.”
   - “Accent color appears decorative; restrict terracotta to action/proof states.”

## Prompt skeleton

```text
Create a high-fidelity artifact for [product].

Quality target: Claude Design official-demo level.
Use [reference/design system] as a base, but do not copy it. Desired distance: [same warmth, clearly original].

Brief gate:
- Platform: [responsive]
- Audience: [specific]
- Motif: [structural metaphor]
- Motion: [policy]
- Copy density: [density]
- Hates: [anti-patterns]
- Replacement aesthetic: [positive visual direction]

Before coding, state the visual system and page rhythm.
Then implement a self-contained artifact.
After implementation, self-critique against design quality, originality, craft, functionality, and anti-slop; apply one refinement pass.
```

## Example learned pattern

A strong first-pass direction used:

- Parchment base
- Near-black instrumentation panels
- Terracotta as the only chromatic action
- “Signal desk” motif: scanlines, proof ticks, calibrated control strips
- Editorial serif for voice, warm sans for UI, mono only for instrument labels
- Compact masthead, command-brief hero, product preview, workflow, quality rubric, proof section, quiet CTA

This worked because it replaced banned generic patterns with a concrete, reusable visual metaphor instead of only listing dislikes.
