# Open Design Quality Escalation Notes

Use when iterating Claude Design/Open Design-style generators toward official-demo-level web design quality rather than merely producing a plausible landing page.

## 10-point target rubric

Treat **10/10** as: the artifact could plausibly appear in an official Claude Design demo without looking like a generic AI-generated SaaS page.

Score each run on:
- **Design quality**: composition, hierarchy, color, type, spacing, polish.
- **Originality**: whether the visual language has a memorable concept beyond a standard landing page template.
- **Craft**: fine details, coherent motifs, responsive adaptation, precise visual rhythm across the full page.
- **Functionality**: clear product story, CTA, semantic structure, accessibility, and responsive behavior.
- **Anti-slop**: absence of generic AI fingerprints such as purple/blue gradients, glassmorphism, identical card grids, huge icon cards, stock dashboard mockups, and vague AI copy.

Suggested bands:
- **5/10**: plausible AI SaaS landing page.
- **6/10**: polished but conventional premium landing page.
- **7/10**: avoids generic AI look and has a coherent editorial direction.
- **8/10**: shows a custom product world, stronger motif, and intentional interface artifacts.
- **9/10**: first viewport is memorable, product surface feels real, full page keeps art direction and craft.
- **9.7–10/10**: official-demo quality; distinctive enough that the design reads as art-directed, not prompted.

## Escalation pattern when stuck at 7–8/10

Common 7–8/10 failure: the page looks elegant but behaves like an editorial poster or generic landing-page stack. Push the next run with concrete structural constraints, not broader adjectives.

Effective constraints:
- **Above-the-fold must show the product world immediately.** Do not allow an empty right side or hero-only typography; require a dense real-looking cockpit/product surface in the first viewport.
- **Specify the spatial split.** Example: “right 55% cockpit / left 45% editorial command brief.”
- **Name the cockpit parts.** Example: brief ledger, visual lock matrix, screenshot QA strip, taste gauge, refinement diff, proof stamp, run timeline, status needles.
- **Convert sections into instruments.** Protocol becomes a measured rail; quality gates become a gauge; proof becomes a ledger with stamps and deltas; CTA becomes an operations handoff.
- **Preserve the replacement aesthetic.** Pair each anti-pattern with a desired artifact language, e.g. “no generic card grids; use calibrated measurement rails, stamped labels, connected rule lines, miniature run timeline.”
- **Demand terse product copy.** Official-demo quality usually needs instrument-like labels and short branded terms, not generic AI workflow paragraphs.

## Quick brief handling

Open Design may insert a “Quick brief — 30 seconds” form before building. If radio clicks do not register, answer the same choices as a normal chat message and tell the agent to proceed. Useful answer categories:
- Audience
- Product/job-to-be-done
- Copy density
- Motion policy
- Composition ratio
- Explicit avoid list

## Prompt shape for a 9+ run

```text
Target: 9.0+ official-demo quality.

Observed weakness from previous run:
- [specific visual failure]

Non-negotiable first viewport:
- [composition ratio]
- [dense product/cockpit elements]
- [what must not be blank or generic]

Visual architecture:
- [reference warmth/style distance]
- [surface/palette/type/motif]
- [custom details]

Page rhythm:
1. [hero/product split]
2. [instrument-like protocol]
3. [artifact panel]
4. [gauge/quality gate]
5. [proof ledger]
6. [quiet handoff CTA]

Runtime:
- Create index.html early.
- Emit progress before long steps.
- Keep desktop/mobile screenshots.
- Finish immediately after final note.
```
