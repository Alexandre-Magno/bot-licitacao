import sqlite3


class SetupDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.file_path_create_table = "sql/create.sql"

    def execute_sql_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            sql_script = file.read()
        self.cursor.executescript(sql_script)
        self.conn.commit()


db_setup = SetupDB("db/pncp.db")
db_setup.execute_sql_file(db_setup.file_path_create_table)
