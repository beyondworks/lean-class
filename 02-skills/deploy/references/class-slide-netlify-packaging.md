# Class slide Netlify packaging checklist

Use this when converting an instructor slide deck into a student-facing static Netlify bundle.

## Build shape

- Output directory root must contain `index.html`.
- ZIP from inside the output directory so Netlify sees `index.html` at archive root.
- Prefer a standalone HTML with embedded CSS, JS, and data for Telegram/mobile reliability.

## Instructor → student scrub

Remove or neutralize:

- slide `note` fields or other speaker-script data;
- Notes / Presenter buttons and popup code;
- textareas and autosave state/UI;
- strings such as `강사용`, `대본`, `speaker note`, `presenter`, `notes` unless intentionally learner-facing;
- localStorage keys dedicated to instructor notes.

Keep:

- learner-facing slide content;
- previous/next controls;
- fullscreen control;
- keyboard navigation;
- progress/footer metadata if useful.

## Verification pattern

Before delivery, verify with a real browser/automation:

- JS parses and no page errors occur;
- expected slide count renders;
- exactly one slide is active;
- keyboard navigation changes the active slide/hash;
- buttons are only learner controls;
- `window.deckData.slides.some(s => Object.hasOwn(s, 'note'))` is false;
- rendered body contains no instructor-only strings;
- ZIP listing shows `index.html` at root.

## Reporting

Send the ZIP path as the primary deliverable and briefly list the scrub/verification results. For Telegram, include `MEDIA:/absolute/path/to/file.zip`.