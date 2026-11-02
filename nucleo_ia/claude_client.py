"""
Cliente da Claude API com cálculo de custo — cópia Django-free de agentes/claude_client.py
(legitima_lojavirtual). Única mudança: a chave da API vem de `os.environ` em vez de
`django.conf.settings`. Inclui `chamar_com_web_search` (usado pelo Pesquisador de Tecido,
nucleo_ia/pesquisa_tecido.py).

IDs de modelo e preços verificados em jul/2026 — confirme a tabela vigente antes de assumir.

IMPORTANTE: Sonnet 5 e Opus 4.8 REJEITAM (HTTP 400) parâmetros de sampling
(temperature/top_p/top_k). Por isso `chamar()` NÃO envia temperature — o steering é feito
via prompt.

IMPORTANTE 2 — `max_tokens` inclui o THINKING: o Sonnet 5 roda thinking adaptativo por padrão
(quando o parâmetro `thinking` é omitido, como aqui), e o raciocínio é cobrado e conta no teto
mesmo chegando com texto vazio (`thinking.display == "omitted"`). Um `max_tokens` apertado é
gasto pensando e corta a resposta no meio. Não passamos `thinking` explícito de propósito: o
Haiku 4.5 não aceita `{"type": "adaptive"}` e o default de cada modelo já é o que queremos.
"""
import os
import time
from decimal import Decimal
from decouple import config

from anthropic import Anthropic


client = Anthropic(api_key=config("ANTHROPIC_API_KEY") or None)

# Apelido -> ID de modelo (confirmar disponibilidade na sua conta).
MODELOS = {
    "haiku": "claude-haiku-4-5",
    "sonnet": "claude-sonnet-5",
    "opus": "claude-opus-4-8",
}

# Preços por 1M de tokens (input, output) em USD. Atualizar conforme tabela vigente.
PRECOS = {
    "haiku": (Decimal("1.00"), Decimal("5.00")),
    "sonnet": (Decimal("3.00"), Decimal("15.00")),
    "opus": (Decimal("5.00"), Decimal("25.00")),
}

# Teto de output por chamada. Cobre thinking + texto (ver docstring do módulo).
MAX_TOKENS_PADRAO = 16000

# Busca web (server-tool): US$ 10 por 1.000 buscas = US$ 0,01 por busca. Buscas com erro não
# são cobradas — a API já reflete o cobrável em usage.server_tool_use.web_search_requests.
PRECO_WEB_SEARCH_POR_BUSCA = Decimal("0.01")


class RespostaTruncada(RuntimeError):
    """A resposta bateu o teto de max_tokens e veio incompleta."""


def calcular_custo(apelido: str, tokens_in: int, tokens_out: int) -> Decimal:
    pi, po = PRECOS[apelido]
    return (Decimal(tokens_in) * pi + Decimal(tokens_out) * po) / Decimal(1_000_000)


def custo_web_search(buscas: int) -> Decimal:
    return Decimal(buscas) * PRECO_WEB_SEARCH_POR_BUSCA


def _checar_truncada(resposta, max_tokens: int) -> None:
    """
    Falha barulhenta quando a resposta bateu o teto. Sem isso o texto volta cortado e o erro
    aparece longe daqui, como um parse de JSON que falha sem explicar por quê.
    """
    if resposta.stop_reason == "max_tokens":
        raise RespostaTruncada(
            f"A resposta bateu o teto de max_tokens ({max_tokens}) e veio cortada "
            f"({resposta.usage.output_tokens} tokens de saída). Lembre que o teto cobre o "
            "thinking do modelo, não só o texto: aumente max_tokens ou peça uma saída menor."
        )


def chamar(
    modelo: str,
    system: str,
    mensagens: list[dict],
    max_tokens: int = MAX_TOKENS_PADRAO,
) -> dict:
    """
    Chama a Claude API e retorna texto + métricas de custo.

    `modelo` é o apelido ('haiku' | 'sonnet' | 'opus').
    """
    inicio = time.time()
    resposta = client.messages.create(
        model=MODELOS[modelo],
        max_tokens=max_tokens,
        system=system,
        messages=mensagens,
    )
    _checar_truncada(resposta, max_tokens)
    texto = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
    tokens_in = resposta.usage.input_tokens
    tokens_out = resposta.usage.output_tokens
    return {
        "texto": texto,
        "tokens_input": tokens_in,
        "tokens_output": tokens_out,
        "custo_usd": calcular_custo(modelo, tokens_in, tokens_out),
        "duracao_s": time.time() - inicio,
        "modelo": MODELOS[modelo],
    }


def chamar_com_web_search(
    modelo: str,
    system: str,
    mensagens: list[dict],
    max_tokens: int = MAX_TOKENS_PADRAO,
    max_buscas: int = 5,
    max_continuacoes: int = 5,
) -> dict:
    """
    Igual a `chamar()`, mas habilita a tool server-side de busca na web e roda o loop
    server-side (tratando `stop_reason == "pause_turn"`). Retorna o mesmo dict de `chamar()`,
    somando o uso de todas as iterações.

    Exige um modelo que suporte `web_search_20260209` (Sonnet 5, Opus 4.6/4.7/4.8). O apelido
    'sonnet' atende.

    `custo_usd` já inclui o custo das buscas (US$ 0,01/busca, ver `custo_web_search`) além dos
    tokens; `buscas_web` traz a contagem para logging.
    """
    inicio = time.time()
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": max_buscas}]
    mensagens = list(mensagens)
    tokens_in = tokens_out = buscas = 0
    resposta = None
    # +1 porque a primeira chamada não é uma "continuação".
    for _ in range(max_continuacoes + 1):
        resposta = client.messages.create(
            model=MODELOS[modelo],
            max_tokens=max_tokens,
            system=system,
            messages=mensagens,
            tools=tools,
        )
        tokens_in += resposta.usage.input_tokens
        tokens_out += resposta.usage.output_tokens
        uso_tool = getattr(resposta.usage, "server_tool_use", None)
        if uso_tool is not None:
            buscas += getattr(uso_tool, "web_search_requests", 0) or 0
        if resposta.stop_reason != "pause_turn":
            break
        # Loop server-side pausado: reenviar com o turno do assistente anexado. Não adicionar
        # um "Continue." — a API detecta o server_tool_use pendente e retoma sozinha.
        mensagens.append({"role": "assistant", "content": resposta.content})

    _checar_truncada(resposta, max_tokens)
    texto = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
    return {
        "texto": texto,
        "tokens_input": tokens_in,
        "tokens_output": tokens_out,
        "buscas_web": buscas,
        "custo_usd": calcular_custo(modelo, tokens_in, tokens_out) + custo_web_search(buscas),
        "duracao_s": time.time() - inicio,
        "modelo": MODELOS[modelo],
    }
