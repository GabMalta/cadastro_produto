import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from apps.data_scraping.utils.selenium_webdriver import create_webdriver
import re


def aquarela_scraping(url, fabric_name):

    nav = create_webdriver()

    nav.get(url)
    picture_div = nav.find_elements(By.CLASS_NAME, "item")

    infos = nav.find_element(By.TAG_NAME, "h2").text
    cod = re.search(r"Ordem: (\d+)", infos).group(1)
    composition = re.search(r"Composição: (.+)", infos).group(1)
    width = re.search(r"Largura: (\d+,\d+)", infos)
    width = width.group(1) if width else "1,50"
    folder_name = f"{fabric_name} A{cod}"
    urls = []

    for img in picture_div:
        url_img = img.find_element(By.TAG_NAME, "a").get_attribute("href")
        nome = img.find_element(By.CLASS_NAME, "color-code").text
        formato = url_img.split(".")[-1]

        urls.append(
            {
                "name": nome,
                "url_img": url_img,
                "format": formato,
            }
        )

    response = {
        "fabric_name": fabric_name,
        "cod": f"A{cod}",
        "folder_name": folder_name,
        "composition": composition,
        "width": width,
        "pictures": urls,
    }

    nav.close()

    return response


# def aquarela_requests():
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Connection": "keep-alive",
#     }
#     response = requests.get("https://aquarelatecidos.com/Tecidos%20Lisos/03%20-%20Brim%20Leve%20Const%C3%A2ncia%20Vieira/index.html", headers=headers)


#     soup = BeautifulSoup(response.text, 'html.parser')

#     items = soup.find_all("div", class_='item')

#     for item in items:
#         links = item.find_all("a")  # Buscar todas as tags <a> dentro do div
#         for link in links:
#             print("Texto do link:", link.get_text(strip=True))
#             print("URL do link:", link.get("href"))


# aquarela_requests()
