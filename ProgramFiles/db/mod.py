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

    def update_by_df(self,
        df: pd.DataFrame,
        tablename: str,
        if_exists: str,
        index: bool=False) -> None:
        """更新"""
        with self.connection as conn:
            df.to_sql(
                name=tablename,
                con=conn,
                if_exists=if_exists,
                index=index)
            conn.commit()

    def update_by_sql(self,
        sql: str) -> None:
        """更新"""
        with self.connection as conn:
            conn.cursor().execute(sql)
            conn.commit()

class SystemDictionary:
    """ システム変数クラス """
    def __init__(self, file_path: str):
        self.file = file_path
        self.con_update_data = True
        try:
            with open(self.file, mode="r", encoding="utf-8") as f:
               self.dic = json.load(f)
        except(FileNotFoundError):
            self.clear()
            self.save()

    @property
    def max_display_lines(self) -> int:
        """最大表示行数"""
        return int(self.dic["最大表示行数"])

    def clear(self):
        self.dic = {
                "最大表示行数":"",
                "最終更新日時":""
                }

    def update(self, key: str, value: str):
        """更新"""
        self.dic[key] = value

    def save(self):
        """ファイル保存"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)


class UserDictionary:
    """ ユーザー変数クラス 
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
        except(FileNotFoundError):
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