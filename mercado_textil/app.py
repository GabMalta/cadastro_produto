from core.imagens.img import monta_capa
from core.precificacao.precificacao import precificacao, pega_preco
from core.bling.produto import Produto, Estoque
from core.chat_gpt.chat_gpt import Descricao
from core.interface import *
import os


pasta_tecidos = os.listdir('D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\PROMOCAO')

for pasta in pasta_tecidos:
  if 'desktop.ini' in pasta:
    pass
  else:
    nome_anuncio = pasta.split(' D')
    
    img_capa = fr"D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\MERCADO TEXTIL\{pasta}\Capa"
    pasta_produto = fr"D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\MERCADO TEXTIL\{pasta}\Fotos"
    origem = 2
    ncm = 54075210
    largura = '1,50'
    qtd_mt = [1,3,6,7,10,12,15,20]
    peso = [0.3, 0.7, 0.9, 1.2, 1.5, 1.7, 2, 2.3]
    alt = [5, 7, 7, 7, 7, 7, 10, 10]
    larg = [5, 5, 7, 7, 7, 7, 10, 10]
    profund = [5, 5, 7, 7, 7, 10, 10, 10]
    
    with open(f"D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\MERCADO TEXTIL\{pasta}\composicao.txt", 'r') as comp:
      composicao = comp.read()
    
    
    
    cod = nome_anuncio[1]
    tt = cod.split('D')[0]
    preco_bruto = pega_preco(cod.split('D')[0])
    
    monta_capa(caminho_img=pasta_produto, caminho_salvar=img_capa)
    
    for i,qtd in enumerate(qtd_mt):
      if qtd > 1:
        cod = f'({qtd})D{nome_anuncio[1]}'
      else:
        cod = f'D{nome_anuncio[1]}'
      titulo_anuncio = f'{nome_anuncio[0]} ({qtd}m x {largura}m)'
      
      preco_venda = precificacao(percent_desconto_atacado=23.5, percent_lucro_desejado=17, plataforma='shopee', preco_custo_bruto= preco_bruto, qtd_metros= qtd)
      
      descricao = Descricao(titulo_anuncio, composicao, qtd_mt, largura)
      descricao_gpt = descricao.desc_chatgpt(ref=False)
      descricao_final = descricao.monta_descricao(descricao_gpt)
    
      Produto(img_capa,pasta_produto,titulo_anuncio,cod,preco_venda,descricao_final,peso[i],origem,ncm,img_capa,
                          alt[i],larg[i],profund[i]).cadastrar(mudou_nome=True)

      Estoque(cod, 150).lanca_estoque()
  
#   (img_capa,pasta_produto,titulo_anuncio[i],cod[i],preco_venda[i],descricao_final[i],peso[i],origem,ncm,img_capa,
#                         alt[i],larg[i],profund[i]
