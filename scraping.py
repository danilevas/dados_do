import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

# Configurar e iniciar o driver do Selenium
def iniciar_driver():
    chrome_options = Options()
    # Remova o comentário abaixo se quiser ver o navegador rodando na sua frente
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def rolar_container(driver, data, passo=1367, intervalo_base=0.2):
    time.sleep(3.6)  # espera a página carregar
    container = driver.find_element(By.ID, "viewerContainer")

    # altura_total = driver.execute_script("return arguments[0].scrollHeight", container)
    altura_total = passo*10
    posicao = 0

    print("📜 Rolando o div#viewerContainer para carregarmos toda a parte do PDF que precisamos...")

    # Vai até a página 10
    mult=10
    while posicao < altura_total:
        driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", container, posicao)
        time.sleep(intervalo_base*mult)
        posicao += passo
        # print(f"Posição: {posicao}/{altura_total} (passo = {passo})")
        # altura_total = driver.execute_script("return arguments[0].scrollHeight", container)
        mult -= 1

    # Volta pra página 1
    posicao = 0
    # print(f"Posição: {posicao}/{altura_total} (passo = {passo})")

    # Vai até a página 9
    altura_total = passo*9
    mult=10
    while posicao < altura_total:
        driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", container, posicao)
        time.sleep(intervalo_base*mult)
        posicao += passo
        # print(f"Posição: {posicao}/{altura_total} (passo = {passo})")
        # altura_total = driver.execute_script("return arguments[0].scrollHeight", container)
        mult -= 1

    print("✅ Rolagem finalizada")

    # Salva todo o HTML visível após rolagem e o retorna
    html = driver.page_source
    with open(f"htmls/diario_oficial_{data}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 HTML salvo como htmls/diario_oficial_{data}.html")
    return html

# Obter o HTML da página
def obter_html(url, data):
    driver = iniciar_driver()
    driver.get(url)
    print("\nRolando página para carregar todo conteúdo...")
    html = rolar_container(driver, data)
    driver.quit()
    return html

