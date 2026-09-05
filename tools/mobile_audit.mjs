import { chromium, devices } from "playwright";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(__dirname, "tmp-shots", "mobile-audit");
fs.mkdirSync(out, { recursive: true });

const BASE = "http://127.0.0.1:4173";
const pages = [
  ["home", "/"],
  ["neuropsicologia", "/neuropsicologia/"],
  ["avaliacao", "/avaliacao-neuropsicologica/"],
  ["braga", "/avaliacao-neuropsicologica/braga/"],
  ["estimulacao-braga", "/estimulacao-cognitiva/braga/"],
  ["rastreio-sono", "/rastreio-sono/"],
  ["rastreio-memoria", "/rastreio-memoria/"],
  ["blog", "/blog/"],
];

const iPhone = devices["iPhone 13"];

const browser = await chromium.launch();
const context = await browser.newContext({
  ...iPhone,
  locale: "pt-PT",
});

const report = [];

for (const [name, route] of pages) {
  const page = await context.newPage();
  const url = `${BASE}${route}`;
  await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
  await page.waitForTimeout(1200);

  const metrics = await page.evaluate(() => {
    const vw = window.innerWidth;
    const issues = [];
    const note = (type, detail, el) => {
      issues.push({
        type,
        detail,
        tag: el?.tagName?.toLowerCase() || "",
        className: el?.className?.toString().slice(0, 80) || "",
        text: (el?.innerText || el?.alt || "").replace(/\s+/g, " ").trim().slice(0, 100),
      });
    };

    document.querySelectorAll("img").forEach((img) => {
      const rect = img.getBoundingClientRect();
      if (rect.width > vw + 1) {
        note("overflow", `img wider than viewport (${Math.round(rect.width)}px > ${vw}px)`, img);
      }
      if (rect.height > vw * 1.25 && rect.width > vw * 0.85) {
        note("hero-image", `very tall image (${Math.round(rect.width)}×${Math.round(rect.height)})`, img);
      }
    });

    document.querySelectorAll("p, h1, h2, h3, li").forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.width > vw + 1) {
        note("overflow", `text wider than viewport`, el);
      }
      const style = getComputedStyle(el);
      const lh = parseFloat(style.lineHeight);
      const fs = parseFloat(style.fontSize);
      if (el.tagName === "P" && lh / fs > 2.1 && el.innerText.length > 120) {
        note("line-height", `loose paragraph rhythm (${(lh / fs).toFixed(2)})`, el);
      }
    });

    document.querySelectorAll(".venue-card, .single-team, .triage-question, .section-title").forEach((el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      if (parseFloat(style.marginTop) > 48 || parseFloat(style.marginBottom) > 48) {
        note("spacing", `large block margin (${style.marginTop}/${style.marginBottom})`, el);
      }
      if (rect.height > vw * 2.2 && el.classList.contains("single-team")) {
        note("card-height", `venue card very tall (${Math.round(rect.height)}px)`, el);
      }
    });

    const mobileBar = document.querySelector(".mobile-cta-bar");
    const footer = document.querySelector(".footer");
    if (mobileBar && footer) {
      const barTop = mobileBar.getBoundingClientRect().top;
      const footerBottom = footer.getBoundingClientRect().bottom;
      if (footerBottom > barTop - 8) {
        note("overlap", "footer content may sit under mobile CTA bar", footer);
      }
    }

    return {
      title: document.title,
      viewport: vw,
      scrollHeight: document.documentElement.scrollHeight,
      issueCount: issues.length,
      issues: issues.slice(0, 12),
    };
  });

  report.push({ name, url, ...metrics });

  await page.screenshot({
    path: path.join(out, `${name}-full.png`),
    fullPage: true,
  });

  await page.screenshot({
    path: path.join(out, `${name}-hero.png`),
    clip: { x: 0, y: 0, width: 390, height: 844 },
  });

  await page.close();
  console.log(`${name}: ${metrics.issueCount} issues`);
}

await browser.close();

fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 2));
console.log("report written to", path.join(out, "report.json"));
