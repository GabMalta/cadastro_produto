# file: gerar_usos_tecido.py
import os
import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

SYSTEM_INSTRUCTIONS = (
    "Você é um especialista em moda e tecidos para marketplaces. "
    "Receba o nome de um tecido e sua composição e retorne exatamente 5 principais usos recomendados, fundamentados nas características do tecido e casos de uso que tenha em sua base. "
    "Regras de saída: responder em UMA ÚNICA STRING; separar os usos por vírgula; "
    "cada uso começa com letra maiúscula; termos curtos e objetivos otimizados para marketplaces; "
    "evitar repetições;"
    # "evitar termos genéricos como 'Roupas', 'Vestuário', 'Confecção em geral', 'Acessórios', 'Decoração' sem especificação."
)

# SYSTEM_INSTRUCTIONS = (
#     "Você é um especialista em têxteis para marketplaces. "
#     "Receba o nome de um tecido e produza usos específicos do ponto de vista técnico, "
#     "fundamentados nas características do tecido (brilho, caimento, gramatura, toque, elasticidade, opacidade, resistência, composição e acabamento). "
#     "Responda SEMPRE em uma ÚNICA STRING, com EXATAMENTE 5 itens separados por vírgula. "
#     "Cada item deve ser curto (3–7 palavras), iniciar com maiúscula e refletir aplicações REALISTAS e comuns para aquele tecido. "
#     "Evite termos genéricos como 'Roupas', 'Vestuário', 'Confecção em geral', 'Acessórios', 'Decoração' sem especificação. "
#     "Prefira itens como 'Vestidos de festa com caimento', 'Lingerie com toque acetinado', 'Forro de alfaiataria leve', 'Camisolas e pijamas finos', 'Cortinas leves com brilho'. "
#     "Nunca repita o mesmo conceito com palavras diferentes."
# )

def gerar_usos_tecido(nome_tecido: str, composicao: str, model: str = "gpt-5-mini") -> str:

    prompt_usuario = (
        f"Tecido: {nome_tecido}\n"
        f"Composição: {composicao}\n"
        "Retorne apenas a lista final (sem títulos), por exemplo:\n"
        "Confecção de Vestidos de Festa, Forro de Roupas Sociais, "
        "Saias Sofisticadas, Decoração (Cortinas e Almofadas), Artesanato e Fantasias"
    )

    resp = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt_usuario},
        ],
    )

    saida = resp.choices[0].message.content

    # Pós-validação simples: garantir 5 itens separados por vírgula
    partes = [p.strip() for p in saida.split(",") if p.strip()]
    if len(partes) != 5:
        # Tenta normalizar removendo possíveis quebras de linha e vírgulas duplicadas
        saida = ", ".join(partes[:5]) if partes else saida
    return saida

