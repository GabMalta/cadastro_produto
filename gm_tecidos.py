from core.bling.produto import Produto, Estoque
from core.precificacao.precificacao import precificacao, pega_preco
from core.imagens.img import monta_capa
from core.chat_gpt.chat_gpt import Descricao
import os

caminho = r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\DISPARADA'

pasta_geral = os.listdir(caminho)
pasta_geral.remove('CADASTRADOS')
pasta_geral.remove('desktop.ini')

artigos_capitalize = [' '.join(palavra.capitalize() for palavra in artigo.split()) for artigo in pasta_geral]

metragens = [
    {'mt':3, 'peso': 0.4, 'l': 7, 'c': 7, 'p': 7},
    {'mt':4, 'peso': 0.6, 'l': 7, 'c': 7, 'p': 7},
    {'mt':5, 'peso': 0.8, 'l': 7, 'c': 7, 'p': 10},
    {'mt':6, 'peso': 1.3, 'l': 7, 'c': 10, 'p': 10},
    {'mt':10, 'peso': 2, 'l': 10, 'c': 10, 'p': 10},
]

for art in pasta_geral:
    
    pasta_capa = os.path.join(caminho, art, 'Capa')
    pasta_fotos =  os.path.join(caminho, art, 'Fotos')
    
    with open(os.path.join(caminho,art,'Codigo.txt'), 'r') as arq:
        codigo = arq.read()
    
    with open(os.path.join(caminho,art,'Composicao.txt'), 'r') as arq:
        composicao = arq.read()
    
    with open(os.path.join(caminho,art,'Largura.txt'), 'r') as arq:
        largura = arq.read()
    
    for mt in metragens:
        
        print(mt['mt'])
        
        monta_capa(pasta_fotos, pasta_capa, titulo_tecido=art)
            
        titulo_anuncio = f'{str(mt['mt'])} Metros Tecido {" ".join(palavra.capitalize() for palavra in art.split())} ({str(mt['mt'])}m x {largura}m)'
        
        preco_custo = pega_preco(codigo)
        preco_venda = precificacao(preco_custo,23.5,mt['mt'],18,'shopee')
        
        descricao = Descricao(art, composicao, mt['mt'], largura)
        descricao_final = descricao.desc_chatgpt(ref=False)
        
        peso = mt['peso']
        origem = '2'
        ncm = '54075210'
        alt = mt['c']
        larg = mt['l']
        profund = mt['p']
        codigo_bling = f'{mt["mt"]}m-D{str(codigo)}'
        
        try:
            print(f'Cadastrando {titulo_anuncio}')
            Produto(pasta_capa, pasta_fotos, titulo_anuncio, codigo_bling, preco_venda, descricao_final, peso, origem, ncm, pasta_capa, alt, larg, profund).cadastrar(True)
            print(f'{art} - {mt['mt']}m Cadastrado')
            Estoque(codigo_bling, 100).lanca_estoque()
        except Exception as e:
            print('Erro aqui no gm_tecidos\n', e)
            
        
        
        
        
        
        
        
        
        
        
        
        
        

            
