import pandas as pd
from price_generator import calculate_price
import os

df_custos = pd.read_csv(r"C:\Users\gabri\www\extracao_precos\precos2.csv", sep=";", encoding="utf-8-sig")
def calcular_preco_venda(row):    
        try:
            custo = float(row["custos"])
            preco_venda = calculate_price(custo, float(row["Metragem"]), 20)  
            return preco_venda[0]
        except ValueError:
            return None

df = pd.read_excel(r"C:\Users\gabri\Downloads\descontos em massa.xlsx", sheet_name="Sheet1")

df["custos"] = df["SKU"].map(df_custos.set_index("cod")["preco"])
df["custos"] = df["custos"].apply(
    lambda x: float(x.replace("R$", "").replace(",", ".").strip()) if pd.notnull(x) else None
)
df["preco_novo"] = df.apply(calcular_preco_venda, axis=1)

df.to_excel("produtos_shopee/precos_calculados.xlsx", index=False)