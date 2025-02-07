import json, re, requests, os
from apps.amazon_s3.upload_s3 import upload_folder_to_s3_parallel, path_is_image
from apps.price_generator.price_generator import price_generator
from apps.bling_api.bling import BlingApi
from apps.bling_api import settings
from IMGUR.imgur import Imgur
from requests_policy.http import http


class Produto(BlingApi):
    def __init__(
        self,
        cover_path,
        path_variations,
        name,
        folder_name,
        quantidade,
        code,
        price,
        description="",
        weight=0.3,
        origin=2,
        ncm=54075210,
        img="",
        alt=7,
        larg=7,
        profun=7,
        marca="Legítima Têxtil",
        two_variations=False,
        price_cost=None,
        *args,
        **kwargs,
    ):

        # DEFINE TODAS AS CARACTERISTICAS DO PRODUTO
        self.path_variations = path_variations
        self.name = name
        self.folder_name = folder_name
        self.quantidade = quantidade
        self.code = code
        self.price = price
        self.description = description
        self.weight = weight
        self.origin = origin
        self.ncm = ncm
        self.img = img
        self.alt = alt
        self.larg = larg
        self.profun = profun
        self.cover_path = cover_path
        self.marca = marca

        self.two_variations = two_variations
        self.second_variations = ""

        self.composition = ""
        self.fabric_width = ""

        self.covers_urls = ""
        self.price_cost = price_cost

        super().__init__(*args, **kwargs)

    def get_upload_cover(self):

        if "image_urls.json" in os.listdir(self.cover_path):
            img_json = self.get_image_json(
                os.path.join(self.cover_path, "image_urls.json")
            )
            images_url = [{"link": img[1]["img"]} for img in img_json.items()]
            
            self.covers_urls = images_url

        else:
            s3_folder = f"{self.folder_name}/Capa"

            upload_folder_to_s3_parallel(self.cover_path, s3_folder)

            self.get_upload_cover()

    def compose_product(self, changed_name=True):
        self.variations = (
            self.compose_variations(changed_name)
            if not self.two_variations
            else self.compose_two_variations(changed_name)
        )
        product = self.get_product_json()

        product["nome"] = self.name
        product["codigo"] = self.code
        product["preco"] = self.price
        product["descricaoCurta"] = self.description
        product["pesoLiquido"] = self.weight
        product["pesoBruto"] = self.weight
        product["marca"] = self.marca
        product["dimensoes"]["largura"] = self.larg
        product["dimensoes"]["altura"] = self.alt
        product["dimensoes"]["profundidade"] = self.profun
        product["tributacao"]["origem"] = self.origin
        product["tributacao"]["ncm"] = self.ncm
        product["midia"]["imagens"] = {"imagensURL": self.covers_urls}
        product["variacoes"] = self.variations
        product["camposCustomizados"][3]["valor"] = self.quantidade
        product["camposCustomizados"][7]["valor"] = self.composition
        product["camposCustomizados"][8]["valor"] = self.fabric_width
        product["camposCustomizados"][11]["valor"] = self.code

        self.product = product
        return product

    def compose_variations(self, changed_name=True):

        folder = os.listdir(self.path_variations)
        variations = []

        for color in folder:
            path_color = os.path.join(self.path_variations, color)

            if "desktop.ini" in color or not path_is_image(path_color):
                continue

            color_name, cod_sku = self.generate_colorname_and_codsku(
                color, changed_name
            )
            image_url = ""

            if "image_urls.json" in folder:
                img_json = self.get_image_json(
                    os.path.join(self.path_variations, "image_urls.json")
                )

                if img_json:
                    for img in img_json.items():
                        if img[0] == color_name:
                            image_url = img[1]["img"]
                            break

            variation = self.get_variation_json()

            variation["nomeVariacao"] = f"Cor:{color_name}"
            variation["codigo"] = f"{self.code}-{cod_sku}"
            variation["preco"] = self.price
            variation["pesoLiquido"] = self.weight
            variation["pesoBruto"] = self.weight
            variation["marca"] = self.marca
            variation["dimensoes"]["largura"] = self.larg
            variation["dimensoes"]["altura"] = self.alt
            variation["dimensoes"]["profundidade"] = self.profun
            variation["tributacao"]["origem"] = self.origin
            variation["tributacao"]["ncm"] = self.ncm
            variation["midia"]["imagens"]["imagensURL"] = [{"link": image_url}]

            variations.append(variation)

        self.get_upload_cover()

        self.variations = variations
        return variations

    def compose_two_variations(self, changed_name=True):

        folder = os.listdir(self.path_variations)
        variations = []

        for color in folder:

            path_color = os.path.join(self.path_variations, color)

            if "desktop.ini" in color or not self.imgur.path_is_image(path_color):
                continue

            color_name, cod_sku = self.generate_colorname_and_codsku(
                color, changed_name
            )
            image_url = ""
            album_id = ""

            if "image_urls.json" in folder:
                img_json = self.get_image_json(
                    os.path.join(self.path_variations, "image_urls.json")
                )

                if img_json:
                    for img in img_json:
                        if img.get("color") == color_name:
                            image_url = img.get("url")
                            break
            if not image_url:

                album_id = self.check_exists_album_title(self.folder_name)

                if not album_id:
                    album_id = self.imgur.create_album(self.folder_name)["id"]

                image = self.imgur.upload_image(path_color, album_id)
                self.save_image_json(self.path_variations, image)

                image_url = image["link"]

            for secont_variate in self.second_variations:
                variation = self.get_variation_json()

                variate = str(secont_variate)

                multiplier = float(variate.replace(",", "."))

                variation["nomeVariacao"] = f"Cor:{color_name};Tamanho:{variate}m"
                variation["codigo"] = f"{self.code}-{variate}m-{cod_sku}"
                variation["preco"] = price_generator(self.price_cost, multiplier, 20)
                variation["pesoLiquido"] = self.weight * multiplier
                variation["pesoBruto"] = self.weight * multiplier
                variation["marca"] = self.marca
                variation["dimensoes"]["largura"] = self.larg
                variation["dimensoes"]["altura"] = self.alt
                variation["dimensoes"]["profundidade"] = self.profun
                variation["tributacao"]["origem"] = self.origin
                variation["tributacao"]["ncm"] = self.ncm
                variation["midia"]["imagens"]["externas"] = [{"link": image_url}]
                variation["estrutura"] = {"tipoEstoque": "V", "lancamentoEstoque": ""}

                variations.append(variation)

        with open("poise.json", "w", encoding="utf-8") as arq:
            json.dump(variations, arq, ensure_ascii=False, indent=4)

        self.variations = variations
        self.get_upload_cover(album_id)

        return variations

    def get_image_json(self, path):
        try:
            with open(path, "r") as arq:
                images = json.load(arq)

            return images

        except FileNotFoundError as err:
            return None

    def get_estoque_json(self):
        path = os.path.join(settings.PATH_SRC, "jsons", "estoque.json")
        with open(path, "r", encoding="utf-8") as arq:
            return json.load(arq)

    def get_variation_json(self):
        path = os.path.join(settings.PATH_SRC, "jsons", "variation.json")
        with open(path, "r", encoding="utf-8") as arq:
            return json.load(arq)

    def get_product_json(self):
        path = os.path.join(settings.PATH_SRC, "jsons", "product.json")
        with open(path, "r", encoding="utf-8") as arq:
            return json.load(arq)

    def save_image_json(self, path_folder, image):
        path = os.path.join(path_folder, "image_urls.json")
        data = {"color": image["title"], "url": image["link"], "id": image["id"]}

        try:
            with open(path, "r") as arq:
                images = json.load(arq)

            images.append(data)

        except FileNotFoundError as err:
            images = [data]

        with open(path, "w") as arq:
            json.dump(images, arq, ensure_ascii=False, indent=4)

        return images

    def check_exists_album_title(self, title):
        albums = self.imgur.get_albums()

        for album in albums:
            if album.get("title") and title in album.get("title"):
                return album["id"]

        return False

    def generate_colorname_and_codsku(self, color, changed_name):

        color_name, _ = os.path.splitext(color)
        color_name = color_name.title()

        if changed_name:
            cod_sku = re.sub("[^0-9]", "", color_name)

            if not cod_sku or cod_sku == "":
                cod_sku = color_name
        else:
            cod_sku = color_name

        return color_name, cod_sku

    def upload_product(self, changed_name=True, product: dict = None):
        link = "https://www.bling.com.br/Api/v3/produtos"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        if not product:
            product = self.compose_product(changed_name)

        body_message = json.dumps(product)

        try:
            response = http.post(link, headers=headers, data=body_message)
            print(f"Produto {self.name} cadastrado com sucesso. {response.status_code}")
            response = response.json()

            data = {
                "id_pai": response["data"]["id"],
                "variations": [
                    {"id": var["id"], "nome": var["nomeVariacao"]}
                    for var in response["data"]["variations"]["saved"]
                ],
            }

            return data

        except requests.exceptions.HTTPError as err:
            print(err.response.json())

    def add_estoque(self, id_deposito: str, id_products: list, qtd: float):
        link = "https://www.bling.com.br/Api/v3/estoques"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        deposito1 = 10610809064  # -> LEGITIMA

        # deposito1 = 14886526196

        estoque_json = self.get_estoque_json()
        for i,id_product in enumerate(id_products, start=1):
            estoque_json["produto"]["id"] = id_product
            estoque_json["deposito"]["id"] = id_deposito
            estoque_json["quantidade"] = qtd

            body_message = json.dumps(estoque_json)

            response = http.post(link, headers=headers, data=body_message)

            if response.status_code == 201:
                print(f"Lançamento de estoque: OK {i}")

    def edit_product(self, id_product, payload):
        link = f"https://www.bling.com.br/Api/v3/produtos/{id_product}"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        body_message = json.dumps(payload)

        try:
            response = http.put(link, headers=headers, data=body_message)
            print(f"Produto {self.name} editado com sucesso. {response.status_code}")
            response = response.json()

            data = {"status": 200}

            return data

        except requests.exceptions.HTTPError as err:
            print(err.response.json())
