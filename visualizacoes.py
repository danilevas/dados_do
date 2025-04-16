import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        Visualizações de Dados de Nomeações do Poder Executivo do Estado do Rio de Janeiro
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

st.header("Parte 1: Dados sobre as nomeações")
st.write("---")

df1 = pd.read_csv('csvs/agregados/nomeacoes_por_dia.csv')

fig1 = px.bar(df1,
             x='Data DO',
             y='Quantidade Nomeações',
             title="<span style='font-size:24px; font-weight: 600;'>Nomeações do Poder Executivo do Estado do Rio de Janeiro por dia<br>(entre 7 e 11 de Abril de 2025)</span>", 
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
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    autosize=True,
)

with c2:
    st.plotly_chart(fig2, use_container_width=False)

# Carregar os dados do CSV 
df3 = pd.read_csv('csvs/agregados/nomeacoes_por_lotacao.csv')

# Invertendo a ordem dos dados e pegando o Top 10
df3 = df3.sort_values(by='Quantidade Nomeações', ascending=True).tail(10)

fig3 = px.bar(df3, 
             y='Lotação',
             x='Quantidade Nomeações', 
             title="<span style='font-size:24px; font-weight: 600;'>Lotações com mais nomeações</span>", 
             labels={'Lotação': 'Lotação', 'Quantidade Nomeações': 'Quantidade de Nomeações'},
             color='Quantidade Nomeações', 
             color_continuous_scale=azuis,
             orientation='h',
             text=df3['Quantidade Nomeações'].apply(lambda x: f"{x}  ")) # Formatar os rótulos para que não fiquem tão perto da borda direita da barra

# Ajustes do tooltip
fig3.update_traces(
    textfont=dict(size=16),  
    textposition='inside',
    insidetextanchor='end',
    hovertemplate='<b>Lotação:</b> %{y}<br>' +
                  '<b>Quantidade de Nomeações:</b> %{x}<br>' +
                  '<extra></extra>'
)

fig3.update_layout(
    hoverlabel=dict(
        font_size=16  # Aumenta a fonte do tooltip
    ),
    height=600,
    width=800,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    autosize=True,
)

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig3, use_container_width=False)

# Carregar os dados
df4 = pd.read_csv('csvs/agregados/nomeacoes_por_simbolo.csv')

# Pegar o Top 10
# df4 = df4.sort_values(by='Quantidade Nomeações', ascending=False).head(10)

# Criar o treemap
fig4 = px.treemap(
    df4,
    path=['Símbolo'],  # Hierarquia
    values='Quantidade Nomeações',
    color='Quantidade Nomeações',
    labels={'Símbolo': 'Símbolo do Cargo', 'Quantidade Nomeações': 'Quantidade de Nomeações'},
    color_continuous_scale=azuis,
    title="<span style='font-size:24px; font-weight: 600;'>Símbolos de Cargo com mais nomeações</span>",
)

# Ajustar tooltip e aparência
fig4.update_traces(
    hovertemplate='<b>Símbolo do Cargo:</b> %{label}<br>' +
                  '<b>Quantidade de Nomeações:</b> %{value}<extra></extra>',
    textinfo='label+value',
    textfont=dict(size=16),
    root_color="white"
)

fig4.update_layout(
    hoverlabel=dict(font_size=16),
    height=600,
    width=800,
    margin=dict(t=50, b=50, l=50, r=50),
    autosize=True,
    # plot_bgcolor='rgba(0,0,0,0)',
    # paper_bgcolor='rgba(0,0,0,0)'
)

# fig4.update_traces(root_color="white")

# # Essa linha remove o fundo branco atrás dos blocos
# fig4.update_layout(uniformtext=dict(minsize=12, mode='hide'))

with c2:
    st.plotly_chart(fig4, use_container_width=False)

df5 = pd.DataFrame()

# Gráfico de barra empilhada
fig = px.bar(
    df,
    x='Categoria',
    y='Valor',
    color='Subcategoria',
    title='Barra Empilhada',
    text='Valor'
)

st.plotly_chart(fig, use_container_width=True)

# # Extraindo dados do CSV
# df_relogio = pd.read_csv("csvs/analise_python/1.3_chamados_por_hora_01_04_2023.csv")

# # Criar gráfico polar
# fig_relogio = go.Figure()

