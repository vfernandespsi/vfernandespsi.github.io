"""Add Informação Regulatória and LRE links to site footers."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"node_modules", ".git"}
LRE = (
    '<li><a href="https://www.livroreclamacoes.pt/" target="_blank" rel="noopener">'
    '<img draggable="false" src="/assets/images/misc/livroreclamacoes.png" '
    'alt="Livro de Reclamações Electrónico"></a></li>'
)
REPLACEMENTS = [
    (
        """                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>""",
        """                    <li><a href="/informacao-regulatoria/">Informação Regulatória</a></li>
                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>
                    """
        + "                    "
        + LRE,
    ),
    (
        """                                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>""",
        """                                    <li><a href="/informacao-regulatoria/">Informação Regulatória</a></li>
                                    <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                    <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                    <li><button type="button" class="vf-consent-link" data-vf-open-consent>Cookies</button></li>
                                    """
        + "                                    "
        + LRE,
    ),
    (
        """                                        <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                        <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                        <li><button type="button" class="vf-consent-link"
                                                data-vf-open-consent>Cookies</button></li>""",
        """                                        <li><a href="/informacao-regulatoria/">Informação Regulatória</a></li>
                                        <li><a href="/tos/" target="_self">Termos e Condições</a></li>
                                        <li><a href="/privacy/" target="_self">Política de Privacidade</a></li>
                                        <li><button type="button" class="vf-consent-link"
                                                data-vf-open-consent>Cookies</button></li>
                                        """
        + "                                        "
        + LRE,
    ),
]


def main() -> None:
    updated = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP for part in path.parts):
            continue
        if "informacao-regulatoria" in str(path):
            continue
        text = path.read_text(encoding="utf-8")
        if "informacao-regulatoria" in text:
            continue
        new_text = text
        for old, new in REPLACEMENTS:
            if old in new_text:
                new_text = new_text.replace(old, new, 1)
                break
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated.append(str(path.relative_to(ROOT)))
    print(f"Footers updated: {len(updated)}")
    for name in updated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
