import json
import os
from typing import List
import pandas as pd

from apps.data_scraping.create_covers import create_covers
from functions import input_choices
from generate_price_multiloja import alterar_preco_multiloja
from generate_title_with_ia import generate_title_variations


def excluir_arq_pasta(path):
    for arq in os.listdir(os.path.join(path, "Capa")):
        path_remove = os.path.join(path, "Capa", arq)
        if os.path.isfile(path_remove):
            os.remove(path_remove)


def mudar_titulo(title):
    while True:
        choices = generate_title_variations(title, number_of_variations=10)
        new_title = input_choices(choices, "QUAL TÍTULO DESEJA UTILIZAR?")

        if new_title:
            from prompt_toolkit import prompt

            new_title = prompt("EDITE O TITULO SE PRECISAR:\n", default=new_title)

            if new_title:
                return new_title

        restart = input_choices(
            {"1": "GERAR NOVAMENTE", "2": "NÃO MUDAR O TITULO"},
            "DESEJA GERAR NOVAMENTE O TÍTULO?",
        )

        if restart == "NÃO MUDAR O TITULO":
            return None


def change_infos_for_GM(names: List):
    df = pd.read_csv(r"C:\Users\gabri\Downloads\PRODUTOS GM.csv", sep=";", encoding="utf-8-sig")
    df["Código"] = df["Código"].astype(str)
    for name in names:
        print(name)
        path_name, cod, title, mt, price_cost, change_title = name
        path = os.path.join(r"D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL", path_name)

        if price_cost > 0:
            print("ALTERANDO PREÇO")
            alterar_preco_multiloja(cod, mt, price_cost)

        excluir_arq_pasta(path)

        if change_title:
            new_title = mudar_titulo(f"Tecido {title.capitalize()}")

        for i, m in enumerate(mt, start=1):

            cod_ = f"{m}m-{cod}"
            print(cod_)
            create_covers(
                path,
                title,
                upload_for_s3=True,
                time_color_change=False,
                company="GM",
                font_color="#000",
                stroke_fill="white",
                fill="#FF4433",
                name_saved=f"CAPA ({m}m {i+1})",
                create_img_info=True,
            )

            with open(os.path.join(path, "Capa", "image_urls.json"), "r", encoding="utf-8") as arq:
                links = json.load(arq)

            text = "|".join([value["img"] for _, value in links.items()])

            df.loc[df["Código"].str.strip().eq(cod_), "URL Imagens Externas"] = text

            if new_title:

                with open(os.path.join(path, "product_data.json"), "r", encoding="utf-8") as arq:
                    info_product = json.load(arq)
                    width_product = info_product["width"]

                os.system("cls" if os.name == "nt" else "clear")

                new_title_formated = f"{m} {'Metros' if float(str(m).replace(',', '.')) > 1 else 'Metro'} {new_title} ({m}m x {width_product}m)"

                df.loc[df["Código"].str.strip().eq(cod_), "Descrição"] = new_title_formated
                print("\n", new_title_formated)

            excluir_arq_pasta(path)

    df.to_csv(
        r"C:\Users\gabri\Downloads\PRODUTOS GM_EDITED.csv",
        sep=";",
        encoding="utf-8-sig",
        index=False,
    )
