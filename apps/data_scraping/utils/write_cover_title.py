from PIL import Image, ImageDraw, ImageFont


def write_cover_title(
    path_image,
    text,
    fill="#daa520",
    font_color="#000",
    path_font=None,
    font_size=None,
    stroke_fill=None,
    stroke_width=None,
):
    def percent_of_size(size, percent):
        return int(round(size * percent))

    image = Image.open(path_image)
    width, height = image.size
    draw = ImageDraw.Draw(image)

    if not path_font:
        path_font = r"C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling\apps\data_scraping\utils\fonts\SIFONN_PRO.otf"

    if not font_size:
        font_size = percent_of_size(width, 0.07)

    if len(text) > 18:
        words = text.split()
        new_text, rest_text = [], []
        count = 0

        for word in words:
            if count + len(word) + len(new_text) <= 18:
                new_text.append(word)
                count += len(word)
            else:
                rest_text.append(word)

        text = f"{' '.join(new_text)}\n{' '.join(rest_text)}"

    if fill:
        draw.rounded_rectangle(
            (
                percent_of_size(width, 0.04140625),
                percent_of_size(height, 0.36875),
                percent_of_size(width, 0.95859375),
                percent_of_size(height, 0.63125),
            ),
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
    )

    image.save(path_image)
