"""
Instance for SQLite3
"""
import sqlite3

from ProgramData import DATABASE

class DB_SQL_CLS:
    def __init__(self):
        self.database = DATABASE
        self.connection = None
        self.cursor = None
    
    def db_open(self):
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.database,
                check_same_thread=False)
        if self.cursor is None:
            self.cursor = self.connection.cursor()

    def db_execute(self, sql):
        """参照"""
        self.cursor.execute(sql)

    def db_commit(self):
        """更新"""
        self.connection.commit()

    def db_close(self):
        if self.cursor is not None:
            self.connection.close()
        self.connection = None
        self.cursor = None

DB_SQL = DB_SQL_CLS()