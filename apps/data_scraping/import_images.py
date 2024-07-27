import os

from data_scraping.sites_scraping.disparada import disparada_scraping
from data_scraping.sites_scraping.pitangui import pitangui_scraping
from data_scraping.sites_scraping.aquarela import aquarela_scraping
from data_scraping.utils.create_save_directory import create_save_directory
from data_scraping.utils.download_picture import download_picture
from data_scraping.utils.save_product_json import save_product_json
from data_scraping.utils.convert_to_jpg import convert_folder_to_jpg

def import_images(company:str, cod_or_url:str, fabric_name:str, path:str):
    
    try:
        match company.upper():
            case 'DISPARADA':
                product = disparada_scraping(cod_or_url, fabric_name)
            case 'PITANGUI':
                product = pitangui_scraping(cod_or_url, fabric_name)
            case 'AQUARELA':
                product = aquarela_scraping(cod_or_url, fabric_name)
            case _:
                return print('Metodo de download para atacado nao encontrado ou nome de atacado inválido')
    except Exception as e:
        return print('Erro ao fazer scraping, confira se passou o codigo correto ou url correta... \n', e)

    save_path = create_save_directory(path,product['folder_name'])

    save_product_json(save_path, product)

    pictures_directory = os.path.join(save_path, 'Fotos')
    cover_directory = os.path.join(save_path, 'Capa')

    for arq in product['pictures']:
        path_img = os.path.join(pictures_directory, arq['name'] + '.' + arq['format'])
        download_picture(arq['url_img'], path_img)
    
        
    return {'path': save_path, 'pictures_directory': pictures_directory, 'cover_directory':cover_directory}

#pitangui_scraping('025', 'OXFORD DE NATAL')
# #PEGA AS IMAGENS EXPORTADAS E CRIA AS CAPAS
# if 'titulo_tecido' in kwargs:
#     monta_capa(pictures_directory, cover_directory, titulo_tecido=kwargs['titulo_tecido'])

# elif 'titulo_promo' in kwargs:
#     monta_capa(pictures_directory, cover_directory, titulo_promo=kwargs['titulo_promo'])

# else:
#     monta_capa(pictures_directory, cover_directory)