from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import os, random

from apps.data_scraping.utils.write_cover_title import write_cover_title


class CoverProduct:

    def __init__(self, path, size_cover: int | float = 1280):

        if not isinstance(size_cover, (int, float)):
            raise ValueError("O Parametro size_cover deve ser um int ou float")

        self.path = path
        self.size_cover = self.int_round(size_cover)

    def set_paths_cover(self):
        self.path_images = os.path.join(self.path, "Fotos")
        self.path_save = os.path.join(self.path, "Capa")

        self.images = os.listdir(self.path_images)

        if "desktop.ini" in self.images:
            self.images.remove("desktop.ini")

        images_copy = self.images[:]
        for img in images_copy:
            try:
                if os.path.isfile(os.path.join(self.path_images, img)):
                    with Image.open(os.path.join(self.path_images, img)) as image:
                        image.verify()
                else:
                    self.images.remove(img)
            except (UnidentifiedImageError, FileNotFoundError):
                self.images.remove(img)
            
        self.len_path_images = len(self.images)

        if not os.path.exists(self.path_save):
            os.mkdir(self.path_save)

    def new_background(self, color=(255, 255, 255), model="RGB"):
        return Image.new(model, (self.size_cover, self.size_cover), color)

    def int_round(self, value):
        return int(round(value))

    def percent_of_size(self, percent):
        return self.int_round(self.size_cover * percent)

    def cover_grid(self, name_save, title=None, fill=None, stroke_fill='#fff', stroke_width=5, font_color="#000"):

        self.set_paths_cover()

        if self.len_path_images < 9:
            print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 9 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )
            return None
        background = self.new_background()

        resize_value = self.percent_of_size(0.32421875)
        position_1 = 0
        position_2 = self.percent_of_size(0.33828125)
        position_3 = self.percent_of_size(0.67578125)

        positions_coord = [position_1, position_2, position_3]

        positions = [(x, y) for x in positions_coord for y in positions_coord]

        images = random.sample(self.images, 9)

        for i, picture in enumerate(images):

            path_img = os.path.join(self.path_images, picture)

            img_mask = Image.open(path_img).resize((resize_value, resize_value))

            background.paste(img_mask, positions[i])

            if i == 8:
                break

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

            
        
        background.save(cover_save)
        
        if title:
            write_cover_title(cover_save, title, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width, font_color=font_color)
            
        return cover_save

    def cover_three(self, name_save, title=None, fill=None, stroke_fill='#fff', stroke_width=5, font_color="#000"):
        self.set_paths_cover()

        if self.len_path_images < 3:
            print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 3 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )
            return None

        background = self.new_background()

        images = random.sample(self.images, 3)

        for i, img in enumerate(images):

            image = Image.open(os.path.join(self.path_images, img))

            size = self.percent_of_size(0.49296875)
            position = self.percent_of_size(0.50703125)

            match i:
                case 0:
                    props = {"resize": (size, self.size_cover), "positions": (0, 0)}
                case 1:
                    props = {"resize": (size, size), "positions": (position, position)}
                case 2:
                    props = {"resize": (size, size), "positions": (position, 0)}

            image = image.resize(props["resize"])
            background.paste(image, props["positions"])

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)
        
        if title:
            write_cover_title(cover_save, title, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width, font_color=font_color)
            
        return cover_save

    def cover_grid_2(self, name_save, title=None, fill=None, stroke_fill='#fff', stroke_width=5, font_color="#000"):
        self.set_paths_cover()

        if self.len_path_images < 5:
            print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 3 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )
            return None

        background = self.new_background()

        images = random.sample(self.images, 5)

        for i, img in enumerate(images):

            image = Image.open(os.path.join(self.path_images, img))

            size_rectangle_h = (
                self.percent_of_size(0.7),
                self.percent_of_size(0.29375),
            )
            size_rectangle_v = (
                self.percent_of_size(0.29375),
                self.percent_of_size(0.7),
            )
            size_square = self.percent_of_size(0.4)
            size_square = (size_square, size_square)

            match i:
                case 0:
                    props = {"resize": size_rectangle_h, "positions": (0, 0)}
                case 1:
                    props = {
                        "resize": size_rectangle_v,
                        "positions": (0, self.percent_of_size(0.3)),
                    }
                case 2:
                    props = {
                        "resize": size_rectangle_h,
                        "positions": (
                            self.percent_of_size(0.3),
                            self.percent_of_size(0.70625),
                        ),
                    }
                case 3:
                    props = {
                        "resize": size_rectangle_v,
                        "positions": (self.percent_of_size(0.70625), 0),
                    }
                case 4:
                    props = {
                        "resize": size_square,
                        "positions": (
                            self.percent_of_size(0.3),
                            self.percent_of_size(0.3),
                        ),
                    }

            image = image.resize(props["resize"])
            background.paste(image, props["positions"])

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)
        if title:
            write_cover_title(cover_save, title, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width, font_color=font_color)
        return cover_save

    def cover_grid_3(self, name_save, title=None, fill=None, stroke_fill='#fff', stroke_width=5, font_color="#000"):
        self.set_paths_cover()

        if self.len_path_images < 6:
            print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 6 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )
            return None

        background = self.new_background()

        images = random.sample(self.images, 6)

        for i, img in enumerate(images):
            image = Image.open(os.path.join(self.path_images, img))

            size_rectangle_v = (
                self.percent_of_size(0.2453125),
                self.percent_of_size(0.32265625),
            )
            size_rectangle_h = (
                self.percent_of_size(0.4984375),
                self.percent_of_size(0.32265625),
            )
            size_square = self.percent_of_size(0.4921875)
            size_square = (size_square, size_square)

            match i:
                case 0:
                    props = {"resize": size_rectangle_h, "positions": (0, 0)}
                case 1:
                    props = {
                        "resize": size_rectangle_h,
                        "positions": (0, self.percent_of_size(0.67734375)),
                    }
                case 2:
                    props = {
                        "resize": size_rectangle_v,
                        "positions": (0, self.percent_of_size(0.3390625)),
                    }
                case 3:
                    props = {
                        "resize": size_rectangle_v,
                        "positions": (
                            self.percent_of_size(0.253125),
                            self.percent_of_size(0.3390625),
                        ),
                    }
                case 4:
                    props = {
                        "resize": size_square,
                        "positions": (self.percent_of_size(0.5078125), 0),
                    }
                case 5:
                    props = {
                        "resize": size_square,
                        "positions": (
                            self.percent_of_size(0.5078125),
                            self.percent_of_size(0.5078125),
                        ),
                    }

            image = image.resize(props["resize"])

            background.paste(image, props["positions"])

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)
        
        if title:
            write_cover_title(cover_save, title, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width, font_color=font_color)
        return cover_save

    def cover_full_logo(self, title, name_save, company="LEGITIMA"):
        self.set_paths_cover()
        
        if company == "LEGITIMA":
            logo_path = r"C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling\apps\data_scraping\utils\img\LOGO LEGITIMA.png"
        elif company == "GM":
            logo_path = r"C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling\apps\data_scraping\utils\img\LOGO GM.png"

        if self.len_path_images < 1:
            print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 1 IMAGEM PARA SE CRIAR ESSE TIPO DE CAPA"
            )
            return None
        path_font = r"C:\Users\gabri\OneDrive\Área de Trabalho\PROGRAMACAO\PYTHON\cadastra_produto_bling\apps\data_scraping\utils\fonts\SIFONN_PRO.otf"

        font_size = self.percent_of_size(0.05)
        font = ImageFont.truetype(path_font, font_size)

        background = self.new_background(model="RGBA", color=(255, 255, 255, 0))

        logo = Image.open(logo_path)

        logo = logo.resize((self.percent_of_size(0.2), self.percent_of_size(0.2)))

        image = random.sample(self.images, 1)[0]
        
        image = Image.open(os.path.join(self.path_images, image)).convert("RGBA")

        image = image.resize((self.size_cover, self.size_cover))

        draw = ImageDraw.Draw(background)

        draw.ellipse(
            (
                self.percent_of_size(0.0859375),
                self.percent_of_size(0.63359375),
                self.percent_of_size(0.9140625),
                self.percent_of_size(0.9),
            ),
            fill=(255, 255, 255, 100),
        )

        draw.text(
            (self.percent_of_size(0.5), self.percent_of_size(0.766796875)),
            title,
            font=font,
            anchor="mm",
            fill="black",
            stroke_fill="white",
            stroke_width=3,
        )

        background.paste(logo, (self.percent_of_size(0.4), self.percent_of_size(0.05)))

        result = Image.alpha_composite(image, background)
        result = result.convert("RGB")

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        result.save(cover_save)
        
        return cover_save
