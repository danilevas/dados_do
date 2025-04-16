import requests
from bs4 import BeautifulSoup
import re

url_pagina = "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg=="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

resp = requests.get(url_pagina, headers=headers)
resp.raise_for_status()

soup = BeautifulSoup(resp.content, "html.parser")
link_pdf = soup.find("a", href=re.compile(r"moduloArquivo/pdf/.*\.pdf"))

if link_pdf:
    url_pdf = "https://www.ioerj.com.br/portal/" + link_pdf["href"]
    print("Link do PDF encontrado:")
    print(url_pdf)
else:
    print("Nenhum link de PDF encontrado.")