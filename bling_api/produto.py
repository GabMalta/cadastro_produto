import json, re, requests, os
from bling import BlingApi
from IMGUR.imgur import Imgur

from bling_api import settings
from requests_policy.http import http


class Produto(BlingApi):
    def __init__(self,cover_path,path_variations,name,code,price,description='',weight=0.3,origin=2,ncm=54075210,img='',alt=7,larg=7,profun=7, marca='Legítima Têxtil', client_id=None, client_secret=None):

        #DEFINE TODAS AS CARACTERISTICAS DO PRODUTO
        self.path_variations = path_variations
        self.name = name
        self.code = code
        self.price = price
        self.description = description
        self.weight = weight
        self.origin = origin
        self.ncm = ncm
        self.img = img
        self.alt = alt
        self.larg = larg
        self.profun = profun
        self.cover_path = cover_path
        self.marca = marca
        
        super().__init__(client_id, client_secret)
        
        self.generate_client_imgur()
        
    def generate_client_imgur(self):
        client_id = self.get_client_id_imgur()
        client_secret = self.get_client_secret_imgur()
        
        if not client_id or not client_secret:
            print('''Para cadastrar produtos precisamos hospedar imagens na web, para isso utilizamos o serviço do imgur.
                  Cadastre um aplicativo e digite o client_id e client_secret abaixo:''')
            
            client_id = input('Digite ou cole o client_id: ')
            client_secret = input('Digite ou cole o client_secret: ')
            
            self.set_client_id_imgur(client_id)
            self.set_client_secret_imgur(client_secret)
        
        self.imgur = Imgur(client_id, client_secret)
        
    def get_client_id_imgur(self) -> str:
        with open('./tokens/client_id_imgur.txt', 'r') as token:
            return token.read()

    def get_client_secret_imgur(self) -> str:
        with open('./tokens/client_secret_imgur.txt', 'r') as token:
            return token.read()

    def set_client_id_imgur(self, client_id:str):
        with open('./tokens/client_id_imgur.txt', 'w') as token:
            token.write(client_id)

    def set_client_secret_imgur(self, client_secret:str):
        with open('./tokens/client_secret_imgur.txt', 'w') as token:
            token.write(client_secret)
    
    def get_upload_cover(self, album_id=None):
        images = self.imgur.upload_images(self.cover_path, album_id=album_id)['data']
        
        for image in images:
            self.save_image_json(self.cover_path, image)
        
        images_url = [{'link': img['link']} for img in images]
        
        self.covers_urls = images_url
    
    def compose_product(self, changed_name=True):
        variations = self.compose_variations(changed_name)
        product = self.get_product_json()
        
        product['nome'] = self.name
        product['codigo'] = self.code
        product['preco'] = self.price
        product['descricaoCurta'] = self.description
        product['pesoLiquido'] = self.weight
        product['pesoBruto'] = self.weight
        product['marca'] = self.marca
        product['dimensoes']['largura'] = self.larg
        product['dimensoes']['altura'] = self.alt
        product['dimensoes']['profundidade'] = self.profun
        product['tributacao']['origem'] = self.origin
        product['tributacao']['ncm'] = self.ncm
        product['midia']['imagens'] = {'externas': self.covers_urls}
        product['variacoes'] = variations

        self.product = product
        return product
    
    def compose_variations(self, changed_name=True):
        
        folder = os.listdir(self.path_variations)
        variations = []
        
        album_id = self.check_exists_album_title(self.name)
                
        if not album_id:
            album_id = self.imgur.create_album(self.name)['id']
        
        for color in folder:
            path_color = os.path.join(self.path_variations, color)
       
            if 'desktop.ini' in color or not self.imgur.path_is_image(path_color):
                pass
            
            else:
                color_name, cod_sku = self.generate_colorname_and_codsku(color, changed_name)
                
                image = self.imgur.upload_image(path_color, album_id)
                self.save_image_json(self.path_variations, image)
                
                image_url = image['link']
                
                variation = self.get_variation_json()
                
                variation['nomeVariacao'] = f'Cor:{color_name}'
                variation['codigo'] = f'{self.code} - {cod_sku}'
                variation['preco'] = self.price
                variation['pesoLiquido'] = self.weight
                variation['pesoBruto'] = self.weight
                variation['marca'] = self.marca
                variation['dimensoes']['largura'] = self.larg
                variation['dimensoes']['altura'] = self.alt
                variation['dimensoes']['profundidade'] = self.profun
                variation['tributacao']['origem'] = self.origin
                variation['tributacao']['ncm'] = self.ncm
                variation['midia']['imagens']['externas'] = [{'link': image_url}]
                
                variations.append(variation)
        
        
        self.variations = variations
        self.get_upload_cover(album_id)
        
        return variations
    
    def get_variation_json(self):
        path = os.path.join(settings.BASEDIR, 'jsons', 'variation.json')
        with open(path, 'r', encoding='utf-8') as arq:
                return json.load(arq)

    def get_product_json(self):
        path = os.path.join(settings.BASEDIR, 'jsons', 'product.json')
        with open(path, 'r', encoding='utf-8') as arq:
                return json.load(arq)
    
    def save_image_json(self, path_folder, image):
        path = os.path.join(path_folder, 'image.urls.json')
        data = {'color': image['title'], 'url': image['link'], 'id': image['id']}
        
        try:
            with open(path, 'r', encoding='utf-8') as arq:
                images = json.load(arq)
            
            images.append(data)
        
        except FileNotFoundError as err:
            images = [data]
        
        with open(path, 'w') as arq:
            json.dump(images, arq, ensure_ascii=False, indent=4)
                
        return images
                
    def check_exists_album_title(self, title):
        albums = self.imgur.get_albums()
        
        for album in albums:
            
            if title in album['title']:
                return album['id']
            else:
                return False
   
    def generate_colorname_and_codsku(self, color, changed_name):
                
        color_name,_ = os.path.splitext(color)
        color_name = color_name.title()
                
        if changed_name:
            cod_sku = re.sub('[^0-9]', '', color_name)
        
            if not cod_sku or cod_sku == '':
                cod_sku = color_name
        else:
            cod_sku = color_name
        
        return color_name, cod_sku
    
    def upload_product(self, changed_name=True):
        link = 'https://www.bling.com.br/Api/v3/produtos'
        
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}

        product = self.compose_product(changed_name)
        body_message = json.dumps(product)
        
        try:
            response = http.post(link, headers=headers, data=body_message)
            
            return print(f'Produto: {self.name} cadastrado com sucesso. {response.status_code}')
        
        except requests.exceptions.HTTPError as err:
            print(err.response.json())
            
        # except Exception as err:
        #     print('eero aqui', err)
        