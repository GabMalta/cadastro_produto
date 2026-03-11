from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import os, random

from apps.data_scraping.utils.write_cover_title import write_cover_title


try:
    # Tente usar uma fonte bold do sistema. Ajuste o caminho se necessário.
    FONTE_PADRAO = ImageFont.truetype("arialbd.ttf", 90)  # Windows
    # FONTE_PADRAO = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", 90) # Mac
except IOError:
    print("Aviso: Fonte Arial Bold não encontrada. Usando padrão.")
    FONTE_PADRAO = ImageFont.load_default()


class CoverProduct:

    def __init__(self, path, size_cover: int | float = 1280, promocao=False):

        if not isinstance(size_cover, (int, float)):
            raise ValueError("O Parametro size_cover deve ser um int ou float")

        self.path = path
        self.size_cover = self.int_round(size_cover)
        self.promocao = promocao

    def set_paths_cover(self):
        self.path_images = os.path.join(self.path, f"{self.path.split('\\')[-1]} - Fotos")
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

    def aspect_fill_crop(self, image_path, target_width, target_height):
        """
        Abre uma imagem, redimensiona proporcionalmente para preencher
        o tamanho alvo e corta os excessos centralizados.
        """
        img = Image.open(image_path).convert("RGB")
        width, height = img.size

        # Calcula a proporção necessária para preencher a área
        ratio_w = target_width / width
        ratio_h = target_height / height
        scale = max(ratio_w, ratio_h)

        new_w = int(width * scale)
        new_h = int(height * scale)

        img_resized = img.resize((new_w, new_h), Image.LANCZOS)

        # Calcula o corte central
        left = (new_w - target_width) // 2
        top = (new_h - target_height) // 2

        img_cropped = img_resized.crop((left, top, left + target_width, top + target_height))
        return img_cropped

    def new_background(self, color=(255, 255, 255), model="RGB"):
        return Image.new(model, (self.size_cover, self.size_cover), color)

    def int_round(self, value):
        return int(round(value))

    def percent_of_size(self, percent):
        return self.int_round(self.size_cover * percent)

    def layout_faixa_horizontal(
        self,
        name_save,
        title=None,
        fill=None,
        font_color="#000",
        altura_banner=150,
    ):
        self.set_paths_cover()
        
        if title and len(title) > 20:
            print("\nAVISO: O título é muito longo e pode não caber corretamente na faixa da capa.")
            
            while True:
                print(f"\nErro em: {title}\n")
                title = input("Por favor, insira um título para a capa com até 20 caracteres: \n").upper()
                if len(title) <= 20:
                    break
        
        if self.len_path_images < 4:
            print("\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 4 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA")
            return None
        
        # 1. Canvas
        canvas = self.new_background()
        draw = ImageDraw.Draw(canvas)

        # 2. Calcula tamanho das imagens (4 lado a lado)
        largura_img = self.size_cover // 4
        altura_img = self.size_cover - altura_banner

        # 3. Processa e cola as imagens
        
        images = random.sample(self.images, 4)
        
        for i, img_path in enumerate(images):
            
            path_completo = os.path.join(self.path_images, img_path)

            img_processada = self.aspect_fill_crop(path_completo, largura_img, altura_img)
            canvas.paste(img_processada, (i * largura_img, 0))

        # 4. Desenha o Banner Inferior
        draw.rectangle([(0, altura_img), (self.size_cover, self.size_cover)], fill=fill)

        # 5. Texto Centralizado no Banner
        bbox = draw.textbbox((0, 0), title, font=FONTE_PADRAO)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        pos_x = (self.size_cover - text_w) / 2
        # Centro vertical do banner inferior
        pos_y = altura_img + (altura_banner - text_h) / 2 - 10

        draw.text((pos_x, pos_y), title, fill=font_color, font=FONTE_PADRAO)
        
        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        canvas.save(cover_save, quality=95)
        
        return cover_save

    def cover_grid(
        self,
        name_save,
        title=None,
        fill=None,
        stroke_fill="#fff",
        stroke_width=5,
        font_color="#000",
    ):

        self.set_paths_cover()

        if self.len_path_images < 9:
            print("\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 9 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA")
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

            img_mask = self.aspect_fill_crop(path_img, resize_value, resize_value)

            background.paste(img_mask, positions[i])

            if i == 8:
                break

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)

        if title:
            write_cover_title(
                cover_save,
                title,
                fill=fill,
                stroke_fill=stroke_fill,
                stroke_width=stroke_width,
                font_color=font_color,
                promocao=self.promocao,
            )

        return cover_save

    def cover_three(
        self,
        name_save,
        title=None,
        fill=None,
        stroke_fill="#fff",
        stroke_width=5,
        font_color="#000",
    ):
        self.set_paths_cover()

        if self.len_path_images < 3:
            print("\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 3 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA")
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

            image = self.aspect_fill_crop(os.path.join(self.path_images, img), props["resize"][0], props["resize"][1])
            background.paste(image, props["positions"])

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)

        if title:
            write_cover_title(
                cover_save,
                title,
                fill=fill,
                stroke_fill=stroke_fill,
                stroke_width=stroke_width,
                font_color=font_color,
                promocao=self.promocao,
            )

        return cover_save

    def cover_grid_2(
        self,
        name_save,
        title=None,
        fill=None,
        stroke_fill="#fff",
        stroke_width=5,
        font_color="#000",
    ):
        self.set_paths_cover()

        if self.len_path_images < 5:
            print("\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 3 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA")
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

            image = self.aspect_fill_crop(os.path.join(self.path_images, img), props["resize"][0], props["resize"][1])
            background.paste(image, props["positions"])

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)
        if title:
            write_cover_title(
                cover_save,
                title,
                fill=fill,
                stroke_fill=stroke_fill,
                stroke_width=stroke_width,
                font_color=font_color,
                promocao=self.promocao,
            )
        return cover_save

    def cover_grid_3(
        self,
        name_save,
        title=None,
        fill=None,
        stroke_fill="#fff",
        stroke_width=5,
        font_color="#000",
    ):
        self.set_paths_cover()

        if self.len_path_images < 6:
            print("\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 6 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA")
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

            image = self.aspect_fill_crop(os.path.join(self.path_images, img), props["resize"][0], props["resize"][1])

            background.paste(image, props["positions"])

        cover_save = os.path.join(self.path_save, f"{name_save}.jpg")

        background.save(cover_save)

        if title:
            write_cover_title(
                cover_save,
                title,
                fill=fill,
                stroke_fill=stroke_fill,
                stroke_width=stroke_width,
                font_color=font_color,
                promocao=self.promocao,
            )
        return cover_save

    def cover_full_logo(self, title, name_save, company="LEGITIMA"):
        self.set_paths_cover()

        if company == "LEGITIMA":
            logo_path = r"C:\Users\gabri\www\cadastro_produto\apps\data_scraping\utils\img\LOGO LEGITIMA.png"
        elif company == "GM":
            logo_path = r"C:\Users\gabri\www\cadastro_produto\apps\data_scraping\utils\img\LOGO GM.png"

        if self.len_path_images < 1:
            print("\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 1 IMAGEM PARA SE CRIAR ESSE TIPO DE CAPA")
            return None
        path_font = r"C:\Users\gabri\www\cadastro_produto\apps\data_scraping\utils\fonts\SIFONN_PRO.otf"

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

