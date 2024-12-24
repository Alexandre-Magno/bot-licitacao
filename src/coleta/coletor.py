import requests


class Coletor:
    def __init__(
        self,
    ):
        self.base_url = "https://pncp.gov.br/api/consulta/v1/"
        self.publicao_endpoint = "contratacoes/publicacao?"

    def coleta_publicacoes(self):
        headers = {"accept": "*/*"}
        params = f"dataInicial=20241220&dataFinal=20241220&codigoModalidadeContratacao=8&pagina=1"
        full_url = self.base_url + self.publicao_endpoint + params
        response = requests.get(full_url, headers=headers)
        print(full_url)
        if response.status_code == 200:
            return response
        else:
            response.raise_for_status()


api = Coletor()
r = api.coleta_publicacoes()
print(r)
