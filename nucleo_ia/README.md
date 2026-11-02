# nucleo_ia

Núcleo portátil (sem Django, sem Bling) de três agentes extraídos do projeto
`legitima_lojavirtual`: **Pesquisador de Tecido**, **Curador de Descrição** e **Inspiração de
Uso**. Copie a pasta `nucleo_ia/` inteira para o outro projeto — não depende de nada daqui além
das bibliotecas listadas abaixo.

## Instalação

```bash
pip install anthropic google-genai httpx Pillow
```

Variáveis de ambiente (nunca hardcode):

- `ANTHROPIC_API_KEY` — obrigatória (Pesquisador/Curador/escrita do prompt de Inspiração).
- `GEMINI_API_KEY` — só se for gerar imagem (`inspiracao_uso.gerar_imagem_inspiracao`).

## O que cada função faz

| Função | Módulo | Chama | O que devolve |
|---|---|---|---|
| `pesquisar_tecido(...)` | `pesquisa_tecido` | Claude + busca web | `{briefing, buscas_web, custo_usd, tokens_input, tokens_output}` |
| `curar_descricao(...)` | `curador_descricao` | Claude | `{titulo, descricao, palavras_chave, tags, custo_usd, ...}` |
| `escrever_prompt_inspiracao(...)` | `inspiracao_uso` | Claude | `{prompt, cena, justificativa, custo_usd, ...}` |
| `gerar_imagem_inspiracao(...)` | `inspiracao_uso` | Gemini | bytes JPEG (já com o selo "imagem ilustrativa") |

Nenhuma delas grava nada em banco/arquivo — são funções puras de entrada/saída. Cache,
persistência e fluxo de aprovação humana ficam por conta do projeto que usar isto.

## O parâmetro `contexto`

Todas as funções que chamam a Claude recebem um parâmetro `contexto: str` — é o texto de
tom de voz / glossário / personas / o que mais fizer sentido pro seu negócio, concatenado como
uma única string. No projeto original isso vem de arquivos `.md` versionados; aqui você monta do
jeito que quiser, por exemplo:

```python
contexto = "\n---\n".join(
    open(f"contexto/{arq}", encoding="utf-8").read()
    for arq in ("tom-de-voz.md", "glossario.md", "personas.md")
)
```

Pode ser uma string vazia se você não tiver essa camada — as funções funcionam sem ela, só
perdem a consistência de tom/vocabulário entre chamadas.

## Uso básico — pipeline completo

```python
from nucleo_ia import pesquisa_tecido, curador_descricao, inspiracao_uso

contexto = "..."  # seu tom de voz / glossário / personas, já concatenados

# 1. Pesquisa (opcional, mas recomendado — alimenta o Curador com contexto real do tecido).
# Cacheie o resultado por família de produto pra não pagar de novo a cada item: esta função
# não sabe nada sobre o seu banco de dados.
pesquisa = pesquisa_tecido.pesquisar_tecido(
    nome="Cetim Charmeuse Liso",
    categoria="Tecidos",
    contexto=contexto,
)
briefing = pesquisa["briefing"]

# 2. Curadoria da ficha (título, descrição, palavras-chave, tags).
resultado = curador_descricao.curar_descricao(
    codigo="SKU-123",
    nome="Cetim Charmeuse Liso",
    contexto=contexto,
    categoria="Tecidos",
    preco="49.90",
    cores=["Azul Royal", "Vermelho", "Preto"],
    briefing=briefing,
)
print(resultado["titulo"], resultado["descricao"])

# 3. Inspiração de uso (opcional): escreve o prompt, você revisa, depois gera a imagem.
prompt_info = inspiracao_uso.escrever_prompt_inspiracao(
    nome_tecido="Cetim Charmeuse Liso",
    briefing=briefing,
    contexto=contexto,
)
# ... revise/edite prompt_info["prompt"] como quiser antes do próximo passo ...
imagem_bytes = inspiracao_uso.gerar_imagem_inspiracao(
    prompt_info["prompt"],
    referencia_url="https://.../foto-real-do-tecido.jpg",
)
with open("inspiracao.jpg", "wb") as f:
    f.write(imagem_bytes)
```

## Refação com feedback (revisão humana)

`curar_descricao` e `escrever_prompt_inspiracao` aceitam um pedido de ajuste em vez de gerar do
zero — mesma ideia do painel original: mostre a sugestão anterior + o feedback, e a Claude
reescreve incorporando o pedido.

```python
resultado_2 = curador_descricao.curar_descricao(
    codigo="SKU-123", nome="Cetim Charmeuse Liso", contexto=contexto,
    feedback="título muito longo, encurte",
    sugestao_anterior={
        "titulo": resultado["titulo"],
        "palavras_chave": resultado["palavras_chave"],
        "tags": resultado["tags"],
        "descricao": resultado["descricao"],
    },
)
```

## Testes

```bash
python -m unittest nucleo_ia/test_nucleo_ia.py -v
```

Não precisa de Django nem das chaves de API reais — tudo mockado.

## O que NÃO foi portado (de propósito)

- Persistência (`AgentRun`/`AgentAction`, cache de briefing por família, status de aprovação) —
  é decisão de cada projeto como/se guardar isso.
- Upload pro S3 / integração com Bling — infraestrutura da loja original, não do agente.
- Os 9 layouts de capa de marketplace (`agentes/capa_render.py` original tinha muito mais que
  `selo_ilustrativo`) — fora do que foi pedido.
- Sugestão automática de glossário encadeada após pesquisa nova — específica do painel Django.
