// Element/section scroll recorder template for HTML artifacts.
// Copy this file into a run directory and edit ROOT, selectors, names, width/height.
// Requires: npm package `playwright` available, ffmpeg installed.

const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const { mkdirSync, rmSync, existsSync, writeFileSync } = require('fs');
const path = require('path');

const ROOT = '/ABSOLUTE/PATH/TO/RUN';
const URL = 'file://' + path.join(ROOT, 'artifact/index.html');
const OUT = path.join(ROOT, 'recordings');
const FPS = 30;
const W = 1440;
const H = 1000;

const SEGMENTS = [
  { selector: '#section-one', name: '01-section-one-scroll', seconds: 7 },
  { selector: '#section-two', name: '02-section-two-scroll', seconds: 9 },
];

function clean(dir) {
  if (existsSync(dir)) rmSync(dir, { recursive: true, force: true });
  mkdirSync(dir, { recursive: true });
}

function encode(frameDir, output) {
  execFileSync('ffmpeg', [
    '-y', '-framerate', String(FPS),
    '-i', path.join(frameDir, 'frame_%05d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-crf', '18', '-preset', 'fast', '-movflags', '+faststart',
    output,
  ], { stdio: 'inherit' });
}

async function recordScroll(page, { selector, name, seconds }) {
  const frameDir = path.join(OUT, `${name}-frames`);
  clean(frameDir);
  const metrics = await page.evaluate(({ selector, H }) => {
    const el = document.querySelector(selector);
    if (!el) throw new Error(`Missing selector: ${selector}`);
    const rect = el.getBoundingClientRect();
    const top = window.scrollY + rect.top;
    return { top, height: rect.height, max: Math.max(0, rect.height - H) };
  }, { selector, H });

  const total = Math.max(1, Math.round(seconds * FPS));
  for (let i = 0; i < total; i++) {
    const t = total === 1 ? 0 : i / (total - 1);
    const eased = t * t * (3 - 2 * t);
    await page.evaluate((y) => window.scrollTo(0, y), metrics.top + metrics.max * eased);
    await page.waitForTimeout(8);
    await page.screenshot({
      path: path.join(frameDir, `frame_${String(i).padStart(5, '0')}.png`),
      clip: { x: 0, y: 0, width: W, height: H },
    });
  }

  const output = path.join(OUT, `${name}.mp4`);
  encode(frameDir, output);
  return output;
}

(async () => {
  clean(OUT);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto(URL, { waitUntil: 'load' });

  const outputs = [];
  for (const segment of SEGMENTS) outputs.push(await recordScroll(page, segment));

  const concat = path.join(OUT, 'concat.txt');
  writeFileSync(concat, outputs.map((file) => `file '${file}'`).join('\n') + '\n');
  execFileSync('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', concat, '-c', 'copy', '-movflags', '+faststart', path.join(OUT, '00-combined.mp4')], { stdio: 'inherit' });

  await browser.close();
  console.log(JSON.stringify({ outputs, combined: path.join(OUT, '00-combined.mp4') }, null, 2));
})();
