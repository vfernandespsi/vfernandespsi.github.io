"""Validate JSON-LD on key pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html",
    "neuropsicologia/index.html",
    "alzheimer/index.html",
    "marcar/index.html",
    "avaliacao-neuropsicologica/braga/index.html",
    "psicologia-do-sono/index.html",
]


def validate() -> list[str]:
    errors: list[str] = []
    for rel in PAGES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{rel}: file not found")
            continue
        text = path.read_text(encoding="utf-8")
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            text,
            re.DOTALL,
        )
        if not match:
            errors.append(f"{rel}: no JSON-LD block")
            continue
        try:
            data = json.loads(match.group(1))
            nodes = len(data.get("@graph", []))
            print(f"{rel}: {nodes} nodes OK")
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON ({exc})")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print("\nJSON-LD validation failed:")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
