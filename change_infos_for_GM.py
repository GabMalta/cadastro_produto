from excel_pandas import change_infos_for_GM
import pandas as pd
import os

path_excel = r"C:\Users\gabri\Downloads\PRODUTOS GM.csv"
path_catalogo = r"D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL"

df = pd.read_csv(path_excel, sep=";")


def get_path(sku):
    
    arquivos = os.listdir(path_catalogo)
    for path in arquivos:
        if path.endswith(sku):
            return path
    return None

def format_metragem(x):
    x = float(x)
    return int(x) if x.is_integer() else x

df["sku"] = df["Código"].apply(lambda x: x.split("m-")[-1].strip())
df["metragem"] = df["Código"].apply(lambda x: x.split("m-")[0].strip())
df["path"] = df["sku"].apply(get_path)


resultado = (
    df.groupby("sku")
      .agg({
          "metragem": lambda x: [format_metragem(v) for v in x],
          "path": "first"
      })
      .reset_index()
      .rename(columns={"metragem": "metragens"})
      .to_dict(orient="records")
)

names = []
nao_encontrados = []

for item in resultado:
    sku = item["sku"]
    metragens = item["metragens"]
    path = item["path"]
    name = " ".join(path.split(" ")[:-1]) if path is not None else None
    
    if path is not None and name is not None:
        names.append((path, sku, name, metragens, 0))
        
    else:
        nao_encontrados.append(sku)
        
if nao_encontrados:
    print("SKUs não encontrados:", nao_encontrados)
    input("Pressione Enter para continuar...")

change_infos_for_GM(names)
