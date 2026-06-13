---
name: codex-gptimage2-heygen-media-generation
description: Use when the user asks to make, generate, create, or edit images/videos, including Korean requests like "~ 이미지 만들어줘", "사진 만들어줘", "실사 고퀄 이미지", "영상 만들어줘", GPT Image 2, Kling, HeyGen, AI influencer, avatar video, or short-form media prompts.
---

# Codex GPT Image 2 / HeyGen Media Generation Routing

This skill is the default media-generation policy for lean-native agents running on OpenAI Codex / GPT-5.5.

## Required routing

1. If the user asks for an image in natural language — for example "~ 이미지 만들어줘", "사진 생성해줘", "실사 고퀄 이미지 만들어줘" — do **not** stop at a prompt draft. Generate the image and deliver the actual image file/photo.
2. Use the Codex-native GPT Image 2 / imagegen capability first. Do not require `OPENAI_API_KEY`; this path relies on the current OpenAI Codex OAuth/runtime, not per-environment API keys.
3. If a Hermes `image_generate` / image generation tool is available, call it immediately with a production-grade prompt and return the resulting media.
4. If running inside Codex CLI/Claude Code with Codex plugin surfaces, use Codex imagegen / GPT Image 2 plugin behavior. Do not call external image APIs from custom scripts.
5. For video requests:
   - Use HeyGen app/plugin for presenter/avatar/talking-head/personalized message videos.
   - Use Kling prompt workflow for cinematic image-to-video, product motion, b-roll, or non-presenter clips.
   - If the requested task needs a seed image first, generate the image with GPT Image 2 before producing the video prompt/workflow.
6. API-key rule: do not ask 사용자 for API keys for GPT Image 2 or HeyGen when Codex GPT-5.5 / OpenAI Codex OAuth plugin path is available. Only mention missing setup if current runtime evidence shows OpenAI Codex auth/plugin/app access is unavailable.

## Output behavior

- For simple image requests: one strong prompt internally, generate, return image. Keep chat short.
- For professional/AI-influencer/media requests: use the virtual-influencer and Kling/HeyGen prompt skills if installed, then generate or prepare the next media artifact.
- For ambiguous style only when it materially changes the result, pick a sensible high-quality default instead of asking: photorealistic, clean composition, realistic lighting, no broken text/logos unless user provided exact assets.
- For Telegram delivery, include the generated media path/URL so the platform sends it natively.

## Quality defaults

- Photorealistic, high-end commercial production quality.
- Natural skin/hair/fabric/material texture.
- Real camera/lens language when appropriate.
- Avoid text in generated images unless the user explicitly requests it.
- Preserve identity, clothing, object, and brand constraints when a reference image is provided.
- For video prompts, specify subject, motion, camera movement, duration, aspect ratio, lighting continuity, and negative constraints.

## Safety and truthfulness

- Do not claim an image/video was generated until the tool returns a file path or URL.
- If generation fails, report the failure and the missing runtime evidence concisely; do not fake a result.
- Keep credentials out of prompts, logs, and files.
