import streamlit as st
import pandas as pd
import plotly.express as px

# Dados de exemplo
data = {
    'Categoria': ['Frutas', 'Frutas', 'Frutas', 'Legumes', 'Legumes', 'Verduras'],
    'Item': ['Maçã', 'Banana', 'Laranja', 'Cenoura', 'Batata', 'Alface'],
    'Valor': [100, 80, 60, 50, 90, 40]
}

df = pd.DataFrame(data)

# Adiciona uma coluna "Raiz" só para forçar a hierarquia completa
df['Raiz'] = ''  # string vazia para nome do nó raiz

# Treemap
fig = px.treemap(
    df,
    path=['Raiz', 'Categoria', 'Item'],
    values='Valor',
    color='Categoria',
    color_discrete_map={
        'Frutas': 'lightblue',
        'Legumes': 'orange',
        'Verduras': 'green'
    }
)

# Esconde o nó raiz ajustando o layout manualmente
fig.update_traces(
    tiling=dict(pad=5),
    root_color="white"
)
fig.data[0].textinfo = 'label+value+percent parent'  # opcional, pra personalizar os labels

# Renderiza no Streamlit
st.plotly_chart(fig, use_container_width=True)
