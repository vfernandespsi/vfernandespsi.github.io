"""Patch static HTML pages with performance and accessibility head/social fixes."""

from __future__ import annotations

import re
from pathlib import Path

from consent_snippets import HEAD_LCP_PRELOAD, HEAD_STYLES

ROOT = Path(__file__).resolve().parents[1]

OLD_HEAD_VARIANTS = [
    """  <link rel="stylesheet" href="/assets/css/animate.css">
  <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
  <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css">
  <link rel="stylesheet" href="/assets/css/main.css">
  <link rel="stylesheet" href="/assets/css/funnel.css">
  <link rel="stylesheet" href="/assets/css/consent.css">""",
    """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
  <link rel="stylesheet" href="/assets/css/bootstrap.min.css">
  <link rel="stylesheet" href="/assets/css/LineIcons.2.0.css">
  <link rel="stylesheet" href="/assets/css/main.css">
  <link rel="stylesheet" href="/assets/css/funnel.css">
  <link rel="stylesheet" href="/assets/css/consent.css">
  <link rel="stylesheet" href="/assets/css/animate.css" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="/assets/css/animate.css"></noscript>""",
]

SOCIAL_REPLACEMENTS = [
    (
        r'<a href="https://www\.facebook\.com/verafernandes\.psi/"><i class="lni lni-facebook-filled"></i></a>',
        '<a href="https://www.facebook.com/verafernandes.psi/" aria-label="Facebook"><i class="lni lni-facebook-filled"></i></a>',
    ),
    (
        r'<a href="https://www\.instagram\.com/verafernandes\.psi"><i class="lni lni-instagram"></i></a>',
        '<a href="https://www.instagram.com/verafernandes.psi" aria-label="Instagram"><i class="lni lni-instagram"></i></a>',
    ),
    (
        r'<a href="https://www\.linkedin\.com/in/vera-fernandes/"><i class="lni lni-linkedin-original"></i></a>',
        '<a href="https://www.linkedin.com/in/vera-fernandes/" aria-label="LinkedIn"><i class="lni lni-linkedin-original"></i></a>',
    ),
    (
        r'<a href="mailto:vfernandes\.psi@gmail\.com"><i class="lni lni-envelope"></i></a>',
        '<a href="mailto:vfernandes.psi@gmail.com" aria-label="Enviar email"><i class="lni lni-envelope"></i></a>',
    ),
]


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    for old in OLD_HEAD_VARIANTS:
        if old in text:
            replacement = HEAD_STYLES
            if path.name == "index.html" and path.parent == ROOT:
                replacement = HEAD_LCP_PRELOAD + HEAD_STYLES
            text = text.replace(old, replacement, 1)
            break
        old_indent4 = old.replace("  ", "    ")
        if old_indent4 in text:
            replacement = HEAD_STYLES.replace("  ", "    ")
            if path.name == "index.html" and path.parent == ROOT:
                replacement = HEAD_LCP_PRELOAD.replace("  ", "    ") + replacement
            text = text.replace(old_indent4, replacement, 1)
            break

    for pattern, replacement in SOCIAL_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("index.html")):
        if "node_modules" in path.parts:
            continue
        if patch_file(path):
            changed += 1
            print(f"patched {path.relative_to(ROOT)}")
    print(f"done: {changed} files")


if __name__ == "__main__":
    main()
