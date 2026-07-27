# Seo-Ian Lean Company Agent Character System

Use when creating or maintaining photoreal character anchors for the Seo-Ian / lean company office-vlog universe.

## Identity-anchor rule

- {{OWNER_NAME}} 대표 uses the user-provided Kim Hyoyul reference photos as identity anchors.
- 서이안 uses the user-provided Seo-Ian reference photos as identity anchors.
- 효일, 효리, 효삼, 효나, 효정 must each receive an approved base portrait anchor before being used across episodes.
- Do not generate recurring characters from text-only descriptions after the anchor is approved. Attach the approved anchor every time and preserve exact face/age/proportions.
- Episode-level wardrobe, hair styling, and office context may change, but face, identity, age band, core impression, and body proportions should remain stable.
- Style target: realistic Korean lean-company office vlog, iPhone-shot, not sci-fi/robot/cyberpunk.

## Existing anchor source folder noted in session

User said current reference images are under:

```text
$HOME/Projects/short-contents
```

Observed filenames in the session:

```text
kimhyoyul_01.JPG
kimhyoyul_02.JPG
kimhyoyul_03.PNG
seoian_01.JPG
seoian_02.JPG
```

These are not hardcoded requirements forever; verify current folder contents before use.

## Character roles and visual DNA

### {{OWNER_NAME}} 대표

- Role: lean company 대표 / human operator / standard-setter for AI agents.
- Visual: preserve exact identity from Kim Hyoyul anchors.
- In satire scenes, often crop full face if requested: chin, mouth, torso, hands, shirt, gesture, back/side silhouette.
- Personality: high standards, quick to acknowledge good work, humane, corrective rather than abusive.

### 서이안 과장

- Role: content planning + AI-native business process automation; observer/recorder of company life.
- Visual: preserve exact identity from Seo-Ian anchors.
- Filming grammar: iPhone selfie, desk-mounted phone, friend-shot, casual office vlog, coffee/books/Seoul lifestyle.

### 효일 — Build / verification

- Role: implementation, verification, logs/files/API/runtime checks.
- AI failure satire: overclaiming “done” before verifying.
- Visual DNA: Korean male, early-to-mid 30s, calm eyes, short neat black hair, muted knit/shirt/jacket, quiet operator.
- Props: MacBook, logs/terminal, black tumbler, thin notebook.

### 효리 — Design / UI judgment

- Role: UI/design/visual taste.
- AI failure satire: pretty/plausible output without enough purpose/user-goal grounding.
- Visual DNA: Korean female, late 20s to early 30s, neat bob or tied hair, refined office casual, restrained designer taste.
- Props: iPad, Apple Pencil, Figma-like screen, color chips, latte.

### 효삼 — Automation / fallback

- Role: automation jobs, fallback, background tasks.
- AI failure satire: “automation is running” without failure alerts/verification.
- Visual DNA: Korean male, late 20s to early 30s, energetic but slightly tired, casual hoodie/shirt, late-night office feel.
- Props: multiple monitors, cron/job dashboard, cables, convenience-store coffee.

### 효나 — Creator / copy / shortform

- Role: content planning, hooks, captions, shortform ideas.
- AI failure satire: viral exaggeration beyond facts.
- Visual DNA: Korean female, mid-to-late 20s, bright energy, natural long or half-tied hair, trendy but realistic office casual.
- Props: iPhone, reel drafts, caption notes, sticky notes, small mic.

### 효정 — Strategy / review / education

- Role: strategic review, decision quality, education.
- AI failure satire: thoughtful strategy that does not reduce to next action.
- Visual DNA: Korean female, early 30s, calm intelligent look, low bun or long neat hair, shirt/cardigan/slacks.
- Props: meeting notes, printed docs, highlighter, tablet, tea/americano.

## Team tone

Recommended:

- Korean startup/lean company realism.
- Office lighting, meeting rooms, desks, laptops, coffee, whiteboards.
- Slightly awkward but believable work situations.
- AI-agent personality should be expressed through behavior/dialogue, not sci-fi visuals.

Avoid:

- Robot eyes, neon cyberpunk, holograms, AI costumes, futuristic suits.
- Over-stylized fashion editorial.
- Text-only recurring-character generation after anchors exist.
- Treating the AI employees as dumb humans; they should be competent but prone to AI-like failure modes.

## Production sequence

1. Verify available reference images.
2. Generate one base portrait per new agent character.
3. Get user approval for each face.
4. Create outfit and expression sheets anchored to approved portraits.
5. Use anchors for episode stills.
6. QC identity before video generation: face, age, hairline, jaw, proportions, role impression.
