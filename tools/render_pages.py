"""One-off renderer for inner pages. Output is static HTML for GitHub Pages."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://verafernandes.com"
WA = "https://api.whatsapp.com/send?phone=351914166181&text=Tenho%20uma%20d%C3%BAvida%20sobre%20avalia%C3%A7%C3%A3o%20neuropsicol%C3%B3gica."

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
        "more": "https://www.cnscampus.com/pt",
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
        f'<li><a href="{v["tel"]}" data-track="telefone" rel="noopener"><i class="lni lni-xl lni-phone"></i> Marcar avaliação</a></li>'
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


def professional_graph():
    return {
        "@type": ["Person", "Physician", "MedicalBusiness"],
        "@id": f"{SITE}/#professional",
        "name": "Vera Fernandes",
        "alternateName": [
            "Vera Fernandes - Neuropsicóloga | Braga, Barcelos, Guimarães e Porto",
            "Dra. Vera Fernandes",
        ],
        "jobTitle": "Neuropsicóloga",
        "image": f"{SITE}/assets/images/vera1.webp",
        "url": f"{SITE}/",
        "telephone": "+351914166181",
        "email": "vfernandes.psi@gmail.com",
        "description": "Neuropsicóloga em Portugal (não confundir com profissionais homónimas noutros países). Membro Efectivo da Ordem dos Psicólogos Portugueses n.º 21502, com Especialidade Avançada em Neuropsicologia. Avaliação neuropsicológica e estimulação cognitiva para adultos e idosos em Braga, Barcelos, Guimarães e Porto.",
        "knowsLanguage": "pt-PT",
        "identifier": {
            "@type": "PropertyValue",
            "name": "Cédula OPP",
            "value": "21502",
        },
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Especialidade Avançada em Neuropsicologia",
            "recognizedBy": {
                "@type": "Organization",
                "name": "Ordem dos Psicólogos Portugueses",
            },
        },
        "sameAs": [
            "https://www.facebook.com/verafernandes.psi/",
            "https://www.instagram.com/verafernandes.psi",
            "https://www.linkedin.com/in/vera-fernandes/",
            "https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0",
            "https://www.cnscampus.com/pt",
        ],
        "areaServed": [
            {"@type": "City", "name": "Braga"},
            {"@type": "City", "name": "Barcelos"},
            {"@type": "City", "name": "Guimarães"},
            {"@type": "City", "name": "Porto"},
        ],
    }


def jsonld(url, name, crumbs, faqs=None):
    graph = [
        professional_graph(),
        {
            "@type": "WebSite",
            "@id": f"{SITE}/#website",
            "url": f"{SITE}/",
            "name": "Vera Fernandes - Neuropsicóloga | Braga, Barcelos, Guimarães e Porto",
            "inLanguage": "pt-PT",
            "publisher": {"@id": f"{SITE}/#professional"},
        },
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": name,
            "isPartOf": {"@id": f"{SITE}/#website"},
            "about": {"@id": f"{SITE}/#professional"},
            "inLanguage": "pt-PT",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": n, "item": u}
                for i, (n, u) in enumerate(crumbs, 1)
            ],
        },
    ]
    if faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faqs
                ],
            }
        )
    return json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        indent=2,
    )


def page(path, title, description, canonical, crumbs, body, faqs=None):
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
        <div class="button" style="margin-top:30px;text-align:center;">
            <a href="/marcar/" class="btn" data-track="marcar"><i class="lni lni-calendar"></i> Marcar avaliação</a>
            <a href="{WA}" class="btn btn-alt" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>
        </div>
    </div>
</section>'''
    html = f'''<!DOCTYPE html>
<html class="no-js page-inner" lang="pt-pt">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-PXV8NTKC6D"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-PXV8NTKC6D');
    </script>
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
{jsonld(canonical, title, crumbs, faqs)}
    </script>
    <link rel="shortcut icon" type="image/x-icon" href="/assets/images/favicon.ico" />
    <link rel="stylesheet" href="/assets/css/animate.css">
    <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
    <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/tiny-slider.css">
    <link rel="stylesheet" href="/assets/css/funnel.css">
</head>
<div class="preloader"><div class="preloader-inner"><div class="preloader-icon"><span></span><span></span></div></div></div>
<script type="text/javascript" src="https://cookieconsent.popupsmart.com/src/js/popper.js"></script>
<script> window.start.init({{ Palette: "palette2", Theme: "edgeless", Mode: "banner bottom", Message: "Este website utiliza cookies para melhorar a sua experiência. Concorda? ", ButtonText: "Aceita", LinkText: "Saber Mais", Location: "https://verafernandes.com/privacy/", Time: "0", }})</script>
<header class="header navbar-area sticky">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-12">
                <div class="nav-inner">
                    <nav class="navbar navbar-expand-lg">
                        <a class="navbar-brand" href="/" target="_self">
                            <img draggable="false" src="/assets/images/logo/logo.svg" alt="Vera Fernandes, neuropsicóloga">
                        </a>
                        <button class="navbar-toggler mobile-menu-btn" type="button" data-bs-toggle="collapse"
                            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                            aria-expanded="false" aria-label="Toggle navigation">
                            <span class="toggler-icon"></span><span class="toggler-icon"></span><span class="toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse sub-menu-bar" id="navbarSupportedContent">
                            <ul id="nav" class="navbar-nav ms-auto">
                                <li class="nav-item"><a href="/#inicio">Início</a></li>
                                <li class="nav-item"><a href="/#consultas">Consultas</a></li>
                                <li class="nav-item"><a href="/#localizacao">Localizações</a></li>
                                <li class="nav-item"><a href="/#faq">FAQ</a></li>
                            </ul>
                        </div>
                        <div class="button add-list-button">
                            <a href="/marcar/" class="btn" data-track="marcar" data-track-location="nav">Marcar avaliação</a>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    </div>
</header>
{body}
{faq_block}
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
    <a href="/marcar/" data-track="marcar" data-track-location="mobile-bar">Marcar avaliação</a>
    <a class="cta-secondary" href="{WA}" data-track="whatsapp" data-track-location="mobile-bar" rel="noopener">Tenho uma dúvida</a>
</div>
<script src="/assets/js/bootstrap.min.js"></script>
<script src="/assets/js/wow.min.js"></script>
<script src="/assets/js/tiny-slider.js"></script>
<script src="/assets/js/count-up.min.js"></script>
<script src="/assets/js/main.js"></script>
<script src="/assets/js/site-data.js"></script>
<script src="/assets/js/funnel.js"></script>
</body>
</html>
'''
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def section(title, kicker, html, hid="inicio"):
    k = f"<h3>{kicker}</h3>" if kicker else ""
    return f'''
<section id="{hid}" class="section page-content">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="section-title">
                    {k}
                    <h1>{title}</h1>
                </div>
            </div>
        </div>
        {html}
    </div>
</section>'''


def cta():
    return f'''
        <div class="button" style="margin:24px 0;">
            <a href="/marcar/" class="btn" data-track="marcar"><i class="lni lni-calendar"></i> Marcar avaliação</a>
            <a href="{WA}" class="btn btn-alt" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a>
        </div>'''


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
    body = section(
        f"Avaliação neuropsicológica em {label}",
        "Localização",
        f"""
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>Vera Fernandes, neuropsicóloga (OPP 21502), realiza avaliação neuropsicológica em {label} para adultos e idosos. O exame caracteriza o funcionamento cognitivo e inclui relatório entregue até 4 dias úteis. O valor depende do local e é confirmado na marcação.</p>
                {cta()}
            </div>
        </div>
        <div class="localizacao">
        <div class="row">{cards}</div>
        </div>
        <div class="row" style="margin-top:24px;">
            <div class="col-lg-8 offset-lg-2">
                <p>Também disponível em <a href="/avaliacao-neuropsicologica/braga/">Braga</a>, <a href="/avaliacao-neuropsicologica/barcelos/">Barcelos</a>, <a href="/avaliacao-neuropsicologica/guimaraes/">Guimarães</a> e <a href="/avaliacao-neuropsicologica/porto/">Porto</a>.</p>
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
        COMMON_FAQS
        + [
            (
                f"Onde marcar em {label}?",
                f"Os locais e horários em {label} estão nesta página. A marcação faz-se pelo telefone do local ou em /marcar/.",
            )
        ],
    )