# Extrair dados do HTML
def extrair_dados(data, html):
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(separator=" ", strip=True)

    # Salvando txt para fins de checagem
    with open(f"txts/texto_html_{data}.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    
    # Encontrar todas as instâncias de "NOMEAR"
    padrao_nomeacao = r'NOMEAR'
    nomeacoes = []
    cargos = []
    simbolos = []
    lotacoes = []
    
    # Buscando todos os matches do padrão de nomeação
    for match in re.finditer(padrao_nomeacao, html):
        parte_html_nomeacao = html[match.end():]

        eh_tag = False
        estamos_no_nome = False
        nome = ""

        # Reconhecendo onde qual é o primeiro nome depois da palavra "NOMEAR", ignorando tags e possíveis outras palavras em minúscula
        for i in range(len(parte_html_nomeacao)):
            # Para fins de debug
            letra = parte_html_nomeacao[i]
            
            # Início de tag
            if letra == "<":
                eh_tag = True
                continue
            
            # Fim de tag
            elif letra == ">" and eh_tag:
                eh_tag = False
                if estamos_no_nome:
                    nome += " "
                continue
            
            if letra == " ":
                # Espaços que fazem parte do nome
                if estamos_no_nome == True and not eh_tag:
                    nome += letra

            # Letras do nome
            elif letra != "," and not letra.isdigit() and letra.upper() == letra and not eh_tag:
                estamos_no_nome = True
                nome += letra
            
            # Condição de parada
            elif not eh_tag and estamos_no_nome and letra.lower() == letra:
                break
        
        # Tirar as tags HTML do nome
        nome_limpo = BeautifulSoup(nome, "html.parser").get_text(separator=" ").strip()
        while "  " in nome_limpo:
            nome_limpo = nome_limpo.replace("  ", " ")

        # Encontrar o cargo logo após o nome
        parte_html_1 = html[match.end()+i:]  # Captura tudo após o nome
        cargo_match = re.search(r'car-?(?:<[^>]*>)*go(?:[^,]*),', parte_html_1)  # Pega tudo entre "cargo" ou "car- go" e a próxima vírgula, ignorando tags HTML

        if cargo_match:
            cargo = cargo_match.group(0)
            cargo_limpo = BeautifulSoup(cargo, "html.parser").get_text(separator=" ").strip()
            de = re.search("de", cargo_limpo)
            cargo_limpo = cargo_limpo[de.end():-1].lstrip()
            while "  " in cargo_limpo:
                cargo_limpo = cargo_limpo.replace("  ", " ")

            # Tirar as instâncias de "- " que é simplesmente uma quebra de linha no meio da palavra,
            # sem tirar as instâncias de " - ", que é um hífen mesmo
            cargo_limpo = re.sub(r'(?<! )- ', '', cargo_limpo)
        else:
            cargo_limpo = "Cargo não encontrado"
        
        # Caso Especial para nomeações para o Corpo de Bombeiros
        if cargo_limpo == "Soldado Bombeiro Militar":
            # Encontrar o símbolo do cargo
            offset_simbolo = match.end()+i + cargo_match.end()
            parte_html_2 = html[offset_simbolo:]
            simbolo_match = re.search(r'Qua-?(?:<[^>]*>)*li-?(?:<[^>]*>)*fi-?(?:<[^>]*>)*ca-?(?:<[^>]*>)*ção(?:[^,]*),', parte_html_2)  # Pega tudo entre "Qualificação" e a próxima vírgula, ignorando tags HTML

            if simbolo_match:
                simbolo = simbolo_match.group(0)  # Agora estamos pegando o texto entre as vírgulas
                simbolo_limpo = BeautifulSoup(simbolo, "html.parser").get_text(separator=" ").strip()
                
                # Buscando a primeira parte com pelo menos duas letras maiúsculas seguidas (entende-se que este é o símbolo)
                simbolo_real = ""
                estamos_no_simbolo = False
                for c in range(len(simbolo_limpo)-1):
                    if estamos_no_simbolo and simbolo_limpo[c] == " ":
                        break
                    if simbolo_limpo[c].upper() == simbolo_limpo[c] and simbolo_limpo[c+1].upper() == simbolo_limpo[c+1] and simbolo_limpo[c].isalpha() and simbolo_limpo[c+1] != " ":
                        estamos_no_simbolo = True
                    if estamos_no_simbolo:
                        simbolo_real += simbolo_limpo[c]
                
                simbolo_limpo = simbolo_real
            
            else:
                simbolo_limpo = "Símbolo não encontrado"
        
            # Aqui sabemos que é essa a lotação, por ser um caso específico do Corpo de Bombeiros
            lotacao_limpo = "Corpo de Bombeiros Militar do Estado do Rio de Janeiro, da Secretaria de Estado de Defesa Civil"

        # Não sendo esse caso especial dos bombeiros, esse é o caso geral
        else:
            # Encontrar o símbolo do cargo
            offset_simbolo = match.end()+i + cargo_match.end()
            parte_html_2 = html[offset_simbolo:]
            simbolo_match = re.search(r'^([^,]+)', parte_html_2) # Pega tudo até a primeira vírgula

            if simbolo_match:
                simbolo = simbolo_match.group(1)  # Agora estamos pegando o texto entre as vírgulas
                simbolo_limpo = BeautifulSoup(simbolo, "html.parser").get_text(separator=" ").strip()
                simbolo_limpo = simbolo_limpo.split("lo ", 1)[-1].replace(" ","")
            else:
                simbolo_limpo = "Símbolo não encontrado"

            # Encontrar a lotação (órgão) do cargo
            offset_lotacao = match.end()+i + cargo_match.end() + simbolo_match.end() + 2
            parte_html_3 = html[offset_lotacao:]
            lotacao_match = re.search(r'^(([^,]+,){2}[^,]+)', parte_html_3) # Pega tudo até a segunda vírgula

            # Eu percebi que sempre depois da lotação aparecem uma de duas coisas: ou a palavra "anteriormente", citando a pessoa que ocupava o cargo antes,
            # ou "em vaga", denotando o decreto que gerou a nomeação. Usamos isso para reconhecer quando acaba a parte da lotação
            anteriormente_regex = r'a(?:-?\s*)n(?:-?\s*)t(?:-?\s*)e(?:-?\s*)r(?:-?\s*)i(?:-?\s*)o(?:-?\s*)r(?:-?\s*)m(?:-?\s*)e(?:-?\s*)n(?:-?\s*)t(?:-?\s*)e'
            em_vaga_regex = r'e(?:-?\s*)m(?:-?\s*)v(?:-?\s*)a(?:-?\s*)g(?:-?\s*)a'

            if lotacao_match:
                lotacao = lotacao_match.group(1)
                lotacao_limpo = BeautifulSoup(lotacao, "html.parser").get_text(separator=" ").strip()

                # A lotação vai até a palavra "anteriormente" ou "em vaga", vamos pegar o que vem antes disso
                anteriormente = re.search(anteriormente_regex, lotacao_limpo)
                em_vaga = re.search(em_vaga_regex, lotacao_limpo)
                
                if anteriormente:
                    lotacao_limpo = lotacao_limpo[:anteriormente.start()]
                elif em_vaga:
                    lotacao_limpo = lotacao_limpo[:em_vaga.start()]

                # Retirando o resto de html que às vezes sobra no início do texto
                resto = re.search("/div>", lotacao_limpo)
                if resto and resto.start() == 0:
                    lotacao_limpo = lotacao_limpo.replace("/div>", "")
                
                # Tirar os espaços no início do texto
                lotacao_limpo = lotacao_limpo.lstrip()

                # Procurando pelo "do" ou "da" que sobra no início do texto e pegando só o que vem depois disso
                do = re.search("do", lotacao_limpo)
                da = re.search("da", lotacao_limpo)
                
                # Se tiver "do" ou "da" no início do texto, tira
                if do and do.start() == 0:
                    lotacao_limpo = lotacao_limpo[do.end():]
                elif da and da.start() == 0:
                    lotacao_limpo = lotacao_limpo[da.end():]

                # Tirar os espaços no início do texto de novo
                lotacao_limpo = lotacao_limpo.lstrip()

                # Tira espaços e vírgulas do final
                while lotacao_limpo[-1] in [" ", ","]:
                    lotacao_limpo = lotacao_limpo[:-1]

                # Tirar os espaços duplos
                while "  " in lotacao_limpo:
                    lotacao_limpo = lotacao_limpo.replace("  ", " ")
                
                # Tirar as instâncias de "- " que é simplesmente uma quebra de linha no meio da palavra,
                # sem tirar as instâncias de " - ", que é um hífen mesmo
                lotacao_limpo = re.sub(r'(?<! )- ', '', lotacao_limpo)
            
            else:
                lotacao_limpo = "Lotação não encontrada"

        # Colocando os dados em suas respectivas listas
        nomeacoes.append(nome_limpo)
        cargos.append(cargo_limpo)
        simbolos.append(simbolo_limpo)
        lotacoes.append(lotacao_limpo)
    
    return nomeacoes, cargos, simbolos, lotacoes

# Salvar os dados em CSV, adicionando aos dados já existentes, se houverem
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
        print(f"\n > Obtendo e salvando html do DO do dia {data}")
        html = obter_html(url, data)
        print(f"Extraindo dados do DO do dia {data}")
        nomes, cargos, simbolos, lotacoes = extrair_dados(data, html)
        print(f"Salvando o CSV do DO do dia {data}")
        df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes)
    
    return df

