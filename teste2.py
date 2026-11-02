from bling_api.bling import BlingApi
from bling_api.exceptions import BlingRequestError
import json, requests


class BlingCustom(BlingApi):

    def get_contas_receber(self, params: dict | None = None):
        return self._request_json("get", "contas/receber", params=params)

    def get_conta_receber(self, id_conta: int, params: dict | None = None):
        return self._request_json("get", f"contas/receber/{id_conta}", params=params)

    def delete_contas_receber(self, idContaReceber: int):
        return self._request_json("delete", f"contas/receber/{idContaReceber}")


api = BlingCustom()

data_inicial = "2023-01-01"
data_final = "2023-12-31"

i = 1
todas_contas = {"page": 1, "ids": []}

while True:
    try:
        contas_receber = api.get_contas_receber(
            params={"tipoFiltroData": "E", "dataInicial": data_inicial, "dataFinal": data_final, "pagina": i}
        ).get("data")
    except BlingRequestError as e:
        print(e.response_body)

    if not contas_receber:
        break

    ids_contas = [conta["id"] for conta in contas_receber]

    todas_contas["ids"].extend(ids_contas)
    todas_contas["page"] = i

    with open("contas_receber.json", "w", encoding="UTF-8") as arq:
        json.dump(todas_contas, arq, ensure_ascii=False, indent=2)

    print(f'Pagina {i} salva {len(ids_contas)} Salvos. Total = {len(todas_contas["ids"])}')

    i += 1

with open("contas_receber.json", "r", encoding="UTF-8") as arq:
    todas_contas = json.load(arq)

restantes = []
for i, conta in enumerate(todas_contas["ids"]):
    try:
        deletr = api.delete_contas_receber(conta)
        print(deletr)
        print(f"Conta com id {conta} removida com sucesso!")
    except BlingRequestError as e:
        print(e.response_body, f' -> {i}')
        restantes.append(conta)
    except requests.exceptions.JSONDecodeError:
        print(f"Excluído com sucesso (resposta sem corpo) -> {i}")

todas_contas["ids"] = restantes

with open("contas_receber.json", "w", encoding="UTF-8") as arq:
    json.dump(todas_contas, arq, ensure_ascii=False, indent=2)
