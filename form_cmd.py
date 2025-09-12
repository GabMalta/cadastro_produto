import json
import os

from apps.chat_gpt.create_description import create_description_gpt
from apps.data_scraping.create_covers import create_covers
from apps.data_scraping.utils import save_product_json
from functions import (
    import_images_of_company,
    input_choices,
    input_custom,
    input_dimensions,
    input_number,
    input_sizes,
    verify_path_product,
    profit_for_loja
)
import settings


def form_cmd() -> dict:
    os.system("cls" if os.name == "nt" else "clear")

    operation_type = input_choices(
        {"1": "BAIXAR/CADASTRAR", "2": "CADASTRAR", "3": "BAIXAR"},
        "O QUE DESEJA FAZER?",
    )

    if operation_type == "BAIXAR":
        imported_product = import_images_of_company()
        return {"operation_type": operation_type}

    elif operation_type == "CADASTRAR":
        imported_product = verify_path_product()

    elif operation_type == "BAIXAR/CADASTRAR":
        imported_product = import_images_of_company()

    my_company = input_choices(
        settings.MY_COMPANYS, "PARA QUAL EMPRESA SERÁ FEITO O CADASTRO?"
    )

    fabric_name = imported_product["fabric_name"]

    title_ad = input_custom(
        "DIGITE O TITULO DO ANUNCIO (O ANUNCIO SERA CADASTRADO COM ESSE NOME):"
    )

    if imported_product.get("price_cost_bruto", None):
        cost_price = input_choices({"1":imported_product["price_cost_bruto"], "2":"OUTRO"}, f"O PREÇO DE CUSTO DO TECIDO É R$ {imported_product['price_cost_bruto']}, DESEJA USAR ESSE VALOR?")
        if cost_price == "OUTRO":
            cost_price = input_number("QUAL O PREÇO DE CUSTO DO TECIDO?")
            imported_product["price_cost_bruto"] = cost_price
            save_product_json(imported_product['path'], imported_product)
    else:
        cost_price = input_number("QUAL O PREÇO DE CUSTO DO TECIDO?")
        imported_product["price_cost_bruto"] = cost_price
        save_product_json(imported_product['path'], imported_product)

    if not imported_product.get("id_fornecedor", None):
        fornecedor = input_choices(settings.COMPANYS, "QUAL O FORNECEDOR PRINCIPAL?")
        imported_product["id_fornecedor"] = fornecedor['id_fornecedor']
        imported_product["fornecedor"] = fornecedor['name']
        save_product_json(imported_product['path'], imported_product)

    profit_margin = input_number("QUAL A MARGEM GERAL DE LUCRO DESEJADA?")

    profit_loja = profit_for_loja()

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
                create_cover = False
                break
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print(
                    "A PASTA CAPA NÃO EXISTE OU NÃO CONTEM NENHUM CONTEÚDO, CRIE A PASTA CAPA E ADICIONE AS FOTOS DE CAPA OU PEÇA AO SISTEMA PARA CRIAR AUTOMATICAMENTE."
                )

    with open(os.path.join(path, "product_data.json"), encoding="utf-8") as arq:
        product_json = json.load(arq)

    changed_name = (
        True
        if input_choices(
            {"S": "SIM", "N": "NÃO"}, "O NOME DAS CORES SERÃO OU FORAM ALTERADOS?"
        )
        == "SIM"
        else False
    )

    nome = title_ad if title_ad else f"Tecido {product_json['fabric_name'].title()}"

    desc_gpt = input_choices(
        {"S": True, "N": False},
        "DESEJA ADICIONAR UMA DESCRIÇÃO CRIADA PELO CHAT GPT?",
    )

    desc_gpt = create_description_gpt(nome) if desc_gpt else False

    estoque_padrao = input_number(
        "QUAL A QUANTIDADE ESTOQUE SERÁ CADASTRADO PARA AS VARIAÇÕES?"
    )

    return {
        "operation_type": operation_type,
        "imported_product": imported_product,
        "my_company": my_company,
        "fabric_name": fabric_name,
        "nome": nome,
        "cost_price": cost_price,
        "profit_margin": profit_margin,
        "weight_by_size": weight_by_size,
        "sizes": sizes,
        "sizes_and_dimensions": sizes_and_dimensions,
        "cover_path": cover_path,
        "pictures_path": pictures_path,
        "path": path,
        "create_cover": create_cover,
        "changed_name": changed_name,
        "estoque_padrao": estoque_padrao,
        "desc_gpt": desc_gpt,
        "profit_loja": profit_loja,
        "width": product_json["width"],
        "composition": product_json["composition"],
        "cod": product_json["cod"],
        #"fornecedor": imported_product["fornecedor"],
        "id_fornecedor": imported_product["id_fornecedor"]
    }
