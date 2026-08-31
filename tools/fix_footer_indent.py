"""Fix over-indented LRE footer links."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LRE = (
    '<li><a href="https://www.livroreclamacoes.pt/" target="_blank" rel="noopener">'
    '<img draggable="false" src="/assets/images/misc/livroreclamacoes.png" '
    'alt="Livro de Reclamações Electrónico"></a></li>'
)


def main() -> None:
    fixed = 0
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        out = []
        changed = False
        for index, line in enumerate(lines):
            if LRE in line and line.lstrip().startswith("<li><a href"):
                for prev in reversed(lines[:index]):
                    if any(
                        token in prev
                        for token in (
                            "Cookies",
                            "informacao-regulatoria",
                            "Política de Privacidade",
                        )
                    ):
                        indent = re.match(r"^(\s*)", prev).group(1)
                        line = indent + LRE
                        changed = True
                        break
            out.append(line)
        if changed:
            newline = "\n" if text.endswith("\n") else ""
            path.write_text("\n".join(out) + newline, encoding="utf-8")
            fixed += 1
    print(f"Fixed indent in {fixed} files")


if __name__ == "__main__":
    main()
