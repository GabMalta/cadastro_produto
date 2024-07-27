import requests
import time

# Lança estoque em determinado produto no bling
class Estoque:
  def __init__(self, codigo, qtd_lancar):
    self.codigo = codigo
    self.qtd_lancar = qtd_lancar
#PEGA O ID DO PRODUTO PAI PARA DEPOIS PEGAR O ID DAS VARIACOES E LANCAR O ESTOQUE
  def pega_id(self):
      
    link = f'https://www.bling.com.br/Api/v3/produtos?pagina=1&limite=100&criterio=2&tipo=P&codigo={self.codigo}'
    headers = {"Authorization": f"Bearer {'acess_token_bling'}", "Content-Type": "application/json"}
    
    requisicao = requests.get(link, headers=headers)
    if requisicao.status_code == 401:
      time.sleep(1)
      headers = {"Authorization": f"Bearer {'acess_token_bling'}", "Content-Type": "application/json"}
      requisicao = requests.get(link, headers=headers)
      
    resposta = requisicao.json()
    id_produto = resposta['data'][0]['id']
    
    return id_produto
#PEGA O ID DAS VARIACOES PARA LANCAR O ESTOQUE
  def id_var(self):
    
    id_pai = Estoque.pega_id(self)
    
    link = f'https://www.bling.com.br/Api/v3/produtos/variacoes/{id_pai}'
    headers = {"Authorization": f"Bearer {'acess_token_bling'}", "Content-Type": "application/json"}
    
    requisicao = requests.get(link, headers=headers)
    if requisicao.status_code == 401:
      atualizar_token = atualizar_token()
      headers = {"Authorization": f"Bearer {'acess_token_bling'}", "Content-Type": "application/json"}
      requisicao = requests.get(link, headers=headers)
    
    resposta = requisicao.json()
    variacoes = resposta['data']['variacoes']
    id_variacoes = []
    
    for var in variacoes:
      id_variacao = var['id']
      id_variacoes.append(id_variacao)
    
    return id_variacoes
     
