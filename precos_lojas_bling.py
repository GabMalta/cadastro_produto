import requests
import json
from core.bling.tokens_bling import ler_senhas
from core.img_bb.imgbb import hospeda_imagem
import time
from core.bling.tokens_bling import atualiza_token
from pprint import pprint

access_token_bling = ler_senhas()[0]

def pega_id_var(id_pai):
  link = f'https://www.bling.com.br/Api/v3/produtos/variacoes/{id_pai}'

  headers = {"Authorization": f"Bearer {access_token_bling}", "Content-Type": "application/json"}
  
  requisicao = requests.get(link, headers=headers)
  if requisicao.status_code == 401:
    atualiza_token()
    time.sleep(1)
    headers = {"Authorization": f"Bearer {access_token_bling}", "Content-Type": "application/json"}
    requisicao = requests.get(link, headers=headers)
    
  resposta = requisicao.json()
  try:
    variacoes = resposta['data']['variacoes']
    
    id_var = []
    for var in variacoes:
        id_var.append(var['id'])
  except:
      return ""
  
  return id_var
  
def pega_vinculo_loja(id_produto):
    link = f'https://www.bling.com.br/Api/v3/produtos/lojas?pagina=1&limite=100&idProduto={id_produto}&idLoja=203549015'
    headers = {"Authorization": f"Bearer {access_token_bling}", "Content-Type": "application/json"}
  
    requisicao = requests.get(link, headers=headers)
    if requisicao.status_code == 401:
        atualiza_token()
        time.sleep(1)
        headers = {"Authorization": f"Bearer {access_token_bling}", "Content-Type": "application/json"}
        requisicao = requests.get(link, headers=headers)
        
    resposta = requisicao.json()
    codigo = resposta['data'][0]['codigo']
    id_vinculo = resposta['data'][0]['id']
    
    return id_vinculo, codigo

def atualiza_preco(id_vinculo, id_produto, codigo, preco, id_loja = 203549015):
    """ id_vinculo (int) : id unico de vinculo com a loja 
        id_produto (int) : id do produto no bling
        codigo (int): codigo do produto na loja
        preco (float): preco a ser atualizado
        id_loja (int) : id da loja (por padrão tem a loja da Shopee)
    """
    
    link = f'https://www.bling.com.br/Api/v3/produtos/lojas/{id_vinculo}'
    headers = {"Authorization": f"Bearer {access_token_bling}", "Content-Type": "application/json"}
    
    body = {
  "codigo": codigo,
  "preco": preco,
  "precoPromocional": preco,
  "produto": {
    "id": id_produto
  },
  "loja": {
    "id": id_loja
}
    }
    
    body = json.dumps(body)
    
    requisicao = requests.put(link, headers=headers, data=body)
    resposta = requisicao.json()
    
    if requisicao.status_code == 200:
        print('Ok')
    else:
        pprint(resposta)
    

id_pai = [{'id': 10802261663, 'preco': 282.69},
{'id': 10736941760, 'preco': 14.99},
{'id': 10935019837, 'preco': 129.9},
{'id': 10736942428, 'preco': 51.79},
{'id': 10736942444, 'preco': 24.89},
{'id': 11129310710, 'preco': 26.89},
{'id': 10736942451, 'preco': 18.89},
{'id': 10935016748, 'preco': 45.99},
{'id': 10732487392, 'preco': 17.39},
{'id': 10935022069, 'preco': 87.89},
{'id': 10802300184, 'preco': 169.9},
{'id': 10935013970, 'preco': 144.9},
{'id': 10802410440, 'preco': 78.89},
{'id': 10935027740, 'preco': 116.89},
{'id': 10935030160, 'preco': 42.59},
{'id': 10736941750, 'preco': 13.9},
{'id': 10802181639, 'preco': 87.39},

]

for X,pai in enumerate(id_pai):
    id_pai = pai['id']
    preco = pai['preco']
    id_vinculo,codigo = pega_vinculo_loja(id_pai)
    atualiza_preco(id_vinculo,id_pai,codigo,preco)
    
    variacoes = pega_id_var(id_pai)
    try:
        for var in variacoes:
            id_vinculo,codigo = pega_vinculo_loja(var)
            atualiza_preco(id_vinculo,var,codigo,preco)
    except:
        pass
    print(X, "\n")



