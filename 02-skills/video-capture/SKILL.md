---
name: video-capture
description: HTML 시각화를 Playwright로 프레임 캡처하여 MP4로 변환. "캡처", "capture", "HTML 영상", "씬 렌더링" 키워드에 트리거.
user_invocable: true
---

# Video Capture — HTML → MP4

HTML 시각화 파일을 Playwright headless 브라우저로 프레임 캡처하고 ffmpeg로 MP4 변환.

## 캡처 스크립트 템플릿

프로젝트마다 `capture.mjs`를 생성한다. 핵심 구조:

```javascript
import { chromium } from 'playwright';
import { execFileSync } from 'child_process';
import { mkdirSync, existsSync, readdirSync, unlinkSync, rmdirSync, writeFileSync } from 'fs';
import { join, resolve } from 'path';

const SEGMENTS = [
  { file: 'seg-01.html', dur: 10 },  // duration = 오디오 파형 기준
  { file: 'seg-02.html', dur: 15 },
];

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
```

## 캡처 로직 핵심

### CSS 애니메이션 제어 (pause + currentTime)
CSS 애니메이션은 실시간이라 프레임 캡처 속도를 못 따라감. 반드시:
1. `getAnimations().pause()` — 모든 애니메이션 정지
2. `animation.currentTime = frameTime` — 프레임별 수동 진행

```javascript
// 초기화: 모든 애니메이션 pause (sceneOut은 cancel)
await page.evaluate(() => {
  document.getAnimations({ subtree: true }).forEach(a => {
    if (a.animationName === 'sceneOut') { a.cancel(); return; }
    a.pause();
  });
});

// 프레임 루프: currentTime 수동 제어
for (let i = 0; i < totalFrames; i++) {
  const timeMs = (i / FPS) * 1000;
  await page.evaluate((t) => {
    document.getAnimations({ subtree: true }).forEach(a => { a.currentTime = t; });
  }, timeMs);
  await page.screenshot({ path: framePath, clip: { x:0, y:0, width:1920, height:1080 } });
}
```

### 프로그래매틱 페이드 (마지막 15프레임)
sceneOut 애니메이션은 HTML에 넣지 말고 캡처 스크립트에서:
```javascript
const FADE_FRAMES = 15;
const framesLeft = totalFrames - i;
if (framesLeft <= FADE_FRAMES) {
  await page.evaluate((op) => { document.body.style.opacity = op; }, framesLeft / FADE_FRAMES);
}
```

### ffmpeg 인코딩
```javascript
execFileSync('ffmpeg', [
  '-y', '-framerate', '30',
  '-i', 'frame_%05d.png',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
  '-crf', '18', '-preset', 'fast',
  'output.mp4',
]);
```

### 합본
```javascript
// concat.txt: file 'seg-01.mp4'\nfile 'seg-02.mp4'\n...
execFileSync('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'final.mp4']);
```

## HTML 씬 디자인 규칙 (EP 시리즈 스타일)

## HTML 씬 디자인 규칙 (EP 시리즈 스타일)

For YouTube/Reels explainer overlays such as Keyword/Process/Data/System Map/Before-After/Callout/Timeline/Decision cards, use and before designing scene sources.

For ultra-restrained technical/product motion overlays where 사용자 signals “AI slop 제거”, “컨펌 바늘구멍”, or rejects decorative HUD/card aesthetics, use: reduce to thin lines, sparse points, small readable type, negative space, restrained timing, and strict subtitle-safe composition.

Critical 2026 overlay rule from 사용자 feedback: these are **video overlay cards, not slide notes**. Before making assets, research/choose the target quality bar from current web motion/product-video references (Rive/Lottie, Motionographer, Apple motion, Linear/Vercel/SaaS product demos, Vox lower-thirds/callouts). The card must be a compact floating product-UI layer over footage, leaving subtitle safe zones intact. Do not create full-screen slide layouts, large lecture titles, generic HUD node maps, visible subtitle-safe-zone guides in final renders, or text that competes with subtitles. If the still frame would not pass as a high-end web UI component, it fails. See for the detailed benchmark, failure modes, timing, and scene mapping examples.

