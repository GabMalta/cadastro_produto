import random
from PIL import Image


def random_color():
    """Gera uma cor aleatória em RGB (0-255)."""
    return tuple(random.randint(0, 255) for _ in range(3))


def luminance(rgb):
    """Calcula a luminância relativa de uma cor RGB."""
    r, g, b = [x / 255.0 for x in rgb]

    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = adjust(r), adjust(g), adjust(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1, c2):
    """Calcula o contraste entre duas cores."""
    l1, l2 = luminance(c1), luminance(c2)
    brightest, darkest = max(l1, l2), min(l1, l2)
    return (brightest + 0.05) / (darkest + 0.05)


def rgb_to_hex(rgb):
    """Converte RGB para formato hexadecimal."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def hex_to_rgb(hex_color):
    """Converte hex (#RRGGBB) para tuple RGB."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def gerar_cores_legiveis():
    """Gera uma cor de fundo e uma cor de fonte legível sobre ela."""
    bg = random_color()
    while True:
        fg = random_color()
        if contrast_ratio(bg, fg) >= 4.5:
            return rgb_to_hex(bg), rgb_to_hex(fg)


def get_dominant_color_in_region(image, bbox):
    """Retorna a cor dominante (média RGB) de uma região da imagem.

    Args:
        image: PIL Image já aberta.
        bbox: Tupla (x1, y1, x2, y2) da região a analisar.

    Returns:
        Tuple RGB (r, g, b) com valores 0-255.
    """
    region = image.crop(bbox)
    region = region.resize((50, 50))
    region = region.convert("RGB")

    pixels = list(region.getdata())
    n = len(pixels)
    r = sum(p[0] for p in pixels) // n
    g = sum(p[1] for p in pixels) // n
    b = sum(p[2] for p in pixels) // n

    return (r, g, b)


def get_contrasting_colors(image, bbox, fill=None):
    """Detecta as cores da região e retorna font_color e stroke_fill contrastantes.

    Gera uma cor variada (não apenas preto/branco) que tenha contraste
    WCAG >= 4.5 contra o fundo. O stroke_fill é sempre gerado para
    garantir legibilidade.

    Se `fill` for fornecido, contrasta contra a cor do fill.
    Senão, contrasta contra a cor dominante dos pixels da imagem na região.

    Args:
        image: PIL Image já aberta.
        bbox: Tupla (x1, y1, x2, y2) da região do texto.
        fill: Cor hex do retângulo de fundo (opcional).

    Returns:
        Tuple (font_color_hex, stroke_fill_hex).
    """
    if fill:
        bg_rgb = hex_to_rgb(fill)
    else:
        bg_rgb = get_dominant_color_in_region(image, bbox)

    # Gera font_color aleatório com contraste >= 4.5 contra o fundo
    for _ in range(200):
        fg = random_color()
        if contrast_ratio(bg_rgb, fg) >= 7.5:
            font_color = rgb_to_hex(fg)
            break
    else:
        # Fallback: branco ou preto conforme luminância do fundo
        font_color = "#FFFFFF" if luminance(bg_rgb) < 0.5 else "#000000"
        fg = hex_to_rgb(font_color)

    # Gera stroke_fill com contraste >= 3.0 contra o font_color
    fg_lum = luminance(fg)
    if fg_lum >= 0.5:
        # Fonte clara -> stroke escuro
        stroke_fill = "#000000"
    else:
        # Fonte escura -> stroke claro
        stroke_fill = "#FFFFFF"

    return font_color, stroke_fill
