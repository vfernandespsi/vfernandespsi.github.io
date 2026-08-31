"""Patch JSON-LD into manually maintained pages."""

from __future__ import annotations

import re
from pathlib import Path

from jsonld import build_home_graph, build_neuro_hub_graph

ROOT = Path(__file__).resolve().parents[1]

NEURO_FAQS = [
    (
        "Quando devo agendar uma avaliação neuropsicológica?",
        "A avaliação neuropsicológica é indicada quando surgem falhas de memória, desatenção, desorientação, alterações de linguagem ou mudanças no comportamento e humor. Se nota impacto na autonomia do dia a dia, é o momento indicado para avaliar. Se tem dúvidas se os esquecimentos são normais do envelhecimento: https://verafernandes.com/memoria-e-envelhecimento/",
    ),
    (
        "Quantas consultas são necessárias e qual a duração?",
        "O processo de avaliação está organizado para uma única deslocação, numa consulta de cerca de 2 horas, com recolha da história clínica e testes neuropsicológicos.",
    ),
    (
        "Preciso de encaminhamento médico para realizar a avaliação?",
        "Não é obrigatório ter prescrição ou encaminhamento médico. Pode agendar por iniciativa própria ou para um familiar.",
    ),
    (
        "Posso ir acompanhado/a à consulta?",
        "Sim, e é recomendado. Um familiar ou alguém próximo pode acompanhar na primeira parte da consulta. A ausência de acompanhante não impede a avaliação.",
    ),
    (
        "Como fico a saber os resultados da avaliação?",
        "Os resultados são apresentados num relatório sem custo adicional, entregue por e-mail, presencialmente ou CTT até 5 dias úteis após a avaliação.",
    ),
    (
        "Posso agendar uma avaliação para o meu pai, mãe ou familiar?",
        "Sim. Um familiar pode agendar a consulta sem que a pessoa reconheça as dificuldades. Informação: https://verafernandes.com/familiares/",
    ),
    (
        "Quando devo agendar a consulta de estimulação cognitiva?",
        "É indicada para manter, otimizar ou reabilitar memória e atenção, na prevenção do envelhecimento cerebral, no DCL ou após AVC.",
    ),
    (
        "Qual é a duração da consulta de estimulação cognitiva?",
        "As consultas têm cerca de 50 minutos. A frequência e o número de consultas definem-se em conjunto com o paciente.",
    ),
    (
        "Atende crianças ou adolescentes (menores de 18 anos)?",
        "Não. As consultas estão disponíveis para adultos e idosos com mais de 18 anos.",
    ),
    (
        "Como posso agendar consulta?",
        "Pode agendar online seleccionando local e serviço, ou contactar por mensagem ou telefone para apoio no agendamento.",
    ),
]

PATTERN = re.compile(
    r'  <script type="application/ld\+json">.*?</script>',
    re.DOTALL,
)


def patch(path: Path, jsonld: str) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = f'  <script type="application/ld+json">\n{jsonld}\n  </script>'
    new_text, n = PATTERN.subn(replacement, text, count=1)
    if n != 1:
        raise SystemExit(f"Failed to patch {path}: {n} replacements")
    path.write_text(new_text, encoding="utf-8")
    print("patched", path.relative_to(ROOT))


def main() -> None:
    patch(ROOT / "index.html", build_home_graph())
    patch(ROOT / "neuropsicologia" / "index.html", build_neuro_hub_graph(NEURO_FAQS))


if __name__ == "__main__":
    main()
