"""Patch cookie consent into manually maintained HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

from consent_snippets import CONSENT_BANNER, CONSENT_HEAD

ROOT = Path(__file__).resolve().parents[1]

MANUAL_PAGES = [
    "index.html",
    "neuropsicologia/index.html",
    "privacy/index.html",
    "tos/index.html",
    "colaboracao/index.html",
    "satisfacao/index.html",
]

GTAG_BLOCK = re.compile(
    r"\s*<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-PXV8NTKC6D\"></script>\s*"
    r"<script>.*?</script>\s*",
    re.DOTALL,
)

POPUPSMART_BLOCK = re.compile(
    r"\s*<script type=\"text/javascript\" src=\"https://cookieconsent\.popupsmart\.com/src/js/popper\.js\"></script>\s*"
    r"(?:<script>\s*window\.start\.init\(\{.*?\}\)</script>\s*)?",
    re.DOTALL,
)

BANNER_BLOCK = re.compile(
    r"<div id=\"vf-consent\" class=\"vf-consent\".*?</div>\s*"
    r"(?:<!-- /vf-consent -->\s*)?"
    r"(?:</div>\s*){0,5}",
    re.DOTALL,
)

HEAD_CONSENT_SCRIPT = re.compile(
    r"\s*<script src=\"/assets/js/consent\.js(?:\?v=\d+)?\"(?: defer)?></script>\s*",
)


def ensure_consent_script(text: str) -> str:
    text = HEAD_CONSENT_SCRIPT.sub("\n", text)
    script_tag = CONSENT_HEAD.strip()
    if "consent.js" in text:
        return re.sub(
            r"<script src=\"/assets/js/consent\.js(?:\?v=\d+)?\"(?: defer)?></script>",
            script_tag,
            text,
            count=1,
        )
    if '<script src="/assets/js/funnel.js"></script>' in text:
        return text.replace(
            '<script src="/assets/js/funnel.js"></script>',
            f'{script_tag}\n<script src="/assets/js/funnel.js"></script>',
            1,
        )
    if '<script src="/assets/js/main.js"></script>' in text:
        return text.replace(
            '<script src="/assets/js/main.js"></script>',
            f'{script_tag}\n<script src="/assets/js/main.js"></script>',
            1,
        )
    if "</body>" in text:
        return text.replace("</body>", f"{script_tag}\n</body>", 1)
    return text


def ensure_consent_css(text: str) -> str:
    if "consent.css" in text:
        return text
    if "funnel.css" in text:
        return text.replace(
            '<link rel="stylesheet" href="/assets/css/funnel.css">',
            '<link rel="stylesheet" href="/assets/css/funnel.css">\n  <link rel="stylesheet" href="/assets/css/consent.css">',
            1,
        )
    if "</head>" in text:
        return text.replace(
            "</head>",
            '  <link rel="stylesheet" href="/assets/css/consent.css">\n</head>',
            1,
        )
    return text


def ensure_banner(text: str) -> str:
    if BANNER_BLOCK.search(text):
        text = BANNER_BLOCK.sub(CONSENT_BANNER.strip(), text, count=1)
    elif 'id="vf-consent"' not in text:
        if "<body>" in text:
            text = text.replace("<body>", f"<body>\n{CONSENT_BANNER}", 1)
        elif '<div class="preloader">' in text:
            preloader_end = text.find("<!--End Preloader -->")
            if preloader_end != -1:
                insert_at = preloader_end + len("<!--End Preloader -->")
                text = text[:insert_at] + CONSENT_BANNER + text[insert_at:]
            else:
                text = text.replace(
                    '<div class="preloader">',
                    CONSENT_BANNER + '<div class="preloader">',
                    1,
                )
    text = re.sub(r"(<!-- /vf-consent -->\s*){2,}", "<!-- /vf-consent -->\n", text)
    return text


def ensure_footer_link(text: str) -> str:
    if "data-vf-open-consent" in text:
        return text
    needle = '<a href="/privacy/" target="_self">Política de Privacidade</a>'
    if needle in text:
        return text.replace(
            needle,
            needle
            + '</li>\n                    <li><a href="#" data-vf-open-consent>Cookies</a>',
            1,
        )
    return text


def patch(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = GTAG_BLOCK.sub("\n", text)
    text = POPUPSMART_BLOCK.sub("\n", text)
    text = ensure_consent_css(text)
    text = ensure_banner(text)
    text = ensure_consent_script(text)
    text = ensure_footer_link(text)
    path.write_text(text, encoding="utf-8")
    print("patched", path.relative_to(ROOT))


def main() -> None:
    for rel in MANUAL_PAGES:
        patch(ROOT / rel)


if __name__ == "__main__":
    main()
