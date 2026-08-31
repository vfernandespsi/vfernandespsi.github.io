import fs from "fs";
import path from "path";

const ROOT = path.resolve(import.meta.dirname, "..");

const PAGES = [
  { file: "index.html", kind: "home", expectBtn: false, expectSticky: false, lane: "chooser" },
  { file: "neuropsicologia/index.html", kind: "neuro-funnel", expectBtn: true, expectSticky: false, lane: "neuro" },
  { file: "psicologia-do-sono/index.html", kind: "sono-funnel", expectBtn: true, expectSticky: false, lane: "sono" },
  { file: "blog/index.html", kind: "inner", expectBtn: true, expectSticky: true, lane: "inner" },
  { file: "cursos/index.html", kind: "inner", expectBtn: true, expectSticky: true, lane: "inner" },
  { file: "avaliacao-neuropsicologica/index.html", kind: "inner", expectBtn: true, expectSticky: true, lane: "neuro" },
  { file: "marcar/index.html", kind: "inner", expectBtn: true, expectSticky: true, lane: "neuro" },
  { file: "sono-e-memoria/index.html", kind: "inner", expectBtn: true, expectSticky: true, lane: "neuro" },
];

function check(name, ok, detail = "") {
  const status = ok ? "OK" : "FAIL";
  console.log(`${status}  ${name}${detail ? ` — ${detail}` : ""}`);
  return ok;
}

let passed = 0;
let failed = 0;

function assert(name, ok, detail) {
  if (check(name, ok, detail)) passed += 1;
  else failed += 1;
}

const css = fs.readFileSync(path.join(ROOT, "assets/css/funnel.css"), "utf8");

assert("CSS: header CTA harmonization", css.includes(".header .button.add-list-button .btn"));
assert("CSS: neuro lane header states", css.includes("html:not(.page-chooser):not(.page-sono) .header.sticky .button .btn"));
assert("CSS: sono lane header states", css.includes("html.page-sono .header.sticky .button .btn"));
assert("CSS: page-inner copy rhythm", css.includes(".page-inner .page-content p"));
assert("CSS: home scrolled nav links", css.includes("html.page-chooser .header.navbar-area.is-scrolled .navbar-nav .nav-item a"));
assert(
  "CSS: home header pinned",
  /html\.page-chooser \.header\.navbar-area\s*\{[^}]*position:\s*fixed/.test(css)
);

const js = fs.readFileSync(path.join(ROOT, "assets/js/main.js"), "utf8");
assert("JS: chooser header stays sticky", js.includes("header_navbar.classList.add('sticky')") && js.includes("header_navbar.classList.remove('is-scrolled')") && !js.includes("header_navbar.classList.remove('sticky', 'is-scrolled')"));
assert("JS: chooser header swaps at section seam", js.includes("doorsBottom <= headerHeight"));


for (const page of PAGES) {
  const filePath = path.join(ROOT, page.file);
  const html = fs.readFileSync(filePath, "utf8");
  const prefix = `${page.kind} (${page.file})`;

  assert(`${prefix}: loads funnel.css`, html.includes("/assets/css/funnel.css"));
  assert(
    `${prefix}: header present`,
    /<header class="header navbar-area/.test(html)
  );

  const hasSticky = /header class="header navbar-area sticky/.test(html);
  assert(
    `${prefix}: sticky class`,
    hasSticky === page.expectSticky,
    hasSticky ? "has sticky" : "no sticky"
  );

  const hasAgendar = /add-list-button[\s\S]*?Agendar/.test(html);
  assert(
    `${prefix}: Agendar CTA`,
    hasAgendar === page.expectBtn,
    hasAgendar ? "present" : "absent"
  );

  if (page.lane === "sono") {
    assert(`${prefix}: page-sono class`, html.includes("page-sono"));
    assert(`${prefix}: lane switch in header`, /navbar-nav[\s\S]*?nav-cta-item[\s\S]*?Agendar[\s\S]*?header-nav-sep[\s\S]*?header-lane-item/.test(html));
  }
  if (page.lane === "neuro" && page.kind === "neuro-funnel") {
    assert(`${prefix}: lane switch in header`, /navbar-nav[\s\S]*?nav-cta-item[\s\S]*?Agendar[\s\S]*?header-nav-sep[\s\S]*?header-lane-item/.test(html));
  }
  if (page.lane === "chooser") {
    assert(`${prefix}: page-chooser class`, html.includes("page-chooser"));
  }
  if (page.kind === "inner") {
    assert(`${prefix}: page-inner class`, html.includes("page-inner"));
    assert(`${prefix}: page-content section`, html.includes("page-content"));
  }
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
