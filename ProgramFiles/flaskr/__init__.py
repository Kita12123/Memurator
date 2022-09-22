"""
FLASK Initialize
"""
from ProgramFiles.db.sql_ins import DB_SQL
DB_SQL.db_open()

from flask import Flask
app = Flask(__name__)

from ProgramFiles.flaskr import main