When 사용자 says “텍스트 필요 없음”, “오버레이 카드”, or provides abstract AI/system scene prompts, use: convert narration into icon/state/micro-component motion only, keep the current palette if requested, produce 2–3 styleframes before full rendering, and do not proceed to a long full sequence until the overlay-card art direction passes visual QA.

**Hard-learned correction:** When 사용자 says “오버레이 카드”, “텍스트 필요 없음”, or provides a visual prompt, do **not** render a full explainer video first. Convert the prompt into 2–3 small premium styleframes, QA them visually, and deliver for direction check before a long MP4. Preserve the requested/current palette. Express concepts with compact component states, icons, signals, layers, and motion affordances — not big labels, bullet text, or full-screen symbolic diagrams. For the no-text/styleframe workflow, see.

When 사용자 says “텍스트 필요 없고, 오버레이 카드” or gives a symbolic motion prompt for an explainer overlay, use: remove readable text entirely, preserve the current palette, map each scene to compact icon/geometry/object-state transitions, and verify the contact sheet for no labels, no dashboard copy, no slide-like composition, and subtitle-safe lower space.

- 1920x1080, 배경 #111111
- Pretendard(본문) + JetBrains Mono(코드)
- 액센트 #FFC505 (노란색), 뱃지 #28C840 (녹색), 경고 #FF6B6B
- 텍스트 #f1f1f1, 보조 rgba(241,241,241,0.5)
- fadeUp/fadeLeft/fadeRight CSS 애니메이션
- 노이즈 오버레이 div (opacity:0.03)
- word-break: keep-all; overflow: hidden;
- YouTube 자막이 들어갈 영상은 하단 subtitle safe zone을 비우고, 모션은 현재 자막/내레이션 의미를 뒷받침하는 visual support layer로 설계한다.

## Element/section scroll recording

For web-design recreation reviews, the user may ask to “show each full screenshot as a screen recording.” Use Playwright to open the artifact, scroll each target section or element, capture frames, encode each section to MP4, and optionally concat. A reusable CommonJS template is available at `scripts/element-scroll-record.cjs`.

Important:
- Prefer element/selector-based recording over arbitrary page scroll so adjacent sections do not contaminate the viewport.
- If the user says “run 008” or similar and multiple projects have a run with that number, do **not** pick the first match. Resolve the intended artifact from recent conversation/session context and project name (e.g. “Cartier/까르띠에”, “montage”), then confirm by checking the artifact title/path before capture.
- For WebGL/scroll-story artifacts, serve the artifact folder with a local static server and capture the HTTP URL rather than `file://` if assets/scripts depend on browser origin behavior. Reuse the same verified preview URL if prior QA used one.
- After recording, extract QA contact sheets from the MP4s and inspect them before claiming success.
- If a section is a reel/demo sequence rather than a scrollable page, record each frame/card in sequence instead of forcing a website-scroll metaphor.

## Preserved run artifact scroll capture

When 사용자 says “run 008 결과물 스크롤 캡처” or similar, do not ask for a path first if a likely run artifact can be found. Search preserved agent/Open Design caches for `runs/run-008/index.html` or matching project folders, then capture that exact artifact.

Useful locations/patterns:
- `~/.cache/agent-runs/runs/run-00N/index.html`
- `~/.cache/agent-runs/run-00N/index.html`
- project-specific caches such as `~/.cache/agent-runs/runs/run-00N/index.html`

For full-page artifact previews, use a smooth page-scroll recording rather than section-only capture. A reusable template is available at `scripts/smooth-scroll-capture.cjs`:

```bash
cd /path/to/runs/run-008
node ~/.claude/skills/video-capture/scripts/smooth-scroll-capture.cjs
# or explicitly:
HTML=/path/to/index.html OUT=/path/to/run008_scroll_capture.mp4 DURATION=14 WIDTH=1440 HEIGHT=1100 node ~/.claude/skills/video-capture/scripts/smooth-scroll-capture.cjs
```

Verification before delivery:
- Run `ffprobe` or `ls -lh` to confirm MP4 duration/size.
- Generate and inspect a contact sheet (`*_contact_sheet.jpg`) to confirm top/mid/bottom render correctly, with no blank screen, failed fonts, or clipping.
- Deliver the MP4 via `MEDIA:/absolute/path/to/file` on Telegram.

## Visual QA / 레이아웃 수정 루프

