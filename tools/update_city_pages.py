"""Update avaliacao-neuropsicologica city landing pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITIES = {
    "braga": "em Braga",
    "barcelos": "em Barcelos",
    "guimaraes": "em Guimarães",
    "porto": "no Porto",
}

INTRO_P2 = (
    "A avaliação permite perceber como estão a funcionar diferentes capacidades, "
    "como a memória, atenção, linguagem e raciocínio, e se o desempenho está dentro "
    "do esperado para a idade e escolaridade. Inclui relatório, entregue até 5 dias "
    "úteis. O valor depende do local e é confirmado no momento da marcação."
)

CTA = """
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
        <div class="button cta-pair" style="margin:24px 0;">
            <a href="/agendar/" class="btn" data-track="marcar">Agendar</a>
            <a href="https://api.whatsapp.com/send?phone=351914166181&text=Tenho%20uma%20d%C3%BAvida%20sobre%20avalia%C3%A7%C3%A3o%20neuropsicol%C3%B3gica." class="btn btn-alt" data-track="whatsapp" rel="noopener noreferrer">Tenho uma dúvida</a>
        </div>
            </div>
        </div>"""

RELATED = """
                <h2>Tópicos relacionados</h2>
                <ul class="related-list"><li><a href="/avaliacao-neuropsicologica/">Como é feita a avaliação?</a></li><li><a href="/familiares/">Posso agendar para um familiar?</a></li><li><a href="/agendar/">Como posso agendar?</a></li></ul>"""

FAQ_SECTION = re.compile(
    r"\n<section id=\"faq\" class=\"faq section\">.*?</section>\n</main>",
    re.DOTALL,
)

FAQ_JSON = re.compile(r",\s*\{\s*\"@type\": \"FAQPage\".*?\}\s*(?=\]\s*\})", re.DOTALL)

OLD_INTRO_CTA = re.compile(
    r"<div class=\"row\">\s*<div class=\"col-lg-8 offset-lg-2\">\s*"
    r"<p>Vera Fernandes, neuropsicóloga \(OPP 21502\).*?</p>\s*"
    r"<div class=\"button cta-pair\".*?</div>\s*"
    r"</div>\s*</div>",
    re.DOTALL,
)

TAMBEM = re.compile(
    r'(<div class="row" style="margin-top:24px;">\s*)'
    r'<div class="col-lg-8 offset-lg-2">'
)


def intro_block(prep: str) -> str:
    return f"""        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <p>Vera Fernandes, neuropsicóloga clínica (cédula profissional n.º 21502), realiza avaliação neuropsicológica {prep} para adultos e idosos.</p>
                <p>{INTRO_P2}</p>
            </div>
        </div>"""


def main() -> None:
    for slug, prep in CITIES.items():
        path = ROOT / "avaliacao-neuropsicologica" / slug / "index.html"
        text = path.read_text(encoding="utf-8")

        text = FAQ_JSON.sub("", text, count=1)
        text = OLD_INTRO_CTA.sub(intro_block(prep), text, count=1)
        text = TAMBEM.sub(
            r'\1<div class="col-lg-8 offset-lg-2 text-center">', text, count=1
        )

        if CTA.strip() not in text:
            text = text.replace(
                '    </div>\n</section>\n\n<section class="related-questions">',
                CTA + '\n    </div>\n</section>\n\n<section class="related-questions">',
                1,
            )

        text = re.sub(
            r"<h2>Perguntas seguintes</h2>\s*<ul class=\"related-list\">.*?</ul>",
            RELATED.strip(),
            text,
            count=1,
            flags=re.DOTALL,
        )

        text = FAQ_SECTION.sub("\n</main>", text, count=1)
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
