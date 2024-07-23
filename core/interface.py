import time
import os
def linha(tam=40):
    """
    Renderizar linhas divisorias no programa.
    
    Arg: int, opcional

    Return: str

    """    
    return '-' * tam


def cabecalho(msg):
    """ Titulo do Cabeçalho formatado

        args: str, titulo do cabecalho
        
        Return: Cabecalho renderizado
    """
    print(linha())
    print(msg.center(40))
    print(linha())

def body(body, limpa_tela=False):
    """ Printa a mensagem no programa
        Caso o argumento limpa_tela for verdadeiro, limpa todo o programa
    """
    
    if limpa_tela:
        os.system('cls')
    print(body.center(40) + '\n')

def perg_s_n(pgt):
    """ Faz a verificação se a resposta do usuario sera 's' ou 'n' """
    
    pergunta = input(pgt + ' ')
    pergunta = pergunta.lower()
    while True:
        if pergunta == "s" or pergunta == "n":
            break
        else:
            print("Responda com 's' para sim ou 'n' para não\n")
            pergunta = input(pgt)
            pergunta = pergunta.lower()
    return pergunta

def verifica_num(pgt,tipo='f'):
    """ VERIFICA SE A ENTRADA SERA UM NUMERO
        Args:   pgt (str): A pergunta que o usuário deverá responder
                tipo (str): o tipo de numero que o usuario devera digitar 'f' para float ou 'i' para int
        
        Return: o numero digitado pelo usuario
        """
    pergunta = input(pgt + ' ')
    while True:
        if tipo == 'i':
            try:
                pergunta = int(pergunta)
                break
            except:
                print("\nRESPONDA COM UM NÚMERO INTEIRO\n")
                pergunta = input(pgt + ' ')
        elif tipo == 'f':
            try:
                pergunta = float(pergunta)
                break
            except:
                print("\nRESPONDA COM UM NÚMERO\n")
                pergunta = input(pgt + ' ')
    return pergunta
            

def pega_info_produto():
    atacado = input('De qual atacado é o tecido?')
    cod = input('Qual o código do tecido ? ')
    palavra_chave = input("Qual o titulo do anuncio que vamos criar? ")
    
    mais_anuncios = perg_s_n("Vai criar mais de um anuncio com metragens diferentes? (s/n) ")
    if mais_anuncios == 's':
        qtd_metros,alt,larg,profund,peso = cria_lista("Digite os dados variáveis dos anuncios: \n", 'Metragem', 'Altura', 'Largura', 'Profundidade', 'Peso').values()
        mais_anuncios = True
    elif mais_anuncios == 'n':
        qtd_metros = verifica_num('O anúncio será de quantos metros?')
        alt = verifica_num('Altura:')
        larg = verifica_num('Largura:')
        profund = verifica_num('Profundidade:')
        peso = verifica_num('Peso:')
        mais_anuncios = False
    
    origem = verifica_num('Origem (0 ou 2):','i')
    ncm = input('NCM: ')
    
    
    print(os.system('cls'))
    
    return mais_anuncios,atacado,cod,palavra_chave,qtd_metros,peso,origem,ncm,alt,larg,profund

def print_info_produto(pasta_produto,titulo_anuncio,composicao,cod,preco_venda,origem,ncm,img_capa,alt,larg,profund,peso):
    while True:
        print(f'Caminho da pasta: {pasta_produto}')
        print(f'Titulo do anúncio: {titulo_anuncio}')
        print(f'Composição: {composicao}')
        print(f'Código do anúncio: {cod}')
        print(f'Preço: {preco_venda}')
        print(f'Origem: {origem}')
        print(f'NCM: {ncm}')
        print(f'Imagem de capa: {img_capa}')
        print(f'Altura: {alt}')
        print(f'Largura: {larg}')
        print(f'Profundidade: {profund}')
        print(f'Peso: {peso}')

        continuar = perg_s_n('Podemos continuar?\n Digite "s" para sim ou "n" para trocar alguma informação')
    
        if continuar == 's':
            break
        
        elif continuar == 'n' or continuar == 'N':
            altera = verifica_num('''Digite o número da opção de atributo deseja alterar?
                            1.Caminho da pasta
                            2.Titulo do anúncio
                            3.Código do anúncio
                            4.Preço
                            5.Origem
                            6.NCM
                            7.Imagem de capa
                            8.Altura
                            9.Largura
                            10.Profundidade
                            11.Peso 
                            ''')
            match altera:
                case '1':
                    pasta_produto = input('Digite o novo caminho da pasta do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '2':
                    titulo_anuncio = input('Digite o novo título para o produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '3':
                    cod = input('Digite o novo código para o produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '4':
                    preco_venda = input('Digite o preço de venda do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '5':
                    origem = input('Digite qual a origem fiscal do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '6':
                    ncm = input('Digite o novo NCM do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '7':
                    img_capa = input('Digite o novo caminho da imagem de capa do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '8':
                    alt = input('Digite a nova altura do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '9':
                    larg = input('Digite a nova largura do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '10':
                    profund = input('Digite a nova profundidade do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case '11':
                    peso = input('Digite o novo peso do produto: ')
                    print(os.system('cls'))
                    cabecalho("CONFERENCIA DE INFORMAÇÕES")
                    body("Confira os dados que serão cadastrados")
                case _:
                    print('Número inválido. Insira um númeo de 1 a 11')

    return pasta_produto,titulo_anuncio,composicao,cod,preco_venda,origem,ncm,img_capa,alt,larg,profund,peso
    
def cria_lista(msg,*args):
    print(msg)
        
    
    anuncio = {}
    
    num_anuncios = verifica_num("Quantos anuncios serão? ", 'i')
    
    for i in range(num_anuncios):
        for x in args:
            mt = verifica_num(f"Digite {x} do anuncio {i+1} ou aperte 'ENTER' para terminar: ")
            if x in anuncio:
                anuncio[x].append(mt)
            else:
                anuncio[x] = [mt]
        print('\n')
         
    return anuncio

    
    