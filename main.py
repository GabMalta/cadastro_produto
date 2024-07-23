from core.imagens.img import importa_disparada,importa_aquarela, reduzir_tamanho,monta_capa
from core.precificacao.precificacao import precificacao, pega_preco
from core.bling.produto import Produto, Estoque
from core.chat_gpt.chat_gpt import Descricao
from core.interface import *
import sys, os

sys.path.append(os.path.abspath(os.curdir))

#---------- PRIMEIRAMENTE TEMOS QUE ARMAZENAR TODAS AS INFORMAÇÕES NECESSÁRIAS EM VARIÁVEIS-------------

# RECOLHE TODAS AS INFORMAÇÕES QUE NÃO É POSSÍVEL PEGAR AUTOMATICAMENTE
cabecalho('CRIADOR DE ANUNCIO')
body('Vamos começar o cadastro de seu anúncio, mas antes preciso coletar algumas informações...')
time.sleep(2)

mais_anuncios,atacado,cod,palavra_chave,qtd_metros,peso,origem,ncm,alt,larg,profund = pega_info_produto()

cabecalho('CRIADOR DE ANUNCIO')
print("Caracteristicas do produto armazenadas com sucesso\n")

tem_img = perg_s_n('Já tem as imagens do tecido?(s/n)')
print('\n') 

# PERGUNTA SE JÁ TEM AS IMAGENS TODAS PRONTAS NO PC
if tem_img == 's':
    pasta_produto = input('Informe o caminho da pasta onde as imagens estão:')
    composicao = input("Qual a composição do produto? ")
    largura_tecido = input('Qual a largura do tecido? ')
    img_capa = input('Qual o caminho da pasta da Imagem de Capa:')
    
    criar_capa = perg_s_n('Deseja que criemos a capa do produto para você?')
    if criar_capa == 's':
        promocao = perg_s_n('Tecido de Promoção?')
        if promocao == 's':
            titulo_promo = palavra_chave.split('Tecido ')[1].upper()
            monta_capa(pasta_produto,img_capa, titulo_promo=titulo_promo)
        else:
            nome_tecido = palavra_chave.split('Tecido ')[1].upper()
            monta_capa(pasta_produto,img_capa, titulo_tecido=nome_tecido)
        
# SE NAO TEM AS IMAGENS PRONTAS, ENTRA NO SITE DO ATACADO E BAIXA TODAS ELAS
elif tem_img == 'n':
    nome_tecido = palavra_chave.split('Tecido ')[1].upper()
    
    if atacado.lower() == 'disparada':
        nome_pasta = input('Qual será o nome da pasta que vai ficar as cores? ')
        print('Nosso sistema entrará no site da Disparada e vai baixar todas as fotos do produto selecionado.')
        
        while True:
            prossiga = input('Pressione enter para continuar...')
            
            if not prossiga:
                break
        
        pasta_produto,composicao,largura_tecido,img_capa = importa_disparada(cod, nome_pasta, titulo_tecido=nome_tecido)
    
    elif atacado.lower() == 'aquarela':
        url = input('Digite a URL onde fica as imagens da Aquarela ')
        print('Nosso sistema entrará no site da Aquarela e vai baixar todas as fotos do produto selecionado.')
        
        while True:
            prossiga = input('Pressione enter para continuar...')
            
            if not prossiga:
                break
       
        pasta_produto,composicao,largura_tecido,img_capa = importa_aquarela(url, nome_tecido=nome_tecido, titulo_tecido=nome_tecido)

if mais_anuncios:
    titulo_anuncio = []
    for mt in qtd_metros:
        titulo = f'{mt:,.0f} Metros {palavra_chave} ({mt:,.0f}m x {str(largura_tecido).replace(".",",")}m)' 
        titulo_anuncio.append(titulo) 
else:
    titulo_anuncio = f'{palavra_chave} ({qtd_metros:,.0f}m x {str(largura_tecido).replace(".",",")}m)'

print(os.system('cls'))
cabecalho("TRATAMENTO DE IMAGENS")
# PERGUNTA SE JA ARRUMOU O NOME DAS CORES NA PASTA
pergunta = perg_s_n('O nome das cores na pasta, está com o codigo extraido do site da Disparada, precisa modificar?')
if pergunta == 's':
    mudou_nome = True
elif pergunta == 'n':
    mudou_nome = False

# PERGUNTA SE DESEJA REDUZIR O TAMANHO DAS IMAGENS
pergunta = perg_s_n('Deseja reduzir o tamanho das imagens baixadas?(s/n)')
if pergunta == 's':
    reduzir_tamanho(pasta_produto,300)

print(os.system('cls'))
cabecalho("PRECIFICAÇÃO")
# PERGUNTA SE QUER RODAR O PROGRAMA DE PRECIFICAR
if atacado.lower() == 'disparada': 
    pergunta = perg_s_n('Rodar programa de precificacao?(s/n)')
else:
    pergunta = 'n'
    
if pergunta == 's' or pergunta == 'S':
    custo_bruto = pega_preco(cod)
    desconto = verifica_num('Qual o desconto no atacado?')
    lucro = verifica_num('Qual o lucro bruto deseja obter?')
    loja = input('Qual a loja em que vai publicar?')
    if mais_anuncios:
        preco_venda = []
        for mt in qtd_metros:
            qtd = mt
            preco = precificacao(custo_bruto,desconto,qtd,lucro,loja)
            preco_venda.append(preco)
            print(os.system('cls'))
    else:
        qtd = qtd_metros
        print(os.system('cls'))
        preco_venda = precificacao(custo_bruto,desconto,qtd,lucro,loja)
    
    print(f'\nPreço Custo: {custo_bruto}\n Preço Venda: {preco_venda}\n')
