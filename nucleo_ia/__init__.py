"""
nucleo_ia — núcleo portátil (sem Django, sem Bling) dos agentes Curador de Descrição e
Inspiração de Uso do projeto legitima_lojavirtual.

Extraído de agentes/curador_catalogo.py e agentes/inspiracao_uso.py: mesma lógica de
prompt/parsing/geração de imagem, mas os dados de produto entram como parâmetros explícitos em
vez de um model Django (`Produto`), e a camada de contexto (tom de voz, glossário, personas) entra
como uma string já montada pelo chamador, em vez de ler arquivos do disco via `settings`.

Pacote autocontido: pode ser copiado inteiro para outro projeto Python. Dependências externas:
`anthropic`, `google-genai`, `httpx`, `Pillow`. Segredos via variáveis de ambiente
(`ANTHROPIC_API_KEY`, `GEMINI_API_KEY`), nunca hardcoded.
"""
