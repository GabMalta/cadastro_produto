# from apps.bling_api.bling import BlingApi
# import json

# bling = BlingApi()

# total_pages = 572

# for page in range(1, total_pages + 1):

#     contatos = bling.get_contacts(pagina=page)["data"]

#     contatos_telefone = ["Pagina 0 de 0"]

#     for contato in contatos:
#         if contato["telefone"] or contato["celular"]:
#             contatos_telefone.append(
#                 {"nome": contato["nome"], "telefone": contato["telefone"], "celular": contato["celular"]}
#             )

#     contatos_telefone[0] = f"Pagina {page} de {total_pages}"

#     with open("contatos_telefone.json", "r") as f:
#         contatos_telefone_json = json.load(f)

#     contatos_telefone_json.extend(contatos_telefone)

#     with open("contatos_telefone.json", "w") as f:
#         json.dump(contatos_telefone_json, f, indent=4)

#     print(len(contatos_telefone))


import json
import pandas as pd

def clean_phone_number(phone_number):
    return phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "").strip()

def normalize_phone_number(phone_number):
    cleaned_number = clean_phone_number(phone_number)
    if len(cleaned_number) == 10:
        return f"+55 {cleaned_number[:2]} {cleaned_number[2:6]}-{cleaned_number[6:]}"
    elif len(cleaned_number) == 11:
        return f"+55 {cleaned_number[:2]} {cleaned_number[2:7]}-{cleaned_number[7:]}"
    elif len(cleaned_number) == 12:
        return f"+{cleaned_number[:2]} {cleaned_number[2:4]} {cleaned_number[4:8]}-{cleaned_number[8:]}"
    elif len(cleaned_number) == 13:
        return f"+{cleaned_number[:2]} {cleaned_number[2:4]} {cleaned_number[4:9]}-{cleaned_number[9:]}"
    else:
        return phone_number
    

with open("contatos_telefone.json", "r") as f:
    contatos_telefone_json = json.load(f)

contatos_telefone = [x for x in contatos_telefone_json if isinstance(x, dict)]

contatos_filtrados = [contato for contato in contatos_telefone if not "***" in contato["telefone"] or not "****" in contato["celular"]]

for contato in contatos_filtrados:
    contato["telefone"] = normalize_phone_number(contato["telefone"])
    contato["celular"] = normalize_phone_number(contato["celular"])
    
    

df = pd.DataFrame(contatos_filtrados)

df.to_excel("contatos_telefone_filtrados.xlsx", index=False)