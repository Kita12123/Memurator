"""
FLASK Initialize
"""
from flask import Flask
app = Flask(__name__)

from ProgramFiles.db.sql_ins import DB_SQL
DB_SQL.db_open()

from ProgramFiles.flaskr import main