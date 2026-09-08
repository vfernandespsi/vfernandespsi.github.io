"""One-off renderer for inner pages. Output is static HTML for GitHub Pages."""

from __future__ import annotations

import shutil
from pathlib import Path

from consent_snippets import CONSENT_BANNER, HEAD_STYLES
from jsonld import build_graph

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://verafernandes.com"
MANUAL_PAGE_PATHS = frozenset({"psicologia-do-sono", "agendar"})

# Post-launch articles: keep generators below, do not emit HTML/sitemap until copy is ready.
# Flip to True + add URLs to sitemap / llms.txt when real articles ship (same quality as alzheimer/).
PUBLISH_POST_LAUNCH_ARTICLES = False
POST_LAUNCH_ARTICLE_SLUGS = ("avc", "parkinson", "lesao-cerebral")
# Planned, not scaffolded yet:
#   insonia — artigo sono sobre insónia (lane sono)
# Removed permanently (thin duplicate of /avaliacao-neuropsicologica/): avaliacao-cognitiva

WA = "https://api.whatsapp.com/send?phone=351914166181&text=Tenho%20uma%20d%C3%BAvida%20sobre%20avalia%C3%A7%C3%A3o%20neuropsicol%C3%B3gica."
WA_ESTIMULACAO = "https://api.whatsapp.com/send?phone=351914166181&text=Tenho%20uma%20d%C3%BAvida%20sobre%20estimula%C3%A7%C3%A3o%20cognitiva."
WA_SONO = "https://api.whatsapp.com/send?phone=351914166181&text=Tenho%20uma%20d%C3%BAvida%20sobre%20psicologia%20do%20sono."

VENUES = [
    {
        "city": "braga",
        "city_label": "Braga",
        "name": "CNS - Campus Neurológico Braga",
        "day": "Quarta-feira",
        "hours": "15h30-19h30",
        "services": "avaliacao",
        "tel": "tel:+351253401600",
        "maps": "https://maps.app.goo.gl/wDj2fLMUs6n5ADGo8",
        "more": "https://www.cnscampus.com/equipa/vera-fernandes/",
        "wa": None,
        "image": "/assets/images/locais/CNS.webp",
        "alt": "CNS - Campus Neurológico em Braga",
    },
    {
        "city": "braga",
        "city_label": "Braga",
        "name": "Hospital Lusíadas Braga",
        "day": "Sexta-feira",
        "hours": "14h00-18h00",
        "services": "avaliacao,estimulacao",
        "tel": "tel:+351253079579",
        "maps": "https://goo.gl/maps/BH2LG9T8WchMStWv7",
        "more": "https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0",
        "wa": None,
        "image": "/assets/images/locais/braga2.webp",
        "alt": "Hospital Lusíadas Braga",
    },
    {
        "city": "braga",
        "city_label": "Braga",
        "name": "Consultório Médico - Braga",
        "day": "Segunda-feira",
        "hours": "17h30-19h30",
        "services": "avaliacao",
        "tel": "tel:+351914166181",
        "maps": "https://goo.gl/maps/2uarVBvnvWSCpsLX6",
        "more": None,
        "wa": "Estou interessado em agendar avaliação neuropsicológica no Consultório Médico Braga. Pode dar-me mais informações?",
        "image": "/assets/images/locais/braga1.webp",
        "alt": "Consultório médico em Braga",
    },
    {
        "city": "barcelos",
        "city_label": "Barcelos",
        "name": "Clínica FisioMove - Barcelos",
        "day": "Segunda-feira",
        "hours": "17h30-19h30",
        "services": "avaliacao",
        "tel": "tel:+351914166181",
        "maps": "https://goo.gl/maps/33f2zLMDHjTgs4or6",
        "more": None,
        "wa": "Estou interessado em agendar avaliação neuropsicológica na Clínica FisioMove Barcelos. Pode dar-me mais informações?",
        "image": "/assets/images/locais/barcelos.webp",
        "alt": "Clínica FisioMove em Barcelos",
    },
    {
        "city": "guimaraes",
        "city_label": "Guimarães",
        "name": "Gabinete Muralha Business - Guimarães",
        "day": "Quinta-feira",
        "hours": "10h00-12h00",
        "services": "avaliacao",
        "tel": "tel:+351914166181",
        "maps": "https://maps.app.goo.gl/EBDMfvT26QXZaqyR8",
        "more": None,
        "wa": "Estou interessado em agendar avaliação neuropsicológica no Muralha Business em Guimarães. Pode dar-me mais informações?",
        "image": "/assets/images/locais/guimaraes.webp",
        "alt": "Gabinete Muralha Business em Guimarães",
    },
    {
        "city": "porto",
        "city_label": "Porto",
        "name": "Gabinete Psicologia - Porto",
        "day": "Sábado",
        "hours": "9h00-13h00",
        "services": "avaliacao",
        "tel": "tel:+351914166181",
        "maps": "https://goo.gl/maps/TJ4YzB9HapsxGXLs8",
        "more": None,
        "wa": "Estou interessado em agendar avaliação neuropsicológica no Gabinete Psicologia Porto. Pode dar-me mais informações?",
        "image": "/assets/images/locais/porto.webp",
        "alt": "Gabinete de psicologia no Porto",
    },
]


def venue_card(v, booking=False):
    extra = []
    extra.append(
        f'<li><a href="{v["tel"]}" data-track="telefone" rel="noopener noreferrer"><i class="lni lni-xl lni-phone"></i> Ligar</a></li>'
    )
    extra.append(
        f'<li><a href="{v["maps"]}" target="_blank" rel="noopener noreferrer"><i class="lni lni-xl lni-map-marker"></i> Localização</a></li>'
    )
    if v["more"]:
        extra.append(
            f'<li><a href="{v["more"]}" target="_blank" rel="noopener noreferrer"><i class="lni lni-xl lni-laptop-phone"></i> Saber mais</a></li>'
        )
    if v["wa"]:
        from urllib.parse import quote

        extra.append(
            f'<li><a href="https://api.whatsapp.com/send?phone=351914166181&text={quote(v["wa"])}" target="_blank" rel="noopener noreferrer" data-track="whatsapp"><i class="lni lni-xl lni-whatsapp"></i> Tenho uma dúvida</a></li>'
        )
    attrs = f'data-city="{v["city"]}"'
    if booking:
        attrs += f' data-book-venue data-services="{v["services"]}"'
    return f'''
            <div class="col-12 col-md-6 venue-card" {attrs}>
                <div class="single-team wow fadeInUp" data-wow-delay=".2s">
                    <div class="image">
                        <img draggable="false" src="{v["image"]}" alt="{v["alt"]}">
                    </div>
                    <div class="content">
                        <div class="row align-items-center">
                            <div class="text">
                                <h3>{v["name"]}</h3>
                            </div>
                            <div class="col-lg-3 col-12">
                                <div class="text">
                                    <h4>{v["day"]}</h4>
                                    <h5>{v["hours"]}</h5>
                                </div>
                            </div>
                            <div class="col">
                                <ul class="social">
                                    {"".join(extra)}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>'''


def faq_html(items):
    parts = []
    for i, (q, a) in enumerate(items, 1):
        show = " show" if i == 1 else ""
        collapsed = "" if i == 1 else " collapsed"
        expanded = "true" if i == 1 else "false"
        parts.append(f'''
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="heading{i}">
                            <button class="accordion-button{collapsed}" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapse{i}" aria-expanded="{expanded}" aria-controls="collapse{i}">
                                <span class="title"><span class="serial">{i:02d}</span>{q}</span><i class="lni lni-plus"></i>
                            </button>
                        </h2>
                        <div id="collapse{i}" class="accordion-collapse collapse{show}" aria-labelledby="heading{i}"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body"><p>{a}</p></div>
                        </div>
                    </div>''')
    return "\n".join(parts)


def related_html(items, heading="Perguntas seguintes"):
    if not items:
        return ""
    lis = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in items)
    return f"""
<section class="related-questions">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <h2>{heading}</h2>
                <ul class="related-list">{lis}</ul>
            </div>
        </div>
    </div>
</section>"""


