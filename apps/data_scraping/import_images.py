import os

from apps.data_scraping.sites_scraping.disparada import disparada_scraping
from apps.data_scraping.sites_scraping.pitangui import pitangui_scraping
from apps.data_scraping.sites_scraping.aquarela import aquarela_scraping
from apps.data_scraping.utils.create_save_directory import create_save_directory
from apps.data_scraping.utils.download_picture import download_picture
from apps.data_scraping.utils.save_product_json import save_product_json
from apps.data_scraping.utils.cover_product import CoverPicture

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
    
    create_cover = input('Criar capa?')
    
    if not create_cover:
        create_covers(5, fabric_name, cover_directory, pictures_directory)
    
    return {'path': save_path, 'pictures_directory': pictures_directory, 'cover_directory':cover_directory}

def create_covers(qtd, cover_title, cover_path, picture_path, number_of_images: int = 4, max_letters: int = 16, letter_color: str = '#5DC1B9', font_color: str = '#050A30'):
    
    for i in range(qtd):
        cover = CoverPicture(picture_path, cover_path)
        
        cover.compose_cover(f'Capa {i}', cover_title, number_of_images, max_letters, letter_color, font_color)
        