# Executa tudo para um dia só, como teste
def executar_fluxo_um_dia(urls, data):
    # Deleta o arquivo com dados, se existir, para pegarmos dados novos
    if os.path.isfile(f"csvs/dados_teste_{data}.csv"):
        os.remove(f"csvs/dados_teste_{data}.csv")

    print(f"\n > Obtendo e salvando html do DO do dia {data}")
    html = obter_html(urls[data], data)
    print(f"Extraindo dados do DO do dia {data}")
    nomes, cargos, simbolos, lotacoes = extrair_dados(data, html)
    print(f"Salvando o CSV do DO do dia {data}")
    df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes, nome_arquivo=f"csvs/dados_teste_{data}.csv")
    return df

# Faz só a parte de estruturar os dados do HTML, para um dia só
def procurar_no_html_salvo(data):
    with open(f"htmls/diario_oficial_{data}.html", encoding="utf-8") as f:
        html_salvo = f.read()
    print(f"Extraindo dados do DO do dia {data}")
    nomes, cargos, simbolos, lotacoes = extrair_dados(data, html_salvo)
    print(f"Salvando o CSV do DO do dia {data}")
    df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes, nome_arquivo=f"csvs/dados_html_salvo_{data}.csv")
    return df

# Faz só a parte de estruturar os dados do HTML, para todos os dias
def procurar_nos_htmls_salvos(datas):
    # Deleta o arquivo com dados, se existir, para pegarmos dados novos
    if os.path.isfile("csvs/dados_htmls_salvos.csv"):
        os.remove("csvs/dados_htmls_salvos.csv")

    # Iterando pelos dias e os arquivos com os HTMLs dos DOs
    for data in datas:
        with open(f"htmls/copiados/diario_oficial_{data}.html", encoding="utf-8") as f:
            html_salvo = f.read()
        print(f"Extraindo dados do DO do dia {data}")
        nomes, cargos, simbolos, lotacoes = extrair_dados(data, html_salvo)
        print(f"Salvando o CSV do DO do dia {data}")
        df = salvar_em_csv(data, nomes, cargos, simbolos, lotacoes, nome_arquivo=f"csvs/dados_htmls_salvos.csv")
    
    return df

