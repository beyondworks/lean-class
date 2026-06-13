---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", "check my site against best practices", or for accessibility and design audits.
metadata:
  author: vercel-labs (optimized 2026-01)
  version: "2.0.0"
  argument-hint: <file-or-pattern>
allowed-tools: []
---

# Web Interface Guidelines

Review files for compliance with modern web interface best practices.

## How It Works

1. Read the specified files (or prompt for files/pattern)
2. Check against all rules below
3. Output findings in `file:line` format

## Guidelines Checklist

### Accessibility

- Interactive elements need visible `:focus-visible` (never `outline-none` alone)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates need `aria-live="polite"`
- Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<article>`) before ARIA
- Headings hierarchical `<h1>`–`<h6>`; include skip link
- Icon buttons need `aria-label`

### Forms

- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste (`onPaste` + `preventDefault`)
- Labels clickable (`htmlFor` or wrapping control)
- Errors inline next to fields; focus first error on submit
- Placeholders end with `…` and show example pattern

### Animation

- Honor `prefers-reduced-motion`
- Animate `transform`/`opacity` only (compositor-friendly)
- Never `transition: all`—list properties explicitly
- Animations interruptible—respond to user input mid-animation

### Typography

- `…` not `...`
- Curly quotes `"` `"` not straight `"`
- Non-breaking spaces: `10 MB`, `⌘ K`
- Loading states end with `…`: `"Loading…"`
- `font-variant-numeric: tabular-nums` for numbers
- `text-wrap: balance` or `text-pretty` on headings

### Content Handling

- Text containers handle long content: `truncate`, `line-clamp-*`, or `break-words`
- Flex children need `min-w-0` for text truncation
- Handle empty states—don't render broken UI

### Images & Performance

- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold images: `loading="lazy"`
- Above-fold images: `priority` or `fetchpriority="high"`
- Large lists (>50 items): virtualize
- No layout reads in render (`getBoundingClientRect`, `offsetHeight`)

### Navigation & State

- URL reflects state—filters, tabs, pagination in query params
- Links use `<a>`/`<Link>` (Cmd/Ctrl+click support)
- Destructive actions need confirmation or undo

### Touch & Interaction

- `touch-action: manipulation` (prevents zoom delay)
- `overscroll-behavior: contain` in modals/drawers
- Buttons/links need `hover:` state

### Dark Mode & Theming

- `color-scheme: dark` on `<html>` for dark themes
- `<meta theme-color>` matches page background
- Native `<select>`: explicit `background-color` and `color`

### Content & Copy

- Active voice: "Install the CLI" not "The CLI will be installed"
- Title Case for headings/buttons
- Numerals for counts: "8 deployments"
- Error messages include fix/next step

## Anti-patterns (Flag These)

- `user-scalable=no` or `maximum-scale=1`
- `onPaste` with `preventDefault`
- `transition: all`
- `outline-none` without focus-visible replacement
- Inline `onClick` navigation without `<Link>`
- `<div>` or `<span>` with click handlers (should be `<button>`)
- Images without dimensions
- Large arrays `.map()` without virtualization
- Form inputs without labels
- Hardcoded date/number formats (use `Intl.*`)
- `autoFocus` without justification

## Output Format

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion

## src/Modal.tsx

src/Modal.tsx:12 - missing overscroll-behavior: contain

## src/Card.tsx

✓ pass
```

State issue + location. Skip explanation unless fix non-obvious.
