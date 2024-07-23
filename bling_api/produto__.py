import requests
import json
import os 
from ..img_bb.imgbb import hospeda_imagem
import re
import time
from .tokens_bling import atualiza_token, ler_senhas

acess_token_bling = atualiza_token()[0]

# Cadastra o produto no Bling
class Produto:
  def __init__(self,capa,caminho,nome,codigo,preco,descricao='',peso=0.3,origem=2,ncm=54075210,img='',alt=7,larg=7,profun=7):

    #DEFINE TODAS AS CARACTERISTICAS DO PRODUTO
    self.caminho = caminho
    self.nome = nome
    self.codigo = codigo
    self.preco = preco
    self.descricao = descricao
    self.peso = peso
    self.origem = origem
    self.ncm = ncm
    self.img = img
    self.alt = alt
    self.larg = larg
    self.profun = profun
    self.caminho_capa = capa

#CRIA O DICIONARIO COM TODAS AS VARIAÇÕES DE ACORDO COM AS FOTOS QUE ESTÃO NAS IMAGENS
  def compor_variacoes(self,mudou_nome = True):
    pasta = os.listdir(self.caminho)
    variacoes = []
    for cor in pasta:    
      if 'desktop.ini' in cor:
        pass
      else:
        nome_cor = cor.replace('.jpg','')
        nome_cor = nome_cor.replace('.png','')
        nome_cor = nome_cor.replace('.jpeg','')
        nome_cor = nome_cor.replace('.gif','')
        nome_cor = nome_cor.replace('.Gif','')
        nome_cor = nome_cor.title()
        if mudou_nome:
          cod_sku = re.sub('[^0-9]', '', nome_cor)
          if not cod_sku or cod_sku == '':
            cod_sku = nome_cor
        else:
          cod_sku = nome_cor
        url_imagem = hospeda_imagem(f'{self.caminho}/{cor}', nome_cor)
        var = {
          "id": "",
          "nomeVariacao": f'Cor:{nome_cor}',
          "codigo": f'{self.codigo}-{cod_sku}',
          "preco": self.preco,
          "tipo": "P",
          "situacao": "A",
          "formato": "S",
          "descricaoCurta": "",
          "dataValidade": "",
          "unidade": "Mt",
          "pesoLiquido": self.peso,
          "pesoBruto": self.peso,
          "volumes": "",
          "itensPorCaixa": "",
          "gtin": "",
          "gtinEmbalagem": "",
          "tipoProducao": "T",
          "condicao": 1,
          "freteGratis": False,
          "marca": "Legítima Textil",
          "descricaoComplementar": "",
          "linkExterno": "",
          "observacoes": "",
          "categoria": {
            "id": ""
          },
          "produtoPai": {
              "cloneInfo": False
            },
          "estoque": {
            "minimo": "",
            "maximo": "",
            "crossDocking": "",
            "localizacao": ""
          },
          "actionEstoque": "",
          "dimensoes": {
            "largura": self.larg,
            "altura": self.alt,
            "profundidade": self.profun,
            "unidadeMedida": "centimetro"
          },
          "tributacao": {
            "origem": self.origem,
            "nFCI": "",
            "ncm": self.ncm,
            "cest": "",
            "codigoListaServicos": "",
            "spedTipoItem": "",
            "codigoItem": "",
            "percentualTributos": 0,
            "valorBaseStRetencao": 0,
            "valorStRetencao": 0,
            "valorICMSSubstituto": 0,
            "codigoExcecaoTipi": "",
            "classeEnquadramentoIpi": "",
            "valorIpiFixo": 0,
            "codigoSeloIpi": "",
            "valorPisFixo": 0,
            "valorCofinsFixo": 0,
            "codigoANP": "",
            "descricaoANP": "",
            "percentualGLP": 0,
            "percentualGasNacional": 0,
            "percentualGasImportado": 0,
            "valorPartida": 0,
            "tipoArmamento": 0,
            "descricaoCompletaArmamento": "",
            "dadosAdicionais": "",
            "grupoProduto": {
              "id": ""
            }
          },
          "midia": {
            "video": {
              "url": ""
            },
            "imagens": {
              "externas": [
                {
                  "link": url_imagem
                }
              ]
            }
          }
        }
        
        variacoes.append(var)

    return variacoes
#HOSPEDA AS IMAGENS DE CAPA E RETORNA OS LINKS
  def buscar_capa(self):
    pasta_capa = os.listdir(self.caminho_capa)
    links = []
    for capa in pasta_capa:
      if "desktop.ini" in capa:
        pass
      else:
        url_capa = hospeda_imagem(f'{self.caminho_capa}/{capa}',capa)
        dict_capa = {"link": url_capa}
        links.append(dict_capa)
    return links
