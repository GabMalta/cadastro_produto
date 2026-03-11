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

skus_sem_preco = []

for x in os.listdir("produtos_shopee/sem_preco_venda"):
    
    if not os.path.isfile(os.path.join("produtos_shopee/sem_preco_venda", x)):
        continue

    df = pd.read_excel(f"produtos_shopee/sem_preco_venda/{x}", sheet_name="Sheet1")
    
    df["precoVenda"] = df.apply(calcular_preco_venda, axis=1)

    df.to_excel(f"produtos_shopee/sem_preco_venda/{x}", index=False)