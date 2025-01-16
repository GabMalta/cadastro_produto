import os, json
from apps.bling_api.bling import BlingApi
from apps.bling_api.produto import Produto
from apps.data_scraping.import_images import create_covers
from apps.price_generator.price_generator import price_generator
from description.render_template_description import render_template_description
from promocoes.generate_json import generate_json

path = r"D:\SITE LEGITIMA TEXTIL\PROMOCAO 09.24\Tricoline Estampada\TODAS"
pictures_path = os.path.join(path, "Fotos")
cover_path = os.path.join(path, "Capa")
id_deposito_estoque = 10610809064

if "promo.json" in os.listdir(path):
    with open(os.path.join(path, "promo.json"), "r", encoding="utf-8") as arq:
        promo_json = json.load(arq)
else:
    promo_json = generate_json(path, pictures_path)

metragens = sorted(promo_json["sizes"])
promo_min_size = min(
    x for item in promo_json["variations"].values() for x in item["size"]
)
str_promo_min_size = (
    f'{str(int(promo_min_size)).replace(".", ",")}m'
    if promo_min_size >= 1
    else f'{str(promo_min_size).replace(".", ",")}m'
)

price_cost = 16.49
folder_name = "TRICOLINE ESTAMPADA"
tec_title = "Tecido Tricoline Estampada"
titulo = f"PROMOÇÃO {tec_title}"
codigo = f"P-D148"
composition = "100% Algodão"
largura_tec = "1,50"
peso = 0.4
largura = 7
altura = 7
profundidade = 7
description = render_template_description(
    {"larg": largura_tec, "nome": tec_title, "composition": composition},
    desc_gpt=False,
    promo=True,
)

create_covers(
    5, folder_name, cover_path, pictures_path, letter_color="#EE4D2D", promo=True
)


produto = Produto(
    cover_path,
    pictures_path,
    "PROMOCAO",
    "FOLDER_NAME",
    "CODE",
    price_generator(price_cost, 1, 20),
    two_variations=True,
    price_cost=price_cost,
)


produto.name = titulo
produto.folder_name = folder_name
produto.code = codigo
produto.weight = peso
produto.larg = largura
produto.alt - altura
produto.profun = profundidade
produto.description = description
produto.composition = composition
produto.fabric_width = largura_tec
produto.second_variations = [
    int(x) if x >= 1 else str(x).replace(".", ",") for x in metragens
]

product = produto.upload_product()


produto_pai = BlingApi().get_product(product["id_pai"])["data"]


with open("produto_pai.json", "w", encoding="utf-8") as arq:
    json.dump(produto_pai, arq, ensure_ascii=False, indent=4)


for variation in product["variations"]:

    var_tamanho = variation["nome"].split(";")[1]
    var_nome = variation["nome"].split(";")[0].replace("Cor:", "")

    if str_promo_min_size in var_tamanho:

        qtd = promo_json["variations"][var_nome]["amount"] / promo_min_size

        produto.add_estoque(id_deposito_estoque, [variation["id"]], qtd)

        promo_json["variations"][var_nome]["id_min_size"] = variation["id"]

for promo_product in promo_json["variations"]:

    for variacao in produto_pai["variacoes"]:

        if f"Tamanho:{str_promo_min_size}" in variacao["nome"]:
            continue

        if f"Cor:{promo_product}" in variacao["nome"]:

            tamanho = float(
                variacao["nome"].split("Tamanho:")[1].replace(",", ".").replace("m", "")
            )
            qtd = int(tamanho / promo_min_size)

            variacao["formato"] = "E"
            variacao["estrutura"] = {
                "tipoEstoque": "V",
                "lancamentoEstoque": "",
                "componentes": [
                    {
                        "produto": {
                            "id": promo_json["variations"][promo_product]["id_min_size"]
                        },
                        "quantidade": qtd,
                    }
                ],
            }

import time
time.sleep(90)

produto.edit_product(product["id_pai"], produto_pai)
