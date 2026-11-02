import json
import os
from bling_api import BlingApi
import validators
from amazon_s3.upload_s3 import upload_folder_to_s3_parallel
from apps.data_scraping.import_images import import_images
from apps.data_scraping.utils.save_product_json import save_product_json
import settings


def input_choices(choices: dict, question: str) -> str | dict:

    input_choices = "\n".join([f"{key} - {value}" for key, value in choices.items()])

    while True:
        data = input(f"{question}\n{input_choices}\n")

        if data in choices:
            os.system("cls" if os.name == "nt" else "clear")
            return choices[data]

        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("Opção inválida. Por favor, escolha uma das opções acima.")


def input_cod(company: str):
    while True:
        data = input(
            f'INFORME O CÓDIGO REFERENTE AO ARTIGO QUE SERÁ CADASTRADO:\n'
        )
        return data


def input_custom(question: str):
    data = input(f"{question}\n")
    os.system("cls" if os.name == "nt" else "clear")
    return data


def input_path(question: str, accept_empty: bool = False):
    while True:
        path = input(f"{question}\n")

        if os.path.exists(path):
            os.system("cls" if os.name == "nt" else "clear")
            return path
        else:
            if path == "" and accept_empty:
                return path
            print(
                "O CAMINHO INFORMADO ESTÁ INCORRETO OU NÃO EXISTE, INFORME UM CAMINHO DE PASTA VÁLIDO\n"
            )


def input_number(question, tipo: float | int = float):
    while True:
        number = input(f"{question}\n")

        try:
            number = tipo(number)
            os.system("cls" if os.name == "nt" else "clear")
            return number
        except ValueError:
            print(
                f"O VALOR PASSADO DEVE SER UM NÚMERO {'INTEIRO' if tipo == int else ''}"
            )


def input_sizes():
    os.system("cls" if os.name == "nt" else "clear")
    sizes = []
    count = 0
    print(
        "\nDIGITE AS METRAGENS REFERENTE AOS ANUNCIOS QUE SERÃO CRIADOS, QUANDO JÁ TIVER TODAS AS METRAGENS, DIGITE 0 PARA SAIR"
    )
    while True:
        count += 1
        size = input_number(f"\nMETRAGEM DO ANÚNCIO {count}, DIGITE 0 PARA SAIR:\n")

        if size == 0:
            if len(sizes) > 0:
                return sizes
            else:
                count = 0
                print(
                    "VOCÊ DEVE INFORMAR PELO MENOS 1 METRAGEM A CADASTRAR ANTES DE SAIR"
                )
        else:

            sizes.append(size)


def input_dimensions(sizes: list, weight_by_size: float):
    dimensions_and_sizes = []

    for size in sizes:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            width = input_number(f"DIGITE QUAL A LARGURA DO ANUNCIO DE {size} METRO(S)")
            height = input_number(f"DIGITE QUAL A ALTURA DO ANUNCIO DE {size} METRO(S)")
            profundidade = input_number(
                f"DIGITE QUAL A PROFUNDIDADE DO ANUNCIO DE {size} METRO(S)"
            )

            weight = size * weight_by_size

            print(
                f"METRAGEM: {size}\nLARGURA: {width}\nALTURA: {height}\nPROFUNDIDADE: {profundidade}\nPESO: {weight}\n"
            )

            editar = input_choices(
                {"1": "CONTINUAR", "2": "EDITAR"},
                "CONFIRME SE AS INFORMAÇÕES PASSADAS ESTÃO CORRETAS:",
            )

            if editar == "CONTINUAR":
                dimensions_and_sizes.append(
                    {
                        "size": size,
                        "width": width,
                        "height": height,
                        "profundidade": profundidade,
                        "weight": weight,
                    }
                )
                break
    os.system("cls" if os.name == "nt" else "clear")
    return dimensions_and_sizes


def verify_path_product(path=None, upload_for_s3=True):
    while True:
        if path is None:
            path = input_path(
                f"QUAL O CAMINHO ONDE ESTAO AS FOTOS, CAPAS E ARQUIVOS DO PRODUTO?"
            )

        if path == "":
            path = settings.PATH_DEFAULT

        folder_name = path.split("\\")[-1]
        cover_directory = os.path.join(path, "Capa")
        pictures_directory = os.path.join(path, f"{folder_name} - Fotos")
        
        if os.path.exists(cover_directory) or os.path.exists(pictures_directory):
            if os.listdir(pictures_directory):
                break
            os.system("cls" if os.name == "nt" else "clear")
            print(f"A pasta 'Fotos' está vazia.")
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print(
                "O CAMINHO INFORMADO DEVE TER AS PASTAS FOTOS E CAPA COM SUAS RESPECTIVAS IMAGENS DENTRO"
            )

    if not os.path.exists(os.path.join(path, "product_data.json")):
        print(
            "ARQUIVO DE CONFIGURACAO .JSON NAO ENCONTRADO NA PASTA, VAMOS CRIA-LO\n\n"
        )
        fabric_name = input_custom("DIGITE O NOME DO TECIDO:")
        cod = input_custom("DIGITE O CODIGO DO TECIDO:")
        folder_name = input_custom("DIGITE O NOME DA PASTA DO PRODUTO")
        composition = input_custom("DIGITE A COMPOSIÇÃO DO TECIDO:")
        width = input_custom("DIGITE A LARGURA DO TECIDO:")
        price_cost_bruto = input_number("INFORME O PREÇO DE CUSTO BRUTO DO PRODUTO:")
        company = input_choices(settings.COMPANYS, "QUAL É O NOME DO FORNECEDOR PRINCIPAL?")

        data = {
            "fabric_name": fabric_name,
            "cod": cod,
            "folder_name": folder_name,
            "composition": composition,
            "width": width,
            "fornecedor": company['name'],
            "id_fornecedor": company['id_fornecedor'],
            "price_cost_bruto": price_cost_bruto
        }

        with open(
            os.path.join(path, "product_data.json"), "w", encoding="utf-8"
        ) as arq:
            json.dump(data, arq, ensure_ascii=False, indent=4)

    with open(os.path.join(path, "product_data.json"), encoding="utf-8") as arq:
        data = json.load(arq)
    
    if upload_for_s3:
        upload_images = input_choices(
            {"1": "SIM", "2": "NÃO"}, "É NECESSÁRIO SUBIR AS IMAGENS PARA A AWS?"
        )

        if upload_images == "SIM":
            upload_folder_to_s3_parallel(pictures_directory, data["folder_name"])

    product_path = {
        "cover_directory": cover_directory,
        "pictures_directory": pictures_directory,
        "path": path,
    }

    return product_path | data


