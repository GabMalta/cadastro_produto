"""
Curador de Descrição — núcleo portátil (sem Django, sem Bling) extraído de
agentes/curador_catalogo.py (legitima_lojavirtual).

Mesma lógica de prompt/parsing/bloco de metragem do agente original. Diferenças de propósito:
- Os dados do produto entram como parâmetros nomeados de `curar_descricao()`, não como um model
  Django (`Produto`)/payload cru (`dados_bling`).
- `contexto` é uma string já pronta (tom de voz + glossário + personas + o que mais o chamador
  quiser) — este módulo não lê nenhum arquivo do disco, ao contrário de agentes/contexto.py.
- O SYSTEM_PROMPT teve as menções a "dados do Bling" trocadas por "dados fornecidos"/"cadastro
  atual" (mudança só de redação — o Bling era a fonte da verdade de specs no projeto original;
  aqui quem chama decide o que fornecer). Fora isso, o texto é o mesmo.
- Sem `AgentRunner`/`AgentRun`/`AgentAction`: a função devolve o resultado direto, mais
  `custo_usd`/`tokens_input`/`tokens_output` pra quem quiser telemetria própria.

Pra uma descrição realmente boa, rode antes o Pesquisador de Tecido
(`nucleo_ia.pesquisa_tecido.pesquisar_tecido()`) e passe o texto devolvido como `briefing=` aqui
— é o mesmo papel que ele cumpre no projeto original (educar o Curador sobre a família do tecido
antes de escrever). Ver `nucleo_ia/README.md` pro pipeline completo.
"""
import json
import re

from .claude_client import chamar

# Abertura e fechamento do bloco de metragem. Servem de marcador: `_bloco_metragem` gera a partir
# daqui e `sem_bloco_metragem` corta o bloco inteiro usando os dois.
ABERTURA_METRAGEM = "<p>Cada unidade representa 1 metro de tecido"
# Reconhece o bloco inteiro (abertura...fechamento) em qualquer posição do texto — cobre tanto o
# formato atual (bloco antes da copy) quanto um eventual formato antigo (bloco depois).
_BLOCO_METRAGEM_RE = re.compile(
    r"(?:<p>)?Cada unidade representa 1 metro de tecido.*?e assim sucessivamente\.(?:</p>)?",
    re.DOTALL,
)

