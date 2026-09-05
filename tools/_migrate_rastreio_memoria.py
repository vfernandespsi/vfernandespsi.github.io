from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "rastreiomemoria" / "index.html"
dst_dir = ROOT / "rastreio-memoria"
dst_dir.mkdir(exist_ok=True)

text = src.read_text(encoding="utf-8")
text = text.replace(
    "https://verafernandes.com/rastreiomemoria/",
    "https://verafernandes.com/rastreio-memoria/",
)
text = text.replace("/rastreiomemoria/", "/rastreio-memoria/")
text = text.replace(
    "\n            <!-- Rastreio sono: a adicionar numa fase posterior -->"
    '\n            <div id="rastreio-sono" hidden></div>\n',
    "\n",
)
(dst_dir / "index.html").write_text(text, encoding="utf-8")
assert "rastreiomemoria" not in text
assert "rastreio-memoria" in text
print("wrote", dst_dir / "index.html")
