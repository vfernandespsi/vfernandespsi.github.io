"""One-off renderer for inner pages. Output is static HTML for GitHub Pages."""

from __future__ import annotations

from pathlib import Path

from consent_snippets import CONSENT_BANNER
from jsonld import build_graph

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://verafernandes.com"
MANUAL_PAGE_PATHS = frozenset({"psicologia-do-sono"})
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
        f'<li><a href="{v["tel"]}" data-track="telefone" rel="noopener"><i class="lni lni-xl lni-phone"></i> Ligar</a></li>'
    )
    extra.append(
        f'<li><a href="{v["maps"]}" target="_blank" rel="noopener"><i class="lni lni-xl lni-map-marker"></i> Localização</a></li>'
    )
    if v["more"]:
        extra.append(
            f'<li><a href="{v["more"]}" target="_blank" rel="noopener"><i class="lni lni-xl lni-laptop-phone"></i> Saber mais</a></li>'
        )
    if v["wa"]:
        from urllib.parse import quote

        extra.append(
            f'<li><a href="https://api.whatsapp.com/send?phone=351914166181&text={quote(v["wa"])}" target="_blank" rel="noopener" data-track="whatsapp"><i class="lni lni-xl lni-whatsapp"></i> Tenho uma dúvida</a></li>'
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
    brand_home = "/"
    wa = WA_SONO if is_sono else WA
    cta_label = "Agendar"
    cta_href = "/agendar/?servico=sono" if is_sono else "/agendar/"
    nav = """
                                <li class="nav-item"><a href="/">Início</a></li>
                                <li class="nav-item"><a href="/neuropsicologia/">Neuropsicologia</a></li>
                                <li class="nav-item"><a href="/psicologia-do-sono/">Psicologia do sono</a></li>"""
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
            <a href="{wa}" class="btn btn-alt" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>
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
    <link rel="stylesheet" href="/assets/css/animate.css">
    <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/funnel.css">
    <link rel="stylesheet" href="/assets/css/consent.css">
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
                                    <li>Membro Efectivo OPP 21502</li>
                                    <li>Especialidade Avançada em Neuropsicologia</li>
                                    <li><a href="mailto:vfernandes.psi@gmail.com">vfernandes.psi@gmail.com</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Legal</h3>
                                <ul>
                                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>
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
<div class="mobile-cta-bar">
    <a href="{cta_href}" data-track="marcar" data-track-location="mobile-bar">{cta_label}</a>
    <a class="cta-secondary" href="{wa}" data-track="whatsapp" data-track-location="mobile-bar" rel="noopener">Tenho uma dúvida</a>
</div>
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


def cta(sono=False, estimulacao=False):
    if sono:
        return f'''
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/?servico=sono" class="btn" data-track="marcar">Agendar</a>
            <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>
        </div>'''
    if estimulacao:
        return f'''
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/" class="btn" data-track="marcar">Agendar</a>
            <a href="{WA_ESTIMULACAO}" class="btn btn-alt" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>
        </div>'''
    return f'''
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/" class="btn" data-track="marcar">Agendar</a>
            <a href="{WA}" class="btn btn-alt" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>
        </div>'''


def write_sono_funnel_page():
    """Página funnel do sono — estrutura espelhada da neuro, tema azul. Não usar page() genérico."""
    path = "psicologia-do-sono"
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
    <link rel="stylesheet" href="/assets/css/animate.css">
    <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/funnel.css">
    <link rel="stylesheet" href="/assets/css/consent.css">
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
                            <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" data-track-location="triagem" rel="noopener">Tenho uma dúvida</a>
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
                        <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" data-track-location="consultas" rel="noopener">Tenho uma dúvida</a>
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
                    <a href="{WA_SONO}" class="btn btn-alt" data-track="whatsapp" data-track-location="faq" rel="noopener">Tenho uma dúvida</a>
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
                    </div>
                </div>
                <div class="col-lg-8 col-md-8 col-12">
                    <div class="row">
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Contactos</h3>
                                <ul>
                                    <li>Membro Efectivo OPP 21502</li>
                                    <li>Especialidade Avançada em Neuropsicologia</li>
                                    <li><a href="mailto:vfernandes.psi@gmail.com">vfernandes.psi@gmail.com</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-lg-6 col-md-6 col-12">
                            <div class="single-footer f-link">
                                <h3>Legal</h3>
                                <ul>
                                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>
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
<div class="mobile-cta-bar">
    <a href="/agendar/?servico=sono" data-track="marcar" data-track-location="mobile-bar">Agendar</a>
    <a class="cta-secondary" href="{WA_SONO}" data-track="whatsapp" data-track-location="mobile-bar" rel="noopener">Tenho uma dúvida</a>
</div>
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
            <div class="col-lg-8 offset-lg-2">
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
            <div class="col-lg-8 offset-lg-2">
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
            "Avaliação neuropsicológica",
            "Exame complementar de diagnóstico",
            f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>A avaliação neuropsicológica é um exame complementar de diagnóstico que permite avaliar o funcionamento cognitivo, comportamental e emocional de uma pessoa. É realizada através de uma entrevista clínica e da aplicação de testes neuropsicológicos validados para a população portuguesa.</p>
            <p>A avaliação permite caracterizar diferentes capacidades, como memória, atenção, linguagem, raciocínio e funções executivas, e perceber se o desempenho observado se encontra dentro do esperado para a idade e escolaridade da pessoa ou se existem alterações que mereçam atenção clínica.</p>
            <h2>Quando é indicada</h2>
            <p>A avaliação neuropsicológica destina-se a adultos e idosos que apresentem queixas ou alterações ao nível do funcionamento cognitivo ou que tenham necessidade de realizar uma caracterização detalhada do funcionamento cognitivo actual na sequência de uma situação clínica.</p>
            <p>Pode ser indicada perante:</p>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de memória ou esquecimentos frequentes;</li>
                <li><i class="lni lni-checkmark-circle"></i> dificuldades de atenção ou concentração;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações na linguagem, como dificuldade em encontrar palavras ou compreender o que lhe é dito;</li>
                <li><i class="lni lni-checkmark-circle"></i> dificuldades no raciocínio, organização ou resolução de problemas;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações cognitivas associadas a doenças ou lesões neurológicas;</li>
                <li><i class="lni lni-checkmark-circle"></i> alterações observadas pela própria pessoa ou pelos seus familiares;</li>
                <li><i class="lni lni-checkmark-circle"></i> encaminhamento por um médico ou outro profissional de saúde.</li>
            </ul>
            <p>É particularmente útil quando estas alterações começam a interferir com actividades do dia a dia, como gerir medicação, cozinhar, conduzir, organizar tarefas ou lidar com situações que anteriormente eram realizadas com facilidade.</p>
            <p>A avaliação pode também ser realizada para caracterizar o funcionamento cognitivo actual e acompanhar a sua evolução ao longo do tempo, nomeadamente quando existe uma doença neurológica ou outra condição clínica relevante.</p>
            <h2>Como é feita a avaliação</h2>
            <p>A avaliação decorre numa única deslocação, com duração aproximada de 2 horas.</p>
            <h3>Durante a avaliação</h3>
            <p><strong>Entrevista clínica</strong><br>É recolhida informação sobre as dificuldades sentidas, o seu início e evolução, antecedentes clínicos, medicação, escolaridade, actividade profissional e outros factores relevantes para a interpretação dos resultados.</p>
            <p>A entrevista é realizada com a própria pessoa e, sempre que possível e adequado, com um familiar ou outra pessoa próxima, uma vez que esta informação complementar pode ajudar a compreender melhor as alterações observadas e o seu impacto no dia a dia.</p>
            <p><strong>Testes neuropsicológicos</strong><br>São aplicados testes de papel e lápis que avaliam diferentes funções cognitivas, de acordo com as questões clínicas identificadas. Entre as áreas avaliadas podem incluir-se memória, atenção, linguagem, raciocínio, velocidade de processamento, capacidade de pensamento abstracto e flexibilidade cognitiva. A selecção dos testes é realizada de acordo com as características e necessidades de cada pessoa.</p>
            <p><strong>Esclarecimento de dúvidas</strong><br>Durante a avaliação existe também espaço para esclarecer dúvidas sobre o processo, os procedimentos realizados e os passos seguintes.</p>
            <h2>Depois da avaliação</h2>
            <p>A avaliação não termina com a aplicação dos testes. Os resultados são posteriormente analisados e interpretados em conjunto com a informação recolhida na entrevista clínica.</p>
            <p>Os resultados da avaliação neuropsicológica são interpretados tendo em consideração valores de referência ajustados à idade e escolaridade, permitindo compreender se o desempenho está dentro do esperado para a pessoa ou se existem dificuldades que se afastam significativamente do que seria expectável.</p>
            <p>Esta informação é importante porque algumas alterações cognitivas podem fazer parte do envelhecimento normal, enquanto outras podem justificar investigação clínica adicional.</p>
            <p>Com base nessa análise é elaborado um relatório neuropsicológico, que integra os principais resultados e a sua interpretação clínica.</p>
            <h2>O que o relatório descreve</h2>
            <p>O relatório de avaliação neuropsicológica apresenta uma caracterização detalhada do funcionamento cognitivo, de acordo com a problemática clínica que motivou a avaliação.</p>
            <p>Os resultados são interpretados tendo em consideração factores relevantes como a idade, escolaridade e o contexto clínico, permitindo perceber quais as capacidades que se encontram dentro do esperado, quais poderão apresentar alterações e a relevância dessas alterações no contexto da avaliação. Sempre que adequado, o relatório inclui também orientações sobre os próximos passos, tendo em conta os resultados obtidos.</p>
            <p>A entrega do relatório é feita até 5 dias úteis, por e-mail, presencialmente ou por CTT, de acordo com a opção mais conveniente.</p>
            <p>A avaliação neuropsicológica é um exame complementar de diagnóstico e deve ser interpretada em articulação com a informação clínica disponível. Não substitui a avaliação ou o diagnóstico médico.</p>
            <h2>Duração e Preço</h2>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> <strong>Duração:</strong> cerca de 2 horas</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Preço:</strong> desde 185€</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Relatório:</strong> incluído</li>
            </ul>
            <p>O preço inclui a avaliação neuropsicológica, a análise e interpretação dos resultados, a elaboração do relatório e a orientação dos próximos passos.</p>
            <p>O valor pode variar consoante o local de realização. O preço aplicável deverá ser confirmado no momento da marcação, de acordo com o local escolhido.</p>
            <h2>Onde realizar</h2>
            <p>A avaliação neuropsicológica é realizada presencialmente em:</p>
            <p><a href="/avaliacao-neuropsicologica/braga/">Braga</a> · <a href="/avaliacao-neuropsicologica/barcelos/">Barcelos</a> · <a href="/avaliacao-neuropsicologica/guimaraes/">Guimarães</a> · <a href="/avaliacao-neuropsicologica/porto/">Porto</a></p>
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
                <li><i class="lni lni-checkmark-circle"></i> <strong>Memória</strong> — retenção e evocação de informação;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Atenção</strong> — capacidade de manter, seleccionar e alternar a atenção;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Linguagem</strong> — acesso às palavras, compreensão e expressão;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Raciocínio</strong> — análise de informação e resolução de problemas;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Funções executivas</strong> — planeamento, organização, flexibilidade e controlo da acção;</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Velocidade de processamento</strong> — rapidez com que a informação é compreendida e utilizada.</li>
            </ul>
            <p>O objectivo é trabalhar as capacidades cognitivas de forma orientada e funcional, procurando, sempre que possível, estabelecer uma relação entre as actividades realizadas e as exigências do dia a dia.</p>
            <h2>Duração e preço</h2>
            <ul class="table-list">
                <li><i class="lni lni-checkmark-circle"></i> <strong>Duração:</strong> 50 minutos</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Formato:</strong> acompanhamento individual</li>
                <li><i class="lni lni-checkmark-circle"></i> <strong>Preço:</strong> de acordo com a tabela de honorários aplicável no Hospital Lusíadas Braga</li>
            </ul>
            <p>A frequência do acompanhamento é definida em conjunto, de acordo com as necessidades e objectivos da pessoa, e pode ser ajustada ao longo do tempo.</p>
            <p>O preço deverá ser confirmado directamente com o Hospital Lusíadas Braga no momento da marcação, de acordo com as condições aplicáveis.</p>
            <h2 id="onde-realizar">Onde realizar</h2>
            <p>A estimulação cognitiva é realizada presencialmente no <a href="https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0" target="_blank" rel="noopener">Hospital Lusíadas Braga</a>.</p>
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

    page(
        "familiares",
        "Avaliação neuropsicológica para pais e familiares | Vera Fernandes",
        "Pode marcar uma avaliação neuropsicológica para o pai, a mãe ou outro familiar. Informação para filhos e cuidadores em Braga, Barcelos, Guimarães e Porto.",
        f"{SITE}/familiares/",
        [("Início", f"{SITE}/"), ("Para familiares", f"{SITE}/familiares/")],
        section(
            "Avaliação neuropsicológica para pais e familiares",
            "Para quem marca",
            f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>Se observou alterações de memória, comportamento ou autonomia no pai, na mãe ou noutro familiar, pode pedir informação mesmo que a própria pessoa não reconheça as dificuldades.</p>
            <p>A avaliação não estabelece sozinha um diagnóstico médico. Caracteriza o funcionamento cognitivo e produz um relatório que pode ser útil para o médico e para decidir os próximos passos.</p>
            <p>É aconselhável que a pessoa avaliada vá acompanhada na primeira parte da consulta. A marcação pode ser feita por um familiar.</p>
            {cta()}
        </div></div>""",
        ),
        [
            (
                "Posso marcar uma avaliação para o meu pai ou a minha mãe?",
                "Sim. Um familiar pode pedir informação e marcar.",
            ),
            (
                "A pessoa tem de querer vir?",
                "A avaliação realiza-se com o paciente. Pode esclarecer dúvidas antes de marcar, inclusive por WhatsApp.",
            ),
            (
                "O relatório serve para levar ao médico?",
                "Sim. O relatório descreve o funcionamento cognitivo e é entregue até 4 dias úteis.",
            ),
        ],
        related=[
            ("O que acontece no dia da avaliação?", "/avaliacao-neuropsicologica/"),
            ("Memória e envelhecimento", "/memoria-e-envelhecimento/"),
            ("Onde realizar?", "/avaliacao-neuropsicologica/braga/"),
            ("Como marcar?", "/agendar/"),
        ],
    )

    page(
        "sobre",
        "Sobre Vera Fernandes, neuropsicóloga | OPP 21502",
        "Vera Fernandes, neuropsicóloga em Portugal, OPP 21502, especialidade avançada em neuropsicologia. Braga, Barcelos, Guimarães e Porto. Não confundir com homónimas noutros países.",
        f"{SITE}/sobre/",
        [("Início", f"{SITE}/"), ("Sobre", f"{SITE}/sobre/")],
        section(
            "Vera Fernandes, neuropsicóloga",
            "Sobre",
            f"""
        <div class="row align-items-start" style="margin-top: 2rem;">
            <div class="col-lg-5"><img draggable="false" src="/assets/images/vera2.webp" alt="Vera Fernandes, neuropsicóloga — foto de perfil"></div>
            <div class="col-lg-7">
                <p>Membro efetivo da Ordem dos Psicólogos Portugueses, cédula profissional n.º 21502</p>
                <ul class="table-list">
                    <li><i class="lni lni-checkmark-circle"></i> Especialidade Geral de Psicologia Clínica e da Saúde</li>
                    <li><i class="lni lni-checkmark-circle"></i> Especialidade Avançada em Neuropsicologia</li>
                </ul>
                <p>Prática clínica dedicada à avaliação neuropsicológica de adultos e idosos, com particular foco nas alterações cognitivas associadas ao envelhecimento, demências e outras doenças neurodegenerativas, bem como a diferentes condições neurológicas e psiquiátricas. A avaliação permite compreender o funcionamento cognitivo, bem como os aspetos emocionais e comportamentais, proporcionando uma visão mais abrangente das dificuldades apresentadas e do seu impacto no quotidiano, contribuindo para a orientação clínica.</p>
                <p>Na área do sono, intervenção psicológica dirigida à insónia, com formação específica em Terapia Cognitivo-Comportamental para a Insónia (TCC-I), uma abordagem de primeira linha para o tratamento da insónia. A intervenção centra-se na identificação e modificação dos fatores que contribuem para a manutenção das dificuldades de sono, promovendo padrões de sono mais regulares e reparadores.</p>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <h2>Experiência Clínica</h2>
                <p>Experiência na realização de avaliação neuropsicológica de adultos e idosos em contexto hospitalar público, no Hospital de Braga (ULS Braga).</p>
                <p>Prática clínica independente em diferentes clínicas privadas, incluindo a colaboração com o <a href="https://www.cnscampus.com/equipa/vera-fernandes/" target="_blank" rel="noopener">CNS – Campus Neurológico</a> e o <a href="https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0" target="_blank" rel="noopener">Hospital Lusíadas Braga</a>.</p>
                <p>Percurso clínico iniciado em estágios hospitalares no Centro Hospitalar Entre Douro e Vouga e no Hospital de Braga e, posteriormente, consolidado no Serviço de Consulta da Faculdade de Psicologia e de Ciências da Educação da Universidade do Porto (FPCEUP).</p>
                <h2>Investigação e Formação</h2>
                <p>Participação como rater em ensaios clínicos internacionais, integrando equipas de investigação clínica dedicadas ao estudo de novos fármacos na Doença de Alzheimer e noutras patologias neurodegenerativas.</p>
                <p>Apresentação de comunicações e trabalhos científicos em congressos nacionais e internacionais de Neurologia e Neuropsicologia.</p>
                <p>Participação regular em formação clínica especializada, assegurando uma actualização contínua na área clínica.</p>
                <p>Docente no Instituto CRIAP, com colaborações pontuais em instituições de ensino superior.</p>
                <p>Dinamização de sessões de formação e workshops dirigidos a profissionais de saúde e cuidadores.</p>
                <h2>Formação Académica</h2>
                <p><strong>Mestrado Integrado em Psicologia Clínica e da Saúde</strong><br>Faculdade de Psicologia e de Ciências da Educação da Universidade do Porto.</p>
                <p><a href="https://www.linkedin.com/in/vera-fernandes/" target="_blank" rel="noopener">Percurso profissional completo</a></p>
                {cta()}
            </div>
        </div>""",
        ),
        [],
        related=[
            (
                "O que acontece na avaliação neuropsicológica?",
                "/avaliacao-neuropsicologica/",
            ),
            ("O que é a Terapia Cognitivo-Comportamental para a insónia?", "/TCC-i/"),
            (
                "Qual o papel do psicólogo nas doenças neurológicas?",
                "/blog/papel-psicologo-doencas-neurologicas/",
            ),
        ],
        related_heading="Tópicos relacionados",
    )

    cards = "".join(venue_card(v, booking=True) for v in VENUES)
    page(
        "marcar",
        "Agendar | Vera Fernandes",
        "Agendar consultas de neuropsicologia presencial em Braga, Barcelos, Guimarães e Porto. Vera Fernandes, OPP 21502.",
        f"{SITE}/agendar/",
        [("Início", f"{SITE}/"), ("Agendar", f"{SITE}/agendar/")],
        section(
            "Consultas de neuropsicologia",
            "Agendar",
            f'''
        <div class="booking-step">
            <h3>Qual o serviço?</h3>
            <div class="city-chips">
                <button type="button" class="city-chip is-active" data-book-service="avaliacao">Avaliação neuropsicológica</button>
                <button type="button" class="city-chip" data-book-service="estimulacao">Estimulação cognitiva</button>
            </div>
        </div>
        <div id="booking-cities" class="booking-step">
            <h3>Onde pretende realizar?</h3>
            <div class="city-chips">
                <button type="button" class="city-chip" data-book-city="braga">Braga</button>
                <button type="button" class="city-chip" data-book-city="barcelos">Barcelos</button>
                <button type="button" class="city-chip" data-book-city="guimaraes">Guimarães</button>
                <button type="button" class="city-chip" data-book-city="porto">Porto</button>
            </div>
        </div>
        <div id="booking-venues" class="booking-venues localizacao">
            <div class="row">{cards}</div>
        </div>
        <p id="booking-empty" hidden>A estimulação cognitiva está indicada no Hospital Lusíadas Braga. Escolha Braga para ver esse local, ou seleccione avaliação neuropsicológica para os outros concelhos.</p>
        <p id="booking-doubt-presencial">Se ainda tem dúvidas, clique em <a href="{WA}" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>.</p>''',
            hid="inicio",
            extra_class=" booking-page",
        ),
        faqs=None,
        related=[
            ("Será só da idade ou devo preocupar-me?", "/memoria-e-envelhecimento/"),
            ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
            ("E se quiser agendar para um familiar?", "/familiares/"),
        ],
        related_heading="Tópicos relacionados",
        page_kind="booking",
    )

    for slug, label in [
        ("braga", "Braga"),
        ("barcelos", "Barcelos"),
        ("guimaraes", "Guimarães"),
        ("porto", "Porto"),
    ]:
        city_page(slug, label)

    problem_page(
        "memoria-e-envelhecimento",
        "Memória e envelhecimento | Avaliação neuropsicológica",
        "Memória e envelhecimento",
        "Esquecimentos podem fazer parte do envelhecimento esperado. Também podem justificar uma caracterização mais detalhada do funcionamento cognitivo. A avaliação neuropsicológica descreve o perfil actual; não substitui o diagnóstico médico.",
        "Quando os esquecimentos de conversas ou recados recentes se repetem, quando alguém próximo também reparou, ou quando passam a interferir com o dia-a-dia.",
        "O relatório compara funções como memória e atenção com o esperado para a idade e escolaridade, e pode ajudar a decidir se faz sentido um acompanhamento médico ou uma reavaliação posterior.",
        [
            (
                "O esquecimento aos 65 anos é sempre demência?",
                "Não. A avaliação descreve o funcionamento cognitivo. O diagnóstico médico, quando indicado, cabe ao médico.",
            ),
            (
                "Um familiar pode marcar?",
                "Sim. Muitas marcações são feitas por um filho ou uma filha.",
            ),
        ],
        related=[
            ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
            ("É para um familiar?", "/familiares/"),
            ("Quando a dúvida é maior", "/demencia/"),
            ("Como marcar?", "/agendar/"),
        ],
    )
    problem_page(
        "demencia",
        "Avaliação neuropsicológica e demência | Vera Fernandes",
        "Avaliação cognitiva e demência",
        "A avaliação neuropsicológica é um exame complementar usado para caracterizar o perfil cognitivo quando há suspeita de demência ou para acompanhar alterações ao longo do tempo.",
        "Quando existem queixas de memória, linguagem ou autonomia, ou quando um médico pede o exame para auxiliar o diagnóstico diferencial.",
        "O relatório descreve o funcionamento cognitivo actual e pode ser integrado na avaliação médica. Não estabelece sozinho o diagnóstico de demência.",
        [
            (
                "A avaliação diagnostica demência?",
                "Não. É um exame complementar. O diagnóstico médico, quando existir, é da responsabilidade do médico.",
            ),
            (
                "Posso marcar para o meu pai ou a minha mãe?",
                "Sim. Um familiar pode pedir informação e marcar.",
            ),
        ],
        related=[
            ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
            ("Informação para familiares", "/familiares/"),
            ("Doença de Alzheimer", "/alzheimer/"),
            ("Como marcar?", "/agendar/"),
        ],
    )
    problem_page(
        "alzheimer",
        "Avaliação neuropsicológica e doença de Alzheimer | Vera Fernandes",
        "Avaliação neuropsicológica e doença de Alzheimer",
        "A doença de Alzheimer é uma das situações em que a caracterização cognitiva pode ser pedida como exame complementar. Vera Fernandes participa em investigação nesta área enquanto membro de equipa de ensaios clínicos.",
        "Quando há queixas de memória ou quando o médico solicita avaliação para auxiliar o diagnóstico ou o seguimento.",
        "A avaliação descreve o perfil neuropsicológico actual e produz um relatório até 4 dias úteis. Não promete resultados terapêuticos.",
        [
            (
                "Serve para confirmar Alzheimer?",
                "A avaliação caracteriza o funcionamento cognitivo e auxilia o médico. Não substitui a consulta médica.",
            ),
            (
                "Há relatório?",
                "Sim. O relatório é entregue até 4 dias úteis.",
            ),
        ],
        related=[
            ("O que inclui a avaliação?", "/avaliacao-neuropsicologica/"),
            ("Informação para familiares", "/familiares/"),
            ("Avaliação e demência", "/demencia/"),
            ("Como marcar?", "/agendar/"),
        ],
    )
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
    problem_page(
        "avaliacao-cognitiva",
        "Avaliação cognitiva | Vera Fernandes",
        "Avaliação cognitiva",
        "Avaliação cognitiva, neste contexto, refere-se à avaliação neuropsicológica: um exame complementar que caracteriza memória, atenção, linguagem e outras funções.",
        "Quando há queixas cognitivas, pedido médico, ou necessidade de um relatório para o seguimento clínico.",
        "Em cerca de 2 horas, numa única deslocação, com relatório até 4 dias úteis. Disponível em Braga, Barcelos, Guimarães e Porto.",
        [
            (
                "Qual é a diferença para um teste de memória isolado?",
                "A avaliação neuropsicológica cobre várias funções cognitivas e inclui interpretação clínica e relatório.",
            )
        ],
        related=[
            (
                "O que inclui a avaliação neuropsicológica?",
                "/avaliacao-neuropsicologica/",
            ),
            ("Onde em Braga?", "/avaliacao-neuropsicologica/braga/"),
            ("Como marcar?", "/agendar/"),
        ],
    )

    write_sono_funnel_page()

    page(
        "sono-e-memoria",
        "Sono e memória | Vera Fernandes",
        "Se a dúvida é entre dificuldades de sono e queixas de memória, esta página ajuda a escolher o caminho. Vera Fernandes, OPP 21502.",
        f"{SITE}/sono-e-memoria/",
        [("Início", f"{SITE}/"), ("Sono e memória", f"{SITE}/sono-e-memoria/")],
        section(
            "Sono e memória",
            "Escolher o caminho",
            """
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>Sono mau e falhas de memória podem aparecer juntos. São, neste site, dois serviços diferentes. Escolha o que descreve melhor a situação principal.</p>
            <h2>A queixa principal é o sono</h2>
            <p>Não está a conseguir dormir, ou acorda sem recuperação, e procura uma consulta de psicologia do sono. É online, para adultos (18+).</p>
            <p><a href="/psicologia-do-sono/" class="btn">Psicologia do sono</a></p>
            <h2>A queixa principal é a memória ou a cognição</h2>
            <p>Esquecimentos, atenção, linguagem ou autonomia no dia-a-dia, para si ou para um familiar. O caminho é a avaliação neuropsicológica, presencial, em Braga, Barcelos, Guimarães ou Porto.</p>
            <p><a href="/neuropsicologia/" class="btn">Memória e cognição</a></p>
            <p>Vera Fernandes, neuropsicóloga em Portugal, OPP 21502.</p>
        </div></div>""",
        ),
        [
            (
                "Posso fazer os dois?",
                "São consultas diferentes. Comece pela queixa principal. Se mais tarde a outra também fizer sentido, pode marcar essa em separado.",
            )
        ],
        related=[
            ("Consulta de psicologia do sono", "/psicologia-do-sono/"),
            ("Avaliação neuropsicológica", "/avaliacao-neuropsicologica/"),
        ],
    )

    urls = [
        f"{SITE}/",
        f"{SITE}/neuropsicologia/",
        f"{SITE}/rastreiomemoria/",
        f"{SITE}/psicologia-do-sono/",
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
        f"{SITE}/avc/",
        f"{SITE}/parkinson/",
        f"{SITE}/lesao-cerebral/",
        f"{SITE}/avaliacao-cognitiva/",
        f"{SITE}/tos/",
        f"{SITE}/privacy/",
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
