const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const out = path.join(__dirname, 'tmp-shots');
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const pages = [
    ['home', 'http://127.0.0.1:4173/'],
    ['avaliacao', 'http://127.0.0.1:4173/avaliacao-neuropsicologica/'],
    ['marcar', 'http://127.0.0.1:4173/marcar/'],
    ['familiares', 'http://127.0.0.1:4173/familiares/'],
    ['braga', 'http://127.0.0.1:4173/avaliacao-neuropsicologica/braga/'],
  ];

  for (const [name, url] of pages) {
    const desktop = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await desktop.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await desktop.waitForTimeout(800);
    await desktop.screenshot({ path: path.join(out, `${name}-desktop.png`), fullPage: true });
    await desktop.close();

    const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
    await mobile.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await mobile.waitForTimeout(800);
    await mobile.screenshot({ path: path.join(out, `${name}-mobile.png`), fullPage: true });
    await mobile.close();
    console.log('ok', name);
  }
  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
