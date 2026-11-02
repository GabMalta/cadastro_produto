from PIL import Image, ImageDraw, ImageFont
from apps.data_scraping.utils.color_utils import get_contrasting_colors


def write_cover_title(
    path_image,
    text,
    max_length=10,
    fill="#daa520",
    font_color=None,
    path_font=None,
    font_size=None,
    stroke_fill=None,
    stroke_width=0,
    promocao=False,
):
    def percent_of_size(size, percent):
        return int(round(size * percent))

    def split_text(text, max_length):
        words = text.split()
        lines = []
        current_line = []
        count = 0

        for word in words:
            # +len(current_line) considera os espaços
            if count + len(word) + len(current_line) <= max_length:
                current_line.append(word)
                count += len(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                count = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)

    text = split_text(text, max_length)

    image = Image.open(path_image)
    width, height = image.size
    draw = ImageDraw.Draw(image)

    text_bbox = (
        percent_of_size(width, 0.04140625),
        percent_of_size(height, 0.36875),
        percent_of_size(width, 0.95859375),
        percent_of_size(height, 0.63125),
    )

    if font_color is None:
        font_color, auto_stroke = get_contrasting_colors(image, text_bbox, fill=fill)
        if stroke_fill is None:
            stroke_fill = auto_stroke
        if stroke_width == 0:
            stroke_width = 3

    if not path_font:
        path_font = (
            r"C:\Users\gabri\www\cadastro_produto\apps\data_scraping\utils\fonts\MONTSERRAT_EXTRABOLD.ttf"
        )

    if not font_size:

        max_len = max(len(line) for line in text.split("\n"))

        if max_len <= 5:
            font_size = percent_of_size(width, 0.2)
        elif max_len <= 8:
            font_size = percent_of_size(width, 0.175)
        elif max_len <= 10:
            font_size = percent_of_size(width, 0.135)
        else:
            font_size = percent_of_size(width, 0.10)

    if fill:
        draw.rounded_rectangle(
            text_bbox,
            radius=20,
            fill=fill,
        )

    font = ImageFont.truetype(path_font, font_size)

    draw.text(
        (width / 2, height / 2),
        text,
        font_color,
        font,
        anchor="mm",
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
        align="center",
    )

    if promocao:

        draw.rounded_rectangle(
            (
                percent_of_size(width, 0),
                percent_of_size(height, 0),
                percent_of_size(width, 1),
                percent_of_size(height, 0.2),
            ),
            radius=20,
            fill="#ff0000",
        )

        draw.text(
            (percent_of_size(width, 0.5), percent_of_size(height, 0.1)),
            "PROMOÇÃO",
            "#FAFAFA",
            ImageFont.truetype(path_font, percent_of_size(width, 0.085)),
            anchor="mm",
        )
    image.save(path_image)
