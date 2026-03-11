from urllib.parse import urljoin
import requests

def site_request(cod, fabric_name, company):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    data = requests.get(
        urljoin(company["url"], cod),
        headers=headers,
    )

    response = data.json()

    if response["error"] == True:
        raise ValueError(response["message"])

    response = response["data"]["artigo"]
    print(response)

    urls = [
        {
            "name": cor["codigo"],
            "url_img": urljoin(company["pathImage"], cor["image_path"]),
            "format": cor["image_path"].split(".")[-1] if cor["image_path"] else "jpg",
        }
        for cor in response["cores"]
    ]

    response = {
        "fabric_name": fabric_name,
        "cod": f"{company['codPrefix']}{cod}",
        "folder_name": f"{fabric_name} {company['codPrefix']}{cod}",
        "composition": response["composicao"],
        "width": response["largura"],
        "fornecedor": company["name"],
        "id_fornecedor": company["id_fornecedor"],
        "pictures": urls,
    }

    return response
