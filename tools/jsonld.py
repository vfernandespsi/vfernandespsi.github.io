"""Centralized Schema.org JSON-LD graph for verafernandes.com.

Optimized for search engines and commercial LLM recommendation: explicit identity,
credentials, geography, services, venues, booking actions, and page-level context.
"""

from __future__ import annotations

import json
from typing import Any

SITE = "https://verafernandes.com"
PHONE = "+351914166181"
EMAIL = "vfernandes.psi@gmail.com"
WHATSAPP = "https://api.whatsapp.com/send?phone=351914166181"
BOOKING = f"{SITE}/agendar/"
BOOKING_SONO = f"{SITE}/agendar/?servico=sono"
CNS_PROFILE = "https://www.cnscampus.com/equipa/vera-fernandes/"

SAME_AS = [
    "https://www.linkedin.com/in/vera-fernandes/",
    "https://www.facebook.com/verafernandes.psi/",
    "https://www.instagram.com/verafernandes.psi",
    "https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0",
    CNS_PROFILE,
]

KNOWS_ABOUT = [
    "Neuropsicologia",
    "Avaliação Neuropsicológica",
    "Estimulação Cognitiva",
    "Reabilitação Neuropsicológica",
    "Psicologia do sono",
    "Doença de Alzheimer",
    "Doença de Parkinson",
    "Défice Cognitivo Ligeiro",
    "Esclerose Múltipla",
    "Demência",
    "Acidente Vascular Cerebral",
    "Traumatismo Cranioencefálico",
    "Memória e envelhecimento",
    "Epilepsia",
]

AREA_SERVED = [
    {
        "@type": "City",
        "name": "Braga",
        "containedInPlace": {"@type": "Country", "name": "Portugal"},
    },
    {
        "@type": "City",
        "name": "Barcelos",
        "containedInPlace": {"@type": "Country", "name": "Portugal"},
    },
    {
        "@type": "City",
        "name": "Guimarães",
        "containedInPlace": {"@type": "Country", "name": "Portugal"},
    },
    {
        "@type": "City",
        "name": "Porto",
        "containedInPlace": {"@type": "Country", "name": "Portugal"},
    },
]

DAY_MAP = {
    "Segunda-feira": "Monday",
    "Terça-feira": "Tuesday",
    "Quarta-feira": "Wednesday",
    "Quinta-feira": "Thursday",
    "Sexta-feira": "Friday",
    "Sábado": "Saturday",
    "Domingo": "Sunday",
}

VENUES = [
    {
        "id": "cns-braga",
        "name": "CNS - Campus Neurológico Braga",
        "city": "Braga",
        "day": "Quarta-feira",
        "opens": "15:30",
        "closes": "19:30",
        "tel": "+351253401600",
        "url": CNS_PROFILE,
        "services": ["avaliacao"],
    },
    {
        "id": "lusiadas-braga",
        "name": "Hospital Lusíadas Braga",
        "city": "Braga",
        "day": "Sexta-feira",
        "opens": "14:00",
        "closes": "18:00",
        "tel": "+351253079579",
        "url": "https://www.lusiadas.pt/corpo-clinico/dra-vera-fernandes-0",
        "services": ["avaliacao", "estimulacao"],
    },
    {
        "id": "consultorio-braga",
        "name": "Consultório Médico - Braga",
        "city": "Braga",
        "day": "Segunda-feira",
        "opens": "17:30",
        "closes": "19:30",
        "tel": PHONE,
        "url": None,
        "services": ["avaliacao"],
    },
    {
        "id": "fisiomove-barcelos",
        "name": "Clínica FisioMove - Barcelos",
        "city": "Barcelos",
        "day": "Segunda-feira",
        "opens": "17:30",
        "closes": "19:30",
        "tel": PHONE,
        "url": None,
        "services": ["avaliacao"],
    },
    {
        "id": "muralha-guimaraes",
        "name": "Gabinete Muralha Business - Guimarães",
        "city": "Guimarães",
        "day": "Quinta-feira",
        "opens": "10:00",
        "closes": "12:00",
        "tel": PHONE,
        "url": None,
        "services": ["avaliacao"],
    },
    {
        "id": "gabinete-porto",
        "name": "Gabinete Psicologia - Porto",
        "city": "Porto",
        "day": "Sábado",
        "opens": "09:00",
        "closes": "13:00",
        "tel": PHONE,
        "url": None,
        "services": ["avaliacao"],
    },
]

