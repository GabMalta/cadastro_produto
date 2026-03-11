from concurrent.futures import ThreadPoolExecutor
import os

from apps.data_scraping.sites_scraping.requests_site import site_request
from apps.data_scraping.utils.create_save_directory import create_save_directory
from apps.data_scraping.utils.download_picture import download_picture
from apps.data_scraping.utils.save_product_json import save_product_json
from amazon_s3.upload_s3 import upload_folder_to_s3_parallel


def import_images(company: str, cod_or_url: str, fabric_name: str, path: str, upload_for_s3: False):

    while True:
        try:
            product = site_request(cod_or_url, fabric_name, company)
        except Exception as e:
            print(e)
            raise ValueError(e)

        save_path = create_save_directory(path, product["folder_name"])

        from functions import input_number

        product["price_cost_bruto"] = input_number("INFORME O PREÇO DE CUSTO BRUTO POR METRO DO PRODUTO:")

        save_product_json(save_path, product)

        pictures_directory = os.path.join(save_path, f"{save_path.split('\\')[-1]} - Fotos")
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
