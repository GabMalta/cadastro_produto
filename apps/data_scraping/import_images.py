from concurrent.futures import ThreadPoolExecutor
import os

from apps.data_scraping.sites_scraping.requests_site import site_request
from apps.data_scraping.sites_scraping.pitangui import pitangui_scraping
from apps.data_scraping.sites_scraping.aquarela import aquarela_scraping
from apps.data_scraping.utils.create_save_directory import create_save_directory
from apps.data_scraping.utils.download_picture import download_picture
from apps.data_scraping.utils.save_product_json import save_product_json
from apps.amazon_s3.upload_s3 import upload_folder_to_s3_parallel

import settings


def import_images(
    company: str, cod_or_url: str, fabric_name: str, path: str, upload_for_s3: False
):
    from functions import input_choices

    while True:
        try:
            match company['name'].upper():
                case "DISPARADA":
                    product = site_request(cod_or_url, fabric_name, company)
                case "PITANGUI":
                    product = pitangui_scraping(cod_or_url, fabric_name, company)
                case "AQUARELA":
                    product = aquarela_scraping(cod_or_url, fabric_name, company)
                case "JANON":
                    product = site_request(cod_or_url, fabric_name, company)
                case "JR ANDRADE":
                    product = site_request(cod_or_url, fabric_name, company)
                case "CHARMY":
                    product = site_request(cod_or_url, fabric_name, company)
                case "ACTUAL":
                    product = site_request(cod_or_url, fabric_name, company)
                case _:
                    raise ValueError("ATACADO INVÁLIDO")
        except Exception as e:

            raise ValueError(e)

        save_path = create_save_directory(path, product["folder_name"])
        
        from functions import input_number

        product["price_cost_bruto"] = input_number("INFORME O PREÇO DE CUSTO BRUTO POR METRO DO PRODUTO:")

        save_product_json(save_path, product)

        pictures_directory = os.path.join(save_path, "Fotos")
        cover_directory = os.path.join(save_path, "Capa")

        with ThreadPoolExecutor(5) as executor:
            files_to_download = [
                (
                    arq["url_img"],
                    os.path.join(pictures_directory, arq["name"] + "." + arq["format"]),
                )
                for arq in product["pictures"]
            ]
            executor.map(lambda args: download_picture(*args), files_to_download)
            
        break

    if upload_for_s3:
        input(
            "SE PRECISAR FAZER ALTERAÇÕES NA PASTA, COMO NOME DE COR, ETC... FAÇA E DEPOIS PRESSIONE ENTER PARA FAZER UPLOAD DOS ARQUIVOS..."
        )
        upload_folder_to_s3_parallel(pictures_directory, product["folder_name"])

    return {
        "path": save_path,
        "pictures_directory": pictures_directory,
        "cover_directory": cover_directory,
    }