elif pergunta == 'n' or pergunta == 'N':
    if mais_anuncios:
        preco_venda = []
        for mt in qtd_metros:
            preco = verifica_num(f"Qual o preço do anuncio de {mt} metro(s)? ")
            preco_venda.append(preco)
    else:
        preco_venda = verifica_num("Defina o preço de venda do anuncio:")

print(os.system('cls'))
cabecalho("DESCRIÇÃO")
# RETORNA A DESCRICAO, PERGUNTA SE TEM DESCRICAO DE REFERENCIA OU NAO...
descricao = Descricao(palavra_chave,composicao,qtd_metros,largura_tecido)

pedir_gpt = perg_s_n('Pedir ao chatgpt para criar uma descricao? (s/n)')

if pedir_gpt == 's':
    pergunta = perg_s_n('Vamos pedir ao CHAT GPT a descrição. Você tem uma descrição de referencia?')
    if pergunta == 's':
        while True:
            print(os.system('cls'))
            cabecalho("DESCRIÇÃO")
            body('A descricao de referencia deve ser colada no arquivo "descricao.txt" que está na pasta')
            descricao_gpt = descricao.desc_chatgpt(ref = True)
            print(os.system('cls'))
            cabecalho("DESCRIÇÃO")
            print(descricao_gpt)
            
            aprovado = perg_s_n('Gostou da descrição?(s/n)')
            if aprovado == 's':
                break
            elif aprovado == 'n':
                print("\nVamos fazer novamente!\n")
                
    elif pergunta == 'n':
        while True:
            descricao_gpt = descricao.desc_chatgpt(ref = False)
        
            print(os.system('cls'))
            cabecalho("DESCRIÇÃO")
            print(descricao_gpt)
            
            aprovado = perg_s_n('Gostou da descrição?(s/n)')
            if aprovado == 's' or aprovado == 'S':
                break
            elif aprovado == 'n' or aprovado == 'N':
                print("\nVamos fazer novamente!\n")
            
elif pedir_gpt == 'n' or pedir_gpt == 'N':
    body('A descricao deve ser colada no arquivo "descricao.txt" que está na pasta')
    while True:
        prossiga = input("Se já tiver colado a descricao no arquivo, digite enter...")
        if prossiga:
            prossiga = input("Digite enter para continuar...")
        else:
            descricao_gpt = Descricao.descricao_referencia()
            break
    

#MONTA A DESCRICAO COM INFORMAÇÕES DE COMPRA, DO TECIDO E DESCRICAO.
descricao_final = descricao.monta_descricao(descricao_gpt)

#DEFINE O SKU QUE VAI SER CADASTRO NO BLING
if atacado.lower() == 'disparada':
    ref_atacado = 'D'
elif atacado.lower() == 'aquarela':
    ref_atacado = 'A'

if mais_anuncios:
    ref = cod
    cod = []
    for mt in qtd_metros:
        if mt != 1:
            art = f'{mt:,.0f}m-{ref_atacado}{ref}'
            cod.append(art)
        else:
            art = f'{ref_atacado}{ref}'
            cod.append(art)
else:
    if qtd_metros != 1:
        cod = f'{qtd_metros:,.0f}m-{ref_atacado}{cod}'
    else:
        cod = f'{ref_atacado}{cod}'

# ------------ DAQUI PRA BAIXO JÁ TEMOS TODAS AS INFORMAÇÕES ARMAZENADAS PARA REALIZAR O CADASTRO----------------

# CONFIRMA OS DADOS QUE SERÃO CADASTRADOS E PERGUNTA SE PODE SEGUIR COM O CADASTRO NO BLING

pasta_produto,titulo_anuncio,composicao,cod,preco_venda,origem,ncm,img_capa,alt,larg,profund,peso = print_info_produto(pasta_produto,
                                                                                                                       titulo_anuncio,
                                                                                                                       composicao,cod,
                                                                                                                       preco_venda,
                                                                                                                       origem,ncm,
                                                                                                                       img_capa,alt,
                                                                                                                       larg,profund,peso)

#AQUI QUE REALIZA A REQUISIÇÃO PARA FINALMENTE CADASTRAR

if mais_anuncios:
    qtd_lancar = float(input('Quantos metros deseja lançar em cada variação?'))
    for i,x in enumerate(qtd_metros):
        cadastro = Produto(img_capa,pasta_produto,titulo_anuncio[i],cod[i],preco_venda[i],descricao_final[i],peso[i],origem,ncm,img_capa,
                        alt[i],larg[i],profund[i]).cadastrar(mudou_nome)
        if cadastro == 201:
            print(os.system('cls'))
            cabecalho("CADASTRO BLING")
            print('Produto cadastrado no Bling com Sucesso.\n Vamos lançar o estoque.')
            Estoque(cod[i],qtd_lancar).lanca_estoque()
        monta_capa(pasta_produto, img_capa, titulo_tecido=nome_tecido)
else:

    cadastro = Produto(img_capa,pasta_produto,titulo_anuncio,cod,preco_venda,descricao_final,peso,origem,ncm,img_capa,
                            alt,larg,profund).cadastrar(mudou_nome)

    #-----------AGORA SE TUDO TIVER DADO CERTO, VAMOS LANCAR O ESTOQUE DAS VARIAÇÕES.
    #-----------SERÃO LANÇADOS TODOS OS ESTOQUES IGUAIS POIS É ASSIM QUE FAÇO NORMALMENTE.
    if cadastro == 201:
        print(os.system('cls'))
        cabecalho("CADASTRO BLING")
        print('Produto cadastrado no Bling com Sucesso.\n Vamos lançar o estoque.')
        qtd_lancar = float(input('Quantos metros deseja lançar em cada variação?'))
        Estoque(cod,qtd_lancar).lanca_estoque()
        



    
