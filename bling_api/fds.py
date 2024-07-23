import os, sys, json

sys.path.append(os.path.abspath(r'C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling'))

from bling_api import settings

images = [
    {'po': 12, 'link': 33},
    {'po': 13, 'link': 34},
    {'po': 14, 'link': 37},
    {'po': 15, 'link': 36},
]

images_url = [{'link': img['link']} for img in images]

print(images_url)