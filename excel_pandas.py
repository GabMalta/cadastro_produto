import json
import os
from typing import List
import pandas as pd

from apps.data_scraping.create_covers import create_covers
from functions import input_choices
from generate_price_multiloja import alterar_preco_multiloja


def excluir_arq_pasta(path):
    for arq in os.listdir(os.path.join(path, "Capa")):
        if not arq.startswith("IA_"):
            path_remove = os.path.join(path, "Capa", arq)
            if os.path.isfile(path_remove):
                os.remove(path_remove)


def change_infos_for_GM(names: List):

    df = pd.read_csv(r"C:\Users\gabri\Downloads\PRODUTOS GM.csv", sep=";", encoding="utf-8-sig")
    df["Código"] = df["Código"].astype(str)
    for name in names:
        try:
            print(name)
            path_name, cod, title, mt, price_cost = name
            path = os.path.join(r"D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL", path_name)

            if price_cost > 0:
                print("ALTERANDO PREÇO")
                alterar_preco_multiloja(cod, mt, price_cost)

            excluir_arq_pasta(path)

            for i, m in enumerate(mt, start=1):

                cod_ = f"{m}m-{cod}"
                print(cod_)
                create_covers(
                    path,
                    title,
                    upload_for_s3=True,
                    time_color_change=False,
                    company="GM",
                    font_color=None,
                    stroke_fill=None,
                    fill=None,
                    name_saved=f"CAPA ({m}m {i+1})",
                    create_img_info=True,
                )

                with open(os.path.join(path, "Capa", "image_urls.json"), "r", encoding="utf-8") as arq:
                    links = json.load(arq)

                text = "|".join([value["img"] for _, value in links.items()])

                df.loc[df["Código"].str.strip().eq(cod_), "URL Imagens Externas"] = text

                excluir_arq_pasta(path)
        except Exception as e:
            try:
                error = {"Código": [cod], "Erro": [str(e)]}
                df_error = pd.read_csv(
                    r"C:\Users\gabri\Downloads\PRODUTOS GM_ERROR.csv", sep=";", encoding="utf-8-sig"
                )
                df_error = pd.concat(
                    [df_error, pd.DataFrame(error)], ignore_index=True
                )
            except FileNotFoundError:
                df_error = pd.DataFrame(error)

            df_error.to_csv(
                r"C:\Users\gabri\Downloads\PRODUTOS GM_ERROR.csv",
                sep=";",
                encoding="utf-8-sig",
                index=False,
            )

    df.to_csv(
        r"C:\Users\gabri\Downloads\PRODUTOS GM_EDITED.csv",
        sep=";",
        encoding="utf-8-sig",
        index=False,
    )