def page(
    path,
    title,
    description,
    canonical,
    crumbs,
    body,
    faqs=None,
    related=None,
    related_heading="Perguntas seguintes",
    lane="neuro",
    *,
    condition_slug=None,
    service_key=None,
    city=None,
    page_kind="default",
):
    if path in MANUAL_PAGE_PATHS:
        print("skip manual", path)
        return

    is_sono = lane == "sono"
    html_class = "no-js page-inner page-sono" if is_sono else "no-js page-inner"
    if path == "sobre":
        html_class += " sobre-page"
    if path == "sono-e-memoria" and "page-sono" not in html_class:
        html_class += " page-sono"
    brand_home = "/"
    wa = WA_SONO if is_sono else WA
    cta_label = "Agendar"
    cta_href = "/agendar/?servico=sono" if is_sono else "/agendar/"
    nav = """
                                <li class="nav-item"><a href="/">Início</a></li>
                                <li class="nav-item"><a href="/neuropsicologia/">Neuropsicologia</a></li>
                                <li class="nav-item"><a href="/psicologia-do-sono/">Psicologia do Sono</a></li>"""
    faq_block = ""
    if faqs:
        faq_block = f'''
<section id="faq" class="faq section">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="section-title">
                    <h2>Questões frequentes</h2>
                </div>
            </div>
        </div>
        <div class="accordion" id="accordionExample">
            {faq_html(faqs)}
        </div>
        <div class="button cta-pair" style="margin-top:30px;text-align:center;">
            <a href="{cta_href}" class="btn" data-track="marcar"><i class="lni lni-calendar"></i> {cta_label}</a>
            <a href="{wa}" class="btn btn-alt" data-track="whatsapp" rel="noopener noreferrer">Tenho uma dúvida</a>
        </div>
    </div>
</section>'''
    html = f'''<!DOCTYPE html>
<html class="{html_class}" lang="pt-pt">
<head>
    <link rel="api-catalog" href="/llms.txt" />
    <link rel="service-doc" href="/llms.txt" />
    <link rel="sitemap" type="application/xml" href="/sitemap.xml" />
    <link rel="canonical" href="{canonical}" />
    <meta charset="utf-8" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Vera Fernandes" />
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
    <meta property="og:locale" content="pt_PT" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Vera Fernandes - Neuropsicóloga | Braga, Barcelos, Guimarães e Porto" />
    <meta property="og:image" content="{SITE}/assets/images/vera1.webp" />
    <script type="application/ld+json">
{build_graph(canonical, title, crumbs, description=description, faqs=faqs, condition_slug=condition_slug, service_key=service_key, city=city, page_kind=page_kind)}
    </script>
    <link rel="shortcut icon" type="image/x-icon" href="/assets/images/favicon.ico" />
{HEAD_STYLES}
</head>
<body>
<a class="skip-link" href="#inicio">Saltar para o conteúdo</a>
<div class="preloader"><div class="preloader-inner"><div class="preloader-icon"><span></span><span></span></div></div></div>
{CONSENT_BANNER}
<header class="header navbar-area sticky">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-12">
                <div class="nav-inner">
                    <nav class="navbar navbar-expand-lg">
                        <a class="navbar-brand" href="{brand_home}" target="_self">
                            <img draggable="false" src="/assets/images/logo/logo.svg" alt="Vera Fernandes, neuropsicóloga">
                        </a>
                        <button class="navbar-toggler mobile-menu-btn" type="button" data-bs-toggle="collapse"
                            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                            aria-expanded="false" aria-label="Abrir menu">
                            <span class="toggler-icon"></span><span class="toggler-icon"></span><span class="toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse sub-menu-bar" id="navbarSupportedContent">
                            <ul id="nav" class="navbar-nav ms-auto">
{nav}
                            </ul>
                        </div>
                        <div class="button add-list-button">
                            <a href="{cta_href}" class="btn" data-track="marcar" data-track-location="nav">{cta_label}</a>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    </div>
</header>
<main>
{body}
{related_html(related, related_heading)}
{faq_block}
</main>
<footer class="footer">
    <div class="footer-top">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-4 col-12">
                    <div class="single-footer f-about">
                        <div class="logo">
                            <a href="{brand_home}" target="_self">
                                <img draggable="false" src="/assets/images/logo/white-logo.svg" alt="Vera Fernandes, neuropsicóloga">
                            </a>
                        </div>
                        <ul class="social">
                            <li><a href="https://www.facebook.com/verafernandes.psi/"><i class="lni lni-facebook-filled"></i></a></li>
                            <li><a href="https://www.instagram.com/verafernandes.psi"><i class="lni lni-instagram"></i></a></li>
                            <li><a href="https://www.linkedin.com/in/vera-fernandes/"><i class="lni lni-linkedin-original"></i></a></li>
                            <li><a href="mailto:vfernandes.psi@gmail.com"><i class="lni lni-envelope"></i></a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-8 col-md-8 col-12">
                    <div class="row">
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Contactos</h3>
                                <ul>
                                    <li>Membro Efetivo OPP nº 21502</li>
                                    <li>Registo ERS nº 33923</li>
                                    <li><a href="mailto:vfernandes.psi@gmail.com">vfernandes.psi@gmail.com</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Legal</h3>
                                <ul>
                                    <li><a href="/informacao-regulatoria/">Informação Regulatória</a></li>
                                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>
                                    <li><a href="https://www.livroreclamacoes.pt/" target="_blank" rel="noopener noreferrer"><img draggable="false" src="/assets/images/misc/livroreclamacoes.png" alt="Livro de Reclamações Electrónico"></a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        
        <p class="copyright-text">© 2026 Vera Fernandes · Todos os direitos reservados.</p>
</div>
    </div>
</footer>
<a href="#inicio" class="scroll-top" target="_self"><i class="lni lni-chevron-up"></i></a>
<script src="/assets/js/bootstrap.min.js" defer></script>
<script src="/assets/js/wow.min.js" defer></script>
<script src="/assets/js/main.js" defer></script>
<script src="/assets/js/site-data.js" defer></script>
<script src="/assets/js/consent.js?v=3" defer></script>
<script src="/assets/js/funnel.js" defer></script>
</body>
</html>
'''
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def write_legacy_redirect(
    path: str, target: str, label: str = "página actualizada"
) -> None:
    """Keep old URLs working after path renames (e.g. /marcar/ -> /agendar/)."""
    html = f'''<!DOCTYPE html>
<html lang="pt-pt">
<head>
  <meta charset="utf-8" />
  <link rel="canonical" href="{SITE}{target}" />
  <meta http-equiv="refresh" content="0;url={target}" />
  <title>Redireccionar | Vera Fernandes</title>
  <script>
    location.replace("{target}" + location.search + location.hash);
  </script>
</head>
<body>
  <p>Esta página foi movida. <a href="{target}">{label}</a></p>
</body>
</html>
'''
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote redirect", out.relative_to(ROOT), "->", target)


def sobre_section(title, kicker, html, hid="inicio"):
    k = f"<h3>{kicker}</h3>" if kicker else ""
    return f'''
<section id="{hid}" class="section page-content page-content--justify">
    <div class="container">
        <div class="row sobre-layout align-items-start">
            <div class="col-lg-5 sobre-photo-col">
                <div class="sobre-photo">
                    <img draggable="false" src="/assets/images/vera-sobre-400w.webp"
                        srcset="/assets/images/vera-sobre-400w.webp 400w, /assets/images/vera-sobre.webp 721w"
                        sizes="(min-width: 992px) 41.666vw, 320px"
                        width="721" height="1080" loading="eager" decoding="async"
                        alt="Vera Fernandes, neuropsicóloga — foto de perfil">
                </div>
            </div>
            <div class="col-lg-7 sobre-content">
                <div class="section-title sobre-title">
                    {k}
                    <h1>{title}</h1>
                </div>
                {html}
            </div>
        </div>
    </div>
</section>'''


def section(title, kicker, html, hid="inicio", extra_class=""):
    k = f"<h3>{kicker}</h3>" if kicker else ""
    section_class = f"section page-content{extra_class}"
    return f'''
<section id="{hid}" class="{section_class}">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <div class="section-title">
                    {k}
                    <h1>{title}</h1>
                </div>
            </div>
        </div>
        {html}
    </div>
</section>'''


def cta(sono=False, estimulacao=False, label="Agendar"):
    if sono:
        return f'''
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/?servico=sono" class="btn" data-track="marcar">{label}</a>
            <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" rel="noopener noreferrer">Tenho uma dúvida</a>
        </div>'''
    if estimulacao:
        return f'''
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/" class="btn" data-track="marcar">{label}</a>
            <a href="{WA_ESTIMULACAO}" class="btn btn-alt" data-track="whatsapp" rel="noopener noreferrer">Tenho uma dúvida</a>
        </div>'''
    return f'''
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/" class="btn" data-track="marcar">{label}</a>
            <a href="{WA}" class="btn btn-alt" data-track="whatsapp" rel="noopener noreferrer">Tenho uma dúvida</a>
        </div>'''


