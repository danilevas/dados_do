import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Função 1: configurar e iniciar o driver do Selenium
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Função 2: obter o HTML da página
def obter_html(url):
    driver = iniciar_driver()
    driver.get(url)
    time.sleep(5)  # aguarda carregamento
    html = driver.page_source
    driver.quit()
    return html

# Função 3: salvar o HTML em um arquivo local
def salvar_html(html, nome_arquivo="diario_oficial.html"):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

# Função 4: extrair dados do HTML
def extrair_dados(html):
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(separator=" ", strip=True)
    
    # Encontrar todas as instâncias de "NOMEAR" (ignorando tags)
    padrao_nomeacao = r'NOMEAR(?:-SE)?(?:\s*<[^>]+>\s*)*(?P<nome>[A-ZÁ-ÚÂ-ÛÃ-ÕÉ-ÍÓ-ÚÇ\s\-]+)'
    nomeacoes = []
    cargos = []
    simbolos = []
    
    # Buscando todos os matches do padrão de nomeação
    for match in re.finditer(padrao_nomeacao, html):
        nome = match.group("nome")
        
        # Limpar nome das tags HTML
        nome_limpo = BeautifulSoup(nome, "html.parser").get_text(separator=" ").strip()

        # Encontrar o cargo logo após o nome
        parte_html_1 = html[match.end():]  # Captura tudo após o nome
        cargo_match = re.search(r'cargo(?:[^,]*),', parte_html_1)  # Pega tudo entre "cargo" e a próxima vírgula

        if cargo_match:
            cargo = cargo_match.group(0)
            cargo_limpo = BeautifulSoup(cargo, "html.parser").get_text(separator=" ").strip()
            de = re.search("de", cargo_limpo)
            cargo_limpo = cargo_limpo[de.end():-1].lstrip()
        else:
            cargo_limpo = "Cargo não encontrado"
        
        # Encontrar o símbolo do cargo
        offset_simbolo = match.end() + cargo_match.end()
        parte_html_2 = html[offset_simbolo:]
        simbolo_match = re.search(r'^([^,]+)', parte_html_2) # Pega tudo até a primeira vírgula

        if simbolo_match:
            simbolo = simbolo_match.group(1)  # Agora estamos pegando o texto entre as vírgulas
            simbolo_limpo = BeautifulSoup(simbolo, "html.parser").get_text(separator=" ").strip()
            # simbolo_limpo = simbolo_limpo.strip().rsplit(" ", 1)[-1]
            simbolo_limpo = simbolo_limpo.split("lo ", 1)[-1].replace(" ","")
        else:
            simbolo_limpo = "Símbolo não encontrado"

        nomeacoes.append(nome_limpo)
        cargos.append(cargo_limpo)
        simbolos.append(simbolo_limpo)
    
    return nomeacoes, cargos, simbolos

# Função 5: salvar os dados em CSV
def salvar_em_csv(nomeacoes, cargos, simbolos, nome_arquivo="nomeacoes_cargos.csv"):
    df = pd.DataFrame({"Nome": nomeacoes, "Cargo": cargos, "Símbolo": simbolos})
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    return df

# Função principal (executa tudo)
def executar_fluxo_completo(url):
    html = obter_html(url)
    salvar_html(html)
    nomes, cargos, simbolos = extrair_dados(html)
    df = salvar_em_csv(nomes, cargos, simbolos)
    return df

def procurar_no_html_salvo():
    with open("diario_oficial.html", encoding="utf-8") as f:
        html_salvo = f.read()
    nomes, cargos, simbolos = extrair_dados(html_salvo)
    df = salvar_em_csv(nomes, cargos, simbolos)
    return df

# Exemplo de uso:
url = "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VWtSQ1JsRlZUa1JPUkUxMFRVUkdSVTFUTURCT2FrNUhURlJvUlUwd1JYUlJhMDE1VG1wQmVWRlVRa1ZOZWxVeQ=="
df_nomes = procurar_no_html_salvo()