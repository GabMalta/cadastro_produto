import pandas as pd
from price_generator import calculate_price
import os

df_custos = pd.read_csv(r"C:\Users\gabri\www\extracao_precos\precos2.csv", sep=";", encoding="utf-8-sig")
def calcular_preco_venda(row):    
        try:
            custo = float(row["custos"])
            preco_venda = calculate_price(custo, float(row["metragem"]), 20)  
            return preco_venda[0]
        except ValueError:
            if row.name <= 4:
                return 0
            return None

for x in os.listdir("produtos_shopee"):
    
    if not os.path.isfile(os.path.join("produtos_shopee", x)):
        continue

    df = pd.read_excel(f"produtos_shopee/{x}", sheet_name="Sheet1")

    df["metragem"] = df["et_title_variation_sku"].str.split("m-").str[0]
    df["codigo"] = df["et_title_variation_sku"].str.split("m-").str[1].str.split("-").str[0].str.upper()
    df["custos"] = df["codigo"].map(df_custos.set_index("cod")["preco"])
    df["custos"] = df["custos"].apply(
        lambda x: float(x.replace("R$", "").replace(",", ".").strip()) if pd.notnull(x) else None
    )
    df["precoVenda"] = df.apply(calcular_preco_venda, axis=1)

    # Gerar um dataframe apenas com os produtos que nao possuem preco de venda calculado
    df_sem_preco_venda = df[df["precoVenda"].isnull()]

    #gerar um dataframe apenas com os produtos que possuem preco de venda calculado a partir da linha
    df_com_preco_venda = df[df["precoVenda"].notnull()]

    # Salvar os dataframes em arquivos separados
    df_sem_preco_venda.to_excel(f"produtos_shopee/sem_preco_GM/{x}", index=False)
    df_com_preco_venda.to_excel(f"produtos_shopee/com_preco_GM/{x}", index=False)
