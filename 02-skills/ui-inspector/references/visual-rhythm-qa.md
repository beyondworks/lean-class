# Visual rhythm QA with UI Inspector

Use this reference when the user asks for UI polish, layout consistency, auto-layout rhythm, icon consistency, or says the design looks systemically inconsistent.

## Rule learned from 사내 시스템 session
Do not judge UI quality from code alone. Run the preview, inspect the rendered screen, and use screenshots/vision QA before and after edits. The user specifically does **not** want decorative changes such as new gradients or color palette changes when the request is about system consistency.

## Visual QA loop
1. Start or attach the live preview.
2. Enable Inspector when element-level selection is needed.
3. Capture/inspect the rendered screen before editing.
4. Evaluate only the requested dimensions:
   - icon size, stroke width, and baseline alignment
   - layout grid and column weight
   - card height, radius, internal padding, and gap rhythm
   - row height and meta-column wrapping
   - button/input/control height and alignment
   - typography scale, line-height, truncation, and Korean label rhythm
5. Patch the smallest CSS/component changes that improve the system without changing the product tone.
6. Re-open/refresh the preview and run visual QA again.
7. Verify build/API/console before claiming completion.

## Avoid
- Adding gradients, new brand colors, decorative accents, or visual novelty unless explicitly requested.
- Claiming design balance from code inspection alone.
- Treating a component as done before checking the real rendered screenshot.
- Optimizing one component while making the page-level column balance worse.

## Useful prompts for visual QA
- “Check icon uniformity, layout rhythm, card/row height, spacing, button alignment, and component auto-layout consistency. Do not suggest color/gradient changes.”
- “Compare before/after rendered balance: sidebar/main/right-panel weight, KPI card alignment, list row wrapping, and inspector/action button rhythm.”
