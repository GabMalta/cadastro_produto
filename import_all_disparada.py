import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from apps.data_scraping.utils.selenium_webdriver import create_webdriver
from apps.data_scraping.utils.create_save_directory import create_save_directory
from apps.data_scraping.utils.save_product_json import save_product_json
from apps.data_scraping.utils.download_picture import download_picture
import time, os

class AllDisparada:
    
    def __init__(self) -> None:
        self.nav = self.login()

    def login(self):
        nav = create_webdriver()
        
        usuario = 'gabrielm'
        senha = '123gabriel*'
        
        nav.get('https://sistema.disparadatecidos.com.br')
        
        nav.find_element(By.ID, "input_user").send_keys(usuario)
        nav.find_element(By.ID, "input_pass").send_keys(senha)
        nav.find_element(By.ID, "btn_login").click()
        time.sleep(2)
        
        return nav

    def get_all_items_disparada(self):

        self.nav.find_element(By.PARTIAL_LINK_TEXT, "Artigos").click()
        time.sleep(5)
        
        all_list = self.nav.find_element(By.ID, 'all_items_list')
        
        li_list = all_list.find_elements(By.TAG_NAME, 'li')
        
        items = [item.find_element(By.TAG_NAME, 'a').get_attribute('href') for item in li_list]
        
        for i,item in enumerate(items):
            if item == 'https://sistema.disparadatecidos.com.br/main/artigo/522':
                items = items[i:]
                break
            
        
        return items

    def verify_items_stock(self, url):
        
        self.nav.get(url)
        time.sleep(2)
        
        fabric_name =  self.nav.find_element(By.ID, 'input_name').get_attribute('value').replace('/', '')
        cod = self.nav.find_element(By.ID, 'input_reference').get_attribute('value')
        folder_name = f'{fabric_name.upper()} D{cod}'
        composition = self.nav.find_element(By.ID, 'input_composition').get_attribute('value')
        width = self.nav.find_element(By.ID, 'input_width').get_attribute('value')
        price = self.nav.find_element(By.ID, 'input_price').get_attribute('value')
        lenght = self.nav.find_element(By.ID, 'input_length').get_attribute('value')
        density = self.nav.find_element(By.ID, 'input_density').get_attribute('value')
        gramatura = self.nav.find_element(By.ID, 'input_gramatura').get_attribute('value')
        variations = []
        
        
        self.nav.find_element(By.XPATH, '//*[@id="tab_color"]/label').click()
        
        
        div_colors = self.nav.find_element(By.ID, 'colors').find_elements(By.XPATH, './div')
        
        id_colors = [div.get_attribute('id').replace('product_', '') for div in div_colors]
        
        for color in id_colors:
            image = self.nav.find_element(By.ID, f'colorImage{color}').get_attribute('src')
            name = self.nav.find_element(By.ID, f'colorCode{color}').get_attribute('value')
            stock = self.nav.find_element(By.ID, f'colorStock{color}').get_attribute('value')
            
            if float(stock.replace('.', '').replace(',', '.')) >= 50:
                variations.append({
                    'image': image,
                    'name': name,
                    'stock': stock
                })
                
        
        if len(variations) > 0:
            data = {
                'fabric_name': fabric_name,
                'cod': cod,
                'folder_name': folder_name,
                'composition': composition,
                'width': width,
                'price': price,
                'lenght': lenght,
                'density': density,
                'gramatura': gramatura,
                'variations': variations
            }
            
            return data
        
        return None

        
        
    def create_folder_for_json(self, save_path):
        urls = self.get_all_items_disparada()
        
        for url in urls:
            json_data = self.verify_items_stock(url)
            
            if not json_data:
                continue
            
            path_folder = create_save_directory(save_path, json_data['folder_name'])
            save_product_json(path_folder, json_data)
            
def download_images_disparada(path):
    
    folders = os.listdir(path)
    
    products_folder = [os.path.join(path, folder) for folder in folders]
    
    for product in products_folder:
        
        if 'desktop.ini' in product:
            print('oooi')
            continue
        
        picture_path = os.path.join(product, 'Fotos')
        
        with open(os.path.join(product, 'image_urls.json'), 'r') as arq:
        
            product_dict = json.loads(arq.read())
            
        for variation in product_dict['variations']:
            path_save = os.path.join(picture_path, f"{variation['name']}.jpeg")

            download_picture(variation['image'], path_save )
        
        
        
        
download_images_disparada(r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\TODOS ITENS DISPARADA')
        
# with open(r'C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\ITENS\top.txt', 'w') as arq:
#     arq.write('popopop')


        
        
        
        