SERVICES = {
    "avaliacao": {
        "@id": f"{SITE}/avaliacao-neuropsicologica/#service",
        "@type": "MedicalTest",
        "name": "Avaliação Neuropsicológica",
        "alternateName": ["Avaliação cognitiva", "Exame neuropsicológico"],
        "url": f"{SITE}/avaliacao-neuropsicologica/",
        "description": (
            "Exame complementar de diagnóstico para caracterizar memória, atenção, linguagem "
            "e outras funções cognitivas. Duração de cerca de 2 horas, numa única deslocação. "
            "Inclui relatório entregue até 4 dias úteis. Para adultos e idosos (18+). "
            "Presencial em Braga, Barcelos, Guimarães e Porto."
        ),
        "audience": {
            "@type": "PeopleAudience",
            "suggestedMinAge": 18,
            "audienceType": "Adultos e idosos com queixas cognitivas ou pedido médico",
            "geographicArea": {"@type": "Country", "name": "Portugal"},
        },
        "provider": {"@id": f"{SITE}/#professional"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceType": "InPerson",
            "serviceLocation": [
                {"@id": f"{SITE}/#{v['id']}"}
                for v in VENUES
                if "avaliacao" in v["services"]
            ],
        },
    },
    "estimulacao": {
        "@id": f"{SITE}/estimulacao-cognitiva/#service",
        "@type": "TherapeuticProcedure",
        "name": "Estimulação Cognitiva",
        "url": f"{SITE}/estimulacao-cognitiva/",
        "description": (
            "Sessões de 50 a 60 minutos com plano individual para trabalhar memória, atenção e linguagem. "
            "Actualmente indicada no Hospital Lusíadas Braga."
        ),
        "audience": {
            "@type": "PeopleAudience",
            "suggestedMinAge": 18,
            "geographicArea": {"@type": "Country", "name": "Portugal"},
        },
        "provider": {"@id": f"{SITE}/#professional"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceType": "InPerson",
            "serviceLocation": {"@id": f"{SITE}/#lusiadas-braga"},
        },
    },
    "sono": {
        "@id": f"{SITE}/psicologia-do-sono/#service",
        "@type": "Service",
        "name": "Consulta de psicologia do sono",
        "alternateName": [
            "Psicologia do sono",
            "Terapia cognitivo-comportamental do sono",
        ],
        "url": f"{SITE}/psicologia-do-sono/",
        "description": (
            "Consulta de psicologia do sono online para adultos (18+). "
            "Não é laboratório do sono nem substitui avaliação médica quando há sinais de alarme."
        ),
        "audience": {
            "@type": "PeopleAudience",
            "suggestedMinAge": 18,
            "audienceType": "Adultos com dificuldades de sono",
            "geographicArea": {"@type": "Country", "name": "Portugal"},
        },
        "provider": {"@id": f"{SITE}/#professional"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceType": "Online",
            "serviceUrl": BOOKING_SONO,
        },
    },
}

CONDITIONS = {
    "memoria-e-envelhecimento": {
        "name": "Memória e envelhecimento",
        "alternateName": "Queixas de memória na terceira idade",
        "description": "Caracterização de esquecimentos que podem ou não fazer parte do envelhecimento esperado.",
    },
    "demencia": {
        "name": "Demência",
        "alternateName": "Suspeita de demência",
        "description": "Avaliação complementar do perfil cognitivo quando há suspeita de demência.",
    },
    "alzheimer": {
        "name": "Doença de Alzheimer",
        "description": "Caracterização cognitiva como exame complementar na doença de Alzheimer.",
    },
    "avc": {
        "name": "Acidente Vascular Cerebral",
        "alternateName": "AVC",
        "description": "Avaliação neuropsicológica após AVC para caracterizar alterações cognitivas.",
    },
    "parkinson": {
        "name": "Doença de Parkinson",
        "description": "Caracterização cognitiva complementar na doença de Parkinson.",
    },
    "lesao-cerebral": {
        "name": "Lesão cerebral adquirida",
        "alternateName": "Traumatismo cranioencefálico",
        "description": "Avaliação após TCE ou outra lesão cerebral adquirida.",
    },
}


