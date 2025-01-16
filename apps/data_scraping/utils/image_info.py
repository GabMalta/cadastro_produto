import json
import os
from typing import TypedDict
from PIL import Image, ImageDraw, ImageFont


class ImageInfoProps(TypedDict):
    composition: str
    width: str
    fabric_name: str


def image_info(
    path_save: str, props: ImageInfoProps | None = None, path_info: str | None = None, company: str = "LEGITIMA"
):

    if not props:
        if path_info:
            try:
                with open(
                    os.path.join(path_info, "product_data.json"), encoding="utf-8"
                ) as arq:
                    props = json.load(arq)
            except Exception as e:
                return print(e)
        else:
            return print(
                "VOCÊ DEVE PASSAR AS INFORMACOES A SER PREENCHIDAS EM UM DICIONARIO (props), OU O CAMINHO PARA O JSON COM AS INFORMACOES COMO PARAMETRO (path_info)"
            )
            
    if len(props["fabric_name"]) > 18:
            count = 0
            new_text = []
            rest_text = []
            for text in props["fabric_name"].split():
                if (count + len(text)) <= 18:
                    new_text.append(text)
                    count += len(text)
                else:
                    rest_text.append(text)
            
            props["fabric_name"] = " ".join(new_text) + "\n" + " ".join(rest_text)

    font_path = "apps/data_scraping/utils/fonts/SIFONN_PRO.otf"
    font_large = ImageFont.truetype(font_path, 85)
    font_medium = ImageFont.truetype(font_path, 60)
    font_small = ImageFont.truetype(font_path, 45)

    img = Image.open(f"apps/data_scraping/utils/img_info/INFO_TEC_{company.upper()}.jpg")
    draw = ImageDraw.Draw(img)

    title_props = {
        "position": (640, 130),
        "text": props["fabric_name"].upper(),
        "font": font_large,
        "color": "#000",
        "anchor": "mm",
    }

    larg1_props = {
        "position": (125, 300),
        "text": f"{props['width']} m",
        "font": font_small,
        "color": "#ff3131",
    }

    larg2_props = {
        "position": (560, 905),
        "text": f'{props["width"]} Metros',
        "font": font_small,
        "color": "#000",
        "anchor": "ls",
    }

    composition_props = {
        "position": (570, 975),
        "text": props["composition"].upper(),
        "font": font_small,
        "color": "#000",
        "anchor": "ls",
    }

    draw.text(
        title_props["position"],
        title_props["text"],
        anchor=title_props["anchor"],
        font=title_props["font"],
        fill=title_props["color"],
    )

    draw.text(
        larg2_props["position"],
        larg2_props["text"],
        anchor=larg2_props["anchor"],
        font=larg2_props["font"],
        fill=larg2_props["color"],
    )

    draw.text(
        composition_props["position"],
        composition_props["text"],
        anchor=composition_props["anchor"],
        font=composition_props["font"],
        fill=composition_props["color"],
    )

    text_image = Image.new("RGBA", (200, 100), (255, 255, 255, 0))  # Transparente
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text(
        (0, 0), larg1_props["text"], font=larg1_props["font"], fill=larg1_props["color"]
    )
    text_image = text_image.rotate(90, expand=True)
    img.paste(text_image, larg1_props["position"], text_image)

    img.save(os.path.join(path_save, f"CAPA_INFO_{company.upper()}.jpg"))
