const BASE = process.argv[2] || "http://192.168.1.107:4173";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  const text = await res.text();
  return { status: res.status, text };
}

function log(ok, msg) {
  console.log(`${ok ? "OK" : "FAIL"}  ${msg}`);
}

const home = await get("/");
log(home.status === 200, `GET / -> ${home.status}`);
log(home.text.includes("data-open-booking-modal"), "Home: Marcar popup trigger");
log(home.text.includes('href="/blog/"'), "Home: Blog link");
log(home.text.includes('href="/cursos/"'), "Home: Cursos link");
log(home.text.includes("vf-booking-modal"), "Home: booking modal");
log(home.text.includes('id="sobre-mim"'), "Home: sobre section");
log(!home.text.includes("door-identity"), "Home: door-identity removed");

const neuro = await get("/neuropsicologia/");
log(neuro.status === 200, `GET /neuropsicologia/ -> ${neuro.status}`);
log(neuro.text.includes('href="/"'), "Neuro: Início -> /");
log(neuro.text.includes('href="/rastreiomemoria/"'), "Neuro: rastreio memoria link");
log(neuro.text.includes("Rastreio Memória"), "Neuro: Rastreio Memória CTA");
log(!neuro.text.includes("Experiência em contexto hospitalar"), "Neuro: sobre block removed");
log(neuro.text.includes("Tenho uma dúvida"), "Neuro: FAQ CTA");
log(neuro.text.includes("compare-table"), "Neuro: compare table kept");

const sono = await get("/psicologia-do-sono/");
log(sono.status === 200, `GET /psicologia-do-sono/ -> ${sono.status}`);
log(sono.text.includes('href="/"'), "Sono: Início -> /");

for (const path of ["/blog/", "/cursos/", "/blog/memoria-e-envelhecimento-normal/"]) {
  const page = await get(path);
  log(page.status === 200, `GET ${path} -> ${page.status}`);
}