SYSTEM_PROMPT = (
    "Você é o Curador de Descrição de uma loja de tecidos. Enriqueça a ficha de um produto de "
    "tecido para a loja virtual. Use o tom de voz e o glossário do contexto. Seja específico e "
    "honesto: NÃO invente ficha técnica (gramatura, largura, composição) — use só o que vier nos "
    "dados fornecidos.\n\n"
    "A 'Descrição atual' vem do cadastro antigo e NÃO é confiável: pode estar truncada, incompleta "
    "ou ser de OUTRO tecido (copiar e colar errado). Se ela contradisser o nome do produto, confie "
    "no nome e no briefing — nunca na descrição. Aproveite dela só a ficha técnica que for "
    "coerente com o nome.\n\n"
    "PROIBIDO CANAL DE ATENDIMENTO: esta descrição vai para anúncio de marketplace (Shopee e "
    "similares). NUNCA mencione, sugira ou insinue WhatsApp, e-mail, telefone, SAC, chat, "
    "Instagram, Telegram, redes sociais ou qualquer outro canal de contato direto com a loja — em "
    "nenhuma parte do texto (título, corpo, FAQ), de forma alguma. Marketplaces derrubam ou banem "
    "anúncios que tentam desviar o comprador pra fora da plataforma. Isso vale mesmo que o CONTEXTO "
    "abaixo cite WhatsApp/Instagram/e-mail: esse material é compartilhado com outros agentes "
    "(atendimento, redes sociais) e essas menções NÃO se aplicam à descrição de produto — ignore-"
    "as pra este fim.\n\n"
    "TÍTULO: curto, legível para o comprador e otimizado para SEO/Google Shopping. Comece pela "
    "palavra-chave principal (o tipo de tecido) e complete com a característica/uso mais forte. "
    "Alvo de ~60 a 70 caracteres. NUNCA inclua número de cores nem quantidade "
    "(ex.: nada de '12 cores', 'kit', 'atacado'). Exemplos: 'Tecido Tricoline Estampado para "
    "Patchwork'; 'Cetim Charmeuse para Festa e Noiva'.\n\n"
    "DESCRIÇÃO: vende e explica o tecido para quem costura. Seis critérios, todos obrigatórios:\n"
    "1. CLAREZA: nas duas primeiras linhas o leitor entende o que o tecido É de fato.\n"
    "2. BENEFÍCIO ancorado em CARACTERÍSTICA: nunca liste só a spec. 'Soft 240 g/m²' é "
    "característica; 'toque macio que não pinica a pele da criança e mantém quentinho sem pesar' é "
    "benefício. Conecte os dois — a característica dá credibilidade, o benefício dá desejo. Só use "
    "specs que vieram dos dados fornecidos; sem spec, venda o benefício sem inventar número.\n"
    "3. OBJEÇÕES: antecipe as dúvidas reais de quem compra (ver personas.md — cor que pode vir "
    "diferente da foto, prazo, confiança na loja). Responda com honestidade, sem prometer o que "
    "não está nos dados.\n"
    "4. SEO PARA O GOOGLE: a descrição precisa ranquear na busca orgânica — é o tráfego da loja "
    "própria. Três regras concretas:\n"
    "   a) INTENÇÃO: o termo principal é o que a pessoa realmente digita no Google — normalmente "
    "'tecido <tipo>' ou '<tipo> por metro' (ex.: 'tecido soft por metro', 'malha suedine 100% "
    "algodão'). Ele precisa aparecer nas PRIMEIRAS 100 PALAVRAS da descrição, e casar com o "
    "título. E não pode MORRER ali: o termo e suas variações reaparecem ao longo do texto todo, "
    "inclusive nos headings e perto do fim — não adianta cravar no começo e nunca mais tocar.\n"
    "   b) CAUDA LONGA: espalhe naturalmente pelo texto as variações e os termos de uso real "
    "('tecido soft para pijama infantil', 'suedine para body de bebê'), incluindo os sinônimos e "
    "regionalismos do glossário. Use também as COMPARAÇÕES que a cliente busca quando forem "
    "verdadeiras pro tecido ('toque de seda', 'parecido com seda', 'seda sintética') — tem volume "
    "de busca alto e é comparação, não ficha técnica. Isso NÃO abre exceção pra gramatura, "
    "composição ou largura: essas continuam só se vierem dos dados fornecidos. O Google entende "
    "semântica: escrever para humano com vocabulário rico rende MAIS que repetir a palavra-chave. "
    "Repetição forçada (keyword stuffing) atrapalha.\n"
    "   c) SUBSTÂNCIA: mire ~300 palavras de conteúdo ÚTIL. Descrição curta e seca não ranqueia. "
    "MAS o volume tem que vir de informação real — o briefing, as specs fornecidas, usos, "
    "cuidados, quem usa e para quê. NUNCA encha linguiça, repita ideia ou floreie para bater a "
    "meta: texto inflado é pior que texto curto, para o Google e para a cliente. Sem matéria-"
    "prima, prefira 150 palavras boas a 300 vazias.\n"
    "5. ESCANEABILIDADE E ESTRUTURA: frases e parágrafos curtos. Use <ul><li> para os "
    "usos/benefícios — quem compra bate o olho, não lê parágrafo denso. Isso vale mesmo com ~300 "
    "palavras: o texto é maior, não mais denso.\n"
    "   Divida o texto em 2 a 4 seções com <h2>, e ponha o TERMO DE BUSCA no heading — é dos "
    "sinais on-page mais fortes pro Google e ajuda a cliente a achar o que quer. Ex.: 'Para que "
    "serve o cetim charmousse', 'Como cuidar do cetim charmousse'. Escolha as seções conforme o "
    "que você tem a dizer daquele tecido — NÃO siga um molde fixo, senão os produtos ficam todos "
    "iguais e o Google trata como template.\n"
    "   O parágrafo de abertura vem ANTES do primeiro <h2> (é ele que carrega a clareza e o termo "
    "nas primeiras 100 palavras).\n"
    "6. PERGUNTAS FREQUENTES: termine com <h2>Perguntas frequentes</h2> e 3 ou 4 perguntas reais, "
    "cada uma em <h3> com a resposta em <p>. Use as dúvidas que a cliente digita no Google "
    "('cetim charmousse estica?', 'qual a diferença entre cetim e charmousse?', 'serve pra "
    "vestido de festa?', 'como lavar?').\n"
    "   SOMENTE perguntas sobre O TECIDO: o que é, uso, toque, cuidado, diferença pra outro "
    "tecido. NUNCA sobre prazo de entrega, frete, troca, devolução ou pagamento — você não tem "
    "esses dados e responder seria inventar política da loja. Se a dúvida for dessas, não faça a "
    "pergunta. Não tente resolver essa insegurança de outro jeito no texto (ela fica pro processo "
    "de vendas da própria plataforma) — lembre-se da regra PROIBIDO CANAL DE ATENDIMENTO acima: "
    "nada de convidar pra WhatsApp, e-mail ou qualquer contato.\n\n"
    "As PALAVRAS-CHAVE do JSON são o mapa de busca do produto: o termo principal, as variações de "
    "cauda longa e os sinônimos/regionalismos — o que a cliente digita, não o nome técnico "
    "interno.\n\n"
    "Se vier um BRIEFING de pesquisa, use-o como apoio educativo, mas lembre: specs do item vêm "
    "dos dados fornecidos, não da web. NÃO escreva o texto de metragem/medidas de corte — isso é "
    "adicionado automaticamente depois.\n\n"
    "FORMATO da descrição: HTML simples, porque o destino renderiza HTML. Use apenas <p>, <h2>, "
    "<h3>, <ul>, <li>, <strong> e <br>, SEM atributos (nada de style=, class=). NUNCA use "
    "Markdown: nada de **negrito**, '- ' de lista ou '#' de título — isso apareceria cru para o "
    "cliente. Não repita o título do produto dentro da descrição.\n\n"
    "SEÇÃO não é RÓTULO. Um <h2> é uma seção: diz algo ao leitor e carrega o termo de busca — "
    "'Para que serve o cetim charmousse', 'Como cuidar do cetim charmousse'. Já 'Descrição:', "
    "'Benefícios:', 'Especificações:', 'Título:' são rótulos de formulário: NUNCA escreva isso, "
    "nem como heading nem como texto. (Exceção: 'Perguntas frequentes' é seção, e é a única de "
    "nome fixo.)\n\n"
    "LARGURA: preencha 'largura' APENAS se a largura útil estiver literalmente nos dados "
    "fornecidos (ex.: '1,45 m'); caso contrário use null. Nunca chute.\n\n"
    "Responda SOMENTE com um objeto JSON válido, sem texto fora dele, no formato: "
    '{"titulo": "...", "descricao": "<p>abertura</p><h2>seção com o termo</h2><p>...</p>'
    '<ul><li>...</li></ul><h2>Perguntas frequentes</h2><h3>pergunta?</h3><p>resposta</p>", '
    '"palavras_chave": ["..."], "tags": ["..."], "largura": "1,45 m" ou null}'
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


def _bloco_metragem(largura: str | None) -> str:
    """
    Bloco fixo (determinístico) que explica a venda por metro linear. Sempre presente na
    descrição, gerado por código (não pelo LLM). Usa a largura real quando fornecida; senão,
    versão genérica sem citar medida (honestidade: nunca uma largura errada).
    """
    largura = (largura or "").strip()
    if largura and largura.lower() not in {"null", "none", "n/a", "-"}:
        exemplos = (
            f"1 unidade: 1m x {largura}<br>"
            f"2 unidades: 2m x {largura}<br>"
            f"3 unidades: 3m x {largura}"
        )
        abertura = f"{ABERTURA_METRAGEM}, cortado em metragem linear contínua. Por exemplo:</p>"
    else:
        exemplos = "1 unidade: 1 metro<br>2 unidades: 2 metros<br>3 unidades: 3 metros"
        abertura = (
            f"{ABERTURA_METRAGEM}, cortado em metragem linear contínua "
            "(a largura acompanha a largura do rolo do tecido). Por exemplo:</p>"
        )
    return f"{abertura}\n<p>{exemplos}</p>\n<p>e assim sucessivamente.</p>"


def sem_bloco_metragem(descricao: str) -> str:
    """
    A descrição sem o bloco de metragem. Útil ao refazer: se for mostrar a sugestão anterior ao
    modelo (via `sugestao_anterior["descricao"]`), tire o bloco antes — senão o modelo ecoaria de
    volta e a metragem sairia duplicada.
    """
    return _BLOCO_METRAGEM_RE.sub("", descricao or "").strip()


def _resumo_produto(
    *, codigo: str, nome: str,
    categoria: str | None = None, preco: str | None = None,
    descricao_atual: str | None = None, cores: list[str] | None = None,
) -> str:
    """Resumo compacto do produto pra alimentar o prompt (equivalente a _resumo_produto no
    agente original, mas recebendo parâmetros em vez de ler de um model Django)."""
    partes = [f"Código: {codigo}", f"Nome atual: {nome}"]
    if categoria:
        partes.append(f"Categoria: {categoria}")
    if preco:
        partes.append(f"Preço: R$ {preco}")
    if descricao_atual:
        partes.append(f"Descrição atual (do cadastro, pode estar errada ou desatualizada):\n{descricao_atual}")
    if cores:
        partes.append(f"Variações/cores ({len(cores)}): " + "; ".join(cores[:40]))
    return "\n".join(partes)


def _bloco_briefing(briefing: str | None) -> str:
    if not briefing:
        return ""
    return (
        "\n\nBRIEFING (pesquisa de apoio — NÃO é ficha técnica; specs reais vêm dos dados "
        f"fornecidos):\n{briefing}\n"
    )


def _bloco_feedback(feedback: str | None, sugestao_anterior: dict | None) -> str:
    """
    Se esta chamada é uma REFAÇÃO (o revisor pediu ajustes), monta um bloco com a sugestão
    anterior + o feedback, para o modelo revisar em vez de gerar do zero. Sem feedback, devolve
    string vazia (execução normal).

    `sugestao_anterior`, se vier, deve ter as chaves: titulo, palavras_chave, tags, descricao
    (a descrição pode incluir o bloco de metragem — ele é removido automaticamente aqui via
    `sem_bloco_metragem`, pra não ser ecoado e duplicado pelo pós-processamento).
    """
    feedback = (feedback or "").strip()
    if not feedback:
        return ""
    ant = sugestao_anterior or {}
    palavras = ", ".join(ant.get("palavras_chave", []) or [])
    tags = ", ".join(ant.get("tags", []) or [])
    descricao_anterior = sem_bloco_metragem(ant.get("descricao", ""))
    return (
        "Você já sugeriu antes:\n"
        f"- Título: {ant.get('titulo', '')}\n"
        f"- Palavras-chave: {palavras}\n"
        f"- Tags: {tags}\n"
        f"- Descrição: {descricao_anterior}\n\n"
        f"O revisor pediu estes ajustes: {feedback}\n"
        "Gere uma NOVA versão do JSON incorporando o feedback (mesmo formato de sempre).\n\n"
    )


def curar_descricao(
    *,
    codigo: str,
    nome: str,
    contexto: str,
    categoria: str | None = None,
    preco: str | None = None,
    descricao_atual: str | None = None,
    cores: list[str] | None = None,
    briefing: str | None = None,
    feedback: str | None = None,
    sugestao_anterior: dict | None = None,
    modelo: str = "sonnet",
) -> dict:
    """
    Chama a Claude e devolve o enriquecimento do produto.

    `contexto` é uma string já montada por quem chama (tom de voz + glossário + personas + o que
    mais fizer sentido) — este módulo não lê arquivo nenhum do disco.

    `descricao_atual`, se vier, deve chegar já limpa de HTML/boilerplate — é responsabilidade de
    quem chama decidir como higienizar o texto do sistema de origem (nenhuma limpeza é feita aqui).

    Retorna: {titulo, descricao, palavras_chave, tags, custo_usd, tokens_input, tokens_output}.
    `descricao` já sai com o bloco de metragem embutido (metragem primeiro, copy depois).
    """
    system = f"{SYSTEM_PROMPT}\n\n---\n\nCONTEXTO:\n\n{contexto}"
    conteudo = (
        "Enriqueça a ficha deste produto de tecido:\n\n"
        f"{_resumo_produto(codigo=codigo, nome=nome, categoria=categoria, preco=preco, descricao_atual=descricao_atual, cores=cores)}\n"
        f"{_bloco_briefing(briefing)}\n"
        f"{_bloco_feedback(feedback, sugestao_anterior)}"
        "Retorne só o JSON com titulo, descricao, palavras_chave, tags e largura."
    )
    resposta = chamar(
        modelo=modelo, system=system,
        mensagens=[{"role": "user", "content": conteudo}],
    )
    dados = _parse_json(resposta["texto"])
    descricao = str(dados.get("descricao", "")).lstrip()
    descricao_final = f"\n\n{descricao}" if descricao else ""
    return {
        "titulo": str(dados.get("titulo", "")),
        "descricao": descricao_final,
        "palavras_chave": list(dados.get("palavras_chave", []) or []),
        "tags": list(dados.get("tags", []) or []),
        "custo_usd": resposta["custo_usd"],
        "tokens_input": resposta["tokens_input"],
        "tokens_output": resposta["tokens_output"],
    }
