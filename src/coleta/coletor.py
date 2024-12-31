import requests
import json
import os

import time


class Coletor:
    def __init__(
        self,
    ):
        self.base_url = "https://pncp.gov.br/api/consulta/v1/"
        self.publicao_endpoint = "contratacoes/publicacao?"

    def coleta_publicacoes(self, pagina: int, data: str, uf: str, modalidade: int):
        headers = {"accept": "*/*"}
        params = f"dataInicial={data}&dataFinal={data}&codigoModalidadeContratacao={modalidade}&pagina={pagina}&uf={uf}"
        full_url = self.base_url + self.publicao_endpoint + params
        response = requests.get(full_url, headers=headers)
        print(full_url)
        if response.status_code == 200:
            self.salva_json_temporario(response.json(), data, uf, pagina)
            return response
        else:
            response.raise_for_status()

    def salva_json_temporario(self, data: dict, date: str, uf: str, pagina: int):
        current_dir = os.getcwd()
        tempo_dir = os.path.join(current_dir, "temp", date)
        os.makedirs(tempo_dir, exist_ok=True)
        file_path = os.path.join(tempo_dir, f"publicacoes_{uf}_{pagina}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"JSON salvo com sucesso!")
        return file_path

    def coleta_todas_publicacoes(self, data: str, uf: str, modalidade: int):
        pagina = 1
        while True:
            try:
                print("Coletando página:", pagina)
                response = self.coleta_publicacoes(pagina, data, uf, modalidade)
                paginas_restantes = response.json().get("paginasRestantes", 0)
                time.sleep(1)
                if paginas_restantes == 0:
                    break
                pagina += 1
            except requests.exceptions.HTTPError as e:
                print(f"Erro ao coletar publicações: {e}")
                break
