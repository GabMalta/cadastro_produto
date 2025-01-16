import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from apps.data_scraping.utils.selenium_webdriver import create_webdriver


def disparada_scraping(cod, fabric_name):
    nav = create_webdriver()

    folder_name = f"{fabric_name} D{cod}"
    save_path = rf"D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\DISPARADA\{folder_name}"

    # nav.get(f'https://disparadatecidos.com.br/')
    # nav.find_element('xpath', '/html/body/main/a[1]').click()

    # nav.find_element('xpath', '//*[@id="input_search"]').send_keys(cod)
    # nav.find_element('xpath', '//*[@id="input_search"]').send_keys(Keys.ENTER)
    # nav.find_element('xpath', '//*[@id="artigo-list"]/li/a').click()

    nav.get(f"https://disparadatecidos.com.br/artigo/{cod}")

    time.sleep(5)
    composition = nav.find_element("xpath", '//*[@id="artigo-composicao"]')
    composition = composition.text
    width = (
        nav.find_element("xpath", '//*[@id="measurement-value"]')
        .text.replace(".", ",")
        .replace("MT", "")
    )

    pictures = nav.find_elements(By.CSS_SELECTOR, ".col-auto.item-container")

    urls = []
    # BAIXA TODAS AS ESTAMPAS
    for picture in pictures:
        nome_cor = (
            picture.find_element(By.CLASS_NAME, "item")
            .find_element(By.CLASS_NAME, "card-body")
            .find_element(By.CLASS_NAME, "card-title")
            .text
        )
        url = (
            picture.find_element(By.CLASS_NAME, "item")
            .find_element(By.CLASS_NAME, "img-container")
            .find_element(By.TAG_NAME, "img")
            .get_attribute("src")
        )
        formato = url.split(".")[-1]

        urls.append({"name": nome_cor, "url_img": url, "format": formato})

    response = {
        "fabric_name": fabric_name,
        "cod": f"D{cod}",
        "folder_name": folder_name,
        "composition": composition,
        "width": width,
        "pictures": urls,
    }
    nav.close()

    return response


def disparada_requests(cod, fabric_name):

    data = requests.get(
        f"https://disparadatecidos.com.br/api/get_data_for_artigo_view/{cod}"
    )

    response = data.json()

    if response["error"] == True:
        raise ValueError(response["message"])

    response = response["data"]['artigo']

    urls = [
        {
            "name": cor["codigo"],
            "url_img": rf'https://sistema.disparadatecidos.com.br/upload_artigo_images/{cor["image_path"]}',
            "format": cor["image_path"].split(".")[-1],
        }
        for cor in response["cores"]
    ]


    response = {
        "fabric_name": fabric_name,
        "cod": f"D{cod}",
        "folder_name": f"{fabric_name} D{cod}",
        "composition": response["composicao"],
        "width": response["largura"],
        "pictures": urls,
    }
    
    return response