def _venue_node(v: dict[str, Any]) -> dict[str, Any]:
    node: dict[str, Any] = {
        "@type": ["LocalBusiness", "MedicalClinic"],
        "@id": f"{SITE}/#{v['id']}",
        "name": v["name"],
        "telephone": v["tel"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": v["city"],
            "addressRegion": "Norte",
            "addressCountry": "PT",
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": DAY_MAP[v["day"]],
            "opens": v["opens"],
            "closes": v["closes"],
        },
        "areaServed": {"@type": "City", "name": v["city"]},
        "provider": {"@id": f"{SITE}/#professional"},
    }
    if v["url"]:
        node["url"] = v["url"]
    return node


def organization_node() -> dict[str, Any]:
    return {
        "@type": "Organization",
        "@id": f"{SITE}/#opp",
        "name": "Ordem dos Psicólogos Portugueses",
        "alternateName": "OPP",
        "url": "https://www.ordemdospsicologos.pt/",
        "areaServed": {"@type": "Country", "name": "Portugal"},
    }


def professional_node(*, include_locations: bool = True) -> dict[str, Any]:
    node: dict[str, Any] = {
        "@type": ["Person", "Physician"],
        "@id": f"{SITE}/#professional",
        "name": "Vera Fernandes",
        "alternateName": [
            "Vera Fernandes - Neuropsicóloga | Braga, Barcelos, Guimarães e Porto",
            "Dra. Vera Fernandes",
        ],
        "honorificPrefix": "Dra.",
        "jobTitle": "Neuropsicóloga",
        "image": f"{SITE}/assets/images/vera1.webp",
        "url": f"{SITE}/",
        "telephone": PHONE,
        "email": EMAIL,
        "description": (
            "Neuropsicóloga em Portugal (não confundir com profissionais homónimas noutros países, "
            "incluindo Brasil). Membro Efectivo da Ordem dos Psicólogos Portugueses n.º 21502, "
            "com Especialidade Avançada em Neuropsicologia. Mais de 10 anos de experiência clínica. "
            "Avaliação neuropsicológica e estimulação cognitiva presencial em Braga, Barcelos, "
            "Guimarães e Porto. Consulta de psicologia do sono online (18+)."
        ),
        "disambiguatingDescription": (
            "Profissional de saúde em Portugal, OPP 21502. Não é a neuropsicóloga homónima "
            "listada em plataformas de outros países."
        ),
        "nationality": {"@type": "Country", "name": "Portugal"},
        "homeLocation": {"@type": "Country", "name": "Portugal"},
        "knowsLanguage": ["pt-PT"],
        "medicalSpecialty": ["Neuropsychology", "https://schema.org/Psychiatric"],
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "OPP",
            "name": "Cédula Ordem dos Psicólogos Portugueses",
            "value": "21502",
        },
        "hasCredential": [
            {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "Membro Efectivo",
                "recognizedBy": {"@id": f"{SITE}/#opp"},
            },
            {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "Especialidade Avançada em Neuropsicologia",
                "recognizedBy": {"@id": f"{SITE}/#opp"},
            },
        ],
        "memberOf": {"@id": f"{SITE}/#opp"},
        "worksFor": [
            {"@id": f"{SITE}/#cns-braga"},
            {"@id": f"{SITE}/#lusiadas-braga"},
        ],
        "knowsAbout": KNOWS_ABOUT,
        "sameAs": SAME_AS,
        "areaServed": AREA_SERVED,
        "contactPoint": {"@id": f"{SITE}/#contact"},
        "availableService": [
            {"@id": SERVICES["avaliacao"]["@id"]},
            {"@id": SERVICES["estimulacao"]["@id"]},
            {"@id": SERVICES["sono"]["@id"]},
        ],
        "makesOffer": [
            {
                "@type": "Offer",
                "name": "Avaliação neuropsicológica presencial",
                "url": BOOKING,
                "itemOffered": {"@id": SERVICES["avaliacao"]["@id"]},
                "areaServed": ["Braga", "Barcelos", "Guimarães", "Porto"],
                "eligibleCustomerType": "Adultos e idosos (18+)",
                "availability": "https://schema.org/InStock",
            },
            {
                "@type": "Offer",
                "name": "Estimulação cognitiva",
                "url": BOOKING,
                "itemOffered": {"@id": SERVICES["estimulacao"]["@id"]},
                "areaServed": "Braga",
                "availability": "https://schema.org/InStock",
            },
            {
                "@type": "Offer",
                "name": "Consulta de psicologia do sono online",
                "url": BOOKING_SONO,
                "itemOffered": {"@id": SERVICES["sono"]["@id"]},
                "areaServed": "Portugal",
                "eligibleCustomerType": "Adultos (18+)",
                "availability": "https://schema.org/InStock",
            },
        ],
    }
    if include_locations:
        node["location"] = [{"@id": f"{SITE}/#{v['id']}"} for v in VENUES]
    return node


