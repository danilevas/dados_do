# Extração de Dados de Nomeações dos Diários Oficiais do Estado do Rio de Janeiro

## Visão Geral

Este repositório apresenta uma forma de extrair dados sobre as nomeações dos diários oficiais do Estado do RJ e estruturá-los, utilizando Python, com as bibliotecas BeautifulSoup, Selenium, Pandas, entre outras. Ele também fornece uma forma de visualizar análises sobre os dados dos D.O.s de 7 a 11 de Abril de 2025, feitas utilizando Streamlit e Plotly.

## Requisitos

Antes de executar o código, certifique-se de ter instalado:

- Python (>= 3.x)
- Pip
- As bibliotecas necessárias (siga os passos abaixo)

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/danilevas/desafio-junior-data-scientist.git
   cd desafio-junior-data-scientist
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Extração dos HTMLs e Estruturação dos Dados

Meu código para essa parte está no arquivo `scraping.py`. Para rodá-lo, execute o seguinte comando:

   ```bash
   python scraping.py
   ```

Rodar o código gera alguns CSVs:
* `csvs/dados.csv` contém os dados estruturados
* a pasta `csvs/agregados/` contém CSVs com dados agregados, usados de base para gerar as visualizações

## Visualizações

As visualizações foram feitas com Streamlit e Plotly. Para rodar localmente o código, execute o seguinte comando:

   ```bash
   streamlit run visualizacoes.py
   ```

---

**Daniel Adler Levacov**