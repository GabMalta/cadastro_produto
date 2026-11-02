import os
import random
from amazon_s3.upload_s3 import upload_folder_to_s3_parallel
from apps.data_scraping.utils.cover_product import CoverProduct
from apps.data_scraping.utils.image_info import image_info
from apps.data_scraping.utils.write_cover_title import write_cover_title
from apps.data_scraping.utils.color_utils import gerar_cores_legiveis


def create_covers(
    path,
    title=None,
    upload_for_s3=False,
    time_color_change=True,
    create_img_info=True,
    company="LEGITIMA",
    name_saved=None,
    fill=None,
    stroke_fill="#fff",
    stroke_width=5,
    font_color=None,
    promocao=False,
):

    # if not fill and not font_color:
    #     fill, font_color = gerar_cores_legiveis()

    s3_folder = os.path.join(os.path.basename(path), "Capa")

    cover = CoverProduct(path, promocao=promocao)

    cover_1 = cover.cover_grid(
        f"CAPA 1{' - ' + name_saved if name_saved else ''}",
        title=title,
        fill=fill,
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
        font_color=font_color,
    )
    cover_2 = cover.cover_grid_2(
        f"CAPA 2{' - ' + name_saved if name_saved else ''}",
        title=title,
        fill=fill,
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
        font_color=font_color,
    )
    cover_3 = cover.cover_grid_3(
        f"CAPA 3{' - ' + name_saved if name_saved else ''}",
        title=title,
        fill=fill,
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
        font_color=font_color,
    )
    cover_4 = cover.cover_three(
        f"CAPA 4{' - ' + name_saved if name_saved else ''}",
        title=title,
        fill=fill,
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
        font_color=font_color,
    )
    cover_5 = cover.cover_full_logo(
        title, f"CAPA 5 {'- ' + name_saved if name_saved else ''}", company=company
    )

    cover_6 = cover.layout_faixa_horizontal(
        f"CAPA 6{' - ' + name_saved if name_saved else ''}", title=title, fill=fill, font_color=font_color
    )
    
    cover_7 = cover.cover_diagonal_stripes(
        f"CAPA 7{' - ' + name_saved if name_saved else ''}", title=title, fill=fill, font_color=font_color
    )

    cover_8 = cover.cover_wave_stripes(
        f"CAPA 8{' - ' + name_saved if name_saved else ''}", title=title, fill=fill, font_color=font_color
    )
    cover_9 = cover.cover_zigzag_stripes(
        f"CAPA 9{' - ' + name_saved if name_saved else ''}", title=title, fill=fill, font_color=font_color
    )


    if create_img_info:
        cover_path = os.path.join(path, "Capa")
        image_info(
            cover_path,
            path_info=path,
            company=company,
        )

    if upload_for_s3:
        print(cover_5)
        covers = [
            cover
            for cover in (cover_1, cover_2, cover_3, cover_4, cover_5, cover_6, cover_7, cover_8, cover_9)
            if cover and os.path.exists(cover)
        ]

        while len(covers) > 3:
            path_remove = random.choice(covers)
            covers.remove(path_remove)
            os.remove(path_remove)

        covers_random = random.sample(covers, len(covers))

        for i, cover in enumerate(covers_random, start=1):
            path = os.path.dirname(cover)
            name = os.path.basename(cover)

            new_name = os.path.join(path, f"{i}-{name}")

            os.rename(cover, new_name)

        if time_color_change:
            input("CASO PRECISE ALTERAR O NOME DAS CORES ANTES DE SUBIR PARA A AWS, A HORA É ESSA...")

        upload_folder_to_s3_parallel(cover_path, s3_folder)
