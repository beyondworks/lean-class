---
name: codex-gptimage-heygen-video-wrapper
description: Use when producing or modifying AI video/image generation workflows that reference auto-contents, auto-video, GPT Image, Heygen, Codex, CapCut, or short-form production assets
---

# Codex GPT Image 2 + Heygen Video Wrapper

## Overview

This is a wrapper skill for the user AI video production workflow. It preserves existing `auto-contents` / `auto-video` skills and code, but overrides the image/video generation backend assumptions for 팀 페르소나's work.

Do not edit the original auto-contents skill just to change providers. Load this wrapper when working with `~/Agents/auto-contents`, then use the original skill/codebase as the pipeline reference while applying the provider overrides below.

## Canonical Reference

Use this local repo as the video generation harness reference:

```text
~/Agents/auto-contents
```

Important existing references:

```text
~/Agents/auto-contents/.claude/worktrees/determined-edison/skills/auto-video/SKILL.md
~/Agents/auto-contents/.claude/worktrees/determined-edison/skills/nano-banana-prompt-translator/SKILL.md
~/Agents/auto-contents/scripts/
```

## Provider Overrides

When existing docs, agents, scripts, or skills say:

- `Nano Banana`, `Imagen`, `Imagen 4`, `gemini_image.py`, or image generation via Gemini → use **Codex-based GPT Image 2** for image generation.
- `Veo`, `Veo3`, `veo3_video.py`, `Kling`, or other video generation backend → use **Codex-based Heygen** for video generation.

Keep all higher-level pipeline structure intact unless the user asks otherwise.

## Working Rule

For future image/video asset generation:

1. Use `~/Agents/auto-contents` for project structure, scene planning, script organization, subtitles, CapCut integration, and QA conventions.
2. Generate images through Codex with GPT Image 2.
3. Generate videos through Codex with Heygen.
4. Feed generated assets into ffmpeg/CapCut pipelines.
5. Keep CapCut editable drafts and SRT/subtitle files as first-class deliverables.
6. Prefer source-first editing for Shorts/Reels/TikTok: research/scrap source footage first; use GPT Image 2/Heygen only for missing or unsafe shots.

## Preserve From Existing Auto-Contents

Continue using these patterns from auto-contents unless contradicted by the provider override:

- Video-first planning: set runtime first, derive scene count and word budget.
- Scene-level image/video assets.
- Character anchor images before scene generation.
- Explicit ethnicity/skin tone/identity anchors in prompts.
- TTS and voice generation as separate scene-level artifacts.
- WhisperX or alignment-based subtitle synchronization when available.
- CapCut project generation using the existing generator rather than hand-writing draft JSON when a reliable generator exists.
- Copy media into CapCut `Resources/`.
- Maintain editable SRT/CapCut text tracks.

## Shorts-Specific Rule

For 지식창/패션탐정냥-style Shorts, Reels, TikTok, AI influencer reels, or any source-first short-form task, also load and follow:

```text
strict-shortform-production-rules
```

Do not default to HTML/Remotion/web-rendered videos.

Use this order:

1. Research high-performing overseas long-form/short-form source videos.
2. Analyze scene rhythm, hook points, zooms, cuts, and retention structure.
3. Use official/licensed/user-provided footage when possible.
4. Use GPT Image 2/Heygen only to fill missing shots or create safe replacements.
5. Edit with ffmpeg/CapCut as 1–3 second shots, zooms, reorders, and subtitle-driven pacing.
6. Deliver a CapCut-editable draft plus SRT, preview MP4, contact sheet, edit manifest, and QA score.

Hard gate: do not deliver a short-form result if it violates the immediate-fail conditions in `strict-shortform-production-rules`.

## Mike Tyson Case Study Learnings

Use `~/Agents/auto-contents/projects/niche-bending/ep02-mike-tyson` as the canonical completed longform example.

Verified production facts:

- 16:9 AI cinematic documentary, `EP02-MikeTyson-aligned`.
- 4:10 target runtime, 25 scenes, 25 scene images, 25 scene videos, 25 scene narration WAVs.
- Scene video total about 246.96s; scene narration total about 219.68s.
- Four era anchors: young, champion, post-prison, older.
- `script.md` + `script-ko.md`, `image-prompts.md`, `video-prompts.md`, `capcut-config-aligned.json`, `capcut-export/subtitles.aligned.srt`, `alignment/*.json` are the files to inspect first.

Reusable process:

1. Decide runtime first.
2. Derive scene count from clip length.
3. Derive word budget from runtime and speaking speed.
4. Research facts before writing narrative.
5. Create era/identity anchors before scene images.
6. Generate scene images as stable keyframes.
7. For I2V prompts, do not redescribe the image; describe movement, camera, and end state only.
8. Generate scene-level narration, not only one giant narration file.
9. Use script-based forced alignment instead of manual SRT timestamps.
10. Build SRT from video-timeline offsets.
11. In CapCut config, video timeline is the source of truth; place each audio clip at its corresponding video scene start offset.
12. Copy media into CapCut `Resources/` and verify the draft opens.

Critical pitfalls from the Tyson project:

- Character identity breaks if ethnicity/skin tone/body/age/era are omitted. Repeat stable identity traits in every prompt.
- Manual SRT timestamps drift badly over long videos; Tyson had ~12.8s cumulative drift before WhisperX forced alignment.
- Raw Whisper transcription can drift on proper nouns and numbers; align from `script.md` when the script is authoritative.
- Compound numbers and synonyms need normalization (`twenty-seven` ↔ `27`, `KO` ↔ `knockout`).
- If video and audio are each laid sequentially, they desync because video total and narration total differ. Audio must start at the matching video scene offset.
- CapCut draft JSON alone may not show in the home screen; root/meta/index behavior and `Resources/` matter.

For 팀 페르소나's provider override:

- Keep the Tyson/auto-contents structure.
- Replace Gemini/Nano Banana image generation with Codex → GPT Image 2.
- Replace Veo/Kling video generation with Codex → Heygen.
- Preserve Video-First planning, scene-level assets, anchors, forced alignment, CapCut draft, and SRT.

Full learning note:

```text
~/lean-native/output/mike-tyson-video-process-learning.md
```

## Common Mistakes

- Do not say the old skill must be edited. This wrapper intentionally keeps the old skill intact.
- Do not follow old provider names literally if they conflict with this wrapper.
- Do not treat GPT Image 2/Heygen outputs as the whole video by default; they are assets for the edit unless the user asks for fully AI-generated video.
- Do not deliver only a flattened MP4 when the user needs CapCut iteration. Provide editable assets/draft/SRT too.
- Do not use HTML/Remotion/Hyperframe as the default visual layer for source-first Shorts.

## Quick Mapping

- Image generation: Codex → GPT Image 2
- Video generation: Codex → Heygen
- Pipeline/structure: `~/Agents/auto-contents`
- Final editing: ffmpeg + CapCut
- Editable delivery: CapCut draft + SRT + preview MP4
