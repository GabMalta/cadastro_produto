from selenium.webdriver.common.by import By
from apps.data_scraping.utils.selenium_webdriver import create_webdriver

def pitangui_scraping(cod, fabric_name):
    nav = create_webdriver()
    
    nav.get('https://pitanguitecidos.com/')
    nav.find_element(By.XPATH, '//*[@id="layerHome"]/div[2]/div[2]/div/div/div/div[12]/a').click()
    
    search_bar = nav.find_element(By.ID, 'container-busca-input')
    search_bar.send_keys(cod)
    
    itens_body = nav.find_element(By.ID, 'ctl00_ContentPlaceHolderCorpo_ControlPublicacao_lblConteudo')
    itens_content = itens_body.find_element(By.CLASS_NAME, 'content').find_elements(By.CSS_SELECTOR, 'p > a')
    
    for content in itens_content:        
        if cod in content.text:
            content.click()
            break
    
    # ENTROU NA PAGINA DO PRODUTO:
    images = nav.find_elements(By.CLASS_NAME, 'cboxElement')
    
    urls = []
    
    for img in images:
        url = img.get_attribute('href')
        color_name = url.rsplit('/', 1)[1].split('.')[0]
        formato = url.rsplit('/', 1)[1].split('.')[1].split('?')[0]
        
        urls.append({
            'url_img': url,
            'name': color_name,
            'format': formato
        })
    
    composition = nav.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolderCorpo_ControlPublicacao_lblConteudo"]/div/div/div[2]/div/div/span[2]/strong').text
    
    width = nav.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolderCorpo_ControlPublicacao_lblConteudo"]/div/div/div[3]/div/div/span[2]/strong').text.replace('.',',').replace('MT', '').split(' \n')[0]
    
    folder_name = f'{fabric_name} P{cod}'
    
    response = {
        'fabric_name': fabric_name,
        'cod': f'P{cod}',
        'folder_name': folder_name,
        'composition': composition,
        'width': width,
        'pictures': urls
    }
    
    return response