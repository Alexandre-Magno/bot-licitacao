import json
import csv
import os


def ler_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def transformar_em_csv(json_data, csv_file_path):
    # Defina os campos que você deseja extrair do JSON
    campos = [
        "ano_compra",
        "sequencial_compra",
        "cnpj_orgao",
        "modalidade",
        "valor_total",
        "objeto",
        "dt_publicacao",
    ]

    with open(csv_file_path, "w", newline="\n", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        for item in json_data["data"]:
            writer.writerow(
                {
                    "ano_compra": item.get("anoCompra"),
                    "sequencial_compra": item.get("sequencialCompra"),
                    "cnpj_orgao": item.get("orgaoEntidade", {}).get("cnpj"),
                    "modalidade": item.get("modalidadeId"),
                    "valor_total": item.get("valorTotalEstimado"),
                    "objeto": item.get("objetoCompra").replace("\n", ""),
                    "dt_publicacao": item.get("dataInclusao"),
                }
            )
