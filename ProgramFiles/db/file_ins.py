"""
Define Instance for Database
"""
# メモ
#   SQLのカラム名を工夫した方がいいかもしれない。
#   -> create_sql_sqlite3を変更して、テーブルを再作成しないといけないので面倒
import pandas as pd
from ProgramFiles.log import LOGGER
from ProgramFiles.db.sql_ins import DB_SQL
from ProgramFiles.db.host_ins import DB_HOST


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
        self.sql_select_sqlite3 = ",".join([f'{k} {v[1]}' for k, v in self.columns_dic.items()])
        self.sql_select_host    = ",".join([f"{v[0]} AS {k}" for k, v in self.columns_dic.items()])
        # テーブルがなければ、作成する
        DB_SQL.db_open()
        DB_SQL.db_execute(
            sql=f"""
            CREATE TABLE IF NOT EXISTS {self.file_name}(
                {self.sql_select_sqlite3}
                );
            """
        )
        DB_SQL.db_commit()
        DB_SQL.db_close()

    def refresh(
        self,
        where: str=""
        ):
        """Syncing from HOST to sqlite3

        Args:
            where (str, optional): WHERE of SQL("WHERE ~~"). Defaults to "".
        """
        # WHERE句作成（ホスト向け、SQLite3向け）
        sql_where_host = ""
        sql_where_sqlite3 = ""
        if where:
            sql_where_sqlite3 = " WHERE " + where
            for k, v in self.columns_dic.items():
                if k in where:
                    where = where.replace(k, v[0])
            sql_where_host    = " WHERE " + where
        sql_host = f"SELECT {self.sql_select_host} FROM {self.lib_name}.{self.file_name} {sql_where_host}"
        # host -> df
        LOGGER.debug("ODBC Conecting..." + self.file_name)
        DB_HOST.db_open()
        df = pd.read_sql(sql=sql_host, con=DB_HOST.connection)
        DB_HOST.db_close()
        # df -> database.db
        LOGGER.debug("Syncing database.db..." + self.file_name)
        DB_SQL.db_open()
        if sql_where_host:
            DB_SQL.db_execute(sql=f"DELETE FROM {self.file_name} {sql_where_sqlite3}")
        else:
            DB_SQL.db_execute(f"DROP TABLE {self.file_name}")
            DB_SQL.db_execute(f"""
                CREATE TABLE IF NOT EXISTS {self.file_name}(
                    {self.sql_select_sqlite3}
                    );
                """)
        df.to_sql(
            name=self.file_name,
            con=DB_SQL.connection, 
            if_exists="append",
            index=False)
        DB_SQL.db_commit()
        DB_SQL.db_close()


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
        "出荷伝票番号":("SYUDEN", "TEXT"),
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
        "出荷伝票番号":("SYUDEN", "TEXT"),
        "オーダー番号":("ODER", "TEXT"),
        "備考":("BIKO", "TEXT"),
    }
)

ETC_MASTER = FD(
    file_name="ETCMPF",
    lib_name="FLIB",
    columns_dic={
        "レコード区分＊":("RKBN", "INTEGER"),
        "コード＊":("CODE", "INTEGER"),
        "名称＊":("NAME", "TEXT"),
        "カナ＊":("NAME2", "TEXT"),
        "数値＊":("SUU","INTEGER")
    }
)


SOKCD_MASTER = FD(
    file_name="NIHONPF",
    lib_name="FLIB",
    columns_dic={
        "送荷先コード＊":("コード", "INTEGER"),
        "送荷先カナ＊":("日本語１カナ", "TEXT"),
        "送荷先名＊":("日本語１漢字", "TEXT"),
        "県コード＊":("県コード", "INTEGER"),
        "電話番号＊":("電話番号", "TEXT"),
        "郵便番号１＊":("郵便番号１", "INTEGER"),
        "郵便番号２＊":("郵便番号２", "INTEGER"),
        "住所１＊":("日本語２漢字", "TEXT"),
        "住所２＊":("日本語３漢字", "TEXT")
    }
)

TOKCD_MASTER = FD(
    file_name="TOKMPF",
    lib_name="FLIB",
    columns_dic={
        "得意先コード１＊":("TOKCD1", "INTEGER"),
        "得意先コード２＊":("TOKCD2", "INTEGER"),
        "得意先カナ＊":("TOKA1", "TEXT"),
        "得意先名＊":("TOKJ1", "TEXT"),
        "担当者コード＊":("TANCD", "INTEGER"),
        "県コード＊":("KENCD", "INTEGER"),
        "郵便番号１＊":("YUBIA1", "INTEGER"),
        "郵便番号２＊":("YUBIA2", "INTEGER"),
        "住所１＊":("ADLJ1", "TEXT"),
        "住所２＊":("ADLJ2", "TEXT"),
        "電話番号＊":("TELNO", "TEXT"),
        "作成日＊":("SAKUSE", "INTEGER"),
        "締め日＊":("SIMEBI", "INTEGER"),
        "ＬＥＳＳ率＊":("LESS", "INTEGER")
    }
)

KEN_MASTER = FD(
    file_name="KENPF",
    lib_name="FLIB1",
    columns_dic={
        "県コード＊":("CODE", "INTEGER"),
        "県名＊":("NAME", "TEXT")
    }
)

SEIHIN_MASTER = FD(
    file_name="SEIMPF",
    lib_name="FLIB",
    columns_dic={
        "製品コード＊":("機種コード", "INTEGER"),
        "製品カナ＊":("製品名", "TEXT"),
        "分類＊":("製品分類", "INTEGER"),
        "集計コード＊":("集計用ＣＤ", "INTEGER"),
        "１級単価＊":("１級売単価", "INTEGER"),
        "１級原価＊":("１級原価", "INTEGER"),
        "２級単価＊":("２級売単価", "INTEGER"),
        "２級原価＊":("２級原価", "INTEGER"),
        "廃止区分＊":("重点品目区分", "TEXT"),
        "作成日＊":("作成日", "INTEGER"),
        "税率区分＊":("SEKBN", "INTEGER")
    }
)

BUHIN_MASTER = FD(
    file_name="BUHMPF",
    lib_name="FLIB",
    columns_dic={
        "部品コード＊":("RKEY", "INTEGER"),
        "部品カナ＊":("NAME", "TEXT"),
        "部番＊":("BAN", "TEXT"),
        "単価＊":("TANK1", "REAL"),
        "原価＊":("TANK2", "REAL"),
        "旧単価＊":("TANKS", "REAL"),
        "代替区分＊":("DAIK", "INTEGER"),
        "代替コード＊":("DAIC", "INTEGER"),
        "重量＊":("JURYO", "REAL"),
        "廃止区分＊":("HAISIF", "INTEGER"),
        "作成日＊":("CRTYMD", "INTEGER")
    }
)