def contact_node() -> dict[str, Any]:
    return {
        "@type": "ContactPoint",
        "@id": f"{SITE}/#contact",
        "contactType": "customer service",
        "telephone": PHONE,
        "email": EMAIL,
        "url": WHATSAPP,
        "availableLanguage": "pt-PT",
        "areaServed": "PT",
    }


def website_node() -> dict[str, Any]:
    return {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": "Vera Fernandes - Neuropsicóloga | Braga, Barcelos, Guimarães e Porto",
        "description": (
            "Avaliação neuropsicológica presencial no Norte de Portugal e consulta de "
            "psicologia do sono online. Vera Fernandes, OPP 21502."
        ),
        "inLanguage": "pt-PT",
        "publisher": {"@id": f"{SITE}/#professional"},
        "about": {"@id": f"{SITE}/#professional"},
        "potentialAction": [
            {
                "@type": "ReserveAction",
                "name": "Marcar consulta",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": BOOKING,
                    "actionPlatform": [
                        "https://schema.org/DesktopWebPlatform",
                        "https://schema.org/MobileWebPlatform",
                    ],
                },
            },
            {
                "@type": "CommunicateAction",
                "name": "Contactar por WhatsApp",
                "target": WHATSAPP,
            },
        ],
    }


def webpage_node(
    url: str,
    name: str,
    *,
    description: str | None = None,
    page_type: str = "WebPage",
    about: str | None = None,
    main_entity: str | None = None,
    speakable: list[str] | None = None,
) -> dict[str, Any]:
    node: dict[str, Any] = {
        "@type": page_type,
        "@id": f"{url}#webpage",
        "url": url,
        "name": name,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "inLanguage": "pt-PT",
        "author": {"@id": f"{SITE}/#professional"},
    }
    if description:
        node["description"] = description
    if about:
        node["about"] = {"@id": about}
    else:
        node["about"] = {"@id": f"{SITE}/#professional"}
    if main_entity:
        node["mainEntity"] = {"@id": main_entity}
    if speakable:
        node["speakable"] = {
            "@type": "SpeakableSpecification",
            "cssSelector": speakable,
        }
    return node


def breadcrumb_node(crumbs: list[tuple[str, str]], page_url: str) -> dict[str, Any]:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": u}
            for i, (n, u) in enumerate(crumbs, 1)
        ],
    }


