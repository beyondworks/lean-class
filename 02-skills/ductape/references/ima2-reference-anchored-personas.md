# ima2 Reference-Anchored Persona Workflow

Use this note when a local, established virtual influencer/persona must remain consistent across multiple stills or image-to-video scenes.

## Trigger

- User says an established persona is drifting across generated images.
- User asks to use `ima2` / GPT Image 2 / GPT-5 image models with a reference image.
- A project has a local persona library such as `$HOME/Agents/Image-gen/<Persona>/`.

## Why this matters

Independent text-only generation creates plausible but different people. The failure shows up as changed jawline, nose bridge, eye spacing, age, hair density, body proportions, or overall vibe. For a virtual influencer this is a production-blocking failure, not a minor aesthetic issue.

## Canonical command shapes

Reference generation:

```bash
HOME=$HOME ima2 gen "PROMPT" --ref /absolute/path/identity-anchor.png --quality high
```

Edit/recontextualize while preserving the person:

```bash
HOME=$HOME ima2 edit /absolute/path/identity-anchor.png --prompt "Keep the exact same person and face. Change only: [scene/background/outfit/prop]."
```

Status checks before work:

```bash
HOME=$HOME ima2 ping
HOME=$HOME ima2 defaults ls
```

## Prompt prefix

```text
Image 1 is the identity anchor. Preserve the EXACT same face, age, ethnicity, hairstyle, facial proportions, body proportions, and quiet mood from Image 1. Do not invent a new person. No identity change. Only change the scene/action described below.
```

## QC gate before I2V

Reject and regenerate any cut where:

- face reads as a similar stranger rather than the same persona
- age shifts younger/older
- hair length/color/parting changes without intent
- jawline, nose, eye spacing, or cheek structure changes
- body proportions change noticeably
- signature prop/camera mutates, e.g. Leica Q3 turns into DSLR/telephoto

Only after identity passes should the stills be moved to Kling/Grok prompts.
