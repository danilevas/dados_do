import os
import re
import requests
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def baixar_pdf_do_ioerj(url_pagina, caminho_destino_pdf):
    # Setup de sessão com retry + cabeçalho tipo navegador
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Baixa a página HTML da edição
    resp = session.get(url_pagina, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    # Procura o link real do PDF
    link_pdf = soup.find("a", href=re.compile(r"moduloArquivo/pdf/.*\.pdf"))
    if not link_pdf:
        raise Exception("Link do PDF não encontrado na página")

    url_pdf = "https://www.ioerj.com.br/portal/" + link_pdf["href"]
    
    # Faz o download do PDF
    resp_pdf = session.get(url_pdf, headers=headers)
    resp_pdf.raise_for_status()

    with open(caminho_destino_pdf, "wb") as f:
        f.write(resp_pdf.content)
    
    return caminho_destino_pdf

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

def teste_extracao_texto():
    url = "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg=="
    caminho_pdf = "teste_ioerj.pdf"
    caminho_txt = "texto_extraido.txt"

    print("Baixando PDF...")
    baixar_pdf_do_ioerj(url, caminho_pdf)

    print("Extraindo texto...")
    texto = extrair_texto_pdf(caminho_pdf)

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"Texto extraído e salvo em '{caminho_txt}'.")

if __name__ == "__main__":
    teste_extracao_texto()