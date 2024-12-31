from banco_de_dados.loading_data import load


def carga():
    task = {
        "table": "publicacoes",
        "file": "temp/to_load/publicacoes.csv",
        "fields": [
            "ano_compra",
            "sequencial_compra",
            "cnpj_orgao",
            "modalidade",
            "valor_total",
            "objeto",
            "dt_publicacao",
        ],
        "keys": ["ano_compra", "sequencial_compra", "cnpj_orgao"],
    }

    load(task)
