import json
import os
import validators
from apps.amazon_s3.upload_s3 import upload_folder_to_s3_parallel
from apps.data_scraping.import_images import import_images
from apps.data_scraping.utils.save_product_json import save_product_json
import settings


def input_choices(choices: dict, question: str) -> str:

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
    url_request = True if company == "AQUARELA" else False

    while True:
        data = input(
            f'INFORME {"A URL" if url_request else "O CÓDIGO"} REFERENTE AO ARTIGO QUE SERÁ CADASTRADO:\n'
        )

        if url_request:
            if validators.url(data):
                return data
            else:
                print("URL inválida! Por favor, informe uma URL válida.")
        else:
            return data


def input_custom(question: str):
    data = input(f"{question}\n")
    os.system("cls" if os.name == "nt" else "clear")
    return data


def input_path(question: str):
    while True:
        path = input(f"{question}\n")

        if os.path.exists(path):
            os.system("cls" if os.name == "nt" else "clear")
            return path
        else:
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


def verify_path_product():
    while True:
        path = input_path(
            "QUAL O CAMINHO ONDE ESTAO AS FOTOS, CAPAS E ARQUIVOS DO PRODUTO?"
        )

        cover_directory = os.path.join(path, "Capa")
        pictures_directory = os.path.join(path, "Fotos")

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
        print("ARQUIVO DE CONFIGURACAO .JSON NAO ENCONTRADO NA PASTA, VAMOS CRIA-LO")
        fabric_name = input_custom("DIGITE O NOME DO TECIDO:")
        cod = input_custom("DIGITE O CODIGO DO TECIDO:")
        folder_name = input_custom("DIGITE O NOME DA PASTA DO PRODUTO")
        composition = input_custom("DIGITE A COMPOSIÇÃO DO TECIDO:")
        width = input_custom("DIGITE A LARGURA DO TECIDO:")

        data = {
            "fabric_name": fabric_name,
            "cod": cod,
            "folder_name": folder_name,
            "composition": composition,
            "width": width,
        }

        with open(os.path.join(path, "product_data.json"), "w", encoding="utf-8") as arq:
            json.dump(data, arq, ensure_ascii=False, indent=4)
    
    with open(os.path.join(path, "product_data.json"), encoding="utf-8") as arq:
        data = json.load(arq)

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
    path_save = input_path("EM QUAL PASTA SERÁ SALVO OS ARQUIVOS BAIXADOS?")
    cod_or_url = input_cod(company)
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
                "path_save": path_save,
                "fabric_name": fabric_name,
            }
            return imported_product | user_inputs
        except Exception as e:
            #os.system("cls" if os.name == "nt" else "clear")
            print("\n", e)
            print("\nINFORME NOVAMENTE AS INFORMAÇÕES")

            if "ATACADO INVÁLIDO" in str(e):
                company = input_choices(
                    settings.COMPANYS, "EM QUAL ATACADO SERÁ FEITA A EXTRAÇÃO DE FOTOS?"
                )

            path_save = input_path("EM QUAL PASTA SERÁ SALVO OS ARQUIVOS BAIXADOS?")
            cod_or_url = input_cod(company)