# fig_relogio.add_trace(go.Barpolar(
#     r=df_relogio['Chamados Totais'],  # Distância da borda do círculo
#     theta=[h * 15 for h in df_relogio['Hora']],  # Ângulo (15 graus por hora, para cobrir 360°)
#     width=[15] * 24,  # Largura das fatias (15° cada)
#     marker=dict(
#         color=df_relogio['Chamados Totais'], 
#         colorscale=calor,  # Escala de cor baseada na quantidade de chamados
#         cmin=min(df_relogio['Chamados Totais']),
#         cmax=max(df_relogio['Chamados Totais'])
#     ),
#     hoverinfo="theta+r",
#     name="Chamados Totais"
# ))

# # Ajustes do tooltip
# fig_relogio.update_traces(
#     hovertemplate='<b>Hora:</b> %{theta}<br>' +
#                   '<b>Chamados Totais:</b> %{r}<br>' +
#                   '<extra></extra>'
# )

# # Ajustar layout
# fig_relogio.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 65, 'b': 50, 'l': 50, 'r': 50},
#     polar=dict(
#         radialaxis=dict(
#             visible=True,
#             showticklabels=False,
#             ticks="",
#             range=[0, max(df_relogio['Chamados Totais']) * 1.1]  # Para dar espaço extra na borda
#         ),
#         angularaxis=dict(
#             tickmode="array",
#             tickvals=[h * 15 for h in df_relogio['Hora']],
#             ticktext=[f"{h}h" for h in df_relogio['Hora']],
#             direction="clockwise"
#         )
#     ),
#     title="<span style='font-size:24px; font-weight: 600;'>Chamados Totais por Hora do Dia no dia 01/04/2023</span>",
#     title_y=0.959,  # Coloca o título um pouco acima
#     title_yanchor="bottom",  # Alinha o título à parte inferior da posição de y
#     showlegend=False
# )

# c1, c2 = st.columns(2)
# with c1:
#     st.plotly_chart(fig1, use_container_width=False)
# with c2:
#     st.plotly_chart(fig_relogio, use_container_width=False)

# # Carregar os dados dos CSVs
# df2 = pd.read_csv('csvs/analise_sql/3.2_chamados_por_bairro_01_04_2023.csv')
# df3 = pd.read_csv('csvs/analise_sql/4_chamados_por_subprefeitura_01_04_2023.csv')

# st.write("---")
# st.subheader("Capítulo 1.2: Análise do subtipo \"Perturbação do Sossego\" (id_subtipo 5071)")

# df4 = pd.read_csv('csvs/analise_sql/8.2_num_chamados_subtipo_perturb_sossego_por_dia.csv')

# # Convertendo a coluna 'data' para o tipo datetime
# df4['data'] = pd.to_datetime(df4['data'])

# # Agregando os dados por mês
# df_mensal = df4.groupby(pd.Grouper(key='data', freq='ME')).agg({'total_chamados': 'sum'}).reset_index()

# fig4 = px.bar(df_mensal, 
#              x='data',
#              y='total_chamados',
#              title="<span style='font-size:24px; font-weight: 600;'>Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos por mês</span>", 
#              labels={'data': 'Mês', 'total_chamados': 'Chamados Totais'},
#              color='total_chamados', 
#              color_continuous_scale=calor)

# # Ajustes do tooltip
# fig4.update_traces(
#     hovertemplate='<b>Mês:</b> %{x}<br>' +
#                   '<b>Chamados Totais:</b> %{y}<br>' +
#                   '<extra></extra>'
# )

# fig4.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickfont=dict(size=18)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
# )

# st.plotly_chart(fig4, use_container_width=False)

# st.markdown("""
#     <p style="font-size: 18px;">
#         Percebe-se aqui que os chamados com id_subtipo = 5071 (subtipo \"Perturbação do sossego\") começam a aparecer com quantidades escassas
#         em meados de 2013, até que em meados de 2019 eles aumentam significativamente em quantidade. Esse aumento continua, até atingir um pico em Julho de 2022,
#         e depois as quantidades de chamados desse subtipo começam a diminuir até que em Dezembro de 2023 elas caem significativamente. Entre Abril e Agosto de 2024,
#         não há nenhum chamado do subtipo. A partir de Setembro de 2024 eles voltam a quantidades comparáveis ao período Julho de 2019 - Novembro de 2023.
#     </p>
# """, unsafe_allow_html=True)

