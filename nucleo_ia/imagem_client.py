"""
Cliente de geração de imagem (Google Gemini) — cópia Django-free de agentes/imagem_client.py
(legitima_lojavirtual). Única mudança: a chave da API vem de `os.environ` em vez de
`django.conf.settings`.

Recebe um prompt (texto) e, opcionalmente, uma foto de referência (bytes) pra ancorar cor/textura
na geração — a cena é inventada, a referência não deve ser.

"Sem pessoas" é decisão de produto (cenas de ambiente): a garantia vive no PROMPT que o agente
escreve ("no people, no hands, no faces") — o parâmetro `person_generation` da API não serve
aqui, é exclusivo do modo enterprise (a Developer API rejeita com erro).
"""
import logging
import os
from decimal import Decimal
from decouple import config

logger = logging.getLogger("nucleo_ia.imagem")

MODELO_IMAGEM = "gemini-2.5-flash-image"

# Custo aproximado por imagem gerada (o Gemini cobra por token de imagem de saída; 1 imagem
# 1024px ≈ 1290 tokens ≈ US$ 0,039). Usado como estimativa no registro — conferir a fatura.
CUSTO_IMAGEM_USD = Decimal("0.039")


def gerar_imagem(prompt: str, referencia: bytes | None = None,
                 aspect: str = "1:1") -> bytes:
    """
    Gera uma imagem a partir do prompt, opcionalmente ancorada numa foto de referência.
    Devolve os bytes (PNG/JPEG conforme o provedor). Levanta RuntimeError se não vier imagem.
    """
    from google import genai
    from google.genai import types

    api_key = config("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada no ambiente.")

    client = genai.Client(api_key=api_key)

    contents: list = []
    if referencia:
        contents.append(types.Part.from_bytes(data=referencia, mime_type="image/jpeg"))
    contents.append(prompt)

    resposta = client.models.generate_content(
        model=MODELO_IMAGEM,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=aspect),
        ),
    )

    for parte in resposta.candidates[0].content.parts:
        dados = getattr(parte, "inline_data", None)
        if dados and dados.data:
            logger.info("imagem gerada (%s, %d bytes)", MODELO_IMAGEM, len(dados.data))
            return dados.data
    raise RuntimeError("O Gemini não devolveu imagem (resposta sem inline_data).")
