from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, os, requests, random
from PIL import Image, ImageDraw, ImageFont
import re
import sys

sys.path.append(os.path.abspath(os.curdir))

# Caso o nome do tecido seja muito comprido, faz a quebra de linha
def quebra_linha(nome_tecido):
    if len(nome_tecido) > 16:
        teste = nome_tecido.split()
        car = 0
        for i,palavra in enumerate(teste):
            car += len(palavra) + 1
            print(car)
            if car > 16:
                #nome_tecido = f'{teste[:2]}\n{teste[2:]}'
                nome_tecido = f'{" ".join(teste[:i])}\n{" ".join(teste[i:])}'
                break
    return nome_tecido

# Cria uma elipse e escreve Promoção e o nome do tecido na foto de capa
def escreve_promo(draw,nome_tecido):
        draw = ImageDraw.Draw(draw)
        font_promocao = ImageFont.truetype("impact.ttf",size=110)
        font_tecido = ImageFont.truetype("impact.ttf",size=85)
        
        draw.ellipse((275,275,1025,1025), fill='#EE4D2D')
        draw.text((640, 550),'PROMOÇÃO!', fill='black', font=font_promocao, align='center',stroke_fill='white',stroke_width=7, anchor='mm')
        nome_tecido = quebra_linha(nome_tecido)
        draw.text((640, 730),nome_tecido, fill='white', font=font_tecido, align='center',stroke_fill='black',stroke_width=7, anchor='mm')

def escreve_nome_tecido(img,nome_tecido):
        draw = ImageDraw.Draw(img)
        font_promocao = ImageFont.truetype("impact.ttf",size=110)
        font_tecido = ImageFont.truetype("impact.ttf",size=110)
        
        
        draw.rectangle((200,490,1067,795), fill='#FF0000', outline= '#0000') # -> LEGITIMA
        #draw.rectangle((200,490,1067,795), fill='#F4B41A', outline= '#0000') # -> GM TECIDOS
        nome_tecido = quebra_linha(nome_tecido)
        draw.text((640, 640),nome_tecido, fill='#050A30', font=font_tecido, align='center', stroke_fill='white', stroke_width=3, anchor='mm',)

# Monta layout de capa padrão
def monta_capa(caminho_img, caminho_salvar,**kwargs):
    #CRIA LISTA COM NOME DOS ARQUIVOS
    caminho = os.listdir(caminho_img)
    
    if not os.path.exists(caminho_salvar):
        os.mkdir(caminho_salvar)
    
    for i,x in enumerate(caminho):
            if ".ini" in str(x):
                caminho.pop((i))
    
    # SE TIVER 6 OU MAIS IMAGENS DENTRO DA PASTA, VAI CRIAR A CAPA PRINCIPAL COM FOTOS ALEATORIAS
    if len(caminho) >= 6:
        
        
        fundo = Image.new('RGB',(1280,1280),(255,255,255))
        tamanhos = [(640,411), (627,620), (313,423), (313,423), (640,411), (640,640)]
        posicoes = [(0,0), (653,0), (0,428), (326,428), (0,868), (653,640)]
        img_random = random.sample(caminho,6)
        
        for i,img in enumerate(img_random):
            if i <= 5:
                
                foto = Image.open(f'{caminho_img}/{img}').resize(tamanhos[i])
                fundo.paste(foto,posicoes[i])
                
        
        
        if 'titulo_promo' in kwargs:
            nome_tecido = kwargs['titulo_promo']
            escreve_promo(fundo,nome_tecido)
        
        if 'titulo_tecido' in kwargs:
            nome_tecido = kwargs['titulo_tecido']
            escreve_nome_tecido(fundo,nome_tecido)
            # logo = Image.open('core\imagens\LOGO.png').resize((416,100)).convert('RGBA')
            # fundo.paste(logo,(450,790), logo)
        
        fundo.save(f'{caminho_salvar}/CAPA 01.jpg')
        
    # SE TIVER 4 OU MAIS IMAGENS DENTRO DA PASTA, VAI CRIAR 4 CAPAS COM FOTOS ALEATORIAS
    if len(caminho) >= 4:
        for y in range(4):
            fundo = Image.new('RGB',(1280,1280),(255,255,255))
            posicoes = [(0,0), (640,0), (0,640), (640,640)]
            for x in range(4):
                img_random = random.sample(caminho,4)
                for i,img in enumerate(img_random):
                    foto = Image.open(f'{caminho_img}/{img}').resize((635,635))
                    fundo.paste(foto,posicoes[i])
                
                if 'titulo_promo' in kwargs:
                    nome_tecido = kwargs['titulo_promo']
                    escreve_promo(fundo,nome_tecido)
                
                if 'titulo_tecido' in kwargs:
                    nome_tecido = kwargs['titulo_tecido']
                    escreve_nome_tecido(fundo,nome_tecido)
                    # logo = Image.open('core\imagens\LOGO.png').resize((416,100)).convert('RGBA')
                    # fundo.paste(logo,(450,790), logo)
                    
                    fundo.save(f'{caminho_salvar}/CAPA 0{x+2}.jpg')
    #SE TIVER MENOS DE 4 IMAGENS SALVA CAPAS UNICAS
    if len(caminho) < 4:
        fundo = Image.new('RGB',(1280,1280),(255,255,255))
        for i,img in enumerate(caminho):
            foto = Image.open(f"{caminho_img}/{img}").resize((1280,1280))
            fundo.paste(foto)
        
        if 'titulo_promo' in kwargs:
            nome_tecido = kwargs['titulo_promo']
            escreve_promo(fundo,nome_tecido)
        
        if 'titulo_tecido' in kwargs:
            nome_tecido = kwargs['titulo_tecido']
            escreve_nome_tecido(fundo,nome_tecido)
            # logo = Image.open('logo.png').resize((416,100)).convert('RGBA')
            # fundo.paste(logo,(450,790), logo)
        
        #fundo.show()
        
        fundo.save(f"{caminho_salvar}/CAPA 0{i+1}.jpg")
            