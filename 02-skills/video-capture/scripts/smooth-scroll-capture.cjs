const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const { mkdirSync, rmSync, existsSync } = require('fs');
const { join, resolve } = require('path');

// Copy this script into the artifact/run folder or run with:
//   HTML=/abs/path/index.html OUT=/abs/path/output.mp4 node smooth-scroll-capture.cjs
const RUN_DIR = process.cwd();
const HTML = resolve(process.env.HTML || join(RUN_DIR, 'index.html'));
const OUT_DIR = resolve(process.env.FRAMES || join(RUN_DIR, 'scroll_frames'));
const OUT_MP4 = resolve(process.env.OUT || join(RUN_DIR, 'scroll_capture.mp4'));
const WIDTH = Number(process.env.WIDTH || 1440);
const HEIGHT = Number(process.env.HEIGHT || 1100);
const FPS = Number(process.env.FPS || 24);
const DURATION = Number(process.env.DURATION || 14);
const FRAMES = FPS * DURATION;

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

(async () => {
  if (existsSync(OUT_DIR)) rmSync(OUT_DIR, { recursive: true, force: true });
  mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
  await page.goto('file://' + HTML, { waitUntil: 'load' });
  await page.waitForTimeout(800);
  await page.addStyleTag({ content: '*{scroll-behavior:auto!important}html,body{overflow-x:hidden!important}' });
  await page.evaluate(() => document.getAnimations({ subtree: true }).forEach(a => { try { a.pause(); } catch (_) {} }));

  const metrics = await page.evaluate(() => ({
    scrollHeight: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
    viewportHeight: window.innerHeight,
    title: document.title,
  }));
  const maxScroll = Math.max(0, metrics.scrollHeight - HEIGHT);
  console.log(JSON.stringify({ HTML, OUT_MP4, metrics, maxScroll, FRAMES, FPS, DURATION }, null, 2));

  for (let i = 0; i < FRAMES; i++) {
    const p = i / (FRAMES - 1);
    let sp;
    if (p < 0.08) sp = 0;
    else if (p > 0.92) sp = 1;
    else sp = easeInOutCubic((p - 0.08) / 0.84);
    const y = Math.round(maxScroll * sp);
    await page.evaluate(scrollY => window.scrollTo(0, scrollY), y);
    await page.waitForTimeout(20);
    await page.screenshot({ path: join(OUT_DIR, `frame_${String(i).padStart(5, '0')}.png`), clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT } });
  }
  await browser.close();

  execFileSync('ffmpeg', [
    '-y', '-framerate', String(FPS), '-i', join(OUT_DIR, 'frame_%05d.png'),
    '-vf', `scale=${WIDTH}:-2,format=yuv420p`, '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-movflags', '+faststart', OUT_MP4,
  ], { stdio: 'inherit' });

  const QA = OUT_MP4.replace(/\.mp4$/, '_contact_sheet.jpg');
  execFileSync('ffmpeg', ['-y', '-i', OUT_MP4, '-vf', `fps=1/${Math.max(1, Math.floor(DURATION / 6))},scale=480:-1,tile=3x2`, '-frames:v', '1', '-update', '1', QA], { stdio: 'inherit' });
  console.log(JSON.stringify({ done: true, OUT_MP4, QA }, null, 2));
})();
