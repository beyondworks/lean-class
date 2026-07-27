# Seo-Ian Friend-Shot Reels Workflow

Use this when generating stills for an established virtual persona whose SNS concept is a friend-shot 출사/vlog diary rather than polished AI model photos.

## Persona contract

- `서이안` refers to the approved Seo-Ian model in `$HOME/Agents/Image-gen/Seo-Ian`.
- Character: 24-year-old Korean woman, engineering graduate, AI-native developer.
- Public SNS persona: Seoul/nature snap photographer carrying a Leica Q3.
- Narrative device: Seo-Ian is usually with a close friend. The friend shoots her outings on an iPhone; Seo-Ian posts those candid photos/videos to Reels/Shorts.

## Mandatory generation approach

1. Do not use text-only generation for Seo-Ian multi-scene stills.
2. Attach Seo-Ian identity anchors every time. Prefer 2–3 approved references such as `Seo-Ian_04.png`, `Seo-Ian_05.png`, `Seo-Ian_06.png`.
3. Attach Leica Q3 references when the camera appears: `Leica Q3_01.png`, `Leica Q3_02.png`, etc.
4. Prompt the image as a low-quality candid iPhone friend shot, not a professional campaign image.
5. Generate B-roll assets in addition to main scene stills: camera strap/detail, cafe table with book/coffee/Leica Q3, final landscape photo, short talking-to-friend cut.
6. QC identity before video: if any still reads as “similar woman” rather than Seo-Ian, regenerate before Kling/Grok.

## Prompt skeleton

```text
Seo-Ian story reference: Seo-Ian is a 24-year-old Korean woman, engineering graduate and AI-native developer. On SNS she appears as a Seoul/nature snap photographer who carries a Leica Q3. She always travels with a close friend who casually records her photography outings on an iPhone.

Reference handling: Image 1, Image 2, and Image 3 are Seo-Ian identity anchors. Preserve EXACT same face, exact age, exact Korean ethnicity, exact long straight black hair with soft full bangs, exact slim proportions, and exact calm quiet mood. Image 4 and Image 5 are Leica Q3 camera references. Preserve the compact fixed-lens Leica Q3 feeling whenever the camera appears.

Visual style: candid low-quality iPhone snapshot, imperfect framing, slight phone noise, mild motion blur, auto-exposure, casual Korean daily-life color, real friend-shot/vlog texture. Not cinematic, not fashion editorial, not beauty ad, not studio, not glossy, not a tourist poster.

Behavior: Seo-Ian should look natural and unposed. She should not be performing for the camera. If she speaks, she is talking briefly to her friend, not presenting to an audience. Expressions must be situation-specific: focused, quietly pleased, curious, slightly tired, playful only when appropriate.

Constraints: 9:16 vertical Reels still. No text, no captions, no watermark, no logo overlay. No identity change, no new person, no plastic skin, no airbrushed face, no influencer posing, no exaggerated sunset, no wrong camera, no DSLR, no large telephoto lens.
```

## Useful shot list for 25–30s Reels

Main scene stills:
- Hook: Seo-Ian looking at the Han River, not at the camera.
- Arrival/walk: friend follows beside/behind her.
- Waiting: Seo-Ian sits/leans near railing, waiting for light.
- Shooting: Seo-Ian frames the river with Leica Q3.
- After-shot: Seo-Ian checks the result, tiny satisfied expression.

Additional B-roll/talking stills:
- Leica Q3 strap/detail while walking.
- Cafe table: book, coffee, notebook, Leica Q3, Seo-Ian partly in frame.
- Final landscape photo taken by Seo-Ian.
- Short talking cut: Seo-Ian turns slightly toward her friend and says one short line.

## Local ima2 pattern

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