# st.markdown("""
#     <p style="font-size: 18px; font-weight: 600;">
#         Por isso, não temos chamados desse id_subtipo durante os eventos Réveillon 2023-2024, Carnaval 2024, e Rock in Rio 2024 (parte 1 e 2).
#     </p>
# """, unsafe_allow_html=True)

# st.write("---")
# st.subheader("Capítulo 1.3: Dados sobre os chamados entre 01/01/2022 e 31/12/2024")

# df6 = pd.read_csv('csvs/analise_sql/8.2_num_chamados_subtipo_perturb_sossego_por_dia.csv')

# # Convertendo a coluna 'data' para o tipo datetime
# df6['data'] = pd.to_datetime(df6['data'])

# # Recortando o período que queremos
# df6 = df6[(df6['data'].dt.date.between(pd.to_datetime('2022-01-01').date(), pd.to_datetime('2024-12-31').date()))]

# fig6 = px.bar(df6, 
#              x='data',
#              y='total_chamados',
#              title="<span style='font-size:24px; font-weight: 600;'>Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos por dia entre 2022 e 2024</span>", 
#              labels={'data': 'Dia', 'total_chamados': 'Chamados Totais'},
#              color='total_chamados', 
#              color_continuous_scale=calor)

# # Ajustes do tooltip
# fig6.update_traces(
#     hovertemplate='<b>Dia:</b> %{x}<br>' +
#                   '<b>Chamados Totais:</b> %{y}<br>' +
#                   '<extra></extra>'
# )

# fig6.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickfont=dict(size=18)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
# )

# st.plotly_chart(fig6, use_container_width=False)

# st.write("---")
# st.subheader("Capítulo 1.4: Dados sobre os chamados em grandes eventos")

# cores = {
#     'Carnaval': '#67a03d',
#     'Réveillon': '#264653',
#     'Rock in Rio': '#FFA500'
# }

# df7 = pd.read_csv('csvs/visualizacoes/chamados_eventos.csv')

# fig7 = px.bar(df7, 
#              x='evento',
#              y='total_chamados',
#              title="<span style='font-size:24px; font-weight: 600;'>Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos em grandes eventos</span>", 
#              labels={'evento': 'Evento', 'total_chamados': 'Chamados Totais', 'categoria': 'Categoria'},
#              color='categoria',
#              color_discrete_map=cores,
#              text="total_chamados")

# # Formatação para o tooltip
# x2 = [evento.replace('*', ' ') for evento in df7['evento']]

# # Ajustes do tooltip
# fig7.update_traces(
#     textfont=dict(size=22),  
#     textposition='inside',  
#     insidetextanchor='end',
#     customdata=x2,  # Passando os valores personalizados
#     hovertemplate='<b>Evento:</b> %{customdata}<br>' +
#                   '<b>Chamados Totais:</b> %{y}<br>' +
#                   '<extra></extra>'
# )

# fig7.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickvals=df7['evento'],  # As labels dos eventos
#         ticktext=[evento.replace('*', '<br>') for evento in df7['evento']],  # Quebra de linha entre as palavras do evento
#         tickfont=dict(size=14)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
#     legend=dict(
#         font=dict(
#             size=18
#         )
#     )
# )

# st.plotly_chart(fig7, use_container_width=False)

# fig7_1 = px.bar(df7, 
#              x='evento',
#              y='media_diaria',
#              title="<span style='font-size:24px; font-weight: 600;'>Média de chamados do subtipo \"Perturbação do Sossego\" abertos por dia em grandes eventos</span>", 
#              labels={'evento': 'Evento', 'media_diaria': 'Média de Chamados por Dia', 'categoria': 'Categoria'},
#              color='categoria',
#              color_discrete_map=cores,
#              text='media_diaria')

# # Ajustes do tooltip
# fig7_1.update_traces(
#     textfont=dict(size=22),
#     textposition='inside',
#     insidetextanchor='end',
#     customdata=x2,  # Passando os valores personalizados
#     hovertemplate='<b>Evento:</b> %{customdata}<br>' +
#                   '<b>Média de Chamados por Dia:</b> %{y:.2f}<br>' +
#                   '<extra></extra>'
# )

