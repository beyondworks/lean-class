// README 그림을 PNG로 뽑는다(2배 해상도). 사용: node render.mjs <playwright 모듈 경로>
// 예: node docs/assets/src/render.mjs ~/somewhere/node_modules/playwright/index.mjs
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const { chromium } = await import(process.argv[2] ? pathToFileURL(process.argv[2]).href : 'playwright');
const browser = await chromium.launch();
for (const [name, w, h] of [['hero', 1600, 800], ['flow', 1600, 580]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(path.join(here, `${name}.html`)).href);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(here, '..', `${name}.png`) });
  await page.close();
}
await browser.close();