사용자가 특정 초 구간의 겹침·정렬 문제를 지적하면 전체 영상을 다시 보겠다고 말하지 말고 해당 구간 프레임을 즉시 추출해 contact sheet로 확인한다.

```bash
mkdir -p qa_fix
for t in 15 16 17 20 22 24; do
  ffmpeg -y -ss "$t" -i output.mp4 -frames:v 1 "qa_fix/frame_$t.jpg"
done
```

- 진행선/connector line은 카드 위를 관통하지 않게 카드 아래 또는 뒤쪽 레이어에 배치하고, 라벨과도 20px 이상 간격을 둔다.
- 프로필/이름 카드처럼 아이콘+이름+보조문구가 있는 경우, 카드 내부를 `icon area → name → role label`로 나누고 SVG 높이가 이름 위치를 밀지 않도록 고정 높이 wrapper를 둔다.
- 수정 후 같은 타임스탬프 contact sheet를 다시 만들고 눈으로 확인한 뒤 완료라고 말한다.

## 기존 MP4에 TTS 음성만 입히기

사용자가 이미 렌더링된 `01.mp4 ~ 08.mp4` 같은 씬 파일에 “자막과 텍스트 없이 영상+목소리만” 요청하면를 따른다. 핵심은 원본 비디오 스트림을 보존하고, 씬별 TTS WAV를 생성해 duration에 맞춘 뒤 `ffmpeg -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac`로 오디오만 교체/추가하는 것이다. 텍스트 오버레이, 자막, 제목 프레임은 만들지 않는다.

For Shorts where voice/tension matters, also use: create a first-hook voice casting sample before batch rendering, and treat ffprobe/Whisper checks as baseline technical QA, not proof of creative quality.

## 비디오 duration 결정

**오디오 파형 기준으로 결정한다** (대본 예상 시간이 아님).
1. TTS 생성 → 씬별 WAV duration 측정
2. 씬을 N개로 분할 시 duration도 N등분
3. capture.mjs의 SEGMENTS에 반영
4. CapCut에서 비디오/오디오가 자연스럽게 싱크

## 정적 화면 방지 / 사용자 피드백 대응

- 사용자가 “정적인 화면이 2~3초 이상 유지되면 안 된다”고 지적하면, 단순 contact sheet만 보지 말고 씬 구조를 바꾼다.
- **타이밍 숫자를 맹목적으로 준수하지 않는다.** 사용자가 이후 “4~5초 정도”, “꼭 준수할 필요는 없다”, “적합한 판단”이라고 정정하면, 내레이션 호흡·정보량·장면 의미를 기준으로 자연스럽게 결정한다. 정적 체감은 duration보다 장면 안의 의미 있는 micro-motion/단계적 reveal/라인 드로잉으로 줄인다.
- **화면·내용·자막 맥락은 항상 일치**시킨다. 현재 말하는 문장에 맞춰 중앙 오브젝트와 헤더를 바꾼다. 예: “텔레그램 요청”은 request→agent→tool flow, “실행”은 실행 카드, “맥락”은 프로젝트/취향/규칙, “검증”은 파일/프레임/싱크 카드처럼 매핑한다.
- 중앙 오브젝트/레이아웃/카드 유형은 내레이션 세그먼트에 맞춰 전환하고, 배경 그리드·글로우·진행바·점·라인 등은 프레임마다 미세하게 움직이게 한다.
- 상단 제목이 유지되더라도 중앙 오브젝트와 정보 구조가 바뀌면 정적 체감이 줄어든다. 단, 같은 카드가 contact sheet에서 의도 없이 반복되면 `sceneAt()`/세그먼트 fallback 로직을 점검한다.
- QA는 3~6초 간격으로 프레임을 추출해 contact sheet를 만들고, 모든 샘플에서 **자막 내용 ↔ 중앙 오브젝트 ↔ 장면 헤더**가 맞는지 확인한다.
- 음성이 “급하다/겹친다/직접 들으며 수정”을 지적받으면 `ttstudio-voice`의 문장별 Voicebox 생성 + 0.45~0.65초 무음 갭 패턴을 적용한 뒤, Whisper timing을 자막에 반영한다.

## 의존성
- Node.js, playwright (`npx playwright install chromium`)
- ffmpeg
