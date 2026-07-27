# GPT Image 2 Scene Stills for I2V Reels

## Trigger
Use this when turning a virtual influencer/character into a short-form Reel/Shorts/TikTok pipeline where still images will become Kling/Grok image-to-video clips.

## Pattern
1. Build the short as `scene stills first`, not as a single storyboard collage.
2. Generate one clean 9:16 portrait still per clip/scene.
3. Keep image-internal text, captions, titles, logos, and subtitles out unless the user explicitly asks for pixel-locked text. Add captions later in CapCut.
4. Preserve character identity with reference images and repeat identity anchors, but also lock the scene-specific object/camera if it matters.
5. For real-location creator content, learn or document the place before prompting: viewpoints, time window, light behavior, surrounding buildings/shops, visitor age/style, and the creator’s reason for being there.
6. After generation, copy cache outputs into a named project asset directory with semantic filenames before reporting paths.

## Recommended output filenames
```text
01_hook_portrait_[location].png
02_arrival_walk_[location].png
03_waiting_[location].png
04_framing_or_action_[location].png
05_final_result_[location].png
```

## Prompt notes
- If the user says “GPT Image 2 only / no other model,” explicitly report the actual model returned by the generation tool when available, e.g. `gpt-image-2-medium`.
- For camera-creator personas, include the fixed camera as a physical prop and negative-lock generic substitutes. Example: `Leica Q3 with black strap; no DSLR, no telephoto lens, no generic mirrorless camera`.
- For I2V readiness, avoid extreme hands, tiny faces, busy text signage, and collage grids. Prefer medium shot, waist-up, or clean landscape result frames.

## QA before moving to video
- Character identity and hairstyle held.
- Fixed camera/prop did not drift into a wrong device.
- Location mood matches the learned place and time window.
- Hands, camera grip, and face are usable for I2V.
- No accidental text/watermark/subtitle appeared.
- Final scene can function as a still “result photo” if the concept requires it.
