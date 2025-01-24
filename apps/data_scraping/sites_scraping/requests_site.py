from urllib.parse import urljoin
import requests


atacado = {
    "DISPARADA": {
        "url": r"https://disparadatecidos.com.br/api/get_data_for_artigo_view/",
        "pathImage": r"https://sistema.disparadatecidos.com.br/upload_artigo_images/",
        "codPrefix": "D",
    },
    "JANON": {
        "url": r"https://tecidosjanon.com/api/get_data_for_artigo_view/",
        "pathImage": r"https://tecidosjanon.com/sistema/upload_artigo_images/",
        "codPrefix": "J",
    },
}


def site_request(cod, fabric_name, company):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    data = requests.get(
        urljoin(atacado[company]["url"], cod),
        headers=headers,
    )

    response = data.json()

    if response["error"] == True:
        raise ValueError(response["message"])

    response = response["data"]["artigo"]

    urls = [
        {
            "name": cor["codigo"],
            "url_img": urljoin(atacado[company]["pathImage"], cor["image_path"]),
            "format": cor["image_path"].split(".")[-1],
        }
        for cor in response["cores"]
    ]

    response = {
        "fabric_name": fabric_name,
        "cod": f"{atacado[company]['codPrefix']}{cod}",
        "folder_name": f"{fabric_name} {atacado[company]['codPrefix']}{cod}",
        "composition": response["composicao"],
        "width": response["largura"],
        "pictures": urls,
    }

    return response
