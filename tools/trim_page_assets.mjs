import fs from "fs";
import path from "path";

function walk(dir, files = []) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    if (name === "node_modules" || name === ".git") continue;
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, files);
    else if (name.endsWith(".html")) files.push(p);
  }
  return files;
}

const updated = [];

for (const file of walk(".")) {
  let html = fs.readFileSync(file, "utf8");
  const orig = html;
  const hasPhotoSlider = /photo-slider/.test(html);
  const hasCountUp = /data-animateDuration/.test(html);
  const usesGlightbox = /data-glightbox|class="glightbox"|GLightbox\(/.test(html);

  if (!hasPhotoSlider) {
    html = html.replace(/\s*<link rel="stylesheet" href="\/assets\/css\/tiny-slider\.css">\r?\n?/g, "\n");
    html = html.replace(/\s*<script src="\/assets\/js\/tiny-slider\.js"><\/script>\r?\n?/g, "\n");
    html = html.replace(/\s*<script src="\/assets\/js\/slider2\.js"><\/script>\r?\n?/g, "\n");
  }

  if (!hasCountUp) {
    html = html.replace(/\s*<script src="\/assets\/js\/count-up\.min\.js"><\/script>\r?\n?/g, "\n");
  }

  if (!usesGlightbox) {
    html = html.replace(/\s*<link rel="stylesheet" href="\/assets\/css\/glightbox\.min\.css">\r?\n?/g, "\n");
    html = html.replace(/\s*<script src="\/assets\/js\/glightbox\.min\.js"><\/script>\r?\n?/g, "\n");
  }

  html = html.replace(/<script src="(\/assets\/js\/[^"]+)"><\/script>/g, (match, src) => {
    if (match.includes(" defer")) return match;
    return `<script src="${src}" defer></script>`;
  });

  if (html !== orig) {
    fs.writeFileSync(file, html, "utf8");
    updated.push(path.relative(".", file).replace(/\\/g, "/"));
  }
}

console.log(`Updated ${updated.length} files`);
updated.forEach((f) => console.log(` - ${f}`));
