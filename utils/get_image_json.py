import json
def get_image_json(path):
        try:
            with open(path, "r") as arq:
                images = json.load(arq)

            return images

        except FileNotFoundError as err:
            return None