from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# Configuração do Chrome
options = Options()
options.headless = False  # Deixe False para ver o navegador abrindo
driver = webdriver.Chrome(options=options)

# URL da edição do Diário Oficial
url = "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg=="
driver.get(url)

# Espera a página carregar
time.sleep(25)

# TROCA PARA IFRAME, se existir
try:
    iframe = driver.find_element("tag name", "iframe")
    driver.switch_to.frame(iframe)
    print("👉 Mudamos para o iframe com sucesso.")
except:
    print("❌ Nenhum iframe encontrado.")

# Tenta encontrar o link para o PDF
pdf_links = driver.find_elements("xpath", "//a[contains(@href, '.pdf')]")

if pdf_links:
    href = pdf_links[0].get_attribute("href")
    print("✅ Link do PDF encontrado:", href)

    # Faz o download do PDF com requests
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(href, headers=headers)
    with open("edicao_ioerj.pdf", "wb") as f:
        f.write(r.content)
    print("📥 PDF baixado com sucesso!")
else:
    print("❌ Não foi possível encontrar o link do PDF.")

# Fecha o navegador
driver.quit()