---
name: strict-shortform-production-rules
description: Use when producing, reviewing, planning, or QAing Shorts/Reels/TikTok videos, especially source-first Korean Shorts, Jisikchang/Tamjeongcat-style edits, AI influencer reels, CapCut drafts, or GPT Image 2/Heygen short-form assets.
---

# Strict Shortform Production Rules

## Purpose

This skill defines hard production and QA rules for the user short-form videos. Use it to prevent vague “looks okay” judgments.

Applies to:

- YouTube Shorts
- Instagram Reels
- TikTok
- 지식창/패션탐정냥-style Korean Shorts
- source-first scrap edits
- AI influencer/tool demo reels
- GPT Image 2 / Heygen / CapCut short-form workflows

Canonical full document:

```text
~/lean-native/output/strict-shortform-production-rules.md
```

Session research synthesis:

```text

```

## Absolute Rules

1. Source research/scrap comes before generated visuals.
2. CapCut editable draft is the primary deliverable; preview MP4 is only for QA.
3. HTML/Remotion/Hyperframe must not be the main visual layer for Shorts/Reels/TikTok.
4. GPT Image 2/Heygen outputs are gap-fill or safe replacement assets unless the user explicitly asks for fully AI-generated video.
5. Every final edit needs `edit_manifest.json`, SRT/editable captions, preview MP4, contact sheet, and QA score.

## Platform Specs

- Aspect: 9:16
- Resolution: 1080×1920
- FPS: 30fps default
- TikTok default length: 9–21s
- Instagram Reels default length: 7–30s
- YouTube Shorts default length: 15–35s
- Korean information/story Shorts default: 32–52s
- 60s+ requires explicit story reward.

Safe zone for 1080×1920:

- Important text: X 120–840, Y 220–1450
- Avoid: right X 860–1080, bottom Y 1450–1920, top Y 0–160
- CTA: Y 1250–1450 preferred

## Research Minimums

If matching a specific high-performing channel:

- Analyze at least 20 full videos per channel.
- Do not judge from the first 5 seconds only.
- For each video, collect contact sheet, Whisper/transcript, first 5s text, last 20% payoff, cut rhythm, and 5-part structure.

For new topics:

- Candidate sources: minimum 50, preferred 80–100.
- Final usable sources: at least 10 when possible.
- Classify every source:
  - `usable`: official/public-domain/licensed/user-provided/self-shot
  - `reference-only`: rhythm/zoom/structure only; do not reuse clips
  - `gap-fill`: GPT Image 2 / Heygen safe replacement

## Hook Rules

First 1 second must show one of:

- result
- danger
- conflict
- reversal
- proof/evidence
- famous person/event
- money/loss/value
- strange action

Forbidden openings:

- logo
- greeting
- long context
- empty frame
- vague aesthetic shot
- subscribe/follow request
- static face with no information

First subtitle must appear within 1 second. By 3 seconds, the viewer must know why to keep watching.

## Five-Part Retention Structure

All Shorts must follow this structure:

1. 0–20%: Hook + delayed answer. Do not reveal the conclusion.
2. 20–60%: Evidence, examples, process, comparison. No pure background explanation.
3. 60–80%: Tension peak — real risk, hidden constraint, failure point, scale, or reversal setup.
4. 80–100%: Payoff — result, reversal, lesson, short action, or CTA.

Immediate fail if:

- No delayed reveal.
- No tension peak.
- No last-20% payoff.
- Good clips exist but do not match story beats.

## Pacing Rules

- Standard shot: 1–3s
- Normal scene unit: 2–3s
- Tension/emphasis cut: 0.4–1.0s
- Avoid 3s+ same screen.
- Fail 5s+ same information state.

Cut frequency targets:

- Jisikchang-style: 0.2–0.4 cuts/s acceptable
- Weak knowledge topic: 0.4+ cuts/s
- Tamjeongcat-style: 0.5–0.8 cuts/s
- Tamjeongcat-style below 0.4 cuts/s is too slow.

## Korean Voice / Script Density

- Target narration density: 6.6–7.0 Korean chars/s
- Acceptable range: 5.8–8.4 chars/s
- Avoid slow documentary tone for weak topics.
- Each sentence must have one role: hook, question, evidence, comparison, reversal, interpretation, payoff, CTA.
- Delete empty intensifiers and repeated explanations.

## Caption Rules

- Captions are a retention device, not decoration.
- First caption within 1s.
- One line: roughly 10–16 Korean chars.
- Max 2 lines.
- Highlight only key words.
- Avoid bottom 25–30% and right UI zone.
- Use SRT/CapCut editable text first; avoid burn-in during drafts.
- Remove Whisper hallucinations from trailing silence.

