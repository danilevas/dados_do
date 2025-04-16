def categorizar(orgao_str, estrutura, contador={'valor': 1}):
    partes = [p.strip() for p in orgao_str.split(',')]

    def inserir_recursivamente(partes, dicionario):
        nivel_atual = partes[-1]
        
        if nivel_atual not in dicionario:
            dicionario[nivel_atual] = {
                'nomeações': 1,
                'subordinados': {}
            }
            contador['valor'] += 1
        else:
            dicionario[nivel_atual]['nomeações'] += 1

        if len(partes) > 1:
            inserir_recursivamente(partes[:-1], dicionario[nivel_atual]['subordinados'])

    inserir_recursivamente(partes, estrutura)
    return estrutura

estrutura_geral = {}

estrutura_geral = categorizar("coordenadoria x, subsecretaria y, secretaria z", estrutura_geral)
estrutura_geral = categorizar("coordenadoria x, subsecretaria y, secretaria z", estrutura_geral)
estrutura_geral = categorizar("subsecretaria a, secretaria z", estrutura_geral)
estrutura_geral = categorizar("diretoria b, subsecretaria a, secretaria z", estrutura_geral)

from pprint import pprint
pprint(estrutura_geral)