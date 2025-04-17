import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# Configuração da página
st.set_page_config(page_title="Dados Nomeações RJ", page_icon=":brain:", layout="wide")

# Paleta de cores frio-quente
calor = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#e63946"]
azuis = ["#29807B", "#276367", "#264653"]
cor_divisorias = "#264653"

st.markdown(
    """
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <h1 style="text-align: center; font-size: 45px; color: #264653; font-family: 'Montserrat', sans-serif;">
        Visualizações de Dados de Nomeações do Poder Executivo<br>do Estado do Rio de Janeiro
    </h1>
    <h2 style="text-align: center; font-size: 30px; color: #264653; font-family: 'Montserrat', sans-serif;">
        entre os dias 07 e 11 de Abril de 2025
    </h2>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <hr style="border: 2px solid {cor_divisorias}; margin: 40px 0;">
    """, 
    unsafe_allow_html=True
)

st.subheader("Os dados a seguir foram extraídos do portal da Imprensa Oficial do Estado do Rio de Janeiro com uso de Web Scraping")
st.write("---")

df1 = pd.read_csv('csvs/agregados/nomeacoes_por_dia.csv')

fig1 = px.bar(df1,
             x='Data DO',
             y='Quantidade Nomeações',
             title="<span style='font-size:24px; font-weight: 600;'>Nomeações do Poder Executivo do Estado do Rio de Janeiro por dia</span>", 
             labels={'Data DO': 'Data do Diário Oficial', 'Quantidade Nomeações': 'Quantidade de Nomeações'},
             color='Quantidade Nomeações',
             color_continuous_scale=azuis,
             text="Quantidade Nomeações")

# Ajustes para aumentar o tamanho dos valores
fig1.update_traces(
    textfont=dict(size=22),
    textposition='inside',
    insidetextanchor='end',
    hovertemplate='<b>Data do Diário Oficial:</b> %{x}<br>' +
                  '<b>Quantidade de Nomeações:</b> %{y}<br>' +
                  '<extra></extra>'
)

fig1.update_layout(
    hoverlabel=dict(
        font_size=16  # Aumenta a fonte do tooltip
    ),
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickvals=df1['Data DO'],  # As labels
        tickfont=dict(size=18)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    showlegend=False
)

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=False)

# Carregar os dados do CSV 
df2 = pd.read_csv('csvs/agregados/nomeacoes_por_cargo.csv')

# Invertendo a ordem dos dados e pegando o Top 10
df2 = df2.sort_values(by='Quantidade Nomeações', ascending=True).tail(10)

fig2 = px.bar(df2, 
             y='Cargo',
             x='Quantidade Nomeações', 
             title="<span style='font-size:24px; font-weight: 600;'>Cargos com mais nomeações</span>", 
             labels={'Cargo': 'Cargo', 'Quantidade Nomeações': 'Quantidade de Nomeações'},
             color='Quantidade Nomeações', 
             color_continuous_scale=azuis,
             orientation='h',
             text=df2['Quantidade Nomeações'].apply(lambda x: f"{x}  ")) # Formatar os rótulos para que não fiquem tão perto da borda direita da barra

# Ajustes do tooltip
fig2.update_traces(
    textfont=dict(size=16),  
    textposition='inside',
    insidetextanchor='end',
    hovertemplate='<b>Cargo:</b> %{y}<br>' +
                  '<b>Quantidade de Nomeações:</b> %{x}<br>' +
                  '<extra></extra>'
)

fig2.update_layout(
    hoverlabel=dict(
        font_size=16  # Aumenta a fonte do tooltip
    ),
    height=600,
    width=800,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',
        tickfont=dict(size=18)
    ),
    yaxis=dict(
        showgrid=True,
        tickmode='array',
        tickfont=dict(size=18)
    ),
    autosize=True,
)

with c2:
    st.plotly_chart(fig2, use_container_width=False)

# Carregar os dados do CSV 
df3 = pd.read_csv('csvs/agregados/nomeacoes_por_simbolo.csv')

# Criar o treemap
fig3 = px.treemap(
    df3,
    path=['Símbolo'],  # Hierarquia
    values='Quantidade Nomeações',
    color='Quantidade Nomeações',
    labels={'Símbolo': 'Símbolo do Cargo', 'Quantidade Nomeações': 'Quantidade de Nomeações'},
    color_continuous_scale=azuis,
    title="<span style='font-size:24px; font-weight: 600;'>Símbolos de Cargo com mais nomeações</span>",
)

# Ajustar tooltip e aparência
fig3.update_traces(
    hovertemplate='<b>Símbolo do Cargo:</b> %{label}<br>' +
                  '<b>Quantidade de Nomeações:</b> %{value}<extra></extra>',
    textinfo='label+value',
    textfont=dict(size=16),
    root_color="white"
)

fig3.update_layout(
    hoverlabel=dict(font_size=16),
    height=600,
    # width=800,
    margin=dict(t=50, b=50, l=50, r=50),
    autosize=True
)

st.plotly_chart(fig3, use_container_width=False)

def funcao(valor):
    match = re.search("Secretaria de Estado", valor)
    if not match:
        match = re.search("Subsecretaria", valor)
    
    if match:
        valor = valor[:match.end()] + "<br>" + valor[match.end():]
    return valor

# Carregar os dados
df4 = pd.read_csv('csvs/agregados/hierarquia_macro.csv')

# Invertendo a ordem dos dados e pegando o Top 10
df4 = df4.sort_values(by='Quantidade Nomeações', ascending=True).tail(10)

fig4 = px.bar(df4, 
             y='Nível 1',
             x='Quantidade Nomeações', 
             title="<span style='font-size:24px; font-weight: 600;'>Órgãos Macro com mais nomeações</span>", 
             labels={'Nível 1': 'Nível 1', 'Quantidade Nomeações': 'Quantidade de Nomeações'},
             color='Quantidade Nomeações', 
             color_continuous_scale=azuis,
             orientation='h',
             text=df4['Quantidade Nomeações'].apply(lambda x: f"{x}  ")) # Formatar os rótulos para que não fiquem tão perto da borda direita da barra

# Ajustes do tooltip
fig4.update_traces(
    textfont=dict(size=16),  
    textposition='inside',
    insidetextanchor='end',
    hovertemplate='<b>Divisão Macro:</b> %{y}<br>' +
                  '<b>Quantidade de Nomeações:</b> %{x}<br>' +
                  '<extra></extra>'
)

fig4.update_layout(
    hoverlabel=dict(
        font_size=16  # Aumenta a fonte do tooltip
    ),
    height=600,
    # width=800,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',
        tickfont=dict(size=18)
    ),
    yaxis=dict(
        showgrid=True,
        tickmode='array',
        tickfont=dict(size=18)
        ),
    autosize=True,
)

st.plotly_chart(fig4, use_container_width=False)

st.markdown("""
    <p style="font-size: 18px;">
        Aqui define-se órgão macro como o órgão de maior nível citado na parte de lotação da nomeação da pessoa. Por exemplo, quando consta no D.O.:
        \"NOMEAR FULANO DE TAL para exercer o cargo [...] da Subsecretaria de Gestão de Pessoas, da Secretaria de Estado da Casa Civil\",
        o órgão macro é a Secretaria de Estado da Casa Civil.
    </p>
""", unsafe_allow_html=True)

st.write("---")