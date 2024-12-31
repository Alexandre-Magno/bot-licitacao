from coleta.coletor import Coletor
from tratamento.trata_publicacoes import ler_json, transformar_em_csv
from datetime import datetime
from banco_de_dados.carga import carga
import os
from banco_de_dados.db import DB

coletor = Coletor()
list_of_ufs = ["df", "go"]
list_of_modalidades = [8]

if __name__ == "__main__":

    # coleta das publicações do dia
    today = datetime.today().strftime("%Y%m%d")
    today = "20241227"
    for uf in list_of_ufs:
        for modalidade in list_of_modalidades:
            print(f"Coletando publicações para {uf} e modalidade {modalidade}")
            response = coletor.coleta_todas_publicacoes(today, uf, modalidade)

    temp_dir = os.path.join(os.getcwd(), "temp", today)

    # tratamento e carga das publicações
    for file in os.listdir(temp_dir):
        print("Realizando tratamento e carga do arquivo:", file)
        json_file_path = os.path.join(temp_dir, file)
        csv_file_path = "temp/to_load/publicacoes.csv"

        json_data = ler_json(json_file_path)
        transformar_em_csv(json_data, csv_file_path)
        carga()

    # atualiza novas publicações
    db = DB("db/pncp.db")
    db.execute_sql_file("sql/update_control.sql")
