import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pdfplumber

def iniciar_driver_visivel():
    chrome_options = Options()
    # Chrome visível para ver carregamento
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def salvar_html(driver, nome_arquivo):
    html = driver.page_source
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML salvo como {nome_arquivo}")
    return html

def extrair_pdf_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    pdf_links = []

    # Tenta pegar links diretos para PDFs
    for tag in soup.find_all(["a", "iframe", "embed"]):
        src = tag.get("href") or tag.get("src")
        if src and ".pdf" in src.lower():
            pdf_links.append(src)

    return pdf_links

def baixar_pdf(url_pdf, nome_arquivo="saida.pdf"):
    try:
        print(f"🔽 Tentando baixar: {url_pdf}")
        r = requests.get(url_pdf)
        with open(nome_arquivo, "wb") as f:
            f.write(r.content)
        print("✅ PDF salvo como", nome_arquivo)
        return nome_arquivo
    except Exception as e:
        print("Erro ao baixar PDF:", e)
        return None

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() + "\n"
        print("📄 Texto extraído do PDF:")
        print(texto[:1000])  # Mostra os primeiros 1000 caracteres
    except Exception as e:
        print("Erro ao extrair texto do PDF:", e)

def testar_tudo(url):
    driver = iniciar_driver_visivel()
    driver.get(url)
    time.sleep(10)  # Espera inicial

    print("➡️ Rolando página...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)

    print("➡️ Salvando HTML completo...")
    html = salvar_html(driver, "pagina_diario.html")

    print("🔍 Buscando PDFs no HTML...")
    pdf_urls = extrair_pdf_urls(html)
    if pdf_urls:
        print(f"🎯 Encontrado(s) {len(pdf_urls)} link(s) de PDF:")
        for url_pdf in pdf_urls:
            print("-", url_pdf)

        # Testa baixar e extrair texto do primeiro
        caminho_pdf = baixar_pdf(pdf_urls[0])
        if caminho_pdf:
            extrair_texto_pdf(caminho_pdf)
    else:
        print("❌ Nenhum link direto de PDF encontrado.")

    # Como fallback, salva o body renderizado
    body = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
    with open("body_renderizado.html", "w", encoding="utf-8") as f:
        f.write(body)
    print("🧱 Body renderizado salvo como body_renderizado.html")

    driver.quit()

testar_tudo("https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg==")