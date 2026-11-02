"""
Pesquisador de Tecido — núcleo portátil (sem Django, sem Bling) extraído de
agentes/pesquisa_tecido.py (legitima_lojavirtual).

Alimenta o Curador de Descrição: pesquisa na web sobre a FAMÍLIA do tecido (o que é, usos,
sinônimos, termos de busca) e devolve um briefing educativo em texto corrido — que depois vira o
parâmetro `briefing=` de `curador_descricao.curar_descricao()`.

Não portados de propósito (são específicos do projeto original, não da lógica do agente):
- **Cache/reuso do briefing por família** (lá, `Produto.pesquisa_tecido` no produto-pai). Aqui
  quem chama decide se e como cachear — ex.: guardar o texto retornado na sua própria tabela/
  arquivo, e só chamar `pesquisar_tecido()` de novo se não tiver nada salvo.
- **Encadear a sugestão de glossário** (lá, `_sugerir_glossario` após pesquisa nova) — é
  específico do fluxo de aprovação do painel Django deste projeto.
"""
from .claude_client import chamar_com_web_search

SYSTEM_PROMPT = (
    "Você é o Pesquisador de Tecido da loja. Use a busca na web para reunir informações GERAIS e "
    "educativas sobre a FAMÍLIA de um tecido (ex.: tricoline, cetim, zibeline): o que é, "
    "características típicas, para que serve, sinônimos e apelidos regionais, e os termos que "
    "clientes usam para procurá-lo. Consulte o glossário do contexto para falar a língua do nicho.\n\n"
    "REGRAS:\n"
    "- Você descreve a FAMÍLIA, não este item específico. NÃO afirme gramatura, largura, "
    "composição, cor, preço ou estoque de um produto — esses números vêm dos dados fornecidos, "
    "não da web.\n"
    "- Seja honesto: se não achar algo confiável, omita. Não invente.\n"
    "- Responda com um briefing curto em texto corrido (sem JSON, sem títulos markdown), em "
    "português-BR, com no máximo ~200 palavras. Termine com uma linha 'Termos de busca: a, b, c'."
)


def pesquisar_tecido(
    *,
    nome: str,
    contexto: str,
    categoria: str | None = None,
    descricao_atual: str | None = None,
    modelo: str = "sonnet",
    max_buscas: int = 5,
) -> dict:
    """
    Pesquisa a família do tecido na web e devolve o briefing.

    `contexto` é uma string já montada por quem chama (glossário é o mais relevante aqui — o
    prompt pede pra "falar a língua do nicho" — mas pode incluir mais). `descricao_atual` deve
    chegar já limpa se vier de HTML sujo (mesma observação de curador_descricao.curar_descricao).

    Retorna: {briefing, buscas_web, custo_usd, tokens_input, tokens_output}. `briefing` vem vazio
    (string "") se a busca não produzir texto — não levanta exceção nesse caso, mas propaga
    qualquer erro de rede/API normalmente.
    """
    system = f"{SYSTEM_PROMPT}\n\n---\n\nCONTEXTO:\n\n{contexto}"
    conteudo = (
        "Pesquise a família deste tecido e escreva o briefing:\n\n"
        f"Nome no cadastro: {nome}\n"
        + (f"Categoria: {categoria}\n" if categoria else "")
        + (f"Descrição do cadastro: {descricao_atual}\n" if descricao_atual else "")
    )
    resposta = chamar_com_web_search(
        modelo=modelo, system=system,
        mensagens=[{"role": "user", "content": conteudo}],
        max_buscas=max_buscas,
    )
    return {
        "briefing": resposta["texto"].strip(),
        "buscas_web": resposta.get("buscas_web", 0),
        "custo_usd": resposta["custo_usd"],
        "tokens_input": resposta["tokens_input"],
        "tokens_output": resposta["tokens_output"],
    }
