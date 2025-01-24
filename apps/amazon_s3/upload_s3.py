import boto3, os, json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
from PIL import Image


# Configurações da AWS
A_A_T = "AKIA4VDBMCPWMWUNC2SM"
A_S_T = "tmlHv4Sr1Mwn0SDn0p3Vu9KAQR0lDxdhQtdA+gJb"
BUCKET_NAME = "legitimatextil"

# Inicializar cliente S3
s3 = boto3.client("s3", aws_access_key_id=A_A_T, aws_secret_access_key=A_S_T)


def upload_file(local_path, s3_key):
    """
    Faz upload de um único arquivo para o S3.
    """
    try:
        s3.upload_file(
            local_path, BUCKET_NAME, s3_key, ExtraArgs={"ContentType": "image/jpeg"}
        )
        print(f"Arquivo enviado: {s3_key}")

        return s3_key
    except Exception as e:
        print(f"Erro ao fazer upload de {s3_key}: {str(e)}")


def upload_folder_to_s3_parallel(folder_path, s3_folder, max_threads=5):
    s3_folder = f"catalogo/{s3_folder}"
    """
    Faz upload de uma pasta inteira para o S3 utilizando threads.
    """
    files_to_upload = []
    upload_info = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if "desktop.ini" in file or ".json" in file or ".xlsx" in file:
                continue
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path).replace("\\", "/")
            s3_key = f"{s3_folder}/{relative_path}"
            files_to_upload.append((local_path, s3_key))
    # Fazer upload em paralelo
    with ThreadPoolExecutor(max_threads) as executor:
        results = executor.map(lambda args: upload_file(*args), files_to_upload)

        for result in results:

            if result:  # Se o upload for bem-sucedido

                # Adicionar as URLs ao dicionário
                relative_file_name = result.split("/")[-1].split(".")[
                    0
                ]  # Extraindo o nome do arquivo sem a extensão

                if not upload_info.get(relative_file_name):
                    upload_info[relative_file_name] = {}

                # Criar os links com base no S3
                img_url = f"https://{BUCKET_NAME}.s3.us-east-2.amazonaws.com/{quote(result).replace('%20', '+')}"

                if "1_1" in result:
                    upload_info[relative_file_name]["img_1x1"] = img_url
                elif "80x80" in result:
                    upload_info[relative_file_name]["img_80x80"] = img_url
                else:
                    upload_info[relative_file_name]["img"] = img_url

    # Criar o arquivo .json com as informações
    with open(os.path.join(folder_path, "image_urls.json"), "w") as json_file:
        json.dump(upload_info, json_file, indent=4)

    print("Upload concluído e arquivo JSON gerado!")


def path_is_image(path):

    try:
        with Image.open(path) as img:
            img.verify()
        return True

    except:
        return False
