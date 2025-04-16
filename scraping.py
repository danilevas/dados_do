import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

# Configurar e iniciar o driver do Selenium
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Rola a página até o final para carregar todo o PDF
def rolar_ate_o_fim(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # espera carregar
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Obter o HTML da página
def obter_html(url):
    driver = iniciar_driver()
    driver.get(url)
    print("\nRolando página para carregar todo conteúdo...")
    rolar_ate_o_fim(driver)
    print("Capturando HTML final")
    html = driver.page_source
    driver.quit()
    return html

# Salvar o HTML em um arquivo local
def salvar_html(html, nome_arquivo=f"diario_oficial.html"):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

# Extrair dados do HTML
def extrair_dados(data, html):
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(separator=" ", strip=True)
    with open(f"txts/texto_html_{data}.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    
    # Encontrar todas as instâncias de "NOMEAR" (ignorando tags)
    padrao_nomeacao = r'NOMEAR(?:-SE)?(?:\s*<[^>]+>\s*)*(?P<nome>[A-ZÁ-ÚÂ-ÛÃ-ÕÉ-ÍÓ-ÚÇ\s\-]+)'
    nomeacoes = []
    cargos = []
    simbolos = []
    lotacoes = []
    
    # Buscando todos os matches do padrão de nomeação
    for match in re.finditer(padrao_nomeacao, html):
        nome = match.group("nome")
        
        # Limpar nome das tags HTML
        nome_limpo = BeautifulSoup(nome, "html.parser").get_text(separator=" ").strip()
        nome_limpo = nome_limpo.replace("  ", " ")

        # Encontrar o cargo logo após o nome
        parte_html_1 = html[match.end():]  # Captura tudo após o nome
        cargo_match = re.search(r'cargo(?:[^,]*),', parte_html_1)  # Pega tudo entre "cargo" e a próxima vírgula

        if cargo_match:
            cargo = cargo_match.group(0)
            cargo_limpo = BeautifulSoup(cargo, "html.parser").get_text(separator=" ").strip()
            de = re.search("de", cargo_limpo)
            cargo_limpo = cargo_limpo[de.end():-1].lstrip()
            cargo_limpo = cargo_limpo.replace("  ", " ")

            # Tirar as instâncias de "- " que é simplesmente uma quebra de linha no meio da palavra,
            # sem tirar as instâncias de " - ", um hífen mesmo
            cargo_limpo = re.sub(r'(?<! )- ', '', cargo_limpo)
        else:
            cargo_limpo = "Cargo não encontrado"
        
        # Encontrar o símbolo do cargo
        offset_simbolo = match.end() + cargo_match.end()
        parte_html_2 = html[offset_simbolo:]
        simbolo_match = re.search(r'^([^,]+)', parte_html_2) # Pega tudo até a primeira vírgula

        if simbolo_match:
            simbolo = simbolo_match.group(1)  # Agora estamos pegando o texto entre as vírgulas
            simbolo_limpo = BeautifulSoup(simbolo, "html.parser").get_text(separator=" ").strip()
            simbolo_limpo = simbolo_limpo.split("lo ", 1)[-1].replace(" ","")
        else:
            simbolo_limpo = "Símbolo não encontrado"

        # Encontrar a lotação (órgão) do cargo
        offset_lotacao = match.end() + cargo_match.end() + simbolo_match.end() + 2
        parte_html_3 = html[offset_lotacao:]
        lotacao_match = re.search(r'^(([^,]+,){2}[^,]+)', parte_html_3) # Pega tudo até a segunda vírgula

        anteriormente_regex = r'a(?:-?\s*)n(?:-?\s*)t(?:-?\s*)e(?:-?\s*)r(?:-?\s*)i(?:-?\s*)o(?:-?\s*)r(?:-?\s*)m(?:-?\s*)e(?:-?\s*)n(?:-?\s*)t(?:-?\s*)e'
        em_vaga_regex = r'e(?:-?\s*)m(?:-?\s*)v(?:-?\s*)a(?:-?\s*)g(?:-?\s*)a'

        if lotacao_match:
            lotacao = lotacao_match.group(1)  # Agora estamos pegando o texto entre as vírgulas
            lotacao_limpo = BeautifulSoup(lotacao, "html.parser").get_text(separator=" ").strip()
            
            # A lotação vai até a palavra "anteriormente" ou "em vaga", vamos pegar o que vem antes disso
            anteriormente = re.search(anteriormente_regex, lotacao_limpo)
            em_vaga = re.search(em_vaga_regex, lotacao_limpo)
            
            if anteriormente:
                lotacao_limpo = lotacao_limpo[:anteriormente.start()]
            elif em_vaga:
                lotacao_limpo = lotacao_limpo[:em_vaga.start()]

            # Procurando pelo "do" ou "da" que sobra no início do texto e pegando só o que vem depois disso
            do = re.search("do", lotacao_limpo)
            da = re.search("da", lotacao_limpo)
            
            if do and da:
                if do.start() < da.start():
                    lotacao_limpo = lotacao_limpo[do.end():]
                else:
                    lotacao_limpo = lotacao_limpo[da.end():]
            elif do:
                lotacao_limpo = lotacao_limpo[do.end():]
            elif da:
                lotacao_limpo = lotacao_limpo[da.end():]

            # Tira espaços e vírgulas do final
            while lotacao_limpo[-1] in [" ", ","]:
                lotacao_limpo = lotacao_limpo[:-1]
            
            # Tirar os espaços no início do texto
            lotacao_limpo = lotacao_limpo.lstrip()

            # Tirar os espaços duplos
            while "  " in lotacao_limpo:
                lotacao_limpo = lotacao_limpo.replace("  ", " ")
            
            # Tirar as instâncias de "- " que é simplesmente uma quebra de linha no meio da palavra,
            # sem tirar as instâncias de " - ", um hífen mesmo
            lotacao_limpo = re.sub(r'(?<! )- ', '', lotacao_limpo)
        
        else:
            lotacao_limpo = "Lotação não encontrada"

        nomeacoes.append(nome_limpo)
        cargos.append(cargo_limpo)
        simbolos.append(simbolo_limpo)
        lotacoes.append(lotacao_limpo)
    
    return nomeacoes, cargos, simbolos, lotacoes

# Salvar os dados em CSV
def salvar_em_csv(data, nomeacoes, cargos, simbolos, lotacoes, nome_arquivo="csvs/dados.csv"):
    lista_data = [data] * len(nomeacoes)
    df_novo = pd.DataFrame({"Data DO": lista_data, "Nome": nomeacoes, "Cargo": cargos, "Símbolo": simbolos, "Lotação": lotacoes})

    try:
        # Tenta carregar um CSV existente
        df_existente = pd.read_csv(nome_arquivo, encoding="utf-8-sig")
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    except FileNotFoundError:
        # Se o arquivo ainda não existir, usa apenas o novo
        df_final = df_novo

    df_final.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    return df_final

# Função principal (executa tudo)
def executar_fluxo_completo(urls):
    # Deleta o arquivo com dados, se existir, para pegarmos dados novos
    if os.path.isfile("csvs/dados.csv"):
        os.remove("csvs/dados.csv")

    # Iterando pelos dias e os URLs com seus DOs
    for data, url in urls.items():
        print(f"\n > Obtendo html do DO do dia {data}")
        html = obter_html(url)
        print(f"Salvando html do DO do dia {data}")
        salvar_html(html, nome_arquivo=f"htmls/diario_oficial_{data}.html")
        print(f"Extraindo dados do DO do dia {data}")
        nomes, cargos, simbolos, lotacoes = extrair_dados(data, html)
        print(f"Salvando o CSV do DO do dia {data}")
        df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes)
    
    return df

# Função principal (executa tudo)
def executar_fluxo_um_dia(urls, data):
    # Deleta o arquivo com dados, se existir, para pegarmos dados novos
    if os.path.isfile(f"csvs/dados_teste_{data}.csv"):
        os.remove(f"csvs/dados_teste_{data}.csv")

    print(f"\n > Obtendo html do DO do dia {data}")
    html = obter_html(urls[data])
    print(f"Salvando html do DO do dia {data}")
    salvar_html(html, nome_arquivo=f"htmls/diario_oficial_{data}_teste.html")
    print(f"Extraindo dados do DO do dia {data}")
    nomes, cargos, simbolos, lotacoes = extrair_dados(data, html)
    print(f"Salvando o CSV do DO do dia {data}")
    df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes, nome_arquivo=f"csvs/dados_teste_{data}.csv")
    return df

