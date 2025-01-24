import json
import os
import random
from apps.data_scraping.create_covers import create_covers

names = [
    ("CETIM COM LYCRA P019", "CETIM COM LYCRA", [3,4,5,6,7,10]),
    ("CETIM DECORACAO 3M LARGURA A28", "CETIM DECORAÇÃO 3M DE LARGURA", [3,4,6,10]),
    ("CETIM ESTAMPADO L02", "CETIM ESTAMPADO", [3,4,5,6,7,10,15]),
    ("CHITAO 100% ALGODAO A18", "CHITÃO 100% ALGOGÃO", [3,6,7,10]),
    
]

def excluir_arq_pasta(path):
    for arq in os.listdir(os.path.join(path, 'Capa')):
        path_remove = os.path.join(path,'Capa', arq)
        if os.path.isfile(path_remove):
            os.remove(path_remove)

for name in names:
    path_name, title, mt = name
    path = os.path.join("D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL", path_name)

    excluir_arq_pasta(path)
    
    for i, m in enumerate(mt, start=1):
    
        create_covers(os.path.join("D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL", path), title, upload_for_s3=True, time_color_change=False, company="GM", font_color="#000", stroke_fill="orange", name_saved=f'CAPA ({m}m {i+1})')
        
        
        with open(os.path.join(path, "Capa", 'image_urls.json'),'r', encoding='utf-8') as arq:
            links = json.load(arq)

        text = "|".join([value['img'] for key,value in links.items()])

        with open(rf'D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL\1 LINKS GM\{path_name}.txt', 'a') as arq:
            arq.write(f'\n{m} METROS\n{text}\n')
        
        excluir_arq_pasta(path)