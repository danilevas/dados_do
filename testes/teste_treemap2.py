import streamlit as st
import pandas as pd
import plotly.express as px

# Dados normais com 3 camadas
data = {
    'Continente': ['América', 'América', 'América', 'Europa', 'Europa', 'Ásia'],
    'País': ['Brasil', 'Brasil', 'EUA', 'França', 'Alemanha', 'Japão'],
    'Cidade': ['Rio de Janeiro', 'São Paulo', 'Nova York', 'Paris', 'Berlim', 'Tóquio'],
    'População': [6.7, 12.3, 8.4, 2.1, 3.6, 13.9]
}

# Pessoas que moram direto no continente (diferenciando nome)
extra_data = {
    'Continente': ['América', 'Ásia'],
    'País': ['América (outros)', 'Ásia (outros)'],  # evita colisão com nó pai
    'Cidade': [None, None],
    'População': [2.0, 1.0]
}

# Junta os dados
df = pd.concat([pd.DataFrame(data), pd.DataFrame(extra_data)], ignore_index=True)

# Treemap
fig = px.treemap(
    df,
    path=['Continente', 'País', 'Cidade'],
    values='População',
    color='Continente',
    color_discrete_map={
        'América': 'lightblue',
        'Europa': 'lightgreen',
        'Ásia': 'salmon'
    }
)

fig.update_traces(root_color="white")
fig.data[0].textinfo = 'label+value+percent parent'

# Streamlit
st.title("Treemap com Pessoas por Continente, País e Cidade")
st.plotly_chart(fig, use_container_width=True)
