import { JSDOM } from "jsdom";
import fs from "fs";
import path from "path";

const ROOT = path.resolve(import.meta.dirname, "..");
const BASE = "http://localhost:8765";

async function fetchHtml(urlPath) {
  const res = await fetch(`${BASE}${urlPath}`);
  if (!res.ok) throw new Error(`${urlPath} -> ${res.status}`);
  return res.text();
}

function readLocal(relPath) {
  return fs.readFileSync(path.join(ROOT, relPath), "utf8");
}

function check(name, ok, detail = "") {
  const status = ok ? "OK" : "FAIL";
  console.log(`${status}  ${name}${detail ? ` — ${detail}` : ""}`);
  return ok;
}

let passed = 0;
let failed = 0;

function assert(name, ok, detail = "") {
  if (check(name, ok, detail)) passed++;
  else failed++;
}

async function main() {
  const home = await fetchHtml("/");
  const homeDom = new JSDOM(home).window.document;

  assert("Home: header Marcar", !!homeDom.querySelector("[data-open-booking-modal]"));
  assert("Home: header Blog", !!homeDom.querySelector('a[href="/blog/"]'));
  assert("Home: header Cursos", !!homeDom.querySelector('a[href="/cursos/"]'));
  assert("Home: booking modal", !!homeDom.getElementById("vf-booking-modal"));
  assert("Home: neuro choice", !!homeDom.querySelector('[data-booking-choice="neuro"]'));
  assert("Home: sono choice", !!homeDom.querySelector('[data-booking-choice="sono"]'));
  assert("Home: sobre section", !!homeDom.getElementById("sobre-mim"));
  assert("Home: Ver currículo", !!homeDom.querySelector('#sobre-mim a[href="/sobre/"]'));
  assert("Home: no door-identity", !homeDom.querySelector(".door-identity"));
  assert("Home: split hero", !!homeDom.querySelector(".door-chooser .door-portrait img"));

  const funnelCss = readLocal("assets/css/funnel.css");
  assert("CSS: portrait aspect-ratio", funnelCss.includes("aspect-ratio") && funnelCss.includes("746 / 1119"));
  assert("CSS: triagem hidden rule", funnelCss.includes("#triagem:not(.is-visible)"));
  assert("CSS: booking modal", funnelCss.includes(".vf-booking-modal"));

  const neuro = await fetchHtml("/neuropsicologia/");
  const neuroDom = new JSDOM(neuro).window.document;
  assert("Neuro: Início -> /", !!neuroDom.querySelector('.navbar-nav a[href="/"]'));
  assert("Neuro: header Psicologia do sono", !!neuroDom.querySelector('header .navbar-nav a[href="/psicologia-do-sono/"]'));
  assert("Neuro: sono not mid-nav", !neuroDom.querySelector('.navbar-nav .nav-item:nth-child(2) a[href="/psicologia-do-sono/"]'));
  assert("Neuro: rastreio memoria link", !!neuroDom.querySelector('a[href="/rastreio-memoria/"]'));
  assert("Neuro: Fazer rastreio CTA", neuro.includes("Fazer rastreio"));
  assert("Neuro: no sobre block on page", !neuroDom.querySelector('h2')?.textContent?.includes("Experiência em contexto hospitalar") || !Array.from(neuroDom.querySelectorAll("h2")).some((h) => h.textContent.includes("Experiência em contexto hospitalar")));
  const neuroH2s = Array.from(neuroDom.querySelectorAll("h2")).map((h) => h.textContent.trim());
  assert("Neuro: removed experience h2", !neuroH2s.some((t) => t.includes("Experiência em contexto hospitalar")));
  assert("Neuro: consultas compare table", !!neuroDom.querySelector(".compare-table"));
  const faqBtn = Array.from(neuroDom.querySelectorAll("a.btn-alt")).find((a) => a.closest(".faq"));
  assert("Neuro: FAQ CTA text", faqBtn?.textContent.includes("Tenho uma dúvida") ?? false, faqBtn?.textContent?.trim());

  const sono = await fetchHtml("/psicologia-do-sono/");
  const sonoDom = new JSDOM(sono).window.document;
  assert("Sono: Início -> /", !!sonoDom.querySelector('.navbar-nav a[href="/"]'));
  assert("Sono: header Neuropsicologia", !!sonoDom.querySelector('header .navbar-nav a[href="/neuropsicologia/"]'));
  assert("Sono: neuro not mid-nav", !sonoDom.querySelector('.navbar-nav .nav-item:nth-child(2) a[href="/neuropsicologia/"]'));
  assert(
    "Sono: no self-link in header",
    !sonoDom.querySelector('.navbar-nav a[href="/psicologia-do-sono/"]'),
  );

  const blog = await fetchHtml("/blog/");
  assert("Blog: listing page", blog.includes("papel do psicólogo"));

  const post = await fetchHtml("/blog/papel-psicologo-doencas-neurologicas/");
  assert("Blog: article JSON-LD", post.includes("BlogPosting"));

  const cursos = await fetchHtml("/cursos/");
  assert("Cursos: page loads", cursos.includes("Instrumentos de Rastreio Cognitivo"));

  const sitemap = readLocal("sitemap.xml");
  assert("Sitemap: /blog/", sitemap.includes("https://verafernandes.com/blog/"));
  assert("Sitemap: /cursos/", sitemap.includes("https://verafernandes.com/cursos/"));

  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
