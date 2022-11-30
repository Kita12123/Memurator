import pyodbc
import sqlite3
import pandas as pd
import json


class ConnectHostOnOdbc:
    """ ODBC接続クラス """
    def __init__(self, connstring: str):
        self.connstring = connstring

    def create_df(self, sql: str) -> pd.DataFrame:
        """データフレーム作成"""
        with pyodbc.connect(self.connstring) as conn:
            df = pd.read_sql(sql, conn)
        return df


class ConnectOnSqlite3:
    """ SQLite3接続クラス """
    def __init__(self, database: str):
        self.database = database

    @property
    def connection(self) -> sqlite3.Connection:
        return sqlite3.connect(
                self.database,
                timeout=8,
                check_same_thread=False)

    def create_df(self, sql: str) -> pd.DataFrame:
        """データフレーム作成"""
        with self.connection as conn:
            df = pd.read_sql(sql, conn)
        return df

    def create_list(self, sql: str) -> list:
        """リスト作成"""
        with self.connection as conn:
            results = conn.cursor().execute(sql).fetchall()
            conn.commit()
        return results

    def update_by_sql(self, sql: str) -> None:
        """更新"""
        with self.connection as conn:
            conn.cursor().execute(sql)
            conn.commit()

    def update_by_df(
        self,
        df: pd.DataFrame,
        tablename: str,
        if_exists: str,
        index: bool
    ) -> None:
        """更新"""
        with self.connection as conn:
            df.to_sql(
                name=tablename,
                con=conn,
                if_exists=if_exists,
                index=index)
            conn.commit()


class SystemDictionary:
    """ システム変数クラス """
    def __init__(self, file_path: str):
        self.file = file_path
        self.con_update_data = True
        try:
            with open(self.file, mode="r", encoding="utf-8") as f:
                self.dic = json.load(f)
        except (FileNotFoundError):
            self.clear()
            self.save()

    @property
    def max_display_lines(self) -> int:
        """最大表示行数"""
        return int(self.dic["最大表示行数"])

    def clear(self):
        self.dic = {
                "最大表示行数": "",
                "最終更新日時": ""
                }

    def update(self, key: str, value: str):
        """更新"""
        self.dic[key] = value

    def save(self):
        """ファイル保存"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)


class UserDictionary:
    """ユーザー変数クラス
    {
        user1_id : user1_dic,
        user2_id : user2_dic,
         ...
    }
    """
    def __init__(self, file_path: str):
        self.file = file_path
        try:
            with open(self.file, mode="r", encoding="utf-8") as f:
                self.dic = json.load(f)
        except (FileNotFoundError):
            with open(self.file, mode="w", encoding="utf-8") as f:
                json.dump({}, f)
            self.dic = {}

    def load(self, key: str) -> dict:
        """読み込み"""
        if key not in self.dic:
            self.dic[key] = {}
        return self.dic[key]

    def update(self, key: str, dic: dict):
        """更新"""
        self.load(key=key).update(dic)

    def save(self):
        """ファイル保存"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)


class HostFileDefine:
    """ファイル定義クラス"""
    def __init__(
        self, *,
        file_name: str,
        lib_name: str,
        columns_dic: dict
    ):
        """ファイル定義

        Args:
            file_name (str): テーブル名
            lib_name (str): スキーマ名
            columns_dic (dict): {列名:(ホスト列名, データ型)}
        """
        self.file_name = file_name
        self.lib_name = lib_name
        self.columns_dic = columns_dic

    @property
    def sql_create_table(self) -> str:
        """SQLコード(str): テーブル作成"""
        return f"""
            CREATE TABLE IF NOT EXISTS {self.file_name}(
                {",".join([f'{k} {v[1]}'
                    for k, v in self.columns_dic.items()])
                });
        """

    @property
    def sql_deleate_table(self) -> str:
        """SQLコード(str): テーブル削除"""
        return f"DROP TABLE {self.file_name}"

    def to_where_host_by(
        self,
        where_sqlite3: str, /
    ) -> str:
        """WHERE句(str): ホスト用WHERE句に変更"""
        where_host = where_sqlite3
        for c in self.columns_dic:
            if c in where_sqlite3:
                where_host = where_host.replace(c, self.columns_dic[c][0])
        return where_host

    def select_host_where(
        self,
        where_host: str, /
    ) -> str:
        """SQLコード(str): テーブル条件抽出（ホスト用）"""
        # HOSTのSQL文は改行するとエラーになる
        sql = f"""SELECT {','.join([f'{v[0]} AS {k}'
                    for k, v in self.columns_dic.items()])} """
        sql += f" FROM {self.lib_name}.{self.file_name} WHERE {where_host} "
        return sql

    def deleate_sqlite3_where(
        self,
        where_sqlite3: str, /
    ) -> str:
        """SQLコード(str): テーブル条件削除"""
        return f"DELETE FROM {self.file_name} WHERE {where_sqlite3}"
