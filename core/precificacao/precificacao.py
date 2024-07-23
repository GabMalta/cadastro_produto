from core.interface import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def precificacao(preco_custo_bruto, percent_desconto_atacado, qtd_metros, percent_lucro_desejado, plataforma=''):
    
    percent_desconto_atacado = percent_desconto_atacado / 100
    percent_lucro_desejado = percent_lucro_desejado/100
    imposto = 0.05
    
    while True:
        if plataforma.lower() == 'site':
                            
            marketing = 0.1
            plataforma_pgto = 0.08
            frete = 0.05

            preco_custo_total = (preco_custo_bruto*qtd_metros) - (preco_custo_bruto*percent_desconto_atacado)
            porcent_sobrar = 1 - (marketing + imposto + plataforma_pgto + frete + percent_lucro_desejado)
            preco_venda = preco_custo_total / porcent_sobrar
            break
        
        elif plataforma.lower() == "shopee":
            
            comissao_shopee = 0.2
            taxa_shopee = 3
            porcent_sobrar = 1 - (comissao_shopee + imposto + percent_lucro_desejado)

            preco_custo_bruto = preco_custo_bruto*qtd_metros
            preco_custo_total = preco_custo_bruto - (preco_custo_bruto*percent_desconto_atacado) + taxa_shopee
            preco_venda = preco_custo_total / porcent_sobrar
            break
        
        else:
            pergunta = perg_s_n('Plataforma não encontrada, podemos utilizar a Shopee como padrão? (s/n)')
            if pergunta == 's':
                plataforma = 'shopee'
            else:
                plataforma = input('Qual a loja em que vai publicar? ')
    
    return f'{preco_venda:,.2f}'

def pega_preco(cod):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)
    
    usuario = 'gabrielm'
    senha = '123gabriel*'
    
    nav.get('https://sistema.disparadatecidos.com.br')
    
    nav.find_element(By.ID, "input_user").send_keys(usuario)
    nav.find_element(By.ID, "input_pass").send_keys(senha)
    nav.find_element(By.ID, "btn_login").click()
    time.sleep(2)
    nav.find_element(By.PARTIAL_LINK_TEXT, "Artigos").click()
    time.sleep(5)
    nav.find_element(By.ID, "input_search_name").send_keys(cod)
    nav.find_element(By.ID, "button_search").click()
    preco = nav.find_element(By.CLASS_NAME, "right").text
    preco = preco.replace('R$ ','')
    preco = preco.replace(',','.')
    preco = float(preco.replace(' / m',''))
    
    return(preco)