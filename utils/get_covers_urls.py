import os
from apps.amazon_s3.upload_s3 import upload_folder_to_s3_parallel
from utils.get_image_json import get_image_json


def get_covers_urls(folder_name, cover_path):

        if "image_urls.json" in os.listdir(cover_path):
            img_json = get_image_json(
                os.path.join(cover_path, "image_urls.json")
            )
            images_url = [{"link": img[1]["img"]} for img in img_json.items()]

            return images_url

        s3_folder = f"{folder_name}/Capa"

        upload_folder_to_s3_parallel(cover_path, s3_folder)

        return get_covers_urls()