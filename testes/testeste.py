import pandas as pd

# Número de colunas que você deseja (x)
x = 4  # Exemplo: 4 colunas (nível_1, nível_2, etc.)

# Criar um DataFrame vazio com x colunas
colunas = [f'nível_{i+1}' for i in range(x)]  # Gera a lista ['nível_1', 'nível_2', ..., 'nível_x']
df = pd.DataFrame(columns=colunas)

# Adicionar uma linha de dados (exemplo com valores)
nova_linha = ['coordenadoria x', 'subsecretaria y', 'secretaria z', 'diretoria a']
df.loc[len(df)] = nova_linha  # Adiciona a nova linha

# Adicionar outra linha de dados (exemplo com valores diferentes)
nova_linha_2 = ['coordenadoria a', 'subsecretaria b', 'secretaria z', 'diretoria b']
df.loc[len(df)] = nova_linha_2  # Adiciona outra linha

# Exibindo o DataFrame final
print(df)
