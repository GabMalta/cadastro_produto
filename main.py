import json
import os
from apps.bling_api.produto import Produto
from apps.data_scraping.create_covers import create_covers
from description.render_template_description import render_template_description
from apps.price_generator.price_generator import price_generator
from apps.chat_gpt.create_description import create_description_gpt
from functions import *
import settings


def main():

    os.system("cls" if os.name == "nt" else "clear")

    operation_type = input_choices(
        {"1": "BAIXAR/CADASTRAR", "2": "CADASTRAR", "3": "BAIXAR"},
        "O QUE DESEJA FAZER?",
    )

    if operation_type == "BAIXAR":
        while True:
            create_cover = input_choices(
                {"1": "SIM", "2": "NÃO"}, "CRIAR CAPA AUTOMÁTICA PARA O ANÚNCIO?"
            )

            if create_cover == "SIM":
                create_covers(
                    path,
                    fabric_name,
                    upload_for_s3=True,
                    time_color_change=False,
                )
                break
            else:
                break
                # if os.path.exists(cover_path) and os.listdir(cover_path):
                #     break
                # else:
                #     os.system("cls" if os.name == "nt" else "clear")
                #     print(
                #         "A PASTA CAPA NÃO EXISTE OU NÃO CONTEM NENHUM CONTEÚDO, CRIE A PASTA CAPA E ADICIONE AS FOTOS DE CAPA OU PEÇA AO SISTEMA PARA CRIAR AUTOMATICAMENTE."
                #     )
        return import_images_of_company()

    elif operation_type == "CADASTRAR":
        imported_product = verify_path_product()
        my_company = input_choices(
            settings.MY_COMPANYS, "PARA QUAL EMPRESA SERÁ FEITO O CADASTRO?"
        )

    elif operation_type == "BAIXAR/CADASTRAR":
        imported_product = import_images_of_company()

    my_company = input_choices(
        settings.MY_COMPANYS, "PARA QUAL EMPRESA SERÁ FEITO O CADASTRO?"
    )

    id_deposito = settings.MY_COMPANY_SETTINGS[my_company]["id_deposito"]
    letter_color = settings.MY_COMPANY_SETTINGS[my_company]["letter_color"]

    fabric_name = imported_product["fabric_name"]
    title_ad = input_custom(
        "DIGITE O TITULO DO ANUNCIO (O ANUNCIO SERA CADASTRADO COM ESSE NOME):"
    )
    cost_price = input_number("QUAL O PREÇO DE CUSTO DO TECIDO?")
    profit_margin = input_number("QUAL A MARGEM DE LUCRO DESEJADA?")

    weight_by_size = input_number("QUAL O PESO POR METRO DO TECIDO?")

    sizes = input_sizes()
    sizes_and_dimensions = input_dimensions(sizes, weight_by_size)

    cover_path = imported_product["cover_directory"]
    pictures_path = imported_product["pictures_directory"]
    path = imported_product["path"]

    while True:
        create_cover = input_choices(
            {"1": "SIM", "2": "NÃO"}, "CRIAR CAPA AUTOMÁTICA PARA O ANÚNCIO?"
        )

        if create_cover == "SIM":
            break
        else:
            if os.path.exists(cover_path) and os.listdir(cover_path):
                break
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print(
                    "A PASTA CAPA NÃO EXISTE OU NÃO CONTEM NENHUM CONTEÚDO, CRIE A PASTA CAPA E ADICIONE AS FOTOS DE CAPA OU PEÇA AO SISTEMA PARA CRIAR AUTOMATICAMENTE."
                )

    with open(
        os.path.join(imported_product["path"], "product_data.json"), encoding="utf-8"
    ) as arq:
        product_json = json.load(arq)

    changed_name = (
        True
        if input_choices(
            {"S": "SIM", "N": "NÃO"}, "O NOME DAS CORES SERÃO OU FORAM ALTERADOS?"
        )
        == "SIM"
        else False
    )

    produto = Produto(
        cover_path,
        pictures_path,
        f"Tecido {product_json['fabric_name'].title()}",
        product_json["fabric_name"].title(),
        "1",
        product_json["cod"],
        0.00,
    )

    nome = title_ad if title_ad else f"Tecido {product_json['fabric_name'].title()}"
    
    desc_gpt = input_choices(
        {"S": "SIM", "N": "NÃO"},
        "DESEJA ADICIONAR UMA DESCRIÇÃO CRIADA PELO CHAT GPT?",
    )
    
    desc_gpt = create_description_gpt(nome) if desc_gpt == "SIM" else False

    estoque_padrao = input_number(
        "QUAL A QUANTIDADE ESTOQUE SERÁ CADASTRADO PARA AS VARIAÇÕES?"
    )

    for i, info in enumerate(sizes_and_dimensions):
        if create_cover:
            for arq in os.listdir(cover_path):
                path_remove = os.path.join(cover_path, arq)
                if os.path.isfile(path_remove):
                    os.remove(path_remove)
        
            create_covers(
                    path,
                    fabric_name,
                    upload_for_s3=True,
                    time_color_change=False,
                    create_img_info=True,
                    name_saved=f'CAPA ({info['size']}m {i+1})'
                )
            
        info["size"] = int(info["size"]) if info["size"].is_integer() else info["size"]

        description = render_template_description(
            {
                "mt": info["size"],
                "larg": product_json["width"],
                "nome": nome,
                "composition": product_json["composition"],
                "desc_gpt": desc_gpt
            },
        )

        produto.name = (
            f"{info['size']} Metros {nome} ({info['size']}m x {product_json["width"]}m)"
        )
        produto.folder_name = product_json["fabric_name"].title()
        produto.quantidade = f'{info['size']}m x {product_json['width']}m'
        produto.code = f'{info['size']}m-{product_json["cod"]}'
        produto.price = price_generator(cost_price, info["size"], profit_margin, tax=5)
        produto.weight = info["weight"]
        produto.larg = info["width"]
        produto.alt - info["height"]
        produto.profun = info["profundidade"]
        produto.description = description
        produto.composition = product_json["composition"]
        produto.fabric_width = product_json["width"]

        product = produto.upload_product(changed_name=changed_name)

        id_products = [data["id"] for data in product["variations"]]

        produto.add_estoque(id_deposito, id_products, estoque_padrao)


if __name__ == "__main__":
    main()
