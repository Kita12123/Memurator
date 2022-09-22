"""
Instance for HOST
"""
import pyodbc

from ProgramData import HOST_ODBC_STRINGS

class DB_HOST_CLS:
    def __init__(self):
        self.database = HOST_ODBC_STRINGS
        self.connection = None
        self.cursor = None
    
    def db_open(self):
        if self.connection is None:
            self.connection = pyodbc.connect(self.database)
        if self.cursor is None:
            self.cursor = self.connection.cursor()

    def db_close(self):
        if self.cursor is not None:
            self.connection.close()
        self.connection = None
        self.cursor = None

DB_HOST = DB_HOST_CLS()