def procurar_no_html_salvo(data):
    with open(f"htmls/diario_oficial_{data}.html", encoding="utf-8") as f:
        html_salvo = f.read()
    print(f"Extraindo dados do DO do dia {data}")
    nomes, cargos, simbolos, lotacoes = extrair_dados(data, html_salvo)
    print(f"Salvando o CSV do DO do dia {data}")
    df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes, nome_arquivo=f"csvs/dados_teste_{data}.csv")
    return df

urls = {
    "2025-04-07" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VWtSQ1JsRlZUa1JPUkUxMFRVUkdSVTFUTURCT2FrNUhURlJvUlUwd1JYUlJhMDE1VG1wQmVWRlVRa1ZOZWxVeQ==",
    "2025-04-08" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg==",
    "2025-04-09" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VW1wWk1rOUZTa2ROVkdkMFVWUktSbEZUTURCUmVrRTFURlZKZVUwd1NYUlJhbGsxVWxSVmVFMHdUVEJTYW1oRA==",
    "2025-04-10" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wVmVWRnFaelZTUkVGMFVWUkpNRkY1TURCUk1FcENURlZKZDA1VVRYUlBWVTE1VDBSa1IwMUZVVFZOTUZWMw==",
    "2025-04-11" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VFZSQk5WRnJWVEpSVkd0MFVtcG9SVTFETURCTmVrcEdURlZKTlUxNldYUlJlbGw2VDFST1IwMUVUVEZQVkZWNA=="
}

df = executar_fluxo_um_dia(urls, "2025-04-08")