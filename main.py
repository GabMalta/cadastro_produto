import json
import os
import time
from apps.bling_api.produto import Produto
from apps.data_scraping.import_images import import_images
from description.render_template_description import render_template_description
from apps.price_generator.price_generator import price_generator

# imported_product = import_images('AQUARELA',r'https://aquarelatecidos.com/Tecidos%20Lisos/1465%20-%20Malha%20Jacquard%20Piquet/index.html', 'MALHA PIQUET CASINHA DE ABELHA', r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\NOVA EXTRACAO')
path = r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\NOVA EXTRACAO\TEMP_GM\TULE POA COM GLITER A9983'
pictures_path = os.path.join(path, 'Fotos')
capa_path = os.path.join(path, 'Capa')

imported_product = {'path': path, 'pictures_directory': pictures_path, 'cover_directory':capa_path}

with open(os.path.join(imported_product['path'], 'image_urls.json')) as arq:
    product_json = json.load(arq)

cover_path = imported_product['cover_directory']
pictures_path = imported_product['pictures_directory']

changed_name = bool(input('tempo para trocar o nome das cores...'))

produto = Produto(
    cover_path,
    pictures_path,
    f'Tecido {product_json['fabric_name'].title()}',
    product_json['fabric_name'].title(),
    product_json['cod'],
    0.00
)

nome = 'Tecido Tule Poa Com Gliter'#f'Tecido {product_json['fabric_name'].title()}'
folder_name = product_json['fabric_name'].title()
largura_tec = product_json['width']
preco_custo = 7.49
metragens = [1, 3, 4, 6, 10]
codigo = product_json['cod']
preco = [price_generator(preco_custo, mt, 20) for mt in metragens] 
peso = [0.2, 0.6, 0.8, 1, 1.2]
largura = [7, 7, 7, 7, 7]
altura = [7, 7, 7, 10, 10]
profundidade = [7, 7, 7, 7, 7]


    
anuncios = []

with open('./description/desc_gpt.txt', 'r', encoding='utf8') as arq:
    desc_gpt = arq.read()

for i, mt in enumerate(metragens):
    
    composition = product_json['composition']
    description = render_template_description({'mt': mt, 'larg': largura_tec, 'nome': nome, 'composition': composition, 'desc_gpt': desc_gpt})
    
    anuncio = {
        'titulo': f'{mt} Metros {nome} ({mt}m x {largura_tec}m)',
        'folder_name': folder_name,
        'codigo': f'{mt}m-{codigo}',
        'preco': preco[i],
        'peso': peso[i],
        'largura': largura[i],
        'altura': altura[i],
        'profundidade': profundidade[i],
        'description': description
    }
    anuncios.append(anuncio)

for anuncio in anuncios:
    produto.name = anuncio['titulo']
    produto.folder_name = anuncio['folder_name']
    produto.code = anuncio['codigo']
    produto.price = anuncio['preco']
    produto.weight = anuncio['peso']
    produto.larg = anuncio['largura']
    produto.alt - anuncio['altura']
    produto.profun = anuncio['profundidade']
    produto.description = anuncio['description']
    
    product = produto.upload_product(changed_name=changed_name)
    
    #id_deposito = 10610809064 #LEGITIMA
    id_deposito = 14886526196 #GM TECIDOS
    id_products = [data['id'] for data in product['variations']]
    
    produto.add_estoque(id_deposito, id_products, 100)