#CRIA O DICIONARIO QUE DEVE SER UTILIZADO NO BODY DA REQUISICAO
  def criar_cadastro(self,mudou_nome = True):
    if mudou_nome:
      cores = Produto.compor_variacoes(self)
    else:
      cores = Produto.compor_variacoes(self,mudou_nome=False)
    url_capa = Produto.buscar_capa(self)
    esquema = {
    "id": "",
    "nome": self.nome,
    "codigo": self.codigo,
    "preco": self.preco,
    "tipo": "P",
    "situacao": "A",
    "formato": "V",
    "descricaoCurta": self.descricao,
    "dataValidade": "",
    "unidade": "Mt",
    "pesoLiquido": self.peso,
    "pesoBruto": self.peso,
    "volumes": "",
    "itensPorCaixa": "",
    "gtin": "",
    "gtinEmbalagem": "",
    "tipoProducao": "T",
    "condicao": 1,
    "freteGratis": False,
    "marca": "",
    "descricaoComplementar": "",
    "linkExterno": "",
    "observacoes": "",
    "categoria": {
      "id": ""
    },
    "estoque": {
      "minimo": "",
      "maximo": "",
      "crossDocking": "",
      "localizacao": ""
    },
    "actionEstoque": "",
    "dimensoes": {
      "largura": self.larg,
      "altura": self.alt,
      "profundidade": self.profun,
      "unidadeMedida": 1
    },
    "tributacao": {
      "origem": self.origem,
      "nFCI": "",
      "ncm": self.ncm,
      "cest": "",
      "codigoListaServicos": "",
      "spedTipoItem": "",
      "codigoItem": "",
      "percentualTributos": 0,
      "valorBaseStRetencao": 0,
      "valorStRetencao": 0,
      "valorICMSSubstituto": 0,
      "codigoExcecaoTipi": "",
      "classeEnquadramentoIpi": "",
      "valorIpiFixo": 0,
      "codigoSeloIpi": "",
      "valorPisFixo": 0,
      "valorCofinsFixo": 0,
      "codigoANP": "",
      "descricaoANP": "",
      "percentualGLP": 0,
      "percentualGasNacional": 0,
      "percentualGasImportado": 0,
      "valorPartida": 0,
      "tipoArmamento": 0,
      "descricaoCompletaArmamento": "",
      "dadosAdicionais": "",
      "grupoProduto": {
        "id": ""
      }
    },
    "midia": {
      "video": {
        "url": ""
      },
      "imagens": {
        "externas": url_capa
      }
    },
    
    "variacoes": cores

  }
    return esquema
  
  def cadastrar(self,mudou_nome = True):
    link = 'https://www.bling.com.br/Api/v3/produtos'
    headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}

    if mudou_nome:
      body_message = Produto.criar_cadastro(self)
    else:
      body_message = Produto.criar_cadastro(self,mudou_nome=False)

    body_message = json.dumps(body_message)
    requisicao = requests.post(link, headers=headers, data=body_message)
    if requisicao.status_code == 401:
      time.sleep(1)
      headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
      requisicao = requests.post(link, headers=headers, data=body_message)
    
    if requisicao.status_code != 201:
      print(requisicao)
      print(requisicao.json())
      
    return requisicao.status_code

# Lança estoque em determinado produto no bling
class Estoque:
  def __init__(self, codigo, qtd_lancar):
    self.codigo = codigo
    self.qtd_lancar = qtd_lancar
#PEGA O ID DO PRODUTO PAI PARA DEPOIS PEGAR O ID DAS VARIACOES E LANCAR O ESTOQUE
  def pega_id(self):
      
    link = f'https://www.bling.com.br/Api/v3/produtos?pagina=1&limite=100&criterio=2&tipo=P&codigo={self.codigo}'
    headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
    
    requisicao = requests.get(link, headers=headers)
    if requisicao.status_code == 401:
      atualiza_token()
      time.sleep(1)
      headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
      requisicao = requests.get(link, headers=headers)
      
    resposta = requisicao.json()
    id_produto = resposta['data'][0]['id']
    
    return id_produto
#PEGA O ID DAS VARIACOES PARA LANCAR O ESTOQUE
  def id_var(self):
    
    id_pai = Estoque.pega_id(self)
    
    link = f'https://www.bling.com.br/Api/v3/produtos/variacoes/{id_pai}'
    headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
    
    requisicao = requests.get(link, headers=headers)
    if requisicao.status_code == 401:
      atualizar_token = atualizar_token()
      headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
      requisicao = requests.get(link, headers=headers)
    
    resposta = requisicao.json()
    variacoes = resposta['data']['variacoes']
    id_variacoes = []
    
    for var in variacoes:
      id_variacao = var['id']
      id_variacoes.append(id_variacao)
    
    return id_variacoes
#LANCA ESTOQUE EM TODAS AS VARIACOES
  def lanca_estoque(self):
    link = 'https://www.bling.com.br/Api/v3/estoques'
    headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
    lista_ids = Estoque.id_var(self)
    
    deposito1 = 10610809064 #-> LEGITIMA
    
    #deposito1 = 14886526196

    for id_variacao in lista_ids:
      body_message = {
        "produto": {
          "id": id_variacao
        },
        "deposito": {
          "id": deposito1
        },
        "operacao": "B",
        "preco": 0,
        "custo": 0,
        "quantidade": self.qtd_lancar,
        "observacoes": ""
      }

      body_message = json.dumps(body_message)
      requisicao = requests.post(link, headers=headers, data=body_message)
      if requisicao.status_code == 401:
        atualiza_token()
        time.sleep(2)
        headers = {"Authorization": f"Bearer {acess_token_bling}", "Content-Type": "application/json"}
        requisicao = requests.post(link, headers=headers, data=body_message)
        
      if requisicao.status_code == 201:
        print('Lançamento de estoque: OK')
     
