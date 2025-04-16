import pandas as pd
import numpy as np

def categorizar_para_df(lista):
    # Vê qual o maior número de subdivisões
    max_n_virgulas = 0
    for item in lista:
        n_virgulas = item.count(",")
        if n_virgulas > max_n_virgulas:
            max_n_virgulas = n_virgulas

    # Criar um DataFrame vazio com x colunas
    colunas = [f'Nível {i+1}' for i in range(max_n_virgulas+1)]
    df = pd.DataFrame(columns=colunas)

    for item in lista:
        # Divide e limpa os nomes dos órgãos
        partes = [p.strip() for p in item.split(',')]
        partes = [parte[3:] if parte[0:3] in ["na ", "no ", "da ", "do "] else parte for parte in partes]

        while len(partes) < max_n_virgulas+1:
            partes.insert(0, np.nan)

        # Adicionar uma linha de dados (exemplo com valores)
        nova_linha = partes[::-1]
        df.loc[len(df)] = nova_linha

    return df

# Chamada da função
lista = ["coordenadoria x, subsecretaria y, da secretaria z", "coordenadoria x, subsecretaria y, da secretaria z",
         "subsecretaria a, da secretaria z", "diretoria b, subsecretaria a, da secretaria z"]

df = categorizar_para_df(lista)
print(df)