def problem_page(slug, title, h1, lead, when, solution, extra_faq):
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
                <p>Vera Fernandes é neuropsicóloga em Portugal, OPP 21502, com avaliação em Braga, Barcelos, Guimarães e Porto. Não se trata da profissional homónima noutros países.</p>
                {cta()}
                <p><a href="/avaliacao-neuropsicologica/">Saber o que inclui a avaliação</a> · <a href="/#triagem">Perceber se esta avaliação é indicada</a></p>
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
    )


def main():
    avaliacao_faqs = COMMON_FAQS + [
        (
            "O que acontece no dia?",
            "Entrevista clínica, aplicação dos testes com o paciente, interpretação posterior e relatório até 4 dias úteis, com orientação dos próximos passos.",
        ),
        (
            "Posso ir acompanhado?",
            "É aconselhável ir acompanhado na primeira parte. Não ter acompanhante não impede a avaliação.",
        ),
    ]
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
            <p>A avaliação neuropsicológica é um exame complementar de diagnóstico. Caracteriza o estado cognitivo, comportamental e emocional com testes validados para a população portuguesa.</p>
            <h2>Para quem é</h2>
            <p>Adultos e idosos (18+) com queixas de memória, atenção ou linguagem; pessoas com diagnóstico neurológico; familiares que observaram alterações; e quem foi encaminhado por um médico.</p>
            <h2>Quando faz sentido</h2>
            <p>Quando há esquecimentos de conversas ou recados recentes, mudanças na expressão ou compreensão, ou maior dificuldade em gerir medicação, cozinhar ou conduzir. Também para acompanhar alterações ao longo do tempo.</p>
            <h2>O que acontece no dia</h2>
            <ul class="table-list">
                <li><i2 class="lni lni-checkmark-circle"></i2> Entrevista: conhecer as dificuldades e o contexto clínico.</li>
                <li><i2 class="lni lni-checkmark-circle"></i2> Avaliação: aplicação dos testes neuropsicológicos com o paciente.</li>
                <li><i2 class="lni lni-checkmark-circle"></i2> Análise: interpretação dos resultados.</li>
                <li><i2 class="lni lni-checkmark-circle"></i2> Relatório: entrega até 4 dias úteis, por e-mail, presencialmente ou CTT.</li>
                <li><i2 class="lni lni-checkmark-circle"></i2> Próximos passos: orientação de acordo com os resultados.</li>
            </ul>
            <h2>O que o relatório descreve</h2>
            <p>Como está a memória, a atenção, a linguagem e o raciocínio; se as alterações estão dentro do esperado para a idade e escolaridade; e que áreas podem precisar de acompanhamento. Não substitui o diagnóstico médico.</p>
            <h2>O que está incluído</h2>
            <p>Entrevista clínica, avaliação das funções cognitivas, interpretação, relatório e orientação dos próximos passos. Duração de cerca de 2 horas, numa única deslocação. O valor depende do local e é indicado na marcação.</p>
            <h2>Onde realizar</h2>
            <p><a href="/avaliacao-neuropsicologica/braga/">Braga</a>, <a href="/avaliacao-neuropsicologica/barcelos/">Barcelos</a>, <a href="/avaliacao-neuropsicologica/guimaraes/">Guimarães</a> e <a href="/avaliacao-neuropsicologica/porto/">Porto</a>.</p>
            {cta()}
        </div></div>""",
        ),
        avaliacao_faqs,
    )

    page(
        "estimulacao-cognitiva",
        "Estimulação Cognitiva | Vera Fernandes",
        "Consulta de estimulação cognitiva de 50 a 60 minutos, com plano individual, no Hospital Lusíadas Braga.",
        f"{SITE}/estimulacao-cognitiva/",
        [
            ("Início", f"{SITE}/"),
            ("Estimulação cognitiva", f"{SITE}/estimulacao-cognitiva/"),
        ],
        section(
            "Estimulação cognitiva",
            "Acompanhamento",
            f"""
        <div class="row"><div class="col-lg-8 offset-lg-2">
            <p>A estimulação cognitiva consiste em actividades destinadas a trabalhar o desempenho cognitivo, de modo geral ou em domínios específicos, em pessoas saudáveis ou com défices.</p>
            <p>Indicada para favorecer memória, atenção e linguagem; auxiliar pessoas com demência a gerir dificuldades no dia-a-dia; e apoiar a recuperação após AVC ou traumatismo cranioencefálico, quando clinicamente adequado.</p>
            <p>Duração de 50 a 60 minutos, com plano individual. A frequência é definida em conjunto. Actualmente está indicada no Hospital Lusíadas Braga.</p>
            <p>Na maior parte das situações, o primeiro passo é uma <a href="/avaliacao-neuropsicologica/">avaliação neuropsicológica</a>, para conhecer o perfil cognitivo antes de planear o acompanhamento.</p>
            {cta()}
        </div></div>""",
        ),
        [
            (
                "Onde está disponível?",
                "A consulta de estimulação cognitiva está indicada no Hospital Lusíadas Braga.",
            ),
            (
                "Preciso de avaliação primeiro?",
                "Muitas vezes sim, para definir objectivos. Pode esclarecer na marcação.",
            ),
        ],
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
        <div class="row align-items-center">
            <div class="col-lg-5"><img draggable="false" src="/assets/images/vera1.webp" alt="Vera Fernandes, neuropsicóloga em Portugal"></div>
            <div class="col-lg-7">
                <p>Vera Fernandes é neuropsicóloga em Portugal, Membro Efectivo da Ordem dos Psicólogos Portugueses n.º 21502, com Especialidade Avançada em Neuropsicologia. Não se trata de profissionais homónimas noutros países, incluindo resultados de pesquisa no Brasil.</p>
                <p>Experiência clínica em contexto hospitalar e em clínica privada, incluindo avaliação neuropsicológica no Hospital de Braga e colaboração com CNS - Campus Neurológico Braga e Hospital Lusíadas Braga.</p>
                <p>Contributo para a investigação acerca da doença de Alzheimer enquanto membro de equipa de vários ensaios clínicos.</p>
                <p>Dados actualizados em 2026: +10 anos de experiência; &gt;4800 avaliações; &gt;38 casos de reabilitação; &gt;10 ensaios clínicos.</p>
                <p>Atende adultos e idosos em Braga, Barcelos, Guimarães e Porto. Não está disponível o agendamento para menores de 18 anos.</p>
                <p><a href="https://www.linkedin.com/in/vera-fernandes/" rel="noopener">Perfil LinkedIn</a> · <a href="https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0" rel="noopener">Perfil Lusíadas</a></p>
                {cta()}
            </div>
        </div>""",
        ),
        [
            (
                "Qual é a cédula profissional?",
                "Membro Efectivo da Ordem dos Psicólogos Portugueses n.º 21502.",
            ),
            (
                "É a mesma pessoa que aparece no Lusíadas e no CNS?",
                "Sim. Os perfis institucionais em Portugal correspondem a esta profissional.",
            ),
        ],
    )

    cards = "".join(venue_card(v, booking=True) for v in VENUES)
    page(
        "marcar",
        "Marcar avaliação neuropsicológica | Vera Fernandes",
        "Escolha a cidade e o serviço para marcar avaliação neuropsicológica ou estimulação cognitiva em Braga, Barcelos, Guimarães e Porto.",
        f"{SITE}/marcar/",
        [("Início", f"{SITE}/"), ("Marcar", f"{SITE}/marcar/")],
        section(
            "Marcar avaliação",
            "Agendamento",
            f'''
        <div class="booking-step">
            <h3>Onde pretende realizar?</h3>
            <div class="city-chips">
                <button type="button" class="city-chip" data-book-city="braga">Braga</button>
                <button type="button" class="city-chip" data-book-city="barcelos">Barcelos</button>
                <button type="button" class="city-chip" data-book-city="guimaraes">Guimarães</button>
                <button type="button" class="city-chip" data-book-city="porto">Porto</button>
            </div>
        </div>
        <div class="booking-step">
            <h3>Qual o serviço?</h3>
            <div class="city-chips">
                <button type="button" class="city-chip is-active" data-book-service="avaliacao">Avaliação neuropsicológica</button>
                <button type="button" class="city-chip" data-book-service="estimulacao">Estimulação cognitiva</button>
            </div>
            <p>A estimulação cognitiva está indicada no Hospital Lusíadas Braga. O valor depende do local e é indicado na marcação.</p>
        </div>
        <div id="booking-venues" class="booking-venues localizacao">
            <div class="row">{cards}</div>
        </div>
        <p id="booking-empty" hidden>A estimulação cognitiva está indicada no Hospital Lusíadas Braga. Escolha Braga para ver esse local, ou seleccione avaliação neuropsicológica para os outros concelhos.</p>
        <p>Se ainda tem dúvidas, use <a href="{WA}" data-track="whatsapp" rel="noopener">Tenho uma dúvida</a> (WhatsApp).</p>''',
        ),
        COMMON_FAQS,
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
            )
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
            )
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
            )
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
            )
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
            )
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
            )
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
    )

    urls = [
        f"{SITE}/",
        f"{SITE}/avaliacao-neuropsicologica/",
        f"{SITE}/avaliacao-neuropsicologica/braga/",
        f"{SITE}/avaliacao-neuropsicologica/barcelos/",
        f"{SITE}/avaliacao-neuropsicologica/guimaraes/",
        f"{SITE}/avaliacao-neuropsicologica/porto/",
        f"{SITE}/estimulacao-cognitiva/",
        f"{SITE}/familiares/",
        f"{SITE}/sobre/",
        f"{SITE}/marcar/",
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
