import sys



from core.imagens.img import monta_capa
from core.precificacao.precificacao import precificacao, pega_preco
from core.bling.produto import Produto
from core.chat_gpt.chat_gpt import Descricao
from core.interface import *
import os
import re


pasta_tecidos = os.listdir(fr'D:\SITE LEGITIMA TEXTIL\PROMOCOES 02.24\A CADASTRAR')


for pasta in pasta_tecidos:
  if 'desktop.ini' in pasta:
    pass
  else:
    nome_anuncio = 'Tecido ' + pasta
    
    img_capa = fr"D:\SITE LEGITIMA TEXTIL\PROMOCOES 02.24\A CADASTRAR\{pasta}\Capa"
    pasta_produto = fr"D:\SITE LEGITIMA TEXTIL\PROMOCOES 02.24\A CADASTRAR\{pasta}\Fotos"
    origem = 2
    ncm = 54075210
    largura = '1,50'
    qtd_mt = 1
    peso = 0.4
    alt = 7
    larg = 7
    profund = 7
    
    with open(fr"D:\SITE LEGITIMA TEXTIL\PROMOCOES 02.24\A CADASTRAR\{pasta}\composicao.txt", 'r', encoding='utf-8') as comp:
      composicao = comp.read()
      
    with open(fr"D:\SITE LEGITIMA TEXTIL\PROMOCOES 02.24\A CADASTRAR\{pasta}\cod.txt", 'r', encoding='utf-8') as comp:
      cod = comp.read()
      
      print(pasta)
    
    #tt = cod.split('D')[0]
    
    print(nome_anuncio)
    preco_bruto = pega_preco(cod.split('D')[1])
    titulo_promo = nome_anuncio.split('Tecido ')[1].upper()
    monta_capa(pasta_produto, img_capa, titulo_promo)
    
    #for i,qtd in enumerate(qtd_mt):
    if qtd_mt > 1:
      cod = f'({qtd_mt}){cod}'
    else:
      cod = f'[PE]{cod}'
    titulo_anuncio = f'(PROMOÇÃO) {nome_anuncio} ({qtd_mt}m x {largura}m)'
    
    preco_venda = precificacao(percent_desconto_atacado=23.5, percent_lucro_desejado=17, 
                                plataforma='shopee', preco_custo_bruto= preco_bruto, qtd_metros= qtd_mt)
    
    descricao = Descricao(titulo_anuncio, composicao, qtd_mt, largura)
    descricao_gpt = descricao.desc_chatgpt(ref=False)
    descricao_final = descricao.monta_descricao(descricao_gpt)
  
    Produto(img_capa,pasta_produto,titulo_anuncio,cod,preco_venda,descricao_final,peso,origem,ncm,img_capa,
                        alt,larg,profund).cadastrar(mudou_nome=True)

    #Estoque(cod, 150).lanca_estoque()

#   (img_capa,pasta_produto,titulo_anuncio[i],cod[i],preco_venda[i],descricao_final[i],peso[i],origem,ncm,img_capa,
#                         alt[i],larg[i],profund[i]
