import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def iniciar_driver():
    options = Options()
    # Remova o comentário abaixo se quiser headless
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def rolar_container(driver, passo=1367, intervalo_base=0.2):
    time.sleep(3.6)  # espera geral da página carregar
    container = driver.find_element(By.ID, "viewerContainer")

    # altura_total = driver.execute_script("return arguments[0].scrollHeight", container)
    altura_total = passo*10
    posicao = 0

    print("📜 Rolando o div#viewerContainer...")

    # Vai até a página 10
    mult=10
    while posicao < altura_total:
        driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", container, posicao)
        time.sleep(intervalo_base*mult)
        posicao += passo
        print(f"Posição: {posicao}/{altura_total} (passo = {passo})")
        # altura_total = driver.execute_script("return arguments[0].scrollHeight", container)
        mult -= 1

    # Volta pra página 1
    posicao = 0
    print(f"Posição: {posicao}/{altura_total} (passo = {passo})")

    # Vai até a página 9
    altura_total = passo*9
    mult=10
    while posicao < altura_total:
        driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", container, posicao)
        time.sleep(intervalo_base*mult)
        posicao += passo
        print(f"Posição: {posicao}/{altura_total} (passo = {passo})")
        # altura_total = driver.execute_script("return arguments[0].scrollHeight", container)
        mult -= 1

    print("✅ Rolagem finalizada")

    # salva todo o HTML visível após rolagem
    html = driver.page_source
    with open("pagina_completa_headless.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("💾 HTML salvo como pagina_completa_headless.html")

def main():
    url = "https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?session=VG1wb1IxRnFWa1JPVkZGMFRVUlplVTlUTURCU1JWRjZURlZKZDA1clRYUk9hbU0wVFVWUk5FMUVUVFJSVkdzeg=="
    driver = iniciar_driver()
    driver.get(url)
    rolar_container(driver)
    # input("⏸️ Pressione Enter para sair...")
    driver.quit()

if __name__ == "__main__":
    main()
