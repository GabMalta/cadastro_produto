"""
Inspiração de Uso — núcleo portátil (sem Django, sem Bling) extraído de
agentes/inspiracao_uso.py (legitima_lojavirtual).

Fluxo em 2 passos (regra de negócio real do agente — controle de custo antes de gastar com o
Gemini, que é caro comparado à Claude escrevendo o prompt):
1. `escrever_prompt_inspiracao()` — a Claude lê um briefing e escreve o prompt de imagem (barato).
2. `gerar_imagem_inspiracao()` — gera a arte no Gemini ancorada numa foto de referência (caro).

O *gate de aprovação humana* entre os dois passos (mostrar o prompt pra revisão antes de gerar) é
mecanismo de UX do projeto original (painel Django) e não foi portado — quem chama decide se/como
aprovar entre as duas chamadas. Sem persistência: nenhuma das duas funções grava nada em banco
nem sobe pra S3, só devolvem dict/bytes pra quem chama decidir o que fazer.
"""
import json

from .claude_client import chamar
from .imagem_client import gerar_imagem
from .render_utils import baixar_imagem, selo_ilustrativo

SYSTEM_PROMPT = (
    "Você escreve prompts de geração de imagem para a foto secundária de \"inspiração de uso\" "
    "de um tecido no marketplace. A foto principal já mostra o tecido; a sua mostra o CONTEXTO — "
    "uma cena que faz a cliente imaginar o que ela vai criar com ele.\n\n"
    "Você recebe o briefing pesquisado da família do tecido (com os usos reais) e uma foto do "
    "tecido que será passada ao gerador como REFERÊNCIA de cor e textura.\n\n"
    "REGRAS DA CENA:\n"
    "- Escolha UM uso real citado no briefing — o mais aspiracional pra quem compra (ver as "
    "personas do contexto: costureira profissional e ateliê de festa/noivas pesam mais; se o "
    "tecido é de artesanato/decoração, pense na hobbyista).\n"
    "- Cena de AMBIENTE, SEM PESSOAS (nem mãos, nem rostos): o vestido no manequim ou cabide, a "
    "mesa posta, a bancada de ateliê, a poltrona. O tecido da referência deve aparecer na cena "
    "aplicado nesse uso, com a MESMA cor e textura da foto de referência.\n"
    "- SEM texto, logotipo, marca d'água ou letras na imagem.\n"
    "- Luz e clima aspiracionais mas realistas (foto editorial, não render 3D artificial). "
    "Composição quadrada.\n"
    "- NÃO invente características que o briefing não afirma (se o briefing não diz que o tecido "
    "tem brilho, não peça brilho).\n\n"
    "REFAÇÃO: quando a mensagem trouxer um prompt anterior e um pedido do revisor, você está "
    "REVISANDO, não criando do zero — reescreva o prompt incorporando exatamente o que foi "
    "pedido e preserve o que não foi criticado (cena, aplicação do tecido, estilo). As regras de "
    "sempre continuam valendo (sem pessoas, sem texto, referência de cor/textura).\n\n"
    "SAÍDA (JSON):\n"
    "- 'prompt': o prompt de imagem EM INGLÊS (o gerador entende melhor), 60–120 palavras, "
    "descrevendo cena, aplicação do tecido de referência, iluminação, atmosfera e estilo "
    "fotográfico. Inclua instruções como 'use the provided fabric photo as the exact color and "
    "texture reference' e 'no people, no text'.\n"
    "- 'cena': uma ou duas palavras EM PORTUGUÊS nomeando a cena (ex.: 'festa', 'ateliê', "
    "'mesa posta').\n"
    "- 'justificativa': 1–2 frases EM PORTUGUÊS explicando por que esta cena vende este tecido "
    "(pro dono decidir rápido).\n\n"
    "Responda SOMENTE com o objeto JSON: {\"prompt\": \"...\", \"cena\": \"...\", "
    "\"justificativa\": \"...\"}"
)


def _parse_json(texto: str) -> dict:
    """Extrai o objeto JSON da resposta, tolerando cercas ```json e texto ao redor."""
    t = texto.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1]
        if t.startswith("json"):
            t = t[4:]
    ini, fim = t.find("{"), t.rfind("}")
    if ini == -1 or fim == -1:
        raise ValueError("Resposta sem objeto JSON.")
    return json.loads(t[ini:fim + 1])


def _bloco_feedback(feedback: str | None, prompt_anterior: str | None) -> str:
    """Se houver feedback do revisor, monta o bloco com o prompt anterior + o pedido, para o
    modelo revisar em vez de criar do zero. Sem feedback, devolve string vazia."""
    feedback = (feedback or "").strip()
    if not feedback:
        return ""
    return (
        "PROMPT ANTERIOR (que você mesmo escreveu):\n"
        f"{prompt_anterior or ''}\n\n"
        f"O revisor pediu estes ajustes: {feedback}\n"
        "Reescreva o prompt incorporando o pedido (REFAÇÃO — preserve o que não foi criticado).\n\n"
    )


def escrever_prompt_inspiracao(
    *,
    nome_tecido: str,
    briefing: str,
    contexto: str,
    feedback: str | None = None,
    prompt_anterior: str | None = None,
    modelo: str = "sonnet",
) -> dict:
    """
    Passo 1: a Claude escreve o prompt de imagem (barato).

    `contexto` é uma string já montada por quem chama (tom de voz + personas + o que mais fizer
    sentido). Retorna {prompt, cena, justificativa, custo_usd, tokens_input, tokens_output}.
    """
    system = f"{SYSTEM_PROMPT}\n\n---\n\nCONTEXTO:\n\n{contexto}"
    conteudo = (
        "Escreva o prompt de inspiração de uso para este tecido:\n\n"
        f"Nome do produto: {nome_tecido}\n\n"
        f"BRIEFING DA FAMÍLIA (usos reais):\n{briefing}\n\n"
        f"{_bloco_feedback(feedback, prompt_anterior)}"
        "Retorne só o JSON com prompt, cena e justificativa."
    )
    resposta = chamar(
        modelo=modelo, system=system,
        mensagens=[{"role": "user", "content": conteudo}],
    )
    dados = _parse_json(resposta["texto"])
    prompt = str(dados.get("prompt", "")).strip()
    if not prompt:
        raise ValueError("Resposta sem 'prompt'.")
    return {
        "prompt": prompt,
        "cena": str(dados.get("cena", "")).strip(),
        "justificativa": str(dados.get("justificativa", "")).strip(),
        "custo_usd": resposta["custo_usd"],
        "tokens_input": resposta["tokens_input"],
        "tokens_output": resposta["tokens_output"],
    }


def gerar_imagem_inspiracao(
    prompt: str,
    referencia_url: str | None = None,
    aspect: str = "1:1",
) -> bytes:
    """
    Passo 2: gera a arte no Gemini ancorada na foto real (referência de cor/textura, se vier
    `referencia_url`) e aplica o selo "imagem ilustrativa". Devolve os bytes finais (JPEG).

    Falha barulhenta (levanta) se o download da referência ou a geração falharem — diferente do
    agente original, aqui NÃO tem fallback silencioso "gera sem âncora": quem chama decide se
    quer tentar de novo sem referência.
    """
    referencia = baixar_imagem(referencia_url) if referencia_url else None
    imagem = gerar_imagem(prompt, referencia=referencia, aspect=aspect)
    return selo_ilustrativo(imagem)
