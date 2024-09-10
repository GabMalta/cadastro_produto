from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from apps.data_scraping.utils.selenium_webdriver import create_webdriver

def disparada_scraping(cod, fabric_name):
    nav = create_webdriver()

    folder_name = f'{fabric_name} D{cod}'    
    save_path = fr'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\DISPARADA\{folder_name}'
    
    nav.get(f'https://disparadatecidos.com.br/')
    nav.find_element('xpath', '/html/body/main/a[1]').click()

    nav.find_element('xpath', '//*[@id="input_search"]').send_keys(cod)
    nav.find_element('xpath', '//*[@id="input_search"]').send_keys(Keys.ENTER)
    nav.find_element('xpath', '//*[@id="artigo-list"]/li/a').click()
    
    composition = nav.find_element('xpath', '//*[@id="artigo-composicao"]')
    composition = composition.text
    width = nav.find_element('xpath', '//*[@id="artigo-largura"]').text.replace('.',',').replace('MT', '')
    
    pictures = nav.find_elements('class name', 'item')
    

    urls = []
    #BAIXA TODAS AS ESTAMPAS
    for picture in pictures:
        nome_cor = picture.find_element('class name', 'color-code').text
        url = picture.find_element(By.TAG_NAME, 'img').get_attribute('src')
        formato = url.split('.')[-1]
        
        urls.append({
            'name': nome_cor,
            'url_img': url,
            'format': formato
        })
    
    response = {
        'fabric_name': fabric_name,
        'cod': f'D{cod}',
        'folder_name': folder_name,
        'composition': composition,
        'width': width,
        'pictures': urls
    }
    nav.close()
    
    return response
    


    # for arq in urls:
    #     caminho = os.path.join(pictures_directory, arq['nome'] + '.' + arq['formato'])
    #     baixa_imagem(arq['url_img'], caminho)
        
    # #PEGA AS IMAGENS EXPORTADAS E CRIA AS CAPAS
    # if 'titulo_tecido' in kwargs:
    #     monta_capa(pictures_directory, cover_directory, titulo_tecido=kwargs['titulo_tecido'])

    # elif 'titulo_promo' in kwargs:
    #     monta_capa(pictures_directory, cover_directory, titulo_promo=kwargs['titulo_promo'])
    
    # else:
    #     monta_capa(pictures_directory, cover_directory)

    


    