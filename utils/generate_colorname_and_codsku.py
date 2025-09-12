import os


def generate_colorname_and_codsku(color, changed_name):

        color_name, _ = os.path.splitext(color)
        color_name = color_name.title()

        if changed_name:

            cod_sku = color_name.rsplit(" ", 1)[1]

            if not cod_sku or cod_sku == "":
                cod_sku = color_name
        else:
            cod_sku = color_name

        return color_name, cod_sku