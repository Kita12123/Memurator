import pyodbc
import sqlite3
import json

class ConnectOnOdbc:
    """ ODBC接続クラス """
    def __init__(self, connstring: str):
        self.connstring = connstring
        self.connection = None
        self.cursor = None

    def open(self):
        """接続"""
        if self.connection is None:
            self.connection = pyodbc.connect(self.connstring)
        if self.cursor is None:
            self.cursor = self.connection.cursor()

    def close(self):
        """接続解除"""
        if self.cursor is not None:
            self.connection.close()
        self.connection = None
        self.cursor = None


# マルチスレッド非対応
class ConnectOnSqlite3:
    """ SQLite3接続クラス """
    def __init__(self, database: str):
        self.connection = sqlite3.connect(
            database,
            timeout=8,
            check_same_thread=False
            )
        self.cursor = self.connection.cursor()
    
    def open(self):
        """接続"""
        return
    
    def close(self):
        """接続解除"""
        return

    def execute(self, sql: str):
        """参照"""
        self.cursor.execute(sql)

    def commit(self):
        """更新"""
        self.connection.commit()


class SettingDictionary:
    """ システム変数クラス """
    def __init__(self, file_path: str):
        self.file = file_path
        try:
            with open(self.file, mode="r", encoding="utf-8") as f:
               self.dic = json.load(f)
        except(FileNotFoundError):
            self.dic = {
                    "最大表示行数":"",
                    "最終更新日時":""
                    }
            self.update()

    def update(self):
        """更新"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)


class UserDictionary:
    """ ユーザー変数クラス """
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
        if key in self.dic:
            return self.dic[key]
        else:
            return {}

    def update(self, key: str, dic: dict):
        """更新"""
        self.dic[key] = dic

    def refresh(self):
        """データ保存"""
        with open(self.file, mode="w", encoding="utf-8") as f:
            json.dump(self.dic, f, indent=2, ensure_ascii=False)