# Cria dfs com dados agregados para fazermos nossas visualizações
def cria_dfs_agregados(df):
    df_nomeacoes_por_dia = df.groupby('Data DO')['Nome'].count().reset_index(name='Quantidade Nomeações')
    df_nomeacoes_por_dia.to_csv("csvs/agregados/nomeacoes_por_dia.csv", encoding="utf-8", index=False)

    df_nomeacoes_por_cargo = df.groupby('Cargo')['Nome'].count().reset_index(name='Quantidade Nomeações')
    df_nomeacoes_por_cargo = df_nomeacoes_por_cargo.sort_values(by='Quantidade Nomeações', ascending=False)
    df_nomeacoes_por_cargo.to_csv("csvs/agregados/nomeacoes_por_cargo.csv", encoding="utf-8", index=False)
    
    df_nomeacoes_por_simbolo = df.groupby('Símbolo')['Nome'].count().reset_index(name='Quantidade Nomeações')
    df_nomeacoes_por_simbolo = df_nomeacoes_por_simbolo.sort_values(by='Quantidade Nomeações', ascending=False)
    df_nomeacoes_por_simbolo.to_csv("csvs/agregados/nomeacoes_por_simbolo.csv", encoding="utf-8", index=False)

    df_nomeacoes_por_lotacao = df.groupby('Lotação')['Nome'].count().reset_index(name='Quantidade Nomeações')
    df_nomeacoes_por_lotacao = df_nomeacoes_por_lotacao.sort_values(by='Quantidade Nomeações', ascending=False)
    df_nomeacoes_por_lotacao.to_csv("csvs/agregados/nomeacoes_por_lotacao.csv", encoding="utf-8", index=False)

# Cria um df separando as lotações em níveis, e colocando uma coluna com a quantidade de nomeações para cada lotação
def cria_df_hierarquia(lista):
    # Vê qual o maior número de subdivisões
    max_n_virgulas = 0
    for item in lista:
        n_virgulas = item.count(",")
        if n_virgulas > max_n_virgulas:
            max_n_virgulas = n_virgulas

    # Criar um DataFrame vazio com max_n_virgulas+1 colunas
    colunas = [f'Nível {i+1}' for i in range(max_n_virgulas+1)]
    df = pd.DataFrame(columns=colunas)

    for item in lista:
        # Divide e limpa os nomes dos órgãos
        partes = [p.strip() for p in item.split(',')]
        partes = [parte[3:] if parte[0:3] in ["na ", "no ", "da ", "do "] else parte for parte in partes]

        # Quando o número de divisões da lotação não é igual ao número máximo, adicionamos um "-" onde estariam as subdivisões menores
        while len(partes) < max_n_virgulas+1:
            partes.insert(0, "-")

        # Adicionar uma linha de dados (exemplo com valores)
        nova_linha = partes[::-1]
        df.loc[len(df)] = nova_linha
    
    # Agrupar para termos a quantidade de nomeações por lotação
    df_hierarquia = df.groupby(['Nível 1', 'Nível 2', 'Nível 3']).size().reset_index(name='Quantidade Nomeações').sort_values(by="Quantidade Nomeações", ascending=False)
    
    # Agrupar para termos a quantidade de nomeações por lotação, olhando só para o nível mais superior de cada uma
    df_hierarquia_macro = df.groupby(['Nível 1']).size().reset_index(name='Quantidade Nomeações').sort_values(by="Quantidade Nomeações", ascending=False)

    # Salvando os dataframes
    df_hierarquia.to_csv("csvs/agregados/hierarquia.csv", encoding="utf-8", index=False)
    df_hierarquia_macro.to_csv("csvs/agregados/hierarquia_macro.csv", encoding="utf-8", index=False)

def main():
    # Os links do Diário Oficial do Estado do RJ dos dias 7 a 11 de Abril de 2025
    urls = {
        "2025-04-07" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VWtSQ1JsRlZUa1JPUkUxMFRVUkdSVTFUTURCT2FrNUhURlJvUlUwd1JYUlJhMDE1VG1wQmVWRlVRa1ZOZWxVeQ==",
        "2025-04-08" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg==",
        "2025-04-09" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VW1wWk1rOUZTa2ROVkdkMFVWUktSbEZUTURCUmVrRTFURlZKZVUwd1NYUlJhbGsxVWxSVmVFMHdUVEJTYW1oRA==",
        "2025-04-10" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wVmVWRnFaelZTUkVGMFVWUkpNRkY1TURCUk1FcENURlZKZDA1VVRYUlBWVTE1VDBSa1IwMUZVVFZOTUZWMw==",
        "2025-04-11" : "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VFZSQk5WRnJWVEpSVkd0MFVtcG9SVTFETURCTmVrcEdURlZKTlUxNldYUlJlbGw2VDFST1IwMUVUVEZQVkZWNA=="
    }

    # Extrai os HTMLs e estrutura seus dados
    df = executar_fluxo_completo(urls)

    # Cria os dataframes agregados para gerarmos as visualizações
    cria_dfs_agregados(df)

    # Criando os dataframes separando as lotações em níveis
    cria_df_hierarquia(df["Lotação"])

if __name__ == "__main__":
    main()