def import_images_of_company():
    
    company = input_choices(
        settings.COMPANYS, "EM QUAL ATACADO SERÁ FEITA A EXTRAÇÃO DE FOTOS?"
    )
    path_save = input_path(
        f"EM QUAL PASTA SERÁ SALVO OS ARQUIVOS BAIXADOS?\n CASO NÃO SEJA INFORMADO, O CAMINHO PADRÃO SERÁ USADO:\n{settings.PATH_DEFAULT}",
        accept_empty=True,
    )
    if path_save == "":
        path_save = settings.PATH_DEFAULT
    cod_or_url = input_cod(company['name'])
    fabric_name = input_custom("QUAL É O NOME DO TECIDO A SER CADASTRADO?")

    while True:
        try:
            os.system("cls" if os.name == "nt" else "clear")
            print("BAIXANDO IMAGENS...")
            imported_product = import_images(
                company, cod_or_url, fabric_name, path_save, upload_for_s3=True
            )
            user_inputs = {
                "company": company,
                "fabric_name": fabric_name,
            }
            return imported_product | user_inputs
        except Exception as e:
            # os.system("cls" if os.name == "nt" else "clear")
            print("\n", e)
            print("\nINFORME NOVAMENTE AS INFORMAÇÕES")

            if "ATACADO INVÁLIDO" in str(e):
                company = input_choices(
                    settings.COMPANYS, "EM QUAL ATACADO SERÁ FEITA A EXTRAÇÃO DE FOTOS?"
                )

            path_save = input_path("EM QUAL PASTA SERÁ SALVO OS ARQUIVOS BAIXADOS?")
            cod_or_url = input_cod(company)


def profit_for_loja(lojas=settings.LOJAS):

    profit_margin = {}

    for loja in lojas.keys():
        
        profit = input_number(f"QUAL A MARGEM DE LUCRO DA LOJA {loja}? (CASO NÃO DESEJE INFORMAR DIGITE 0)")
        if profit == 0: continue
        
        profit_margin[loja] = profit
        

    return profit_margin

def _str_to_number(key: str):
    try:
        return int(key)
    except ValueError:
        pass
    try:
        return float(key.replace(",", "."))
    except ValueError:
        return None


def criar_estruturas(id_principal: int, api: BlingApi | None = None):

    if not api:
        api = BlingApi()

    metragens = [0.5, 2, 3, 4, 5, 6, 7, 10, 15, 30, 50]

    data = api.get_product(id_principal).get("data")

    if not data:
        print(f"Produto com id {id_principal} não encontrado!")
        return

    produto_principal = {"id": data.get("id"), "codigo": data.get("codigo")}
    variacoes_principal = [
        {
            "id": var.get("id"),
            "sku": var.get("codigo").split("m-")[1],
            "metragem": var.get("codigo").split("m-")[0],
        }
        for var in data["variacoes"]
    ]


    metragem, sku = produto_principal["codigo"].split("m-")

    metragem = _str_to_number(metragem)

    skus_pesquisar = [f"{mt}m-{sku}" for mt in metragens]

    data_produtos_editar = api.get_products({"codigos[]": skus_pesquisar}).get("data")

    if not data_produtos_editar:
        print("sem produtos a editar")
        return

    produtos_editar = [{"id": dt["id"], "codigo": dt["codigo"]} for dt in data_produtos_editar]
    
    for produto_editar in produtos_editar:

        data_editar = api.get_product(produto_editar["id"]).get("data")
        

        variacoes_editar = [{"id": var["id"], "codigo": var["codigo"]} for var in data_editar["variacoes"]]
        
        for var in variacoes_editar:

            metragem_editar = _str_to_number(var["codigo"].split("m-")[0])
            sku_editar = var["codigo"].split("m-")[1]
            
            try:
                variacao_pricipal = [
                    var_princ for var_princ in variacoes_principal if var_princ["sku"] == sku_editar ][0]

                metragem_principal = _str_to_number(variacao_pricipal["metragem"])

                payload = {
                    "formato": "E",
                    "estrutura": {
                        "tipoEstoque": "V",
                        "lancamentoEstoque": "A",
                        "componentes": [
                            {
                                "produto": {"id": variacao_pricipal["id"]},
                                "quantidade": metragem_principal * metragem_editar,
                            }
                        ],
                    },
                }

                api.edit_product(var["id"], payload)

                print(f"{var['codigo']} Editado!")
            except Exception as e:
                print(f"Erro no codigo {var["codigo"]} \n {e}")
