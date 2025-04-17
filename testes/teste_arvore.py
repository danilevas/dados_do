import streamlit as st
import pandas as pd

# Carrega o CSV
df = pd.read_csv("csvs/agregados/hierarquia.csv")

# Ordena pelo Nível 1, depois Nível 2 e 3, mas ordenando pela Quantidade Nomeações dentro de cada nível
df_sorted = df.sort_values(by=['Nível 1', 'Nível 2', 'Nível 3', 'Quantidade Nomeações'], ascending=[True, True, True, False])

# Exibe a hierarquia de forma estruturada no Streamlit
st.write("Estrutura hierárquica das Nomeações (ordenada pela quantidade de nomeações):")

# Variáveis para controle de exibição
nivel_1_atual = None
nivel_2_atual = None

for _, row in df_sorted.iterrows():
    nivel_1 = row['Nível 1']
    nivel_2 = row['Nível 2'] if row['Nível 2'] != '-' else 'Não especificado'
    nivel_3 = row['Nível 3'] if row['Nível 3'] != '-' else 'Não especificado'
    quantidade = row['Quantidade Nomeações']
    
    # Se o nível 1 mudou, exibe ele em destaque
    if nivel_1 != nivel_1_atual:
        st.subheader(nivel_1)  # Exibe o Nível 1 em subheader (maior)
        nivel_1_atual = nivel_1
    
    # Se o nível 2 mudou dentro do Nível 1, exibe ele em título menor
    if nivel_2 != nivel_2_atual:
        st.markdown(f"### {nivel_2}")  # Exibe o Nível 2 em título menor
        nivel_2_atual = nivel_2
    
    # Exibe o Nível 3 com a quantidade de nomeações
    st.markdown(f"#### {nivel_3}: {quantidade} nomeações")  # Exibe o Nível 3 em título ainda menor
