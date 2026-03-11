import json
import os
from amazon_s3.upload_s3 import upload_folder_to_s3_parallel
from bling_api.bling import BlingApi
from bling_api.schemas.fornecedor import Contato, Fornecedor
from bling_api.schemas.vinculo_produto_loja import ProdutoLojaSchema
from apps.data_scraping.create_covers import create_covers
from description.render_template_description import render_template_description
from price_generator.price_generator import calculate_price

# from apps.chat_gpt.create_description import create_description_gpt
from form_cmd import form_cmd

# from functions import input_choices, input_number
from bling_api.schemas.produto import ProdutoSchema
from functions import input_choices
from generate_recommended_uses import gerar_usos_tecido
import settings
from utils.compose_variations import compose_variations
from utils.get_covers_urls import get_covers_urls


def main():

    bling = BlingApi()

    form_response = form_cmd()

    if form_response["operation_type"] == "BAIXAR":
        return

    try:
        print("Gerando usos recomendados...")
        usos_recomendados = gerar_usos_tecido(form_response["fabric_name"], form_response["composition"])
        print("Usos recomendados gerados com sucesso! -> ", usos_recomendados)
    except Exception as e:
        print(f"Erro ao gerar usos recomendados: {e}")
        usos_recomendados = ""
    
    capa_ia = input_choices({"1": "Sim", "2": "Não"}, "Criou capas com IA?")
    for i, info in enumerate(form_response["sizes_and_dimensions"]):
        if form_response["create_cover"]:
            for arq in os.listdir(form_response["cover_path"]):
                path_remove = os.path.join(form_response["cover_path"], arq)
                if os.path.isfile(path_remove) and not arq.startswith("IA_"):
                    os.remove(path_remove)

            create_covers(
                form_response["path"],
                form_response["fabric_name"],
                upload_for_s3=True,
                time_color_change=False,
                create_img_info=True,
                fill=None,
                font_color=None,
                stroke_fill="black",
                name_saved=f"CAPA ({info['size']}m {i+1})",
            )

            

            if capa_ia == "Sim":
                s3_folder = os.path.join(os.path.basename(form_response["path"]), "Capa")
                cover_path = os.path.join(form_response["path"], "Capa")
                upload_folder_to_s3_parallel(cover_path, s3_folder)

        info["size"] = int(info["size"]) if info["size"].is_integer() else info["size"]

        description = render_template_description(
            {
                "mt": info["size"],
                "larg": form_response["width"],
                "nome": form_response["nome"],
                "composition": form_response["composition"],
                "desc_gpt": form_response["desc_gpt"],
            },
        )

        folder_name = form_response["fabric_name"].title()
        covers = get_covers_urls(folder_name, form_response["cover_path"])
        price, cost = calculate_price(
            form_response["cost_price"],
            info["size"],
            form_response["profit_margin"],
            imposto=5,
        )

        codigo = f'{info['size']}m-{form_response["cod"]}'

        produto = ProdutoSchema(
            codigo=codigo,
            nome=f"{info['size']} {'Metros' if int(info['size']) > 1 else 'Metro'} {form_response['nome']} ({info['size']}m x {form_response["width"]}m)",
            preco=price,
            fornecedor={
                "id": 720948394,
                "contato": {"id": 13203733926, "nome": "Aquarela"},
                "codigo": "",
                "precoCusto": 11.49,
                "precoCompra": 11.49,
            },
            descricaoCurta=description,
            pesoLiquido=info["weight"],
            pesoBruto=info["weight"],
            dimensoes={
                "largura": info["width"],
                "altura": info["height"],
                "profundidade": info["profundidade"],
            },
            midia={"imagens": {"imagensURL": covers}},
            variacoes=[],
        )

        variations = compose_variations(
            produto,
            form_response["pictures_path"],
            form_response["changed_name"],
        )
        

        produto.variacoes = variations
        produto.camposCustomizados[2].valor = f"{info['size']}m x {form_response['width']}m"
        produto.camposCustomizados[3].valor = form_response["fabric_name"]
        produto.camposCustomizados[4].valor = "Tecido"
        produto.camposCustomizados[5].valor = form_response["composition"]
        produto.camposCustomizados[6].valor = str(info["size"])
        produto.camposCustomizados[12].valor = "Legítima Têxtil"
        produto.camposCustomizados[15].valor = usos_recomendados
        produto.camposCustomizados[16].valor = str(info["weight"])
        produto.camposCustomizados[20].valor = "x".join(
            [str(int(x)) for x in (info["width"], info["height"], info["profundidade"])]
        )
        
        with open("produto.json", "w", encoding="utf-8") as f:
            json.dump(produto.model_dump(), f, ensure_ascii=False, indent=4)
        
        try:
        
            product_and_variations = bling.create_product(produto)

            if len(form_response["profit_loja"].items()) > 0:

                for i, variation in enumerate(product_and_variations["variations"]):

                    for loja, profit_margin in form_response["profit_loja"].items():
                        price, _ = calculate_price(
                            form_response["cost_price"],
                            info["size"],
                            profit_margin,
                            tax=5,
                        )

                        produto = ProdutoLojaSchema(
                            preco=price,
                            precoPromocional=price,
                            idProduto=variation["id"],
                            idLoja=settings.LOJAS[loja],
                        )
                        if i == 0:
                            produto.idProduto = product_and_variations["id_pai"]
                            bling.create_link_with_store(produto)
                            print("Multiloja para produto produto pai criada!")
                            produto.idProduto = variation["id"]

                        bling.create_link_with_store(produto)
                        print(f"Preço {loja} para {variation['nome']} criada!")

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
