from dotenv import load_dotenv
import csv
import logging
import sqlite3

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Logger")


# TODO Revisar funções repetidas e/ou sem sentidos que podem ser melhoras ou unificadas
def get_conn():
    """
    Estabelece uma conexão com o banco de dados SQL.

    Returns:
        MSSQLDriver: Um objeto de conexão com o banco de dados.
    """
    return sqlite3.connect("db/pncp.db")


def create_tmp(db, table_name, fields):
    """
    Cria uma tabela temporária com base na estrutura da tabela existente.

    Args:
        db (MSSQLDriver): A conexão com o banco de dados.
        table_name (str): O nome da tabela de origem.
        fields (list): A lista de campos a serem selecionados.
    """
    sql = f"""
            CREATE TEMP TABLE {table_name}_tmp AS 
            SELECT {','.join(fields)} 
            FROM {table_name} 
            WHERE 0=1
        """
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    cur.close()


def load_tmp(db, file_name, table_name, fields, keys):
    """
    Carrega dados de um arquivo CSV em uma tabela temporária.

    Args:
        db (MSSQLDriver): A conexão com o banco de dados.
        file_name (str): O nome do arquivo CSV a ser carregado.
        table_name (str): O nome da tabela de destino.
        fields (list): Os campos a serem inseridos na tabela.
    """
    #    create_tmp(db, table_name, fields)

    with open(file_name, "r", encoding="latin1") as f:
        reader = csv.reader(f)
        primeira_linha = next(reader)
        colunas = primeira_linha
        nomes_colunas = ", ".join(colunas)
        placeholders = ", ".join(["?"] * len(colunas))
        sql_insert = (
            f"INSERT INTO {table_name}_tmp ({nomes_colunas}) VALUES ({placeholders})"
        )

        columns = ", ".join(fields)

        # Campos para atualização
        update_fields = set(fields) - set(keys)
        update_clause = ", ".join(
            [f"{field} = EXCLUDED.{field}" for field in update_fields]
        )

        # Monta o SQL
        sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON CONFLICT ({', '.join(keys)})
            DO UPDATE SET {update_clause};
        """
        cur = db.cursor()
        for linha in reader:
            valores = [None if valor == "" else valor for valor in linha]
            try:
                cur.execute(sql, valores)
            except Exception as e:
                logger.warning(f"Erro ao inserir registro: {linha}. Erro: {e}")

        db.commit()
        cur.close()


def upsert(db, table_name, fields, keys):
    """
    Realiza uma operação de upsert (update + insert) em uma tabela SQLite.

    Args:
        db (sqlite3.Connection): A conexão com o banco de dados.
        table_name (str): O nome da tabela de destino.
        fields (list): Os campos a serem inseridos/atualizados.
        keys (list): Os campos que formam a chave primária.
    """
    # Campos para inserção
    placeholders = ", ".join(["?" for _ in fields])
    columns = ", ".join(fields)

    # Campos para atualização
    update_fields = set(fields) - set(keys)
    update_clause = ", ".join(
        [f"{field} = EXCLUDED.{field}" for field in update_fields]
    )

    # Monta o SQL
    sql = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        ON CONFLICT ({', '.join(keys)})
        DO UPDATE SET {update_clause};
    """
    print(sql)
    cur = db.cursor()
    cur.execute(sql)
    db.commit()
    cur.close()


def execute_sql_query(query):
    """
    Executa uma consulta SQL e registra o número de linhas afetadas.

    Args:
        query (str): A consulta SQL a ser executada.
    """
    db = get_conn().get_db()
    with db.cursor() as cur:
        cur.execute(query)
        num_linhas_afetadas = cur.rowcount
        logger.info(f"Número de linhas afetadas: {num_linhas_afetadas}")


def load(config) -> None:
    """
    Carrega dados de um arquivo CSV em uma tabela do banco de dados.

    Esta função registra o início do carregamento, possivelmente trunca a tabela
    de destino, carrega os dados em uma tabela temporária e realiza operações de
    atualização e inserção conforme necessário.

    Args:
        config (dict): Um dicionário de configurações que contém as seguintes chaves:
            - file (str): O caminho do arquivo CSV a ser carregado.
            - table (str): O nome da tabela de destino no banco de dados.
            - fields (list): Lista de campos a serem carregados na tabela.
            - keys (list): Lista de campos que formam a chave primária da tabela.
            - truncate (str, opcional): Se 'true', a tabela será truncada antes do carregamento.
            - surrogates (list, opcional): Lista de dicionários contendo informações sobre
              chaves substitutas a serem atualizadas. Cada dicionário deve conter as chaves:
              - parent (str): Nome da tabela pai.
              - relation (list): Relação entre as tabelas.
              - key (str): O campo de chave substituta a ser atualizado.

    Returns:
        None: Esta função não retorna valor, mas realiza operações no banco de dados.
    """
    logger.info(f'Carregando Dados do Arquivo: {config.get("file")}')
    logger.info(f'Para Tabela: {config.get("table")}')
    db = get_conn()

    load_tmp(
        db,
        config.get("file"),
        config.get("table"),
        config.get("fields"),
        config.get("keys"),
    )

    #    upsert(db, config.get("table"), config.get("fields"), config.get("keys"))
    db.commit()
    db.close()