# fig7_1.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickvals=df7['evento'],  # As labels dos eventos
#         ticktext=[evento.replace('*', '<br>') for evento in df7['evento']],  # Quebra de linha entre as palavras do evento
#         tickfont=dict(size=14)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
#     legend=dict(
#         font=dict(
#             size=18
#         )
#     )
# )

# st.plotly_chart(fig7_1, use_container_width=False)

# df8 = pd.read_csv('csvs/analise_python/7.2_chamados_subtipo_perturb_sossego_dias_de_evento.csv')

# # Garantir que 'data_abertura' está no formato datetime
# df8['data_abertura'] = pd.to_datetime(df8['data_abertura'])

# # Agrupar por 'evento' e 'data_abertura' e contar os chamados
# tabela_resumo = df8.groupby(['evento_id', 'evento', 'data_abertura']).size().reset_index(name='quantidade_chamados')

# # Agrupar por 'evento' e calcular a média de 'quantidade_chamados' por evento
# df8_1 = tabela_resumo.groupby('evento')['quantidade_chamados'].mean().reset_index(name='media_diaria_chamados')

# fig8 = px.bar(df8_1, 
#              x='evento',
#              y='media_diaria_chamados',
#              title="<span style='font-size:24px; font-weight: 600;'>Média de chamados do subtipo \"Perturbação do Sossego\" abertos por dia<br></span>"
#                 "<span style='font-size:24px; font-weight: 600;'>em grandes eventos por categoria de evento<br></span>"
#                 "<span style='font-size:16px; font-weight:normal;'>(entre os dias que tiveram algum chamado do subtipo)</span>",
#              labels={'evento': 'Evento', 'media_diaria_chamados': 'Média de Chamados por Dia'},
#              color='evento',
#              color_discrete_map=cores,
#              text=df8_1['media_diaria_chamados'].apply(lambda x: f"{x:.2f}"))

# # Ajustes do tooltip
# fig8.update_traces(
#     textfont=dict(size=22),
#     textposition='inside',
#     insidetextanchor='end',
#     hovertemplate='<b>Categoria de Evento:</b> %{x}<br>' +
#                   '<b>Média de Chamados por Dia:</b> %{y:.2f}<br>' +
#                   '<extra></extra>'
# )

# fig8.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     width=800,
#     margin={'t': 150, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickvals=df8_1['evento'],  # As labels dos eventos
#         ticktext=[evento.replace('*', '<br>') for evento in df8_1['evento']],  # Quebra de linha entre as palavras do evento
#         tickfont=dict(size=14)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
#     legend=dict(
#         font=dict(
#             size=18
#         )
#     )
# )

# st.plotly_chart(fig8, use_container_width=False)

# st.markdown(
#     f"""
#     <hr style="border: 2px solid {cor_divisorias}; margin: 40px 0;">
#     """, 
#     unsafe_allow_html=True
# )

# st.header("Parte 2: Dados de integração com APIs: Feriados e Tempo")
# st.write("---")
# st.subheader("Capítulo 2.1: Feriados de 2024")

# # Carregar os dados do CSV
# df9 = pd.read_csv('csvs/visualizacoes/feriados_por_mes.csv')

# # Definir as cores baseadas no número de feriados
# color_map = {1: "#29807B", 2: "#276367", 3: "#264653"}

# # Criar uma nova coluna 'Cor' baseada no número de feriados
# df9['Cor'] = df9['Feriados'].apply(lambda x: color_map.get(x, "#264653"))

# # Criar o gráfico de barras
# fig9 = px.bar(df9, 
#              x='Mês',
#              y='Feriados',
#              title="<span style='font-size:24px; font-weight: 600;'>Quantidade de feriados por mês no ano de 2024 no Brasil</span>", 
#              labels={'Mês': 'Mês', 'Feriados': 'Feriados'},
#              color='Cor',
#              color_discrete_map={c: c for c in color_map.values()},  # Mapeando as cores corretamente
#              text='Feriados')

# # Ajustes para aumentar o tamanho dos valores e movê-los para baixo
# fig9.update_traces(
#     textfont=dict(size=22),
#     textposition='inside',  
#     insidetextanchor='end',
#     hovertemplate='<b>Mês:</b> %{x}<br>' +
#                   '<b>Feriados:</b> %{y}<br>' +
#                   '<extra></extra>'
# )

# fig9.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickvals=df9['Mês'],  # As labels dos meses
#         tickfont=dict(size=18)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
#     showlegend=False
# )

