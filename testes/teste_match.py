import re

padrao_nomeacao = r'''
NOMEAR(?:-SE)?                                      # NOMEAR ou NOMEAR-SE
(?:\s*<[^>]+>\s*|\s+|[^A-ZÁ-ÚÂ-ÛÃ-ÕÉ-ÍÓ-ÚÇ<>])+?     # ignora até a primeira palavra em maiúsculas
(?P<nome>                                           # início do grupo 'nome'
    (?:                                             # grupo de nome completo:
        (?:\s*<[^>]+>\s*)*                          # tags opcionais
        [A-ZÁ-ÚÂ-ÛÃ-ÕÉ-ÍÓ-ÚÇ\-]+                    # palavra maiúscula
        (?:\s*<[^>]+>\s*)*                          # tags opcionais entre palavras
        \s+                                         # espaço entre palavras
    )*                                              # zero ou mais repetições
    (?:\s*<[^>]+>\s*)*                              # tags opcionais
    [A-ZÁ-ÚÂ-ÛÃ-ÕÉ-ÍÓ-ÚÇ\-]+                        # última palavra
)
'''

# Exemplos de teste
exemplos = [
    'NOMEAR<asdasdasdasd> validade atéasdas<assads>aasd 30 dias, MARIA DA SILVA',
    'NOMEAR <span>validade: 90 dias,</span> <b>JOÃO</b> <i>PEREIRA</i>',
    'NOMEAR-SE<br><span>até publicação,</span> <strong>JOSÉ</strong> <em>DA</em> <b>SILVA</b>',
    'NOMEAR <div>validei o sistema</div><div>ANA <span>CAROLINA</span> MOURA</div>',
    'NOMEAR <b>validade prorrogada,</b> PAULO <u>HENRIQUE</u> <span>DOS</span> SANTOS',
    'NOMEAR <span style="color:red">não é esse nome</span> <b>RENATO</b> asdasdasds ALMEIDA',
    'NOMEAR <b>JULIANA</b> <script>alert("errado")</script> <b>SILVA</b>',  # para testar caso com script no meio
    'NOMEAR <b>CARLA</b>, será nomeada para o cargo de...'  # deve parar no nome
]

for texto in exemplos:
    match = re.search(padrao_nomeacao, texto, re.VERBOSE)
    if match:
        print(f"✅ Encontrado: {match.group('nome')}")
    else:
        print(f"❌ Nada encontrado em: {texto}")
