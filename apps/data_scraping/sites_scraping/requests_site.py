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

    data_artigo = response["data"]["artigo"]
    estampas = data_artigo.get("cores", [])

    if estampas:
        urls = []
        for estampa in estampas:
            urls.append(
                {
                    "name": estampa["codigo"],
                    "url_img": urljoin(company["pathImage"], estampa["image_path"]),
                    "format": estampa["image_path"].split(".")[-1] if estampa["image_path"] else "jpg",
                }
            )

    else:

        page = 1
        urls = []
        while True:
            response_estampas = requests.get(
                urljoin(company["url_estampas"], cod), headers=headers, params={"page": page}
            )

            if response_estampas.status_code != 200:
                raise ValueError(
                    f"Erro ao buscar estampas: {response_estampas.status_code}, {response_estampas.text}"
                )

            response_estampas_data = response_estampas.json().get("data", {})

            estampas = response_estampas_data.get("estampas", [])

            if not estampas:
                raise ValueError("Nenhuma estampa encontrada para o código fornecido.")

            for estampa in estampas:
                urls.append(
                    {
                        "name": estampa["codigo"],
                        "url_img": urljoin(company["pathImage"], estampa["image_filename"]),
                        "format": (
                            estampa["image_filename"].split(".")[-1] if estampa["image_filename"] else "jpg"
                        ),
                    }
                )

            if not response_estampas_data.get("has_next_page"):
                print(f"Todas as páginas de estampas foram processadas. Pagina atual: {page}")
                break

            page += 1

    response = {
        "fabric_name": fabric_name,
        "cod": f"{company['codPrefix']}{cod}",
        "folder_name": f"{fabric_name} {company['codPrefix']}{cod}",
        "composition": data_artigo["composicao"],
        "width": data_artigo["largura"],
        "fornecedor": company["name"],
        "id_fornecedor": company["id_fornecedor"],
        "pictures": urls,
    }

    return response
