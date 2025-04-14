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

# Função 5: salvar os dados em CSV
def salvar_em_csv(nomeacoes, cargos, simbolos, lotacoes, nome_arquivo="dados.csv"):
    df = pd.DataFrame({"Nome": nomeacoes, "Cargo": cargos, "Símbolo": simbolos, "Lotação": lotacoes})
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    return df

# Função principal (executa tudo)
def executar_fluxo_completo(url):
    html = obter_html(url)
    salvar_html(html)
    nomes, cargos, simbolos, lotacoes = extrair_dados(html)
    df = salvar_em_csv(nomes, cargos, simbolos, lotacoes)
    return df

def procurar_no_html_salvo():
    with open("diario_oficial.html", encoding="utf-8") as f:
        html_salvo = f.read()
    nomes, cargos, simbolos, lotacoes = extrair_dados(html_salvo)
    df = salvar_em_csv(nomes, cargos, simbolos, lotacoes)
    return df

urls = ["https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VWtSQ1JsRlZUa1JPUkUxMFRVUkdSVTFUTURCT2FrNUhURlJvUlUwd1JYUlJhMDE1VG1wQmVWRlVRa1ZOZWxVeQ==",
        "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg==",
        "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VW1wWk1rOUZTa2ROVkdkMFVWUktSbEZUTURCUmVrRTFURlZKZVUwd1NYUlJhbGsxVWxSVmVFMHdUVEJTYW1oRA=="]


# df_nomes = procurar_no_html_salvo()
df_nomes = executar_fluxo_completo(urls[0])