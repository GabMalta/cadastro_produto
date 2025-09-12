import json
from apps.bling_api.bling import BlingApi

bling = BlingApi()

products = bling.get_products(params={"criterio": 4, "tipo": "P"})['data']

print(len(products))

id_products = [product['id'] for product in products][:10]

params = [( "idsProdutos[]", id_) for id_ in id_products]


params2 = "idsProdutos[]=" + "&idsProdutos[]=".join(map(str, id_products))

bling.delete_products(params=params2)
