"""Regenerate the full static site from Python sources.

Run from the repository root:

    python tools/render_site.py

Build steps (alteram ficheiros do site):
  1. render_pages.py   — páginas internas + sitemap.xml
  2. patch_jsonld.py   — JSON-LD em index.html e neuropsicologia/
  3. patch_consent.py  — cookies nas páginas manuais
  4. validate_jsonld.py — valida JSON-LD (falha se inválido)

Referência (não altera o site):
  5. campaign_urls.py — lista URLs com UTM para Instagram / Google Ads

Ao criar nova tool que gera ou patcha HTML, acrescentar a BUILD_STEPS.
Tools só de referência ou validação: BUILD_STEPS ou POST_STEPS, conforme o caso.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

BUILD_STEPS = [
    ("Páginas internas + sitemap", "render_pages"),
    ("JSON-LD (index + neuropsicologia)", "patch_jsonld"),
    ("Cookies (páginas manuais)", "patch_consent"),
    ("Validar JSON-LD", "validate_jsonld"),
]

POST_STEPS = [
    ("URLs de campanha (copiar para anúncios)", "campaign_urls"),
]


def _run_step(label: str, module_name: str) -> None:
    print(f"\n=== {label} ===")
    module = __import__(module_name)
    module.main()


def main() -> None:
    sys.path.insert(0, str(TOOLS))

    for label, module_name in BUILD_STEPS:
        _run_step(label, module_name)

    print("\nSite gerado. Pronto para commit.")

    for label, module_name in POST_STEPS:
        _run_step(label, module_name)


if __name__ == "__main__":
    main()
