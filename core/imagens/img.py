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

def baixa_imagem(url, caminho):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    with open(caminho, 'wb') as img:
        resposta = requests.get(url, headers=headers, stream=True)
        if not resposta.ok:
            print(f'{caminho}, não pode ser baixado')
        else:
            img.write(resposta.content)

# Entra no site da Disparada e busca por todas as imagens 
def importa_disparada(cod, nome_tecido, **kwargs):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)

    nav.get(f'https://disparadatecidos.com.br/')
    nav.find_element('xpath', '/html/body/main/a[1]').click()

    nome_pasta = f'{nome_tecido} D{cod}'
    
    diretorio_salvar = fr'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\DISPARADA\{nome_pasta}'
    nav.find_element('xpath', '//*[@id="input_search"]').send_keys(cod)
    nav.find_element('xpath', '//*[@id="input_search"]').send_keys(Keys.ENTER)
    nav.find_element('xpath', '//*[@id="artigo-list"]/li/a').click()
    composicao = nav.find_element('xpath', '//*[@id="artigo-composicao"]')
    composicao = composicao.text
    largura = nav.find_element('xpath', '//*[@id="artigo-largura"]')
    largura = largura.text
    
    #CRIA OS DIRETORIOS NECESSARIOS CASO ELES NAO EXISTAM
    if (not os.path.exists(diretorio_salvar)):
        os.mkdir(diretorio_salvar)
        diretorio_fotos = fr"{diretorio_salvar}\Fotos"
        diretorio_capa = fr"{diretorio_salvar}\Capa"
        os.mkdir(diretorio_capa)
        os.mkdir(diretorio_fotos)
        
    diretorio_fotos = fr"{diretorio_salvar}\Fotos"
    diretorio_capa = fr"{diretorio_salvar}\Capa"
    
    if not os.path.exists(diretorio_fotos):
        os.mkdir(diretorio_fotos)
    
    if not os.path.exists(diretorio_capa):
        os.mkdir(diretorio_capa)
        
    time.sleep(0.5)

    estampas = nav.find_elements('class name', 'item')

    urls = []
    #BAIXA TODAS AS ESTAMPAS
    for estampa in estampas:
        nome_cor = estampa.find_element('class name', 'color-code').text
        url = estampa.find_element(By.TAG_NAME, 'img').get_attribute('src')
        formato = url.split('.')[-1]
        path = os.path.join(diretorio_fotos,f'{nome_cor}.{formato}')
        
        urls.append({
            'nome': nome_cor,
            'url_img': url,
            'formato': formato
        })
    
    nav.close()
    
    for arq in urls:
        caminho = os.path.join(diretorio_fotos, arq['nome'] + '.' + arq['formato'])
        baixa_imagem(arq['url_img'], caminho)
        
    #PEGA AS IMAGENS EXPORTADAS E CRIA AS CAPAS
    if 'titulo_tecido' in kwargs:
        monta_capa(diretorio_fotos, diretorio_capa, titulo_tecido=kwargs['titulo_tecido'])

    elif 'titulo_promo' in kwargs:
        monta_capa(diretorio_fotos, diretorio_capa, titulo_promo=kwargs['titulo_promo'])
    
    else:
        monta_capa(diretorio_fotos, diretorio_capa)
    
    return diretorio_fotos,composicao,largura,diretorio_capa


def importa_aquarela(url, path=None, nome_tecido=None, **kwargs):
    
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)

    nav.get(url)
    div_estampa = nav.find_elements(By.CLASS_NAME, 'item')
    

    if not path:
        path = fr'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\AQUARELA'
        
    urls = []
    diretorio_fotos = ''
    diretorio_capa = ''
    composicao_tecido = ''
    largura_tecido = ''
    
    for img in div_estampa:
        url_img = img.find_element(By.TAG_NAME, 'a').get_attribute('href')
        nome = img.find_element(By.CLASS_NAME, 'color-code').text
        formato = url_img.split('.')[-1]
        titulo = nav.find_element(By.ID,'artigo-nome').text
        infos = nav.find_element(By.TAG_NAME, 'h2').text
        artigo = re.search(r'Ordem: (\d+)', infos).group(1)
        composicao = re.search(r'Composição: (\d+)', infos).group(1)
        largura = re.search(r'Largura: (\d+)', infos).group(1)
        
        if not nome_tecido:
            nome_tecido = titulo
        
        pasta = nome_tecido + ' A' + artigo
        diretorio_fotos = os.path.join(path, pasta, 'Fotos' )
        diretorio_capa = os.path.join(path, pasta, 'Capa' )
        
        if (not os.path.exists(diretorio_fotos)):
            os.makedirs(diretorio_fotos)
        
        if (not os.path.exists(diretorio_capa)):
            os.makedirs(diretorio_capa)
        
        composicao_tecido = composicao
        largura_tecido = largura
        

        
        urls.append({
            'nome': nome,
            'url_img': url_img,
            'formato': formato,
            })
    
    nav.close()
    for arq in urls:
        caminho = os.path.join(diretorio_fotos, arq['nome'] + '.' + arq['formato'])
        baixa_imagem(arq['url_img'], caminho)
    
    if 'titulo_tecido' in kwargs:
        monta_capa(diretorio_fotos, diretorio_capa, titulo_tecido=kwargs['titulo_tecido'])

    elif 'titulo_promo' in kwargs:
        monta_capa(diretorio_fotos, diretorio_capa, titulo_promo=kwargs['titulo_promo'])
    
    else:
        monta_capa(diretorio_fotos, diretorio_capa)
    
    return diretorio_fotos,composicao_tecido,largura_tecido,diretorio_capa 

# Reduz o tamanho das imagens.
def reduzir_tamanho(caminho,tamanho_max, pastas=0):

    if pastas == 0:
        lista_imagens = os.listdir(caminho)
        for img in lista_imagens:
            nome = f"{caminho}/{img}"
            tamanho = os.path.getsize(nome) / 1000
            while tamanho > tamanho_max:
                imagem = Image.open(nome)
                w = int(imagem.width / 1.45)
                h = int(imagem.height / 1.45)
                nova_imagem = imagem.resize((w, h))
                nova_imagem.save(nome)
                tamanho = os.path.getsize(nome) / 1000
    elif pastas == 1:
        lista_pastas = os.listdir(caminho)
        for pasta in lista_pastas:
            for img in pasta:
                nome = f"{pasta}/{img}"
                tamanho = os.path.getsize(nome) / 1000
                while tamanho > tamanho_max:
                    imagem = Image.open(nome)
                    w = int(imagem.width / 1.45)
                    h = int(imagem.height / 1.45)
                    nova_imagem = imagem.resize((w, h))
                    nova_imagem.save(nome)
                    tamanho = os.path.getsize(nome) / 1000

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
        
        
        draw.rectangle((200,490,1067,795), fill='#ff4700', outline= '#0000') # -> LEGITIMA
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
            