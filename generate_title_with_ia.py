import json
import openai
from decouple import config
from ddgs import DDGS

from functions import input_choices


def buscar_referencias(query: str, max_results: int = 5):
    """Busca referências no DuckDuckGo e retorna títulos e descrições resumidas."""

    try:
        with DDGS() as ddg:
            resultados = ddg.text(query, max_results=max_results)
            # Formata apenas título e descrição curta, ignorando resultados sem body
            refs_formatted = "\n######\n\n".join(
                [
                    f"Título: {r['title'][:80]}...  \nLink: {r['href']}  \nDescrição: {r['body'][:120]}..."
                    for r in resultados
                    if r.get("body")
                ]
            )
            return refs_formatted

    except Exception as e:
        print(f"Erro ao buscar referências: {e}")
        return ""


def ia_generate_title_variations(
    title: str, refs: str = "", info_aditional: str = "", number_of_variations: int = 5, model="gpt-4o-mini"
):

    openai.api_key = config("OPENAI_API_KEY")

    system_prompt = """
        Você é um especialista em SEO para e-commerce na Shopee. Seu trabalho consiste em criar títulos otimizados para os anúncios da Shopee. 
        Regras: 
        - Sempre comece o título utilizando a palavra "Tecido" 
        - Use a palavra-chave principal logo no início do título. 
        - O Anúncio normalmente sempre será de várias cores. 
        - Adicione o uso/aplicação do produto (ex: "para academia", "para praia", "para festa") 
        - Inclua um benefício ou diferencial (ex: "durável", "frete grátis", "secagem rápida") 
        - Otimizados para SEO dentro da Shopee 
        - Claros, chamativos e informativos 
        - Curtos (máximo 120 caracteres) 
        - Diferenciados entre si, mas mantendo relevância 
        - Adequados ao público brasileiro 
        - Não utilize metragem ou medidas nos títulos extraidos de site de busca,(ex:"(1m x 1,60m)")
    """

    prompt = f""" 
        Palavra-chave principal: "{title}" 
        
        Aqui estão algumas referências de busca relacionadas ao produto, que você deve usar apenas como inspiração:
        {refs} 
        
        Informações adicionais relevantes ao produto:
        {info_aditional}
        
        Com base nisso, gere exatamente {number_of_variations} variações de títulos otimizados para Shopee.
        
        Retorne apenas os títulos finais, um por linha, sem explicações extras.
    """

    response_api = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    try:
        titles = [t.strip() for t in response_api.choices[0].message.content.strip().split("\n") if t.strip()]
        return titles
    except Exception as e:
        print(e)
        response = response_api

    return response


def generate_title_variations(title, info_adicional="", number_of_variations: int = 5):

    refs = buscar_referencias(title, 10)
    print(f"GERANDO TITULOS COM GPT... {title}")
    titles = ia_generate_title_variations(title, refs, info_adicional, number_of_variations)

    choices = {f"{i}": t for i, t in enumerate(titles, start=1)}
    choices["0"] = ""

    return choices
