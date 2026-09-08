from pathlib import Path

p = Path(__file__).resolve().parents[1] / "privacy" / "index.html"
text = p.read_text(encoding="utf-8")

start = text.index(
    "                            <li><strong>Dados de análise estatística (Google Analytics 4):</strong>"
)
end = text.index("                        <h2>8. Segurança dos dados</h2>")

new_block = """                            <li><strong>Dados de análise estatística:</strong> Conservados de acordo
                                com as definições do Google Analytics ou até à remoção do consentimento
                                pelo
                                utilizador.</li>
                        </ul>

                        <h2>6. Partilha de dados e subcontratantes</h2>
                        <p>Não vendemos, alugamos nem partilhamos dados pessoais recolhidos no
                            website com terceiros para fins comerciais ou de marketing.</p>
                        <p>Os dados poderão ser acedidos apenas por prestadores de serviços de
                            suporte técnico ao website (ex.: alojamento web e, mediante o seu consentimento,
                            Google Analytics), que atuam como subcontratantes ao nosso
                            serviço e sob rigorosas obrigações de confidencialidade e conformidade com o RGPD.</p>

                        <h2>7. Cookies e tecnologias de análise</h2>
                        <p>O website funciona perfeitamente sem cookies não essenciais. Apenas
                            utilizamos cookies opcionais de análise estatística se aceitar expressamente no aviso
                            apresentado na sua primeira visita.</p>
                        <p>Estes <em>cookies</em> correspondem ao <strong>Google Analytics</strong> e ajudam a
                            compreender como o website é utilizado, permitindo otimizar o conteúdo e a experiência de
                            navegação. Não utilizamos estes dados para publicidade direcionada ou definição de perfis.</p>
                        <p>Pode gerir, alterar ou retirar o seu consentimento a qualquer momento
                            através do atalho <button type="button" class="vf-consent-link"
                                data-vf-open-consent><strong><em>Cookies</em></strong></button> no rodapé do website, ou
                            limpando os dados do seu navegador.</p>

"""

p.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
print("updated", p)
