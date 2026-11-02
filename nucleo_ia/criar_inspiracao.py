from nucleo_ia.pesquisa_tecido import pesquisar_tecido
from nucleo_ia.curador_descricao import curar_descricao
from nucleo_ia.inspiracao_uso import escrever_prompt_inspiracao, gerar_imagem_inspiracao
import os, json, random


def criar_inspiracao(nome: str, path_fotos: str, path_cover: str):
    
    image_urls = os.path.join(path_fotos, "image_urls.json")
    briefing_path = os.path.join(path_fotos, "briefing.md")
    
    if not os.path.exists(image_urls):
        print("Path de fotos ou image_urls nao encontrado")
        return
    
    with open(image_urls, "r") as a:
        json_urls = json.load(a)
        
    with open("nucleo_ia/contexto/glossario-produto.md", "r") as c:
        contexto = c.read()
    
    
    if not os.path.exists(briefing_path):
        
        pesquisa = pesquisar_tecido(nome=nome, contexto=contexto)

        briefing = pesquisa.get("briefing")
        
        with open(briefing_path, "w", encoding="utf-8") as a:
            a.write(briefing)
    else:
        with open(briefing_path, "r", encoding="utf-8") as a:
            briefing = a.read()    
    
    prompt_inspiracao = escrever_prompt_inspiracao(nome_tecido=nome, briefing=briefing, contexto=contexto).get("prompt")
    
    chave_aleatoria = random.choice(list(json_urls.keys()))
    url_referencia = json_urls[chave_aleatoria]["img"]
    
    imagem_inspiracao = gerar_imagem_inspiracao(prompt=prompt_inspiracao, referencia_url=url_referencia)
    
    with open(rf"{path_cover}/IA_01.jpg", "wb") as f:
        f.write(imagem_inspiracao)
        