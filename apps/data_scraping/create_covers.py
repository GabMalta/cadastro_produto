import os
from apps.amazon_s3.upload_s3 import upload_folder_to_s3_parallel
from apps.data_scraping.utils.cover_product import CoverProduct
from apps.data_scraping.utils.image_info import image_info
from apps.data_scraping.utils.write_cover_title import write_cover_title


def create_covers(
    path,
    title=None,
    upload_for_s3=False,
    time_color_change=True,
    create_img_info=True,
    company="LEGITIMA",
    name_saved=None,
):
    s3_folder = os.path.join(os.path.basename(path), "Capa")

    cover = CoverProduct(path)

    cover_1 = cover.cover_grid(f"CAPA 1 {'- ' + name_saved if name_saved else ''}")
    cover_2 = cover.cover_grid_2(f"CAPA 2 {'- ' + name_saved if name_saved else ''}")
    cover_3 = cover.cover_grid_3(f"CAPA 3 {'- ' + name_saved if name_saved else ''}")
    cover_4 = cover.cover_three(f"CAPA 4 {'- ' + name_saved if name_saved else ''}")

    if title:
        for capa in [cover_1, cover_2, cover_3, cover_4]:
            write_cover_title(capa, title)

    if create_img_info:
        cover_path = os.path.join(path, "Capa")
        image_info(cover_path, path_info=path, company=company)

    if upload_for_s3:
        if time_color_change:
            input(
                "CASO PRECISE ALTERAR O NOME DAS CORES ANTES DE SUBIR PARA A AWS, A HORA É ESSA..."
            )
        upload_folder_to_s3_parallel(cover_path, s3_folder)