# st.plotly_chart(fig9, use_container_width=False)

# c1, c2 = st.columns([1.8, 1.2])

# df9_1 = pd.read_csv('csvs/analise_api/3_feriados_por_dia_semana.csv')

# # Criar uma nova coluna 'Cor' baseada no número de feriados
# df9_1['Cor'] = df9_1['Quantidade'].apply(lambda x: color_map.get(x, "#264653"))

# fig9_1 = px.bar(df9_1, 
#              x='Dia da Semana',
#              y='Quantidade',
#              title="<span style='font-size:24px; font-weight: 600;'>Quantidade de feriados por dia da semana no ano de 2024 no Brasil</span>", 
#              labels={'Dia da Semana': 'Dia da Semana', 'Quantidade': 'Feriados'},
#              color='Cor',
#              color_discrete_map={c: c for c in color_map.values()},  # Mapeando as cores corretamente
#              text='Quantidade')

# # Ajustes para aumentar o tamanho dos valores e movê-los para baixo
# fig9_1.update_traces(
#     textfont=dict(size=22),
#     textposition='inside',
#     insidetextanchor='end',
#     hovertemplate='<b>Dia da Semana:</b> %{x}<br>' +
#                   '<b>Feriados:</b> %{y}<br>' +
#                   '<extra></extra>'
# )

# fig9_1.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     # width=1200,
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickvals=df9_1['Dia da Semana'],  # As labels dos dias da semana
#         tickfont=dict(size=18)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
#     showlegend=False
# )

# # Definir categorias para os feriados
# dias_uteis = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira"]
# fim_de_semana = ["Sábado", "Domingo"]

# df9_1["Categoria"] = df9_1["Dia da Semana"].apply(lambda x: "Dia Útil" if x in dias_uteis else "Fim de Semana")

# df_pizza = df9_1.groupby("Categoria")["Quantidade"].sum().reset_index()

# # Criar gráfico de pizza
# fig_pizza = px.pie(df_pizza, 
#                     names='Categoria', 
#                     values='Quantidade', 
#                     title="<span style='font-size:24px; font-weight: 600;'>Distribuição de feriados entre dias úteis<br>e fins de semana em 2024 no Brasil</span>",
#                     color='Categoria',
#                     color_discrete_map={"Dia Útil": "#264653", "Fim de Semana": "#29807B"},
#                     hole=0.4)

# # Ajustes visuais
# fig_pizza.update_traces(
#     textfont=dict(size=22),
#     hovertemplate='<b>Categoria:</b> %{label}<br>' +
#                   '<b>Feriados:</b> %{value}<br>' +
#                   '<extra></extra>'
# )

# fig_pizza.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     showlegend=True,
#     legend=dict(
#         font=dict(
#             size=18
#         )
#     )
# )

# with c1:
#     st.plotly_chart(fig9_1, use_container_width=False)
# with c2:
#     st.plotly_chart(fig_pizza, use_container_width=False)

# st.write("---")

# st.subheader("Capítulo 2.2: Clima")

# df10 = pd.read_csv('csvs/analise_api/4.2_temperaturas_diarias.csv')

# # Convertendo a coluna 'data' para o tipo datetime
# df10['Dia'] = pd.to_datetime(df10['Dia'])

# fig10 = px.bar(df10,
#              x='Dia',
#              y='Temperatura Média',
#              title="<span style='font-size:24px; font-weight: 600;'>Temperaturas médias diárias entre 01/01/2024 e 01/08/2024 no Rio de Janeiro</span>", 
#              labels={'Dia': 'Dia', 'Temperatura Média': 'Temperatura Média'},
#              color='Temperatura Média', 
#              color_continuous_scale=calor)

# # Ajustes para aumentar o tamanho dos valores e movê-los para baixo
# fig10.update_traces(
#     textfont=dict(size=22),
#     textposition='inside',
#     insidetextanchor='end',
#     hovertemplate='<b>Dia:</b> %{x}<br>' +
#                   '<b>Temperatura Média:</b> %{y:.2f}°C<br>' +
#                   '<extra></extra>'
# )

# fig10.update_layout(
#     hoverlabel=dict(
#         font_size=16  # Aumenta a fonte do tooltip
#     ),
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickfont=dict(size=18)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
#     showlegend=False
# )

# st.plotly_chart(fig10, use_container_width=False)

# st.write("---")