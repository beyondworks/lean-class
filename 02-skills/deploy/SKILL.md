---
name: deploy
allowed-tools: []
description: Package and deploy web artifacts, including static Netlify/Vercel class-slide deliverables.
---

# Deploy / Static Web Packaging

Use when preparing a web artifact for deployment or handoff, especially single-page HTML slide decks, static prototypes, and Netlify/Vercel drag-and-drop bundles.

## Core rule

A deployment deliverable is not complete until the artifact has been packaged and actually opened/verified as the audience will receive it. Do not hand over source fragments, shells that depend on missing files, or unverified ZIPs.

## Netlify manual deploy packaging

When the user asks for a Netlify upload package (`https://app.netlify.com/`, “배포용으로 압축”, “수강생 배포용”):

1. Build a clean directory whose root contains `index.html`.
2. Prefer a standalone single-file HTML for Telegram/mobile handoff:
   - embed data/scripts/styles directly;
   - avoid local JS/CSS dependencies unless all files are included in the ZIP with correct relative paths;
   - ensure UTF-8 Korean text is preserved.
3. Create the ZIP from inside the deploy directory so `index.html` is at the archive root, not nested under an extra folder.
4. Verify archive contents with an unzip/list step before delivery.
5. Open the packaged `index.html` in a real browser or browser automation and verify:
   - no JS errors;
   - expected slide/page count;
   - keyboard/buttons work;
   - no overflow/regression in the distributed view.

## Class slide deck privacy modes

For {{OWNER_TITLE}}’s class-slide deliverables, distinguish instructor and student builds:

- Instructor build:
  - include a Notes/new-window speaker script that a lecturer can read aloud;
  - make the script editable when requested;
  - autosave edits per slide;
  - verify the Notes popup, not only the main slide view.
- Student/Netlify distribution build:
  - remove speaker notes, instructor-only script data, presenter controls, Notes buttons, textareas, autosave UI, and presenter windows;
  - scrub visible labels such as “강사용”, “대본”, “speaker note”, “presenter”, “notes” unless intentionally part of learner-facing content;
  - keep only learner controls such as prev/next/fullscreen;
  - verify the runtime data has no `note` field and the rendered body has no instructor-only strings.

See `references/class-slide-netlify-packaging.md` for a concise checklist and verification pattern from the AI Native slide deck session.

## Vercel production deploy

1. Run `vercel --prod` from the project root.
2. After deployment, verify Deployment Protection is disabled when public access is required: Settings → Deployment Protection.
3. Test any webhook endpoint with:
   ```bash
   curl -X POST <deployment-url>/api/webhook -H 'Content-Type: application/json' -d '{"test": true}'
   ```
4. Report the deployment URL and the real test result.

## Reporting back

Return:

- artifact path or deployment URL;
- what was included in the package;
- what was deliberately removed/scrubbed;
- verification results from actual execution.