def write_sono_funnel_page():
    """Página funnel do sono — estrutura espelhada da neuro, tema azul. Não usar page() genérico."""
    path = "psicologia-do-sono"
    if path in MANUAL_PAGE_PATHS:
        print("skip manual", path)
        return
    title = "Consulta de psicologia do sono | Vera Fernandes"
    description = (
        "Consulta de psicologia do sono online para adultos (18+). "
        "Vera Fernandes, neuropsicóloga, OPP 21502. Horário indicado na marcação."
    )
    canonical = f"{SITE}/{path}/"
    crumbs = [("Início", f"{SITE}/"), ("Psicologia do sono", canonical)]
    faqs = [
        ("A consulta é presencial?", "Não. A consulta de psicologia do sono é online."),
        ("É a partir de que idade?", "Para adultos, com 18 ou mais anos."),
        ("Qual é o horário?", "O horário é indicado no momento da marcação."),
        (
            "Substitui um estudo do sono?",
            "Não. Se houver sinais que justifiquem avaliação médica, o passo correcto é um médico.",
        ),
    ]
    graph = build_graph(
        canonical,
        title,
        crumbs,
        description=description,
        faqs=faqs,
        service_key="sono",
    )
    html = f'''<!DOCTYPE html>
<html class="no-js page-sono" lang="pt-pt">
<head>
    <link rel="api-catalog" href="/llms.txt" />
    <link rel="service-doc" href="/llms.txt" />
    <link rel="sitemap" type="application/xml" href="/sitemap.xml" />
    <link rel="canonical" href="{canonical}" />
    <meta charset="utf-8" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Vera Fernandes" />
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
    <meta property="og:locale" content="pt_PT" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:site_name" content="Vera Fernandes - Neuropsicóloga | Braga, Barcelos, Guimarães e Porto" />
    <meta property="og:image" content="{SITE}/assets/images/vera1.webp" />
    <script type="application/ld+json">
{graph}
    </script>
    <link rel="shortcut icon" type="image/x-icon" href="/assets/images/favicon.ico" />
{HEAD_STYLES}
</head>
<body>
<a class="skip-link" href="#inicio">Saltar para o conteúdo</a>
<div class="preloader"><div class="preloader-inner"><div class="preloader-icon"><span></span><span></span></div></div></div>
{CONSENT_BANNER}
<header class="header navbar-area">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-12">
                <div class="nav-inner">
                    <nav class="navbar navbar-expand-lg">
                        <a class="navbar-brand" href="/" target="_self">
                            <img draggable="false" src="/assets/images/logo/white-logo.svg" alt="Vera Fernandes, neuropsicóloga">
                        </a>
                        <button class="navbar-toggler mobile-menu-btn" type="button" data-bs-toggle="collapse"
                            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                            aria-expanded="false" aria-label="Toggle navigation">
                            <span class="toggler-icon"></span><span class="toggler-icon"></span><span class="toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse sub-menu-bar" id="navbarSupportedContent">
                            <ul id="nav" class="navbar-nav ms-auto">
                                <li class="nav-item"><a href="/" aria-label="Página inicial">Início</a></li>
                                <li class="nav-item"><a href="#consultas" class="page-scroll">Consultas</a></li>
                                <li class="nav-item"><a href="#faq" class="page-scroll">FAQ</a></li>
                                <li class="nav-item nav-cta-item">
                                    <div class="button add-list-button">
                                        <a href="/agendar/?servico=sono" class="btn" data-track="marcar" data-track-location="nav">Agendar</a>
                                    </div>
                                </li>
                                <li class="nav-item header-nav-sep" aria-hidden="true"><span>|</span></li>
                                <li class="nav-item header-lane-item"><a href="/neuropsicologia/">Neuropsicologia</a></li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    </div>
</header>

<section id="inicio" class="inicio">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-5 col-md-12 col-12">
                <div class="hero-content">
                    <h1>Dificuldades a dormir?</h1>
                    <p>A consulta de psicologia do sono é online, para adultos (18+). Permite perceber o que está a interferir com o descanso e definir um acompanhamento quando isso fizer sentido.</p>
                    <div class="button">
                        <a href="/agendar/?servico=sono" class="btn" data-track="marcar" data-track-location="hero"><i class="lni lni-calendar"></i> Agendar</a>
                        <button type="button" class="btn btn-alt" data-reveal-triage>Ver se é indicada</button>
                    </div>
                </div>
            </div>
            <div class="col-lg-7 col-md-12 col-12">
                <div class="hero-image">
                    <img draggable="false" src="/assets/images/vera1.webp" alt="Vera Fernandes, neuropsicóloga — consulta de psicologia do sono online">
                </div>
            </div>
        </div>
    </div>
</section>

<section id="overview" class="sobremim section">
    <div class="container">
        <div class="info-one style2">
            <div class="row align-items-center">
                <div class="col-lg-6 col-md-12 col-12">
                    <div class="info-image wow fadeInRight" data-wow-delay=".5s">
                        <div class="single-photo">
                            <img draggable="false" src="/assets/images/mock/sono-cover.jpg" alt="Ambiente calmo e descanso nocturno">
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 col-md-12 col-12">
                    <div class="info-text wow fadeInRight" data-wow-delay=".5s">
                        <div class="main-icon"><i class="lni lni-xl lni-night"></i></div>
                        <h2>A psicologia do sono estuda como pensamentos, hábitos e emoções afectam o descanso.</h2>
                        <p>A consulta destina-se a adultos com dificuldades de sono persistentes — adormecer, manter o sono ou acordar sem recuperação. Realiza-se <strong>online</strong>; o horário é indicado na marcação.</p>
                        <p>Não é uma avaliação neuropsicológica nem um exame de laboratório do sono. Se houver sinais que exijam avaliação médica (por exemplo pausas respiratórias ou sonolência súbita intensa), o passo correcto é um médico.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="triagem" class="faq section">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="section-title">
                    <h3 class="wow zoomIn" data-wow-delay=".2s">Triagem</h3>
                    <h2 class="wow fadeInUp" data-wow-delay=".4s">Está na dúvida se deve marcar uma consulta de sono?</h2>
                    <p class="wow fadeInUp" data-wow-delay=".6s">Responda a 5 perguntas. Isto não é um diagnóstico. Serve apenas para perceber se faz sentido marcar.</p>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <div class="triage-card" id="triage-form">
                    <div class="triage-question">
                        <p>Tem dificuldade em adormecer?</p>
                        <div class="triage-options">
                            <button type="button" data-triage-answer="yes">Sim</button>
                            <button type="button" data-triage-answer="no">Não</button>
                        </div>
                    </div>
                    <div class="triage-question">
                        <p>Acorda durante a noite e custa a voltar a dormir?</p>
                        <div class="triage-options">
                            <button type="button" data-triage-answer="yes">Sim</button>
                            <button type="button" data-triage-answer="no">Não</button>
                        </div>
                    </div>
                    <div class="triage-question">
                        <p>O sono interfere com o seu dia-a-dia?</p>
                        <div class="triage-options">
                            <button type="button" data-triage-answer="yes">Sim</button>
                            <button type="button" data-triage-answer="no">Não</button>
                        </div>
                    </div>
                    <div class="triage-question">
                        <p>Isto se mantém há mais de algumas semanas?</p>
                        <div class="triage-options">
                            <button type="button" data-triage-answer="yes">Sim</button>
                            <button type="button" data-triage-answer="no">Não</button>
                        </div>
                    </div>
                    <div class="triage-question">
                        <p>Um médico recomendou ajuda para o sono?</p>
                        <div class="triage-options">
                            <button type="button" data-triage-answer="yes">Sim</button>
                            <button type="button" data-triage-answer="no">Não</button>
                        </div>
                    </div>
                    <div class="triage-result" id="triage-result" hidden>
                        <p id="triage-result-text"></p>
                        <div class="button">
                            <a href="#consultas" class="btn page-scroll" data-sono-booking data-track="marcar" data-track-location="triagem"><i class="lni lni-calendar"></i> Marcar consulta</a>
                            <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" data-track-location="triagem" rel="noopener noreferrer">Tenho uma dúvida</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="consultas" class="consultas section">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="section-title">
                    <h3 class="wow zoomIn" data-wow-delay=".2s">Consultas</h3>
                    <h2 class="wow fadeInUp" data-wow-delay=".4s">Psicologia do sono online</h2>
                    <p class="wow fadeInUp" data-wow-delay=".6s">Para adultos com 18 ou mais anos. O horário é indicado na marcação.</p>
                </div>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="single-feature wow fadeInUp" data-wow-delay=".2s">
                    <i class="lni lni-xl lni-laptop-phone"></i>
                    <h3>Consulta de psicologia do sono</h3>
                    <p>Consulta de psicologia online com acompanhamento ao longo de várias sessões quando isso fizer sentido. A frequência define-se em conjunto. Não se prometem resultados clínicos nem prazos de melhoria.</p>
                    <div class="table-content">
                        <h4 class="middle-title">Indicada para:</h4>
                        <ul class="table-list">
                            <li><i class="lni lni-checkmark-circle"></i> Dificuldade em adormecer ou em manter o sono;</li>
                            <li><i class="lni lni-checkmark-circle"></i> Acordar sem sensação de recuperação;</li>
                            <li><i class="lni lni-checkmark-circle"></i> Queixas de sono que afectam o dia-a-dia.</li>
                        </ul>
                    </div>
                    <div class="table-content">
                        <h4 class="middle-title">Não substitui:</h4>
                        <ul class="table-list">
                            <li><i class="lni lni-checkmark-circle"></i> Pneumologia, neurologia ou estudo do sono quando há sinais de alarme;</li>
                            <li><i class="lni lni-checkmark-circle"></i> Avaliação neuropsicológica — se a dúvida for memória, veja <a href="/sono-e-memoria/">sono e memória</a> ou <a href="/neuropsicologia/">neuropsicologia</a>.</li>
                        </ul>
                    </div>
                    <div class="button">
                        <a href="/agendar/?servico=sono" class="btn" data-track="marcar" data-track-location="consultas"><i class="lni lni-calendar"></i> Agendar</a>
                        <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" data-track-location="consultas" rel="noopener noreferrer">Tenho uma dúvida</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="faq" class="faq section">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="section-title">
                    <h3 class="wow zoomIn" data-wow-delay=".2s">FAQ</h3>
                    <h2 class="wow fadeInUp" data-wow-delay=".4s">Questões frequentes</h2>
                    <p class="wow fadeInUp" data-wow-delay=".6s">No caso de ter alguma outra questão não hesite em contactar.</p>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="accordion" id="accordionExample">
                    {faq_html(faqs)}
                </div>
                <div class="button cta-pair" style="margin-top:30px;text-align:center;">
                    <a href="/agendar/?servico=sono" class="btn" data-track="marcar" data-track-location="faq"><i class="lni lni-calendar"></i> Agendar</a>
                    <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" data-track-location="faq" rel="noopener noreferrer">Tenho uma dúvida</a>
                </div>
            </div>
        </div>
    </div>
</section>

<footer class="footer">
    <div class="footer-top">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-md-4 col-12">
                    <div class="single-footer f-about">
                        <div class="logo">
                            <a href="/" target="_self">
                                <img draggable="false" src="/assets/images/logo/white-logo.svg" alt="Vera Fernandes, neuropsicóloga">
                            </a>
                        </div>
                        <ul class="social">
                            <li><a href="https://www.facebook.com/verafernandes.psi/"><i class="lni lni-facebook-filled"></i></a></li>
                            <li><a href="https://www.instagram.com/verafernandes.psi"><i class="lni lni-instagram"></i></a></li>
                            <li><a href="https://www.linkedin.com/in/vera-fernandes/"><i class="lni lni-linkedin-original"></i></a></li>
                            <li><a href="mailto:vfernandes.psi@gmail.com"><i class="lni lni-envelope"></i></a></li>
                        </ul>
                        <p class="copyright-text">© 2026 Vera Fernandes · Todos os direitos reservados.</p>
                    </div>
                </div>
                <div class="col-lg-8 col-md-8 col-12">
                    <div class="row">
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Contactos</h3>
                                <ul>
                                    <li>Membro Efetivo OPP nº 21502</li>
                                    <li>Registo ERS nº 33923</li>
                                    <li><a href="mailto:vfernandes.psi@gmail.com">vfernandes.psi@gmail.com</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Legal</h3>
                                <ul>
                                    <li><a href="/informacao-regulatoria/">Informação Regulatória</a></li>
                                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>
                                    <li><a href="https://www.livroreclamacoes.pt/" target="_blank" rel="noopener noreferrer"><img draggable="false" src="/assets/images/misc/livroreclamacoes.png" alt="Livro de Reclamações Electrónico"></a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</footer>
<a href="#inicio" class="scroll-top" target="_self"><i class="lni lni-chevron-up"></i></a>
<script src="/assets/js/bootstrap.min.js" defer></script>
<script src="/assets/js/wow.min.js" defer></script>
<script src="/assets/js/main.js" defer></script>
<script src="/assets/js/site-data.js" defer></script>
<script src="/assets/js/consent.js?v=3" defer></script>
<script src="/assets/js/funnel.js" defer></script>
</body>
</html>
'''
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


COMMON_FAQS = [
    (
        "É necessário encaminhamento médico?",
        "Não. Muitas avaliações são pedidas por um médico como exame complementar, mas também pode marcar por iniciativa própria.",
    ),
    (
        "Posso marcar para o meu pai ou a minha mãe?",
        "Sim. Um familiar pode pedir informação e marcar.",
    ),
    (
        "Quanto custa?",
        "O valor depende do local e é indicado no momento da marcação. A avaliação inclui relatório entregue até 4 dias úteis.",
    ),
    (
        "Quanto tempo demora?",
        "A avaliação está organizada para uma única deslocação, com a duração de cerca de 2 horas.",
    ),
]


