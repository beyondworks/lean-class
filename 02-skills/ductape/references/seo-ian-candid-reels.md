# Seo-Ian candid Reels workflow

Use this when generating Seo-Ian stills or storyboard images for Reels/Shorts.

## Durable story premise
- “Seo-Ian” refers to the established model in `$HOME/Agents/Image-gen/Seo-Ian`.
- Seo-Ian is a 24-year-old woman, engineering graduate, and AI builder.
- Her public SNS persona is a Seoul/nature landscape snap photographer who uses a Leica Q3.
- She usually goes out with a friend. The friend shoots Seo-Ian’s process on an iPhone: photographing, looking at scenery, cafe breaks, mirror OOTD, POV walking, selfies, jokes, and candid vlog clips.
- Seo-Ian posts those friend-shot candid iPhone photos/videos to SNS.

## Generation rule
Do not create Seo-Ian Reels stills from text-only prompts. Use reference-anchored generation with local identity references and camera references.

Recommended refs:
- Identity anchors: `$HOME/Agents/Image-gen/Seo-Ian/Seo-Ian_04.png`, `Seo-Ian_05.png`, `Seo-Ian_06.png` or another user-approved Seo-Ian anchor.
- Leica refs: `$HOME/Agents/Image-gen/Seo-Ian/Leica Q3_01.png`, `Leica Q3_02.png`, `Leica Q3_03.png`.

## Prompt pattern
Include these concepts in every Seo-Ian scene still prompt:

```text
Use Image 1 as the strict Seo-Ian identity anchor. Preserve EXACT same face, exact age, exact Korean ethnicity, exact long straight black hair with soft full bangs, exact slim proportions, exact calm quiet mood. Supplementary images are additional Seo-Ian identity references and Leica Q3 references.

Generate a candid low-quality iPhone snapshot, as if Seo-Ian's friend casually took the photo while walking together. It must not look like a professional fashion shoot, not polished, not cinematic, not studio. Use phone-camera imperfections: slight motion blur, imperfect framing, mild noise, auto-exposure, casual snapshot color, small perspective distortion, real-world Korean phone photo feeling.

Seo-Ian should not be posing for the camera and should not be looking directly into the lens. She is unaware of the photographer or naturally reacting to the situation. Natural expression fitting the scene: quiet, focused, slightly tired, gently absorbed, faintly satisfied, or joking only if the scene calls for it.

Wardrobe continuity: dark Seoul snap-photographer styling, camera strap, Leica Q3 when natural. Keep Leica compact fixed-lens black; no DSLR, no big telephoto.

No text, no watermark, no influencer pose, no model stare, no plastic skin, no airbrushed beauty ad look, no perfect studio lighting, no exaggerated sunset, no identity change.
```

## ima2 command pattern
```bash
HOME=$HOME ima2 gen --stdin \
  --quality high --size 1024x1536 \
  --provider oauth --model gpt-5.5 --reasoning-effort high \
  --out /absolute/output.png \
  --ref $HOME/Agents/Image-gen/Seo-Ian/Seo-Ian_04.png \
  --ref $HOME/Agents/Image-gen/Seo-Ian/Seo-Ian_05.png \
  --ref $HOME/Agents/Image-gen/Seo-Ian/Seo-Ian_06.png \
  --ref $HOME/Agents/Image-gen/Seo-Ian/Leica\ Q3_01.png \
  --ref $HOME/Agents/Image-gen/Seo-Ian/Leica\ Q3_02.png
```

## QC checklist
- Does the image read as the existing Seo-Ian, not just a similar black-haired woman?
- Does it feel like a friend’s iPhone shot rather than a professional fashion/editorial image?
- Is Seo-Ian unaware of or not performing for the camera?
- Is the facial expression situationally natural?
- Is Leica Q3 compact and plausible, not a DSLR/telephoto camera?
- Is the location/context credible for Seoul/Han River or the requested 출사 location?
