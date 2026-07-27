# Open Design Run Operations Notes

Use when operating iterative Open Design / Claude Design-style runs where the user expects every attempt to be captured and sent.

## Durable run-operation lessons

- **Treat generated QA screenshots as artifacts.** Some agents may create screenshots during their own verification, then delete them as “temporary QA files.” If the user wants every run captured, explicitly say: keep desktop/mobile screenshots in the project folder and do not delete QA screenshots.
- **Finish condition matters.** After artifact + screenshots are created, instruct the agent to finish immediately. Otherwise high-reasoning CLI agents can keep looping through cleanup or extra verification even after useful files exist.
- **Stop stale child processes after preserving output.** If the UI still shows Running but `index.html` and screenshots are already on disk, preserve/copy the files first, then stop the run from the UI or terminate the child process. Do not wait indefinitely for a cosmetic completion state.
- **Recapture stable screenshots outside the generator.** Even when the agent creates screenshots, launch a local static server or `file://` preview and recapture known-good desktop/mobile viewports yourself. This gives consistent files to evaluate and send.
- **Telegram/media delivery constraint.** Very tall full-page mobile screenshots can fail to send as a photo. Send mobile as viewport slices (top/middle/bottom) or shorter viewport captures instead of one extremely tall image.
- **Long-thinking agents may need a longer inactivity watchdog.** When Open Design/daemon runs a high-reasoning CLI agent that is useful but silent for long periods, prefer increasing the inactivity timeout through the daemon's supported environment variable over reducing the design ambition. In the observed Open Design repo, `OD_CHAT_RUN_INACTIVITY_TIMEOUT_MS=600000` gave a 10-minute watchdog and allowed long HTML artifacts to complete.
- **Quick brief forms can interrupt autonomous runs.** If a generated “Quick brief” form appears, answer the same choices in chat text when UI radios are unreliable, then explicitly tell the agent to proceed and create the artifact.
- **Design-system documentation clones need a reference bundle, not just a prompt.** Before generation, crawl the sitemap, inventory pages/components, capture representative screenshots, extract computed design tokens, and write a compact absorption document. For the full reusable workflow, see `open-design-quality-loop/references/design-system-doc-cloning.md`; for a concrete Wanted Montage case with observed tokens, see `open-design-quality-loop/references/montage-design-system-case-study.md`.
- **For {{OWNER_TITLE}}, report progress in Korean.** System tool cards may remain English, but assistant-authored updates should explain the operation semantically in Korean instead of foregrounding raw tool names.

## Suggested run prompt clauses

```text
Runtime rules:
- Emit progress before long steps.
- Create the artifact early.
- Do not delete QA screenshots. Save desktop and mobile screenshots if you create them.
- After final screenshots, finish immediately. Do not keep running cleanup loops.

10/10 pixel-craft gate:
- Small components must be optically balanced at px level: aligned borders, baselines, tick marks, panel edges, and CTAs.
- No awkward text wrapping in headings, buttons, labels, or chips; avoid orphaned one-word lines unless deliberately art-directed.
- Repeated gutters, paddings, border radii, and stroke weights must be consistent.
- Desktop grids and mobile stacks must not break, overflow, crop labels, overlap, or create accidental empty zones.
- If a visible component feels off by a few pixels, treat it as a blocker for 10/10 even when the overall direction is strong.

Deliver:
- One self-contained index.html.
- Desktop and mobile screenshots kept in the project folder.
- A concise final note: what changed, known issues, screenshot file names.
```

## Stable recapture pattern

```bash
# Serve the preserved artifact
python3 -m http.server 4892 --directory /path/to/preserved-run
```

```js
// Run from a repo with Playwright available
const { chromium } = require('playwright');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 1 });
await page.goto('http://127.0.0.1:4892/index.html', { waitUntil: 'networkidle' });
await page.screenshot({ path: 'desktop.png', fullPage: false });

const mobile = await browser.newPage({ viewport: { width: 375, height: 900 }, deviceScaleFactor: 1, isMobile: true });
await mobile.goto('http://127.0.0.1:4892/index.html', { waitUntil: 'networkidle' });
const total = await mobile.evaluate(() => document.documentElement.scrollHeight);
for (const [i, y] of [0, Math.max(0, Math.floor(total / 2) - 450), Math.max(0, total - 900)].entries()) {
  await mobile.evaluate((scrollY) => window.scrollTo(0, scrollY), y);
  await mobile.waitForTimeout(100);
  await mobile.screenshot({ path: `mobile_${i + 1}.png`, fullPage: false });
}
await browser.close();
```