def city_page(slug, label):
    cards = "".join(venue_card(v) for v in VENUES if v["city"] == slug)
    others = [
        (lab, f"/avaliacao-neuropsicologica/{s}/")
        for s, lab in [
            ("braga", "Braga"),
            ("barcelos", "Barcelos"),
            ("guimaraes", "Guimarães"),
            ("porto", "Porto"),
        ]
        if s != slug
    ]
    prep = {
        "braga": "em Braga",
        "barcelos": "em Barcelos",
        "guimaraes": "em Guimarães",
        "porto": "no Porto",
    }[slug]
    body = section(
        f"Avaliação neuropsicológica em {label}",
        "Localização",
        f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>Vera Fernandes, neuropsicóloga clínica (cédula profissional n.º 21502), realiza avaliação neuropsicológica {prep} para adultos e idosos.</p>
                <p>A avaliação permite perceber como estão a funcionar diferentes capacidades, como a memória, atenção, linguagem e raciocínio, e se o desempenho está dentro do esperado para a idade e escolaridade. Inclui relatório, entregue até 5 dias úteis. O valor depende do local e é confirmado no momento da marcação.</p>
            </div>
        </div>
        <div class="localizacao">
        <div class="row">{cards}</div>
        </div>
        <div class="row" style="margin-top:24px;">
            <div class="col-lg-8 offset-lg-2 text-center">
                <p>Também disponível em {", ".join(f'<a href="{href}">{lab}</a>' for lab, href in others)}.</p>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-8 offset-lg-2 text-center">
                {cta()}
            </div>
        </div>""",
    )
    page(
        f"avaliacao-neuropsicologica/{slug}",
        f"Avaliação Neuropsicológica em {label} | Vera Fernandes",
        f"Avaliação neuropsicológica em {label} para adultos e idosos. Relatório incluído. Vera Fernandes, OPP 21502.",
        f"{SITE}/avaliacao-neuropsicologica/{slug}/",
        [
            ("Início", f"{SITE}/"),
            ("Avaliação neuropsicológica", f"{SITE}/avaliacao-neuropsicologica/"),
            (label, f"{SITE}/avaliacao-neuropsicologica/{slug}/"),
        ],
        body,
        [],
        related=[
            ("Como é feita a avaliação?", "/avaliacao-neuropsicologica/"),
            ("Posso agendar para um familiar?", "/familiares/"),
            ("Como posso agendar?", "/agendar/"),
        ],
        related_heading="Tópicos relacionados",
        service_key="avaliacao",
        city=label,
        page_kind="city",
    )


def estimulacao_braga_page():
    cards = "".join(
        venue_card(v)
        for v in VENUES
        if v["city"] == "braga" and "estimulacao" in v["services"]
    )
    page(
        "estimulacao-cognitiva/braga",
        "Estimulação Cognitiva em Braga | Vera Fernandes",
        "Estimulação cognitiva em Braga para adultos e idosos. Hospital Lusíadas Braga. Vera Fernandes, OPP 21502.",
        f"{SITE}/estimulacao-cognitiva/braga/",
        [
            ("Início", f"{SITE}/"),
            ("Estimulação cognitiva", f"{SITE}/estimulacao-cognitiva/"),
            ("Braga", f"{SITE}/estimulacao-cognitiva/braga/"),
        ],
        section(
            "Estimulação cognitiva em Braga",
            "Localização",
            f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>Vera Fernandes, neuropsicóloga clínica (cédula profissional n.º 21502), realiza estimulação cognitiva em Braga para adultos e idosos.</p>
                <p>A intervenção permite trabalhar diferentes capacidades, como memória, atenção e linguagem, através de atividades adaptadas às necessidades e objetivos de cada pessoa. O preço deverá ser confirmado no momento da marcação.</p>
            </div>
        </div>
        <div class="localizacao">
        <div class="row">{cards}</div>
        </div>
        <div class="row">
            <div class="col-lg-8 offset-lg-2 text-center">
                {cta(estimulacao=True)}
            </div>
        </div>""",
        ),
        [],
        related=[
            ("Como funciona a estimulação cognitiva?", "/estimulacao-cognitiva/"),
            (
                "Será necessário primeiro uma avaliação neuropsicológica?",
                "/avaliacao-neuropsicologica/",
            ),
            ("Como posso agendar?", "/agendar/"),
        ],
        related_heading="Tópicos relacionados",
        service_key="estimulacao",
        page_kind="city",
    )


