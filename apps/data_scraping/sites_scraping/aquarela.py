from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from data_scraping.utils.selenium_webdriver import create_webdriver
import re

def aquarela_scraping(url, fabric_name):
    
    nav = create_webdriver()

    nav.get(url)
    picture_div = nav.find_elements(By.CLASS_NAME, 'item')
           
    infos = nav.find_element(By.TAG_NAME, 'h2').text
    cod = re.search(r'Ordem: (\d+)', infos).group(1)
    composition = re.search(r'Composição: (\d+)', infos).group(1)
    width = re.search(r'Largura: (\d+)', infos).group(1)
    folder_name = f'{fabric_name} A{cod}'
    urls = []

    for img in picture_div:
        url_img = img.find_element(By.TAG_NAME, 'a').get_attribute('href')
        nome = img.find_element(By.CLASS_NAME, 'color-code').text
        formato = url_img.split('.')[-1]

        urls.append({
            'name': nome,
            'url_img': url_img,
            'format': formato,
            })

    response = {
        'fabric_name': fabric_name,
        'cod': cod,
        'folder_name': folder_name,
        'composition': composition,
        'width': width,
        'pictures': urls
    }

    nav.close()
    
    return response