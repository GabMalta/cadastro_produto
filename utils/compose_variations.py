import os
from bling_api.schemas.produto import ProdutoSchema
from bling_api.schemas.variacao import Variacao
from utils.generate_colorname_and_codsku import generate_colorname_and_codsku
from utils.get_image_json import get_image_json
from utils.path_is_image import path_is_image
from typing import List


def compose_variations(produto_pai: ProdutoSchema, path_variations, changed_name=True, variacao_tamanho=False) -> List[Variacao]:

    folder = os.listdir(path_variations)
    variations = []

    for color in folder:
        path_color = os.path.join(path_variations, color)

        if "desktop.ini" in color or not path_is_image(path_color):
            continue

        color_name, cod_sku = generate_colorname_and_codsku(color, changed_name)
        image_url = ""

        if "image_urls.json" in folder:
            img_json = get_image_json(os.path.join(path_variations, "image_urls.json"))

            if img_json:
                for img in img_json.items():
                    if img[0] == color_name:
                        image_url = img[1]["img"]
                        break
                    
        if variacao_tamanho:
            for tam, price in variacao_tamanho:
                
                tam = str(int(tam))
                
                variation = Variacao(
                nomeVariacao=f"Cor:{color_name};Tamanho:{tam}m",
                codigo=f"{produto_pai.codigo}-{tam}m-{cod_sku}",
                preco=price,
                precoCusto=produto_pai.fornecedor.precoCusto,
                pesoLiquido=produto_pai.pesoLiquido,
                pesoBruto=produto_pai.pesoBruto,
                marca=produto_pai.marca,
                fornecedor=produto_pai.fornecedor,
                dimensoes=produto_pai.dimensoes,
                tributacao=produto_pai.tributacao,
                midia={"imagens": {"imagensURL": [{"link": image_url}]}},
            )

                variations.append(variation)
            
        else:
            
            variation = Variacao(
                nomeVariacao=f"Cor:{color_name}",
                codigo=f"{produto_pai.codigo}-{cod_sku}",
                preco=produto_pai.preco,
                precoCusto=produto_pai.fornecedor.precoCusto,
                pesoLiquido=produto_pai.pesoLiquido,
                pesoBruto=produto_pai.pesoBruto,
                marca=produto_pai.marca,
                fornecedor=produto_pai.fornecedor,
                dimensoes=produto_pai.dimensoes,
                tributacao=produto_pai.tributacao,
                midia={"imagens": {"imagensURL": [{"link": image_url}]}},
            )

            variations.append(variation)

    return variations
