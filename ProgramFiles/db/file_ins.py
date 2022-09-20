"""
Define Instance for Database
"""
# メモ
#   SQLのカラム名を工夫した方がいいかもしれない。
#   -> create_sql_sqlite3を変更して、テーブルを再作成しないといけないので面倒
import pandas as pd
import pyodbc
import sqlite3
from ProgramData import HOST_ODBC_STRINGS, DATABASE
from ProgramFiles.log import LOGGER


#
# Main Class
#
class FD:
    def __init__(
        self,
        file_name: str,
        lib_name: str,
        columns_dic: dict
        ):
        self.file_name = file_name
        self.lib_name = lib_name
        self.columns_dic = columns_dic
        # create table on sqlite3
        sql_select_sqlite3 = ','.join([f'{k} {v[1]}' for k, v in self.columns_dic.items()])
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.file_name}(
                {sql_select_sqlite3}
                );
            """)
            cur.close()

    def refresh(
        self,
        sql: str=""
        ):
        """Syncing from HOST to sqlite3

        Args:
            where (str, optional): WHERE of SQL("WHERE ~~"). Defaults to "".
        """
        # host -> df (pyodbc)
        sql_where_host = ""
        sql_where_sqlite3 = ""
        if sql:
            sql_where_sqlite3 = " WHERE " + sql
            for k, v in self.columns_dic.items():
                if k in sql:
                    sql = sql.replace(k, v[0])
            sql_where_host    = " WHERE " + sql
        sql_select_host = ",".join([f"{v[0]} AS {k}" for k, v in self.columns_dic.items()])
        sql_host = f"SELECT {sql_select_host} FROM {self.lib_name}.{self.file_name} {sql_where_host}"
        LOGGER.debug("ODBC Conecting...\n" + sql_host)
        con = pyodbc.connect(HOST_ODBC_STRINGS)
        cur = con.cursor()
        df = pd.read_sql(
            sql=sql_host,
            con=con)
        cur.close()
        con.close()
        # df -> sqlite3 (to_sql)
        LOGGER.debug("Syncing database.db")
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.file_name} {sql_where_sqlite3}")
            df.to_sql(
                name=self.file_name,
                con=con, 
                if_exists="append",
                index=False)
            con.commit()
            cur.close()


#
# Instance
#
TOTAL_URI = FD(
    file_name="MUJNRPF",
    lib_name="MOLIB",
    columns_dic= {
        "伝票日付":("DYMD", "INTEGER"),
        "得意先コード":("TOKCD", "INTEGER"),
        "得意先カナ":("TOKNM", "TEXT"),
        "雑コード":("ZATUCD", "INTEGER"),
        "伝票区分":("DENK", "INTEGER"),
        "委託区分":("ITAK", "INTEGER"),
        "扱い運送":("ATU", "INTEGER"),
        "担当者コード":("TANCD", "INTEGER"),
        "送荷先コード":("ATUNM", "INTEGER"),
        "送荷先カナ":("SOK", "TEXT"),
        "製品部品コード":("CODE", "INTEGER"),
        "製品部品カナ":("HINNM", "TEXT"),
        "級区分":("KKBN", "INTEGER"),
        "数量":("SUR", "INTEGER"),
        "単価":("TANKA", "INTEGER"),
        "原価":("TANATA", "REAL"),
        "金額":("KIN", "INTEGER"),
        "出荷伝票番号":("SDENNO", "TEXT"),
        "オーダー番号":("ODER", "TEXT"),
        "備考":("BIKO", "TEXT")
        }
)

TEMP_URI1 = FD(
    file_name="UJNRPFW",
    lib_name="FLIB1",
    columns_dic= {
        "伝票日付":("DENYMD", "INTEGER"),
        "得意先コード":("TOKCD", "INTEGER"),
        "得意先カナ":("TOKMEK", "TEXT"),
        "雑コード":("ZATUCD", "INTEGER"),
        "伝票区分":("DENKBN", "INTEGER"),
        "委託区分":("ITACD", "INTEGER"),
        "扱い区分":("ATUKAI", "INTEGER"),
        "運送会社コード":("UNSOCD", "INTEGER"),
        "担当者コード":("TANCD", "INTEGER"),
        "送荷先コード":("ATUMEI", "INTEGER"),
        "送荷先カナ":("SOKMEI", "TEXT"),
        "製品部品コード":("SEIBUC", "INTEGER"),
        "製品部品カナ":("HINMEI", "TEXT"),
        "級区分":("KYUKBN", "INTEGER"),
        "数量":("SURYO", "INTEGER"),
        "単価":("TANKA", "INTEGER"),
        "オーダー番号":("ODER", "TEXT"),
        "備考":("BIKO", "TEXT")
    }
)

TEMP_URI2 = FD(
    file_name="UJNRPF",
    lib_name="FLIB1",
    columns_dic= {
        "伝票日付":("DENYMD", "INTEGER"),
        "得意先コード":("TOKCD", "INTEGER"),
        "得意先カナ":("TOKMEK", "TEXT"),
        "雑コード":("ZATUCD", "INTEGER"),
        "伝票区分":("DENKBN", "INTEGER"),
        "委託区分":("ITACD", "INTEGER"),
        "扱い区分":("ATUKAI", "INTEGER"),
        "運送会社コード":("UNSOCD", "INTEGER"),
        "担当者コード":("TANCD", "INTEGER"),
        "送荷先コード":("ATUMEI", "INTEGER"),
        "送荷先カナ":("SOKMEI", "TEXT"),
        "製品部品コード":("SEIBUC", "INTEGER"),
        "製品部品カナ":("HINMEI", "TEXT"),
        "級区分":("KYUKBN", "INTEGER"),
        "数量":("SURYO", "INTEGER"),
        "単価":("TANKA", "INTEGER"),
        "オーダー番号":("ODER", "TEXT"),
        "備考":("BIKO", "TEXT")
    }
)

ETC_MASTER = FD(
    file_name="ETCMPF",
    lib_name="FLIB",
    columns_dic={
        "レコード区分":("RKBN", "INTEGER"),
        "コード":("CODE", "INTEGER"),
        "名称":("NAME", "TEXT"),
        "カナ":("NAME2", "TEXT"),
        "数値":("SUU","INTEGER")
    }
)