def faq_node(faqs: list[tuple[str, str]], page_url: str) -> dict[str, Any]:
    return {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def condition_node(slug: str) -> dict[str, Any]:
    c = CONDITIONS[slug]
    node: dict[str, Any] = {
        "@type": "MedicalCondition",
        "@id": f"{SITE}/{slug}/#condition",
        "name": c["name"],
        "description": c["description"],
        "url": f"{SITE}/{slug}/",
    }
    if "alternateName" in c:
        node["alternateName"] = c["alternateName"]
    return node


def build_graph(
    url: str,
    name: str,
    crumbs: list[tuple[str, str]],
    *,
    description: str | None = None,
    faqs: list[tuple[str, str]] | None = None,
    condition_slug: str | None = None,
    service_key: str | None = None,
    city: str | None = None,
    page_kind: str = "default",
    include_core: bool = True,
) -> str:
    """Assemble a page-specific @graph and return formatted JSON-LD."""
    graph: list[dict[str, Any]] = []

    if include_core:
        graph.append(organization_node())
        graph.append(professional_node(include_locations=page_kind != "city"))
        graph.extend(_venue_node(v) for v in VENUES)
        graph.append(contact_node())
        graph.extend(SERVICES[k].copy() for k in ("avaliacao", "estimulacao", "sono"))
        graph.append(website_node())

    page_type = (
        "MedicalWebPage" if condition_slug or service_key == "avaliacao" else "WebPage"
    )
    about_id = f"{SITE}/#professional"
    main_entity = None

    if condition_slug and condition_slug in CONDITIONS:
        cond = condition_node(condition_slug)
        graph.append(cond)
        about_id = cond["@id"]
        main_entity = cond["@id"]

    if service_key and service_key in SERVICES:
        main_entity = SERVICES[service_key]["@id"]

    if city:
        city_venues = [v for v in VENUES if v["city"].lower() == city.lower()]
        if city_venues:
            main_entity = f"{SITE}/#{city_venues[0]['id']}"

    graph.append(
        webpage_node(
            url,
            name,
            description=description,
            page_type=page_type,
            about=about_id,
            main_entity=main_entity,
        )
    )
    graph.append(breadcrumb_node(crumbs, url))

    if faqs:
        graph.append(faq_node(faqs, url))

    if page_kind == "home":
        graph.append(
            {
                "@type": "ItemList",
                "@id": f"{SITE}/#services",
                "name": "Serviços de Vera Fernandes",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Avaliação neuropsicológica",
                        "url": f"{SITE}/neuropsicologia/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Consulta de psicologia do sono",
                        "url": f"{SITE}/psicologia-do-sono/",
                    },
                ],
            }
        )

    if page_kind == "booking":
        graph.append(
            {
                "@type": "ReservationPage",
                "@id": f"{url}#reservation",
                "url": url,
                "name": name,
                "provider": {"@id": f"{SITE}/#professional"},
                "potentialAction": {
                    "@type": "ReserveAction",
                    "target": BOOKING,
                },
            }
        )

    return json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        indent=2,
    )


def build_home_graph() -> str:
    return build_graph(
        f"{SITE}/",
        "Vera Fernandes | Neuropsicologia e psicologia do sono",
        [("Início", f"{SITE}/")],
        description=(
            "Neuropsicóloga em Portugal, OPP 21502. Avaliação neuropsicológica presencial "
            "em Braga, Barcelos, Guimarães e Porto. Consulta de psicologia do sono online (18+)."
        ),
        page_kind="home",
    )


def build_neuro_hub_graph(faqs: list[tuple[str, str]]) -> str:
    return build_graph(
        f"{SITE}/neuropsicologia/",
        "Avaliação Neuropsicológica em Braga e Porto | Vera Fernandes",
        [
            ("Início", f"{SITE}/"),
            ("Neuropsicologia", f"{SITE}/neuropsicologia/"),
        ],
        description=(
            "Avaliação neuropsicológica para adultos e idosos em Braga, Barcelos, Guimarães e Porto. "
            "Exame cognitivo, relatório incluído. Vera Fernandes, OPP 21502."
        ),
        faqs=faqs,
        service_key="avaliacao",
        page_kind="neuro",
    )
