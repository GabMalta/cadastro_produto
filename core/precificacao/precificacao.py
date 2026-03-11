from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


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
            pergunta = input('Plataforma não encontrada, podemos utilizar a Shopee como padrão? (s/n)')
            if pergunta == 's':
                plataforma = 'shopee'
            else:
                plataforma = input('Qual a loja em que vai publicar? ')
    
    return f'{preco_venda:,.2f}'