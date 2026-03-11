import json

from bling_api.bling import BlingApi
import pandas as pd


def get_df_custos():
    path_preco_custo = r"C:\Users\gabri\www\extracao_precos\precos_latest.xlsx"
    df = pd.read_excel(path_preco_custo)
    return df


def busca_custo_por_codigo(codigo_produto: str, df: pd.DataFrame) -> float:
    # Buscar preço de custo pelo codigo do produto
    preco_custo = df.loc[df["cod"] == codigo_produto, "preco"].values
    if len(preco_custo) > 0:
        return preco_custo[0]

    return None


bling = BlingApi()
df_custo = get_df_custos()


i = 1
cod_sem_custo = []
while True:

    products = bling.get_products(params={"pagina": i, "limite": 500, "tipo": "V"})["data"]
    if len(products) == 0:
        break

    print("Página:", i)
    df_precos_mudar = []
    for product in products:
        try:
            product_id = product["id"]
            product_metragem = product["codigo"].split("m-")[0]
            product_sku = product["codigo"].split("m-")[1].split("-")[0]
            product_preco_custo = product["precoCusto"]
        except Exception as e:
            print(f"Erro ao processar o produto {product['codigo']}: {e}")
            continue

        preco_custo = busca_custo_por_codigo(product_sku, df_custo)
        if preco_custo is not None:
            try:
                custo_real = round(
                    (preco_custo - (preco_custo * 0.235)) * float(product_metragem.replace(",", ".")), 2
                )
            except Exception as e:
                print(f"Erro ao calcular custo real para o produto {product['codigo']}: {e}")
                continue
            if abs(custo_real - float(product_preco_custo)) > 0.05:
                df_precos_mudar.append(
                    {
                        "id": product_id,
                        "codigo": product["codigo"],
                        "precoCusto": product_preco_custo,
                        "precoCustoReal": custo_real,
                    }
                )
        else:
            cod_sem_custo.append(product_sku)

    if len(df_precos_mudar) > 0:
        try:
            df_precos_mudar_old = pd.read_csv(r"precos_a_mudar.csv")
        except FileNotFoundError:
            df_precos_mudar_old = pd.DataFrame(columns=["id", "codigo", "precoCusto", "precoCustoReal"])

        df_precos_mudar_new = pd.concat(
            [df_precos_mudar_old, pd.DataFrame(df_precos_mudar)], ignore_index=True
        )
        df_precos_mudar_new.to_csv(r"precos_a_mudar.csv", index=False)

    with open("cod_sem_custo.json", "r") as f:
        cod_sem_custo_old = json.load(f)

    cod_sem_custo.extend(cod_sem_custo_old)

    with open("cod_sem_custo.json", "w") as f:
        json.dump(list(set(cod_sem_custo)), f, indent=4)

    i += 1