## Source-First Editing Rules

Source priority:

1. official/public-domain/licensed media
2. user-provided/approved media
3. self-shot/screen-recorded media
4. AI-realistic gap-fill
5. high-performing overseas videos as reference-only

Clip rules:

- Select clips in 1–3s units.
- Avoid over-reliance on one source.
- Avoid repeated shot families.
- Avoid talking-head dominance.
- Reject black bars, letterbox, squeezed crop.
- Replace clips with English lower-thirds/logos that clash with Korean captions.

Default 9:16 crop:

```bash
scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1
```

## CTA Rules

- Only one CTA.
- Place it in the last 15–20%.
- CTA must connect to delivered value.
- Never start with follow/subscribe.

Recommended:

- “원본 소스 필요하면 댓글에 DART.”
- “프롬프트 필요하면 댓글에 프롬프트.”
- “나중에 써야 하니 저장해두세요.”
- “어느 버전이 더 자연스러운지 골라주세요.”

## Format Formulas

### Jisikchang-style

Formula:

```text
strange event/action → delayed reason → principle/background → reversal/result
```

Good hook:

```text
NASA는 멀쩡한 우주선을 일부러 소행성에 박살냈습니다.
```

Bad hook:

```text
NASA의 DART 미션은...
```

### Tamjeongcat-style

Formula:

```text
famous person/fashion event → fast cases → hidden reason/industry pattern → short gossip closure
```

Needs faster rhythm than Jisikchang.

### AI influencer/tool demo

Formula:

```text
visual proof → test cases → tool/method reveal → asset/link/prompt CTA
```

Every scene should answer “이것도 돼?” with visible evidence.

## Immediate Fail Conditions

Do not deliver if any apply:

- No hook in first 1s.
- No reason to keep watching after 5s.
- Conclusion revealed in first 20%.
- No five-part retention structure.
- No delayed reveal.
- No 60–80% tension peak.
- No last-20% payoff.
- Clips are good but story beats do not match narration.
- Repeated image/source.
- Talking head dominates.
- Black bars, letterbox, squeezed crop.
- English lower-thirds/logos clash with Korean captions.
- HTML/Remotion/Hyperframe is the main visual layer.
- Only a flattened MP4 exists when iteration is needed.
- Contact sheet is mostly black/low-information frames.
- Reference-only video is used like copied source footage.
- Copyright risk is not recorded in manifest.

## QA Scorecard

Score 1–10:

1. Hook strength
2. First-frame curiosity
3. Five-part structure
4. Cut rhythm
5. Caption readability/sync
6. Voice density/emphasis
7. Scene-to-narration match
8. Payoff strength
9. Loop/CTA
10. Copyright/reuse safety

Passing rules:

- Every category 8+.
- Core categories 9+: hook, five-part structure, scene-to-narration match, copyright safety.
- Average 9.0+: internal pass.
- Average 9.5+: upload candidate.
- Average 9.8+: target quality.

## Required Deliverables

```text
clips/
voice/full.wav
subtitles/*.srt
capcut_config.json
CapCut draft
edit_manifest.json
preview.mp4
qa/contact_sheet.jpg
qa/score.md
sources/source_manifest.json
```

`qa/score.md` must include scorecard, immediate-fail status, weakest 2 issues, and next 1–2 fixes.

## References

Official/platform:

- YouTube Help — Create YouTube Shorts: https://support.google.com/youtube/answer/10059070
- YouTube Shorts Help Topic: https://support.google.com/youtube/topic/10343432
- YouTube Blog — Longer Shorts: https://blog.youtube/news-and-events/youtube-shorts-longer-videos-updates/
- YouTube Creators — Shorts: https://www.youtube.com/creators/shorts/
- Instagram Help — Reels: https://help.instagram.com/270447560766967
- Instagram Creators: https://creators.instagram.com/
- Meta Business Help Center: https://www.facebook.com/business/help
- Instagram ranking explanation: https://about.instagram.com/blog/announcements/shedding-more-light-on-how-instagram-works
- TikTok Help Center — Creating videos: https://support.tiktok.com/en/using-tiktok/creating-videos
- TikTok Creative Center: https://ads.tiktok.com/business/creativecenter/
- TikTok Business Help Center: https://ads.tiktok.com/help/
- TikTok Creative Codes: https://www.tiktok.com/business/en-US/blog/tiktok-creative-codes
- TikTok recommendation explanation: https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you

Local references:

- `~/lean-native/output/strict-shortform-production-rules.md`
- `~/.cache/agent-runs/channel_deepstudy/style_tokens_v1.md`
- `~/lean-native/output/mike-tyson-video-process-learning.md`
