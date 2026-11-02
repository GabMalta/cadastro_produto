from nucleo_ia.pesquisa_tecido import pesquisar_tecido
from nucleo_ia.curador_descricao import curar_descricao


def criar_descricao_completa(nome: str, codigo: str) -> dict:

    with open("nucleo_ia/contexto/glossario-produto.md", "r") as c:
        contexto = c.read()

    pesquisa = pesquisar_tecido(nome=nome, contexto=contexto)

    briefing = pesquisa.get("briefing")
    custo_briefing = pesquisa.get("custo_usd")
    
    print("Briefing gerado")

    descricao = curar_descricao(
        codigo=codigo, nome=nome, contexto=contexto, briefing=briefing
    )
    custo_descricao = descricao.get("custo_usd")
    
    print("Descricao criada")
    print(f"Custo Briefing:{custo_briefing}\nCusto Descricao:{custo_descricao}")
    
    
    return {"descricao": descricao.get("descricao"), "briefing": briefing}
