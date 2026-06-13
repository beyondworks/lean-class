---
name: virtual-influencer-reference-remake
description: Use when recreating a provided short-form video with a different authorized virtual influencer/model using GPT Image/OpenAI images, Kling image-to-video, lip-sync, CapCut, or browser-based video generation.
---

# Virtual Influencer Reference Remake

## Core Principle

Match the reference video by **structure, camera, timing, motion, subtitles, and props** while replacing only the authorized model identity. Do not promise exact identity/99% matching from generative tools alone; use iterative QA, short clips, overlays, and CapCut assembly.

## Mandatory Preconditions

- Confirm the model image is authorized for synthetic video generation and public use.
- Analyze the reference video to the end before prompting.
- Keep source/reference files and generated outputs in a run folder.
- Use 9:16, 1080×1920+ when possible, 30fps default.

## Workflow

1. **Probe + extract**
   - `ffprobe` duration/FPS/resolution/audio.
   - Extract 1fps frames and scene/contact sheets.
   - If available, run `claude-watch`; if transcript fails, continue with frames and OCR/manual subtitle notes.

2. **Reference breakdown**
   - Write second-by-second notes: shot type, pose, mouth state, camera, objects, text, background, lighting.
   - Group by production segments: hook, proof, process, tutorial, product/UGC examples, CTA.
   - If there are multiple reference videos, analyze the set but **pilot the first video first** unless the user explicitly asks to batch all at once.

3. **Workflow substitution plan**
   - Identify tool-specific claims in the reference video (e.g. Manus, Notion/Instagram integrations, app-specific skills).
   - Preserve the shot rhythm and teaching structure, but replace those tool claims with the user's requested production stack.
   - For GPT Image + Kling remakes: keyframes/identity via GPT Image/OpenAI images, motion/lip-sync via Kling, exact text/UI via CapCut or ffmpeg overlays.

4. **Identity bible**
   - Lock visible model DNA: hairstyle, face styling, outfit, lighting, camera look, background constraints.
   - Use one canonical face reference as Image/Element #1 in every generation.

5. **Fashion/style variants**
   - When the user asks for multiple outfit references on the same virtual influencer, run one outfit style per generation/edit instead of attaching every fashion reference at once.
   - Attach the canonical model as the identity anchor, the current fashion image as the garment/style reference, and optionally a pose/composition image.
   - Explicitly preserve face, hair, bangs, makeup, body proportions, and camera texture; change only outfit, accessories, pose, and styling.
   - For full-look outputs, require `full outfit visible from head to shoes` so shoes/boots are not cropped out.

6. **Recurring creator room / environment bible**
   - When a reference video repeatedly shows the creator's own room, desk, PC, and interior, build a reusable space bible before generating new clips.
   - Preserve the uploaded room's structural DNA (wall texture, window, desk/shelf geometry, PC layout, wall frames), but remove clutter and add character-specific signature objects.
   - For a virtual influencer/가상 인플루언서, use a minimal beige/white/charcoal creator room with black glossy accents, silver details, curated fashion/AI desk objects, abstract moodboard monitor, and no readable generated text.
   - Generate a clean room still first; reuse it as a room reference/start frame. Do not let Kling redesign the room from text on every clip.
   - Exact PC/UI text belongs in CapCut/ffmpeg overlay; generated monitors should be clean plates or abstract moodboards.

7. **GPT Image / OpenAI images**
   - Use reference-image editing/generation, not pure text-to-image.
   - Preserve identity; change only scene, pose, outfit, and props.
   - Generate the 6–10 key stills that map to reference segments.
   - Public docs may call the model GPT Image / Images API rather than “GPT Image 2”; verify current naming in official docs.

5. **Kling I2V / lip-sync**
   - Generate 3–5s clips. One clip = one action + one camera behavior.
   - Use Elements/multi-image: #1 identity face, #2 outfit, #3 background, #4 product only if needed.
   - For lip-sync, use frontal/3⁄4 medium close-up, mouth visible, clean audio, no hand/prop covering lips.
   - Prefer base video with subtle head movement and stable camera; then apply lip-sync.

6. **Overlay instead of generating risky text**
   - Product labels, UI screens, Korean captions, app screens, and price cards should usually be CapCut/ffmpeg overlays, not generated inside Kling.
   - Use generated video as the human motion layer; keep exact UI/text as editable assets.
   - When the user asks for typo-free brand/product text inside a generated clip, prefer a **two-still start/end-frame workflow**: create a front-label still and a rear/detail-label still, then use Kling only for a 3–4s controlled rotation while preserving pixels. If text must be guaranteed, generate blank label areas and add exact logos/labels as overlays.

7. **QA loop**
   - Compare against reference by segment: composition, face continuity, mouth sync, hand/prop artifacts, subtitle timing, cut rhythm.
   - Regenerate only failing clips; do not restart the entire video.
   - Hard fail: identity drift, distorted mouth/teeth, unreadable required text, hand/food warping in hero shots, wrong timing.

## Prompt Blocks

### OpenAI/GPT Image identity-preserving still

```text
Use the provided reference image as the strict identity source. Create a photorealistic 9:16 frame of the same person in [reference-video scene]. Preserve the same face, hairstyle, skin tone, makeup mood, body proportions, and natural asymmetry. Change only [scene/pose/prop]. Real phone-camera/UGC look, natural skin texture, no plastic skin, no identity change, no watermark, no text overlay.
```

### Kling stable speaking base

```text
The same woman as the reference looks directly into the camera, blinks naturally, makes a subtle head tilt and returns, shoulders move gently with breathing. Clear visible mouth, calm talking-ready expression, stable handheld phone camera, single continuous shot, no cuts.
```

Negative:

```text
identity change, different face, face morphing, distorted mouth, extra teeth, warped lips, bad hands, extra fingers, flickering face, sudden camera movement, scene cut, plastic skin, cartoon, low quality
```

### Kling food/product action

```text
Subject performs one small controlled action: [lift food / take one bite / raise can / point at screen]. Camera stays static, face remains stable, background unchanged, natural hand motion only.
```

Negative add-ons:

```text
food warping, hand morph, finger duplication, label distortion, text scramble, mouth distortion, jaw stretch
```

## Browser / Kling UI Operation

- If the user uses a logged-in GUI browser such as Comet, first verify whether the target Kling tab/window exists and whether non-sensitive popups block it.
- Background operation may be possible through macOS Accessibility even when the browser is not frontmost, but uploads/downloads/visual QA can still require the window to be visible or raised.
- Never handle login, password, 2FA, payment, or credential dialogs. Ask the user to complete those.
- Dismiss ordinary browser UI only when it clearly blocks the task, such as translation prompts.

## Common Mistakes

- Asking Kling for 10–30s complex speech/action in one generation → split into 3–5s clips.
- Describing the full appearance in every Kling prompt → can cause drift; use images as anchors and prompt mostly motion.
- Expecting generated app/product text to stay readable → overlay exact UI/text later.
- Generating eating + talking + hand gestures simultaneously → separate into bite/chew/talk clips.
- Reusing a copied reference video as source footage → use it as timing/style reference only unless rights are granted.

## References / Session Notes


## Sources to Check

- OpenAI Image Generation guide: https://platform.openai.com/docs/guides/image-generation
- OpenAI Images API: https://platform.openai.com/docs/api-reference/images
- OpenAI image/video policy guidance: https://openai.com/policies/creating-images-and-videos-in-line-with-our-policies/
- Kling official app/docs: https://app.klingai.com/ and https://app.klingai.com/global/dev/document-api
- PromptHero Kling guide: https://prompthero.com/academy/kling-ai-prompt-guide
