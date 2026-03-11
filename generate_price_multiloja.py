from bling_api.schemas.vinculo_produto_loja import ProdutoLojaSchema
from bling_api.bling import BlingApi
from price_generator.price_generator import calculate_price
from functions import profit_for_loja
import settings

bling = BlingApi()


def alterar_preco_multiloja(codigo: str, metragens: list[str], preco_custo: float):

    params = [("codigos[]", f"{mt}m-{codigo}") for mt in metragens]

    produtos_pai = bling.get_products(params=params)

    produtos = []
    for produto in produtos_pai["data"]:

        produto_var = bling.get_product(produto["id"])

        id_variacoes = [var["id"] for var in produto_var["data"]["variacoes"]]
        id_pai = produto["id"]
        metragem = produto["codigo"].split("-")[0].replace("m", "")

        produtos.append({"id_pai": id_pai, "id_variacoes": id_variacoes, "metragem": metragem})

    margem_por_loja = profit_for_loja()

    print(margem_por_loja)

    for produto in produtos:

        for loja, margem in margem_por_loja.items():

            preco_venda, _ = calculate_price(preco_custo, float(produto["metragem"]), margem)

            produto_loja = ProdutoLojaSchema(
                preco=preco_venda,
                precoPromocional=preco_venda,
                idProduto=produto["id_pai"],
                idLoja=settings.LOJAS[loja],
            )
            try:
                bling.create_link_with_store(produto_loja)
                print(f"Produto PAI cadastrado na loja {loja}")
            except Exception as e:
                print(e)
            bling.create_link_with_store(produto_loja)

            for i, id_variacao in enumerate(produto["id_variacoes"]):
                produto_loja.idProduto = id_variacao
                try:
                    bling.create_link_with_store(produto_loja)
                    print(f"VARIACAO {i + 1} cadastrado na loja {loja}")
                except Exception as e:
                    print(e)

        print(f"PRODUTO COM {produto['metragem']} METROS CADASTRADO COM SUCESSO")


alterar_preco_multiloja("P316", [3], 4.99)
