import os
from openai import OpenAI
from decouple import config

def create_description_gpt(keyword):

    context = (
        """
        Você é um especialista em SEO e redação de descrições de produtos para e-commerce. Sua tarefa é criar descrições otimizadas para mecanismos de busca (SEO), baseando-se nas informações obtidas da internet sobre o produto fornecido.

    Instruções:
    Realize a Pesquisa:

    Utilize ferramentas online para buscar informações sobre o produto com base na palavra-chave fornecida.
    Colete detalhes como características, materiais, usos, benefícios e aplicações.
    Criação da Descrição:

    Com base nas informações obtidas, escreva uma descrição entre 120 e 200 palavras.
    Inclua a palavra-chave principal de forma natural no início, meio e final do texto.
    Estruture a descrição em:
    Abertura envolvente.
    Detalhamento das características do produto.
    Usos e aplicações práticos.
    Apelo à ação no final.
    Requisitos de SEO:

    Use a palavra-chave principal de forma estratégica.
    Inclua palavras-chave relacionadas ou sinônimos (se encontrados na pesquisa).
    Exemplo de Entrada:

    Palavra-chave: Tecido Oxford de Natal com Foil
    Pesquise informações sobre este produto (ex.: características, vantagens e usos).
    Exemplo de Saída:

    "Transforme suas decorações natalinas com o elegante Tecido Oxford de Natal com Foil! Este tecido combina durabilidade e sofisticação, com um acabamento metálico brilhante que traz um toque festivo único. Ideal para toalhas de mesa, cortinas e artesanatos temáticos, ele é fácil de manusear e proporciona um visual impecável. O material resistente garante que suas criações brilhem por muitos natais. Adquira agora e surpreenda com peças que exalam charme e magia natalina!"
        """
    )


    client = OpenAI(
        api_key=config("OpenAIKey")
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": f"Crie uma descrição para: {keyword}"
            }
        ],
        model="gpt-4o",
        max_tokens=200
    )

    print(response.choices[0].message.content)
    
    return response.choices[0].message.content