def problem_page(slug, title, h1, lead, when, solution, extra_faq, related):
    body = section(
        h1,
        None,
        f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>{lead}</p>
                <h2>Quando faz sentido procurar uma avaliação</h2>
                <p>{when}</p>
                <h2>O que a avaliação neuropsicológica pode acrescentar</h2>
                <p>{solution}</p>
                <h2>Próximo passo</h2>
                <p>Se esta descrição se aproxima da situação, o passo seguinte é perceber <a href="/avaliacao-neuropsicologica/">o que inclui a avaliação</a> e, se fizer sentido, <a href="/agendar/">marcar</a>. A triagem na página de neuropsicologia ajuda a decidir se a avaliação poderá ser indicada. Isto não é um diagnóstico.</p>
                <p>Vera Fernandes é neuropsicóloga em Portugal, OPP 21502, com avaliação em Braga, Barcelos, Guimarães e Porto. Não se trata da profissional homónima noutros países.</p>
                {cta()}
            </div>
        </div>""",
    )
    page(
        slug,
        title,
        f"{h1} Avaliação neuropsicológica em Braga, Barcelos, Guimarães e Porto. Vera Fernandes, OPP 21502.",
        f"{SITE}/{slug}/",
        [("Início", f"{SITE}/"), (h1, f"{SITE}/{slug}/")],
        body,
        COMMON_FAQS + extra_faq,
        related=related,
        condition_slug=slug,
        service_key="avaliacao",
    )


def main():
    page(
        "avaliacao-neuropsicologica",
        "Avaliação Neuropsicológica | Vera Fernandes",
        "O que é a avaliação neuropsicológica, para quem é, o que acontece nas 2 horas e o que o relatório descreve. Braga, Barcelos, Guimarães e Porto.",
        f"{SITE}/avaliacao-neuropsicologica/",
        [
            ("Início", f"{SITE}/"),
            ("Avaliação neuropsicológica", f"{SITE}/avaliacao-neuropsicologica/"),
        ],
        section(
            "Avaliação Neuropsicológica",
            "Exame complementar de diagnóstico",
            extra_class=" page-content--justify",
            html=f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>A avaliação neuropsicológica é um exame complementar de diagnóstico que permite compreender em detalhe o funcionamento cognitivo, comportamental e emocional. Através de uma entrevista clínica e da aplicação de testes neuropsicológicos validados, são avaliadas capacidades como a <strong>memória, atenção, linguagem, raciocínio e funções executivas</strong>.</p>
            <p>O objetivo é perceber se o desempenho se encontra dentro do esperado para a idade e escolaridade da pessoa ou se existem alterações que justificam atenção e intervenção clínica.</p>
            <h2>Quando é indicada?</h2>
            <p>Esta avaliação destina-se a adultos e idosos e é indicada quando surgem queixas, dificuldades no dia a dia ou necessidade de acompanhamento clínico, nomeadamente perante:</p>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de memória frequentes;</li>
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de atenção ou concentração;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações na linguagem, como dificuldade em encontrar palavras ou compreender o que lhe é dito;</li>
                <li><i class="lni lni-checkmark-circle"></i> dificuldades no raciocínio, organização ou resolução de problemas;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações cognitivas associadas a doenças ou lesões neurológicas;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações observadas pela própria pessoa ou pelos seus familiares;</li>
                <li><i class="lni lni-checkmark-circle"></i> encaminhamento por um médico ou outro profissional de saúde.</li>
            </ul>
            <p>É particularmente útil quando estas alterações começam a interferir com atividades do dia a dia, como gerir medicação, cozinhar, conduzir ou organizar tarefas.</p>
            <p>A avaliação pode também ser realizada para caracterizar o funcionamento cognitivo atual e acompanhar a sua evolução ao longo do tempo, nomeadamente quando existe uma doença neurológica ou outra condição clínica relevante.</p>
            <h2>Como é feita a avaliação?</h2>
            <p>O processo divide-se essencialmente em três momentos:</p>
            <h3>1. Consulta presencial</h3>
            <ul>
                <li><strong>Entrevista clínica:</strong> É recolhida informação sobre as dificuldades sentidas, o seu início e evolução, antecedentes clínicos e outras informações relevantes para a interpretação dos resultados. Sempre que possível, a presença de um familiar ou pessoa próxima é bem-vinda para complementar a informação.</li>
                <li><strong>Testes neuropsicológicos:</strong> Aplicação de testes práticos de papel e lápis ajustados a cada pessoa, avaliando áreas como memória, atenção, raciocínio e velocidade de processamento.</li>
                <li><strong>Esclarecimento de dúvidas:</strong> Durante a avaliação existe também espaço para esclarecer dúvidas sobre o processo, os procedimentos realizados e os passos seguintes.</li>
            </ul>
            <h3>2. Análise e Relatório</h3>
            <ul>
                <li>Os resultados da avaliação neuropsicológica são interpretados tendo em consideração valores de referência ajustados à idade e escolaridade, permitindo compreender se o desempenho está dentro do esperado para a pessoa ou se existem dificuldades que se afastam significativamente do que seria expectável.</li>
                <li>É elaborado um <strong>relatório neuropsicológico</strong>, com a caracterização detalhada das capacidades preservadas e das dificuldades identificadas, incluindo orientações para os passos seguintes.</li>
            </ul>
            <h3>3. Entrega dos Resultados</h3>
            <ul>
                <li>A entrega do relatório é feita em até <strong>5 dias úteis</strong>, por e-mail, presencialmente ou por CTT, de acordo com a sua preferência.</li>
            </ul>
            <h2>Duração e Preço</h2>
            <p><strong>Duração:</strong> cerca de 2 horas<br>
            <strong>Preço:</strong> desde 185€<br>
            <strong>Relatório:</strong> incluído</p>
            <p>O preço inclui a avaliação neuropsicológica, a análise e interpretação dos resultados, a elaboração do relatório e a orientação dos próximos passos.</p>
            <p>O valor pode variar consoante o local de realização. O preço aplicável deverá ser confirmado no momento da marcação, de acordo com o local escolhido.</p>
            <h2>Onde realizar</h2>
            <p>A avaliação neuropsicológica é realizada presencialmente em: <a href="/avaliacao-neuropsicologica/braga/">Braga</a> · <a href="/avaliacao-neuropsicologica/barcelos/">Barcelos</a> · <a href="/avaliacao-neuropsicologica/guimaraes/">Guimarães</a> · <a href="/avaliacao-neuropsicologica/porto/">Porto</a></p>
            {cta()}
        </div></div>""",
        ),
        [],
        related=[
            ("E se for para um familiar?", "/familiares/"),
            ("Será só da idade?", "/memoria-e-envelhecimento/"),
            ("Onde realizar em Braga?", "/avaliacao-neuropsicologica/braga/"),
        ],
        related_heading="Tópicos relacionados",
        service_key="avaliacao",
    )

    page(
        "estimulacao-cognitiva",
        "Estimulação Cognitiva | Vera Fernandes",
        "Consulta de estimulação cognitiva de 50 minutos, com plano individual, no Hospital Lusíadas Braga.",
        f"{SITE}/estimulacao-cognitiva/",
        [
            ("Início", f"{SITE}/"),
            ("Estimulação cognitiva", f"{SITE}/estimulacao-cognitiva/"),
        ],
        section(
            "Estimulação cognitiva",
            "Intervenção psicológica individualizada",
            f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>A estimulação cognitiva é uma intervenção psicológica individualizada, que utiliza estratégias e actividades adaptadas às capacidades, necessidades e objectivos de cada pessoa.</p>
            <p>A intervenção pode incidir sobre diferentes capacidades cognitivas, como memória, atenção, linguagem, raciocínio e funções executivas, de acordo com o perfil de cada pessoa e com os objectivos definidos para o acompanhamento.</p>
            <p>Pode ser realizada por pessoas sem alterações cognitivas significativas, com o objectivo de manter e estimular determinadas capacidades, ou por pessoas que apresentam alterações cognitivas associadas a uma condição neurológica ou clínica, quando clinicamente adequada.</p>
            <h2>Quando é indicada</h2>
            <p>A estimulação cognitiva pode ser considerada quando existem dificuldades cognitivas que beneficiem de uma intervenção estruturada e individualizada.</p>
            <p>Pode ser indicada perante:</p>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de memória;</li>
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de atenção ou concentração;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações na linguagem;</li>
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de organização, planeamento ou resolução de problemas;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações cognitivas associadas a doenças ou lesões neurológicas;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações cognitivas após um AVC ou traumatismo cranioencefálico, quando clinicamente adequado;</li>
                <li><i class="lni lni-checkmark-circle"></i> necessidade de manter ou estimular determinadas capacidades cognitivas.</li>
            </ul>
            <p>Quando existem alterações cognitivas, a <a href="/avaliacao-neuropsicologica/">avaliação neuropsicológica</a> pode ser importante antes de iniciar a intervenção, permitindo conhecer o perfil cognitivo da pessoa e definir objectivos de acompanhamento mais adequados.</p>
            <h2>Como é feita a intervenção</h2>
            <p>As sessões têm uma duração de cerca de 50 minutos e são realizadas individualmente.</p>
            <p><strong>Avaliação inicial</strong><br>Sempre que possível, a intervenção é precedida por uma avaliação neuropsicológica, que permite conhecer o perfil cognitivo da pessoa, identificar as capacidades mais preservadas e as áreas que apresentam maiores dificuldades. Esta informação ajuda a definir objectivos de intervenção ajustados às necessidades de cada pessoa.</p>
            <p><strong>Definição das actividades</strong><br>A partir da informação disponível são seleccionadas e adaptadas actividades e estratégias de intervenção cognitiva, tendo em consideração as capacidades, dificuldades e objectivos identificados.</p>
            <p>São também considerados os interesses e preferências pessoais, procurando que as actividades sejam significativas e tenham relação com a vida quotidiana da pessoa.</p>
            <p><strong>Acompanhamento</strong><br>Ao longo das sessões, as actividades podem ser ajustadas de acordo com a resposta da pessoa, a evolução observada e os objectivos definidos. Existe também espaço para esclarecer dúvidas e reflectir sobre a aplicação das estratégias no dia a dia.</p>
            <h2>O que pode ser trabalhado</h2>
            <p>De acordo com as necessidades e objectivos de cada pessoa, podem ser trabalhadas diferentes capacidades cognitivas, nomeadamente:</p>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> <strong>Memória</strong>: retenção e evocação de informação;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Atenção</strong>: capacidade de manter, seleccionar e alternar a atenção;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Linguagem</strong>: acesso às palavras, compreensão e expressão;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Raciocínio</strong>: análise de informação e resolução de problemas;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Funções executivas</strong>: planeamento, organização, flexibilidade e controlo da acção;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Velocidade de processamento</strong>: rapidez com que a informação é compreendida e utilizada.</li>
            </ul>
            <p>O objectivo é trabalhar as capacidades cognitivas de forma orientada e funcional, procurando, sempre que possível, estabelecer uma relação entre as actividades realizadas e as exigências do dia a dia.</p>
            <h2>Duração e preço</h2>
            <p><strong>Duração:</strong> 50 minutos<br>
            <strong>Formato:</strong> acompanhamento individual<br>
            <strong>Preço:</strong> de acordo com a tabela de honorários aplicável no Hospital Lusíadas Braga</p>
            <p>A frequência do acompanhamento é definida em conjunto, de acordo com as necessidades e objectivos da pessoa, e pode ser ajustada ao longo do tempo.</p>
            <p>O preço deverá ser confirmado directamente com o Hospital Lusíadas Braga no momento da marcação, de acordo com as condições aplicáveis.</p>
            <h2 id="onde-realizar">Onde realizar</h2>
            <p>A estimulação cognitiva é realizada presencialmente no <a href="https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0" target="_blank" rel="noopener noreferrer">Hospital Lusíadas Braga</a>.</p>
            {cta()}
        </div></div>""",
        ),
        [],
        related=[
            (
                "Será necessário primeiro uma avaliação neuropsicológica?",
                "/avaliacao-neuropsicologica/",
            ),
            ("Onde realizar em Braga?", "/estimulacao-cognitiva/braga/"),
            ("Como posso agendar?", "/agendar/"),
        ],
        related_heading="Tópicos relacionados",
        service_key="estimulacao",
    )

    estimulacao_braga_page()

    page(
        "familiares",
        "Informação para pais e familiares | Vera Fernandes",
        "Pode agendar uma avaliação neuropsicológica para o pai, a mãe ou outro familiar. Informação para filhos e cuidadores em Braga, Barcelos, Guimarães e Porto.",
        f"{SITE}/familiares/",
        [("Início", f"{SITE}/"), ("Para familiares", f"{SITE}/familiares/")],
        section(
            "Informação para pais e familiares",
            "Para quem agenda",
            f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>Se observou alterações de memória, comportamento ou autonomia no pai, na mãe ou noutro familiar, pode agendar uma avaliação neuropsicológica, mesmo que a própria pessoa não reconheça essas dificuldades.</p>
            <p>Geralmente, o agendamento surge após uma consulta médica de especialidade, como a Neurologia ou a Psiquiatria. Embora não seja necessária uma prescrição médica para que possa realizar uma avaliação neuropsicológica, é muito frequente que os médicos a solicitem em conjunto com outros exames.</p>
            <p>A avaliação caracteriza o funcionamento cognitivo no contexto da história daquela pessoa e o relatório final é uma ferramenta para o médico fechar o diagnóstico e definir os próximos passos.</p>

            <h2>Como abordar a consulta com o seu familiar sem gerar resistência</h2>
            <p>Nem sempre o seu familiar terá perceção das suas próprias dificuldades ou achará a consulta necessária. Falar sobre falhas de memória ou envelhecimento pode provocar uma atitude defensiva, medo ou negação. O objetivo é apresentar a consulta de forma natural, segura e acolhedora:</p>
            <ul class="table-list tip-list">
                <li><i class="lni lni-checkmark-circle"></i> <strong>Foque no bem-estar e prevenção:</strong> Evite frases como «estás muito esquecido» ou «precisas de ir ver a tua cabeça». Prefira enquadrar a consulta como um rastreio de rotina ou uma verificação de saúde geral, tal como fazer análises de sangue.
                    <span class="tip-example"><em>Exemplo:</em> «Acho que seria ótimo fazermos um check-up geral à memória e ao raciocínio para garantirmos que está tudo bem e percebermos como podes manter a tua autonomia.»</span>
                </li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Valide as queixas do próprio:</strong> Se o seu familiar se queixa pontualmente de cansaço, ansiedade ou com algumas falhas de memória, use essa preocupação como ponto de partida.
                    <span class="tip-example"><em>Exemplo:</em> «Como me disseste que te tens sentido mais cansado e esquecido ultimamente, marquei uma consulta especializada para percebermos o que se passa e como te podemos ajudar.»</span>
                </li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Assuma a consulta como uma decisão partilhada:</strong> Mostre que estará presente para apoiar e que o processo é tranquilo e sem julgamentos.
                    <span class="tip-example"><em>Exemplo:</em> «Eu vou contigo. Ficamos juntos na primeira parte para explicar o que tem acontecido e depois fazes alguns exercícios para perceber melhor o funcionamento do teu cérebro.»</span>
                </li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Se houver muita resistência, apoie-se na recomendação médica:</strong> Muitas vezes, a palavra de um profissional de saúde retira o peso do conflito familiar.
                    <span class="tip-example"><em>Exemplo:</em> «O médico achou que seria boa ideia fazermos esta avaliação para completar o estudo e ter a certeza do melhor caminho a seguir.»</span>
                </li>
            </ul>

            <h2>O seu papel como acompanhante</h2>
            <p>É muito importante que a pessoa avaliada vá acompanhada. Na primeira parte da consulta, a sua presença é essencial: o seu relato sobre as rotinas e as mudanças observadas no dia a dia ajuda a construir um quadro rigoroso de toda a situação que a própria pessoa nem sempre consegue detalhar.</p>
            <p>Após essa recolha de informação inicial, a avaliação decorre de forma individual com a pessoa, ao seu próprio ritmo e num ambiente calmo e respeitoso.</p>
            {cta()}
        </div></div>""",
        ),
        [],
        related=[
            ("O que acontece no dia da avaliação?", "/avaliacao-neuropsicologica/"),
            ("Como agendar?", "/agendar/"),
            ("Será só da idade?", "/memoria-e-envelhecimento/"),
        ],
        related_heading="Tópicos relacionados",
    )

    page(
        "sobre",
        "Sobre Vera Fernandes, neuropsicóloga | OPP 21502",
        "Vera Fernandes, neuropsicóloga em Portugal, OPP 21502, especialidade avançada em neuropsicologia. Braga, Barcelos, Guimarães e Porto. Não confundir com homónimas noutros países.",
        f"{SITE}/sobre/",
        [("Início", f"{SITE}/"), ("Sobre", f"{SITE}/sobre/")],
        sobre_section(
            "Vera Fernandes, neuropsicóloga",
            "Sobre",
            f"""
                <p>Membro efetivo da Ordem dos Psicólogos Portugueses, cédula profissional n.º 21502</p>
                <ul class="table-list sobre-credentials">
                    <li><i class="lni lni-checkmark-circle"></i> Especialidade Geral de Psicologia Clínica e da Saúde</li>
                    <li><i class="lni lni-checkmark-circle"></i> Especialidade Avançada em Neuropsicologia</li>
                </ul>
                <p>Prática clínica dedicada à avaliação neuropsicológica de adultos e idosos, com particular foco nas alterações cognitivas associadas ao envelhecimento, demências e outras doenças neurodegenerativas, bem como a diferentes condições neurológicas e psiquiátricas. A avaliação permite compreender o funcionamento cognitivo, bem como os aspetos emocionais e comportamentais, proporcionando uma visão mais abrangente das dificuldades apresentadas e do seu impacto no quotidiano, contribuindo para a orientação clínica.</p>
                <p>Na área do sono, intervenção psicológica dirigida à insónia, com formação específica em Terapia Cognitivo-Comportamental para a Insónia (TCC-I), uma abordagem de primeira linha para o tratamento da insónia. A intervenção centra-se na identificação e modificação dos fatores que contribuem para a manutenção das dificuldades de sono, promovendo padrões de sono mais regulares e reparadores.</p>
                <h2>Experiência Clínica</h2>
                <p>Experiência na realização de avaliação neuropsicológica de adultos e idosos em contexto hospitalar público, no Hospital de Braga (ULS Braga).</p>
                <p>Prática clínica independente em diferentes clínicas privadas, incluindo a colaboração com o <a href="https://www.cnscampus.com/equipa/vera-fernandes/" target="_blank" rel="noopener noreferrer">CNS – Campus Neurológico</a> e o <a href="https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0" target="_blank" rel="noopener noreferrer">Hospital Lusíadas Braga</a>.</p>
                <p>Percurso clínico iniciado em estágios hospitalares no Centro Hospitalar Entre Douro e Vouga e no Hospital de Braga e, posteriormente, consolidado no Serviço de Consulta da Faculdade de Psicologia e de Ciências da Educação da Universidade do Porto (FPCEUP).</p>
                <h2>Investigação e Formação</h2>
                <p>Participação como <em>rater</em> em ensaios clínicos internacionais, integrando equipas de investigação clínica dedicadas ao estudo de novos fármacos na Doença de Alzheimer e noutras patologias neurodegenerativas.</p>
                <p>Apresentação de comunicações e trabalhos científicos em congressos nacionais e internacionais de Neurologia e Neuropsicologia.</p>
                <p>Participação regular em formação clínica especializada, assegurando uma actualização contínua na área clínica.</p>
                <p>Docente no Instituto CRIAP, com colaborações pontuais em instituições de ensino superior.</p>
                <p>Dinamização de sessões de formação e workshops dirigidos a profissionais de saúde e cuidadores.</p>
                <h2>Formação Académica</h2>
                <p>Mestrado Integrado em Psicologia Clínica e da Saúde<br>Faculdade de Psicologia e de Ciências da Educação da Universidade do Porto.</p>
                <p><a href="https://www.linkedin.com/in/vera-fernandes/" target="_blank" rel="noopener noreferrer">Ver perfil completo no LinkedIn</a></p>
                {cta()}""",
        ),
        [],
        related=[
            (
                "O que acontece na avaliação neuropsicológica?",
                "/avaliacao-neuropsicologica/",
            ),
            ("O que é a Terapia Cognitivo-Comportamental para a insónia?", "/TCC-I/"),
            (
                "Qual o papel do psicólogo nas doenças neurológicas?",
                "/blog/papel-psicologo-doencas-neurologicas/",
            ),
        ],
        related_heading="Tópicos relacionados",
    )

    write_legacy_redirect("marcar", "/agendar/", "Agendar consulta")
    write_legacy_redirect(
        "rastreiomemoria", "/rastreio-memoria/", "Rastreio de memória"
    )

    for slug, label in [
        ("braga", "Braga"),
        ("barcelos", "Barcelos"),
        ("guimaraes", "Guimarães"),
        ("porto", "Porto"),
    ]:
        city_page(slug, label)

    page(
        "memoria-e-envelhecimento",
        "Será só da idade? | Vera Fernandes",
        "Esquecer nomes ocasionalmente ou demorar mais a encontrar uma palavra podem fazer parte do envelhecimento típico. Saiba quando uma avaliação neuropsicológica faz sentido.",
        f"{SITE}/memoria-e-envelhecimento/",
        [
            ("Início", f"{SITE}/"),
            ("Memória e envelhecimento", f"{SITE}/memoria-e-envelhecimento/"),
        ],
        section(
            "Será só da idade?",
            "Memória e envelhecimento",
            f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>Esquecer nomes ocasionalmente, demorar mais tempo a encontrar uma palavra ou perder o fio à meada perante momentos de cansaço podem fazer parte do envelhecimento típico. No entanto, quando as falhas de memória se tornam mais frequentes ou causam apreensão, é natural surgir a dúvida: será apenas do processo normal de envelhecimento ou justifica uma investigação mais detalhada?</p>
                <p>A avaliação neuropsicológica permite caracterizar detalhadamente o funcionamento cognitivo atual. Descreve o perfil de pontos fortes e pontos fracos, complementando o diagnóstico clínico realizado pelo médico.</p>

                <h2>Exemplos de sinais de alerta</h2>
                <p>A linha entre o envelhecimento expectável e a necessidade de investigação nem sempre é evidente. Pode fazer sentido ponderar uma avaliação quando observa sinais como:</p>
                <ul class="table-list">
                    <li><i class="lni lni-checkmark-circle"></i> Fazer a mesma pergunta várias vezes na mesma conversa ou repetir sistematicamente o assunto das histórias que conta;</li>
                    <li><i class="lni lni-checkmark-circle"></i> Esquecer recados e compromissos recentes importantes, como não estar preparado para sair à hora combinada para uma consulta ou esquecer que o filho avisou que não iria almoçar em casa;</li>
                    <li><i class="lni lni-checkmark-circle"></i> Sentir desorientação ou hesitação invulgar em trajetos habituais, como o caminho para a farmácia da zona ou o regresso a casa;</li>
                    <li><i class="lni lni-checkmark-circle"></i> Trocar palavras com frequência, usar termos de substituição como «isto», «aquilo», «o coiso», assim como esquecer nomes de objetos do dia a dia;</li>
                    <li><i class="lni lni-checkmark-circle"></i> Guardar pertences em locais invulgares (como chaves dentro do frigorífico ou o comando na despensa) sem conseguir reconstituir os passos para os encontrar;</li>
                    <li><i class="lni lni-checkmark-circle"></i> Revelar uma dificuldade nova e invulgar em gerir a medicação habitual, em utilizar o multibanco ou a cozinhar receitas conhecidas;</li>
                    <li><i class="lni lni-checkmark-circle"></i> Perceber que familiares, amigos ou colegas de trabalho começam a notar e a comentar alterações no desempenho ou no comportamento.</li>
                </ul>

                <h2>O que a avaliação neuropsicológica acrescenta</h2>
                <p>Ao contrário de testes de rastreio rápidos, a avaliação neuropsicológica é um processo aprofundado que utiliza instrumentos aferidos e padronizados:</p>
                <p><strong>Comparação rigorosa:</strong> Compara o desempenho em áreas como a memória, atenção, linguagem e funções executivas com o perfil esperado para a idade e a escolaridade da pessoa.</p>
                <p><strong>Clareza objetiva:</strong> Ajuda a diferenciar entre alterações benignas (associadas à idade, ansiedade ou cansaço) e sinais iniciais de declínio cognitivo associado a doenças neurodegenerativas.</p>
                <p><strong>Orientação de passos futuros:</strong> Fornece um relatório detalhado que auxilia o médico assistente (Neurologia, Psiquiatria ou Medicina Geral e Familiar) nas decisões clínicas, na definição de estratégias de intervenção ou no agendamento de uma reavaliação posterior.</p>

                <h2>Próximo passo</h2>
                <p>Se estes exemplos se aproximam do que tem observado em si ou num familiar, o passo seguinte consiste em compreender como funciona o <a href="/avaliacao-neuropsicologica/">processo de avaliação</a>. A realização de uma <a href="/rastreio-memoria/">triagem</a> prévia ajuda a clarificar se a avaliação é o procedimento mais indicado para o seu caso neste momento.</p>
                <p><em>Nota:</em> A triagem prévia é um instrumento de orientação inicial, que não constitui um diagnóstico médico nem substitui uma consulta de avaliação neuropsicológica.</p>
                {cta()}
            </div>
        </div>""",
        ),
        [],
        related=[
            ("Posso agendar para um familiar?", "/familiares/"),
            ("Como agendar?", "/agendar/"),
            ("Saiba mais sobre demência", "/demencia/"),
        ],
        related_heading="Tópicos relacionados",
        condition_slug="memoria-e-envelhecimento",
        service_key="avaliacao",
    )
    page(
        "demencia",
        "O que é a demência? | Vera Fernandes",
        "A demência não é uma doença única, mas um conjunto de sintomas que afetam memória, raciocínio e autonomia. Não faz parte do envelhecimento normal.",
        f"{SITE}/demencia/",
        [("Início", f"{SITE}/"), ("Demência", f"{SITE}/demencia/")],
        section(
            "O que é a demência?",
            "Demência",
            f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>A demência não é uma doença única, mas sim um termo geral utilizado para descrever um conjunto de sintomas que afetam a memória, o raciocínio, a linguagem e a capacidade de realizar tarefas do dia a dia. Apesar de ser mais frequente em idades avançadas, a demência <strong>não faz parte do envelhecimento normal ou expectável.</strong></p>

                <h2>Existem diferentes tipos de demência</h2>
                <p>A demência pode ser causada por diferentes condições neurológicas ou médicas, cada uma com <strong>características e formas de evolução distintas</strong>:</p>
                <ul class="table-list">
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Doença de Alzheimer:</strong> É a causa mais frequente de demência. Carateriza-se tipicamente por uma perda progressiva da memória recente por dificuldade em reter novas informações.</li>
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Demência Vascular:</strong> Causada por alterações na circulação sanguínea no cérebro (como pequenos AVCs), podendo apresentar um declínio em degraus, com períodos de estabilização intercalados com agravamentos.</li>
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Demência por Corpos de Lewy:</strong> Frequentemente associada a flutuações na atenção, alucinações visuais e alterações motoras semelhantes às da Doença de Parkinson.</li>
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Demência Frontotemporal:</strong> Afeta sobretudo as regiões do cérebro responsáveis pelo comportamento, personalidade e linguagem, podendo surgir em idades mais jovens.</li>
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Causas reversíveis ou secundárias:</strong> Quadros de apatia ou falhas cognitivas semelhantes ao que se observa nas outras demências podem ser causados por depressão, alterações na tiróide, défices vitamínicos ou efeitos secundários de medicação, daí a importância de um estudo rigoroso.</li>
                </ul>
                <p>A <strong>avaliação neuropsicológica</strong> é um exame complementar fundamental nestes quadros. Permite descrever com detalhe o perfil de funcionamento cerebral, ajudando a identificar quais as funções preservadas e quais as afetadas. É um exame baseado em entrevista, questionários e tarefas práticas, totalmente não invasivo (não recorre a máquinas nem agulhas) e indolor. Todo o processo é conduzido com proximidade e adaptado ao ritmo de cada pessoa, num ambiente tranquilo e sem a pressão de um teste. O objetivo é simplesmente compreender como a pessoa lida com as exigências do dia a dia, valorizando os seus pontos fortes e identificando onde precisa de apoio.</p>

                <h2>Quando faz sentido procurar uma avaliação?</h2>
                <p>Pode ser indicado agendar uma avaliação neuropsicológica quando:</p>
                <p><strong>Existem queixas persistentes:</strong> Se observam alterações progressivas na memória recente, na orientação, na linguagem, no raciocínio ou no planeamento do dia a dia;</p>
                <p><strong>Há impacto na autonomia:</strong> Se apresenta uma dificuldade crescente em gerir tarefas habituais, como tomar a medicação, gerir o dinheiro, fazer compras ou utilizar eletrodomésticos;</p>
                <p><strong>Surgem alterações de comportamento:</strong> Mudanças no humor, apatia, isolamento social, desinibição (ter «menos filtro» nas atitudes ou palavras) ou alterações invulgares na personalidade;</p>
                <p><strong>Por solicitação médica:</strong> Quando o médico assistente necessita de um exame aprofundado para apoiar o diagnóstico diferencial (por exemplo, diferenciar entre depressão e demência inicial) ou para definir uma linha de base antes de iniciar um tratamento.</p>

                <h2>O que a avaliação neuropsicológica acrescenta</h2>
                <p>Ao contrário de testes de rastreio breves, a avaliação neuropsicológica oferece um estudo aprofundado e individualizado:</p>
                <ul class="table-list">
                    <li><i class="lni lni-checkmark-circle"></i> Identifica com precisão as funções cognitivas preservadas e as que apresentam declínio, comparando os resultados com o esperado para a idade e escolaridade da pessoa.</li>
                    <li><i class="lni lni-checkmark-circle"></i> Fornece um relatório clínico detalhado que auxilia o médico na identificação do tipo provável de demência ou determinação da gravidade da condição.</li>
                    <li><i class="lni lni-checkmark-circle"></i> Ajuda a compreender o significado dos esquecimentos ou comportamentos no quotidiano, permitindo que a família adapte o ambiente, gira a rotina diária e promova a qualidade de vida.</li>
                    <li><i class="lni lni-checkmark-circle"></i> Serve de base para a definição de estratégias de estimulação e para monitorizar a evolução das funções cognitivas ao longo do tempo.</li>
                </ul>

                <h2>Próximo passo</h2>
                <p>Se esta descrição se aproxima do que tem observado em si ou num familiar, o passo seguinte consiste em compreender como funciona o <a href="/avaliacao-neuropsicologica/">processo de avaliação</a>. A realização de uma <a href="/rastreio-memoria/">triagem</a> prévia ajuda a clarificar se a avaliação é o procedimento mais indicado para o seu caso neste momento.</p>
                <p><em>Nota:</em> A triagem prévia é um instrumento de orientação inicial, que não constitui um diagnóstico médico nem substitui uma consulta de avaliação neuropsicológica.</p>
                {cta()}
            </div>
        </div>""",
        ),
        [],
        related=[
            ("Posso agendar para um familiar?", "/familiares/"),
            ("Como agendar?", "/agendar/"),
            ("Saiba mais sobre Alzheimer", "/alzheimer/"),
        ],
        related_heading="Tópicos relacionados",
        condition_slug="demencia",
        service_key="avaliacao",
    )
    page(
        "alzheimer",
        "Avaliação Neuropsicológica e Doença de Alzheimer | Vera Fernandes",
        "A Doença de Alzheimer é a causa mais frequente de demência. A avaliação neuropsicológica ajuda a caracterizar o funcionamento cognitivo e a apoiar o diagnóstico diferencial.",
        f"{SITE}/alzheimer/",
        [
            ("Início", f"{SITE}/"),
            ("Doença de Alzheimer", f"{SITE}/alzheimer/"),
        ],
        section(
            "Avaliação Neuropsicológica e Doença de Alzheimer",
            "Alzheimer",
            extra_class=" page-content--justify",
            html=f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>A <strong>Doença de Alzheimer</strong> é uma doença neurodegenerativa e a causa mais frequente de demência no adulto e no idoso. Caracteriza-se pela perda progressiva de neurónios em regiões cerebrais fulcrais para a memória, linguagem, orientação e capacidade de planeamento.</p>
                <p>Nas fases iniciais, as alterações podem ser subtis e facilmente confundidas com o envelhecimento normal ou com quadro de ansiedade e depressão. Contudo, identificar precocemente os primeiros sinais de declínio cognitivo é fundamental: permite iniciar estratégias de apoio atempadas, planear o futuro com autonomia e tomar decisões terapêuticas informadas.</p>
                <p>A avaliação neuropsicológica surge neste contexto como um <strong>exame complementar de diagnóstico relevante</strong>, permitindo caracterizar com detalhe o funcionamento cerebral e distinguir se as falhas observadas correspondem ao envelhecimento expetável, a um Défice Cognitivo Ligeiro (DCL) ou a uma fase inicial da Doença de Alzheimer.</p>

                <h2>Quando faz sentido procurar uma avaliação?</h2>
                <p>A avaliação neuropsicológica é indicada em duas situações principais:</p>
                <p><strong>Surgimento de queixas cognitivas:</strong> Quando a própria pessoa ou a sua família notam falhas de memória para informações mais recentes (ex.: repetir as mesmas perguntas, esquecer compromissos), dificuldade em encontrar palavras, desorientação no tempo ou no espaço, assim como perda de capacidade a gerir o dia a dia.</p>
                <p><strong>Por solicitação médica:</strong> Quando o médico (Neurologista, Psiquiatra, Médico de Família ou Geriatra) solicita um estudo detalhado do perfil cognitivo para auxiliar o diagnóstico diferencial de demência ou para acompanhar a evolução clínica.</p>

                <h2>O que a avaliação neuropsicológica acrescenta</h2>
                <p>A caracterização cognitiva vai além de um simples rastreio e permite:</p>
                <ul class="table-list">
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Descrever o perfil cognitivo atual:</strong> Identificar detalhadamente quais as funções preservadas e quais as que apresentam compromisso (memória episódica, atenção, funções executivas, linguagem).</li>
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Produção de relatório clínico:</strong> Emissão de um relatório neuropsicológico detalhado, entregue num prazo até 5 dias úteis após a avaliação.</li>
                    <li><i class="lni lni-checkmark-circle"></i> <strong>Apoiar o diagnóstico médico:</strong> Fornecer dados quantitativos e qualitativos rigorosos que auxiliam o médico na distinção entre Alzheimer e outros tipos de demência ou perturbações do humor.</li>
                </ul>

                <h2>Próximo passo</h2>
                <p>Se esta descrição se aproxima do que tem observado em si ou num familiar, o passo seguinte consiste em compreender como funciona o <a href="/avaliacao-neuropsicologica/">processo de avaliação</a>. A realização de uma <a href="/rastreio-memoria/">triagem</a> prévia ajuda a clarificar se a avaliação é o procedimento mais indicado para o seu caso neste momento.</p>
                <p><em>Nota:</em> A triagem prévia é um instrumento de orientação inicial, que não constitui um diagnóstico médico nem substitui uma consulta de avaliação neuropsicológica.</p>
                {cta(label="Agendar avaliação")}
            </div>
        </div>""",
        ),
        [],
        related=[
            (
                "Como funciona a avaliação neuropsicológica?",
                "/avaliacao-neuropsicologica/",
            ),
            ("Será Alzheimer o mesmo que demência?", "/demencia/"),
            ("Posso agendar para um familiar?", "/familiares/"),
        ],
        related_heading="Tópicos Relacionados",
        condition_slug="alzheimer",
        service_key="avaliacao",
    )

    def write_post_launch_condition_stubs() -> None:
        """Scaffold stubs for post-launch condition articles. Not published until flag is True."""
        problem_page(
            "avc",
            "Avaliação neuropsicológica após AVC | Vera Fernandes",
            "Alterações cognitivas depois de um AVC",
            "Após um acidente vascular cerebral podem existir alterações de atenção, memória, linguagem ou outras funções. A avaliação neuropsicológica caracteriza esse perfil.",
            "Quando, depois de um AVC, se notam dificuldades cognitivas no dia-a-dia, ou quando o médico pede o exame. A estimulação cognitiva, quando indicada, está listada no Hospital Lusíadas Braga.",
            "O relatório descreve as funções avaliadas e pode orientar a planificação de estimulação ou reabilitação, quando clinicamente adequada.",
            [
                (
                    "A estimulação está disponível depois do AVC?",
                    "Quando indicada, a estimulação cognitiva está listada no Hospital Lusíadas Braga.",
                ),
                (
                    "Quanto tempo demora a avaliação?",
                    "Cerca de 2 horas, numa única deslocação.",
                ),
            ],
            related=[
                ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
                ("Estimulação cognitiva", "/estimulacao-cognitiva/"),
                ("Lesão cerebral ou TCE", "/lesao-cerebral/"),
                ("Como marcar?", "/agendar/"),
            ],
        )
        problem_page(
            "parkinson",
            "Avaliação neuropsicológica na doença de Parkinson | Vera Fernandes",
            "Avaliação neuropsicológica e Parkinson",
            "Na doença de Parkinson pode ser pedida uma caracterização cognitiva como exame complementar, para descrever o funcionamento actual ou acompanhar alterações.",
            "Quando existem queixas cognitivas, quando o médico solicita o exame, ou para comparar o funcionamento ao longo do tempo.",
            "A avaliação usa testes validados para a população portuguesa e inclui relatório. O valor depende do local.",
            [
                (
                    "Preciso de encaminhamento de neurologia?",
                    "Não é obrigatório. Muitas avaliações são pedidas pelo médico, e também se pode marcar por iniciativa própria.",
                ),
                (
                    "Um familiar pode marcar?",
                    "Sim. Um familiar pode pedir informação e marcar.",
                ),
            ],
            related=[
                ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
                ("Informação para familiares", "/familiares/"),
                ("Como marcar?", "/agendar/"),
            ],
        )
        problem_page(
            "lesao-cerebral",
            "Avaliação após lesão cerebral ou TCE | Vera Fernandes",
            "Lesão cerebral e traumatismo cranioencefálico",
            "Após traumatismo cranioencefálico ou outra lesão cerebral adquirida, a avaliação neuropsicológica pode caracterizar o funcionamento cognitivo.",
            "Quando se notam alterações de memória, atenção, linguagem ou comportamento após a lesão, ou quando o médico pede o exame.",
            "O relatório descreve o perfil actual. A estimulação cognitiva, quando indicada, está listada no Hospital Lusíadas Braga.",
            [
                (
                    "É para adultos?",
                    "O agendamento está disponível para adultos e idosos, com mais de 18 anos.",
                ),
                (
                    "Há estimulação depois da lesão?",
                    "Quando indicada, a estimulação cognitiva está listada no Hospital Lusíadas Braga.",
                ),
            ],
            related=[
                ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
                ("Depois de um AVC", "/avc/"),
                ("Estimulação cognitiva", "/estimulacao-cognitiva/"),
                ("Como marcar?", "/agendar/"),
            ],
        )

    if PUBLISH_POST_LAUNCH_ARTICLES:
        write_post_launch_condition_stubs()
    else:
        for slug in POST_LAUNCH_ARTICLE_SLUGS:
            stale = ROOT / slug
            if stale.is_dir():
                shutil.rmtree(stale)
                print("removed unpublished", slug)

    # avaliacao-cognitiva removed permanently (duplicate of avaliacao-neuropsicologica)
    stale_avaliacao_cognitiva = ROOT / "avaliacao-cognitiva"
    if stale_avaliacao_cognitiva.is_dir():
        shutil.rmtree(stale_avaliacao_cognitiva)
        print("removed", "avaliacao-cognitiva")

    page(
        "consulta-do-sono",
        "Consulta de Psicologia do Sono | Vera Fernandes",
        "Consulta de psicologia do sono online para adultos com dificuldades de sono, com base na TCC-I. Vera Fernandes, OPP 21502.",
        f"{SITE}/consulta-do-sono/",
        [
            ("Início", f"{SITE}/"),
            ("Psicologia do Sono", f"{SITE}/psicologia-do-sono/"),
            ("Consulta do sono", f"{SITE}/consulta-do-sono/"),
        ],
        section(
            "Psicologia do Sono",
            "Consulta online",
            extra_class=" page-content--justify",
            html=f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>A consulta de Psicologia do Sono é um acompanhamento especializado, realizado <strong>online</strong>, dirigido a adultos que enfrentam dificuldades persistentes com o sono.</p>
            <p>Esta intervenção baseia-se na Terapia Cognitivo-Comportamental para a Insónia (TCC-I), que é uma abordagem estruturada e cientificamente reconhecida como o tratamento de primeira linha para a insónia. O objetivo é identificar e reestruturar os fatores, pensamentos, comportamentos e rotinas que perpetuam os problemas de sono de forma a:</p>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> melhorar a qualidade e quantidade do sono</li>
                <li><i class="lni lni-checkmark-circle"></i> melhorar o impacto da insónia durante o dia</li>
            </ul>
            <h2>Quando é indicada?</h2>
            <p>Esta consulta destina-se a adultos que experienciam:</p>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> Dificuldade em adormecer ou sensação de demorar muito tempo a "desligar";</li>
                <li><i class="lni lni-checkmark-circle"></i> Despertares frequentes durante a noite ou acordar demasiado cedo sem conseguir voltar a adormecer;</li>
                <li><i class="lni lni-checkmark-circle"></i> Ansiedade ou hiperativação ao deitar como "sentir a cabeça a 1000" ou receio de não conseguir dormir;</li>
                <li><i class="lni lni-checkmark-circle"></i> Sensação de sono não reparador, acordando com cansaço físico, mental ou falta de energia;</li>
                <li><i class="lni lni-checkmark-circle"></i> Impacto no dia a dia, como fadiga, irritabilidade, menor rendimento ou dificuldades de concentração;</li>
                <li><i class="lni lni-checkmark-circle"></i> Horários de sono desregulados ou dificuldade em manter uma rotina consistente;</li>
                <li><i class="lni lni-checkmark-circle"></i> Vontade de reduzir ou eliminar medicação para dormir (processo realizado sempre em articulação médica).</li>
            </ul>
            <h2>Como funciona o acompanhamento?</h2>
            <p>O processo de intervenção é estruturado e personalizado, desenrolando-se em <strong>três etapas principais</strong>:</p>
            <h3>1. Avaliação Inicial</h3>
            <ul>
                <li>Mapeamento detalhado dos seus hábitos, rotinas, histórico do problema e fatores que estão a interferir com o descanso.</li>
                <li>Utilização de diários de sono e questionários validados para compreender o seu padrão de sono real.</li>
            </ul>
            <h3>2. Intervenção e Estratégias Práticas (TCC-I)</h3>
            <ul>
                <li>Implementação de técnicas comportamentais para recondicionar a associação entre a cama e o sono.</li>
                <li>Estratégias cognitivas para gerir a ansiedade e os pensamentos ruminativos na hora de deitar.</li>
                <li>Ajuste de hábitos de higiene do sono e regulação do ritmo circadiano.</li>
            </ul>
            <h3>3. Consolidação e Prevenção de Recaídas</h3>
            <ul>
                <li>Acompanhamento da evolução dos indicadores de sono.</li>
                <li>Definição de ferramentas autónomas para manter os ganhos a longo prazo e gerir eventuais noites piores no futuro.</li>
            </ul>
            <h2>Duração e Preço</h2>
            <p><strong>Formato:</strong> Online (via videochamada individual e segura)<br>
            <strong>Duração da consulta:</strong> 50 minutos<br>
            <strong>Preço:</strong> 45€ por consulta</p>
            <p>O valor inclui a consulta individual online, a análise dos diários de sono e o envio de materiais de apoio práticos entre sessões, quando aplicável.</p>
            <h2>Onde realizar</h2>
            <p>As consultas são realizadas <strong>exclusivamente em formato online</strong>, permitindo fazer todo o acompanhamento com total comodidade, privacidade e no conforto do seu espaço, sem necessidade de deslocações.</p>
            {cta(sono=True)}
        </div></div>""",
        ),
        [],
        related=[
            ("Saber mais sobre TCC-I", "/TCC-I/"),
            ("Como posso agendar?", "/agendar/?servico=sono"),
            ("Será um problema de memória ou de sono?", "/sono-e-memoria/"),
        ],
        related_heading="Tópicos Relacionados",
        lane="sono",
        service_key="sono",
    )

    write_sono_funnel_page()

    page(
        "sono-e-memoria",
        "Memória e Sono: por onde começar? | Vera Fernandes",
        "O sono e a cognição influenciam-se mutuamente. Esta página ajuda a escolher entre consulta de psicologia do sono e avaliação neuropsicológica.",
        f"{SITE}/sono-e-memoria/",
        [("Início", f"{SITE}/"), ("Sono e memória", f"{SITE}/sono-e-memoria/")],
        section(
            "Memória e Sono: por onde começar?",
            "Orientação clínica",
            extra_class=" page-content--justify",
            html=f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>O sono e a cognição influenciam-se mutuamente. Dormimos pior quando estamos preocupados com a memória, e a falta de um sono reparador afeta diretamente a atenção, a concentração e a retenção de informação no dia a dia. Para identificar a resposta mais adequada à sua situação ou à de um familiar é importante definir qual é a queixa com maior impacto no seu bem-estar ou na sua rotina diária.</p>

            <h2>Se a queixa principal é o sono</h2>
            <p>Se a dificuldade está em adormecer, em manter um sono contínuo, se acorda sistematicamente com sensação de cansaço ou se tem rotinas de sono desreguladas, a indicação é a <a href="/consulta-do-sono/">Consulta de Psicologia do Sono</a>. Este acompanhamento é realizado em formato online e destina-se a adultos.</p>

            <h2>Se a queixa principal é a memória ou o funcionamento cognitivo</h2>
            <p>Quando a principal preocupação envolver esquecimentos frequentes, dificuldades na linguagem, falta de atenção, desorientação, alterações no comportamento, perda de autonomia na realização de tarefas do quotidiano, a indicação é a <a href="/avaliacao-neuropsicologica/">Avaliação Neuropsicológica</a>. Trata-se de um exame complementar de diagnóstico realizado presencialmente em <a href="/avaliacao-neuropsicologica/braga/">Braga</a>, <a href="/avaliacao-neuropsicologica/barcelos/">Barcelos</a>, <a href="/avaliacao-neuropsicologica/guimaraes/">Guimarães</a> ou <a href="/avaliacao-neuropsicologica/porto/">Porto</a>.</p>

            <h2>Ainda com dúvidas sobre qual a opção indicada para si ou para um familiar?</h2>
            <p>Pode consultar mais informações sobre o modo de funcionamento da <a href="/avaliacao-neuropsicologica/">Avaliação Neuropsicológica</a> e da <a href="/consulta-do-sono/">Consulta de Psicologia do Sono</a>.</p>
            {cta(sono=True)}
        </div></div>""",
        ),
        [],
        related=[
            ("O que é a TCC-I", "/TCC-I/"),
            ("Os esquecimentos serão só da idade?", "/memoria-e-envelhecimento/"),
            ("Saber mais sobre estimulação cognitiva", "/estimulacao-cognitiva/"),
        ],
        related_heading="Tópicos Relacionados",
        lane="sono",
    )

    urls = [
        f"{SITE}/",
        f"{SITE}/neuropsicologia/",
        f"{SITE}/rastreio-memoria/",
        f"{SITE}/psicologia-do-sono/",
        f"{SITE}/consulta-do-sono/",
        f"{SITE}/sono-e-memoria/",
        f"{SITE}/avaliacao-neuropsicologica/",
        f"{SITE}/avaliacao-neuropsicologica/braga/",
        f"{SITE}/avaliacao-neuropsicologica/barcelos/",
        f"{SITE}/avaliacao-neuropsicologica/guimaraes/",
        f"{SITE}/avaliacao-neuropsicologica/porto/",
        f"{SITE}/estimulacao-cognitiva/",
        f"{SITE}/familiares/",
        f"{SITE}/sobre/",
        f"{SITE}/agendar/",
        f"{SITE}/blog/",
        f"{SITE}/blog/papel-psicologo-doencas-neurologicas/",
        f"{SITE}/cursos/",
        f"{SITE}/memoria-e-envelhecimento/",
        f"{SITE}/demencia/",
        f"{SITE}/alzheimer/",
        f"{SITE}/tos/",
        f"{SITE}/privacy/",
    ]
    if PUBLISH_POST_LAUNCH_ARTICLES:
        insert_at = urls.index(f"{SITE}/alzheimer/") + 1
        urls[insert_at:insert_at] = [
            f"{SITE}/avc/",
            f"{SITE}/parkinson/",
            f"{SITE}/lesao-cerebral/",
        ]
    items = "\n".join(
        f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-08-12</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if u == SITE + "/" else "0.8"}</priority>
  </url>"""
        for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{items}\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
