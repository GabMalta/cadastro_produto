"""
Utilitários de imagem (Pillow puro) — cópia de partes de agentes/capa_render.py
(legitima_lojavirtual). Só o que a Inspiração de Uso usa: baixar a foto de referência e estampar
o selo "imagem ilustrativa" na arte gerada. Os 9 layouts de capa de marketplace não foram
portados (são de outro agente, fora do escopo deste pacote).
"""
from __future__ import annotations

import io
from pathlib import Path

import httpx
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent / "assets"
FONTE_TITULO = ASSETS / "MONTSERRAT_EXTRABOLD.ttf"


def baixar_imagem(url: str) -> bytes:
    """Baixa os bytes de uma foto (ex.: a referência real do produto)."""
    resp = httpx.get(url, timeout=10.0, follow_redirects=True)
    resp.raise_for_status()
    return resp.content


def abrir_rgb(dados: bytes) -> Image.Image:
    return Image.open(io.BytesIO(dados)).convert("RGB")


def _pct(base: int, p: float) -> int:
    return int(round(base * p))


def _fonte(caminho: Path, tamanho: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(caminho), tamanho)
    except OSError:
        return ImageFont.load_default(size=tamanho)


def selo_ilustrativo(img_bytes: bytes, texto: str = "Inspiração de uso · imagem ilustrativa") -> bytes:
    """
    Estampa uma pílula discreta no rodapé da imagem (honestidade: deixa claro que não é a foto
    real do produto, é uma cena gerada). Devolve JPEG.
    """
    img = abrir_rgb(img_bytes)
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")
    font = _fonte(FONTE_TITULO, max(16, _pct(w, 0.022)))

    l, t, r, b = draw.textbbox((0, 0), texto, font=font)
    tw, th = r - l, b - t
    pad_x, pad_y = _pct(w, 0.014), _pct(w, 0.008)
    margem = _pct(w, 0.02)
    x1 = w - margem
    x0 = x1 - tw - 2 * pad_x
    y1 = h - margem
    y0 = y1 - th - 2 * pad_y

    draw.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) // 2, fill=(0, 0, 0, 140))
    draw.text((x0 + pad_x - l, y0 + pad_y - t), texto, font=font, fill=(255, 255, 255, 230))

    saida = io.BytesIO()
    img.save(saida, format="JPEG", quality=92)
    return saida.getvalue()
