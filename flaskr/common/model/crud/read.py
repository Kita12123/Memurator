"""
Read DataBase
"""
import pandas as pd
from pathlib import Path

from flaskr.common.model import engine

dir = Path(__file__).parent
sql_display_dir = dir / "sql_display"
sql_download_dir = dir / "sql_download"


def _real_sql_display(filename, tablename, where, /) -> str:
    sql_file = sql_display_dir / (filename + ".sql")
    with open(sql_file, "r", encoding="utf-8") as f:
        text = f.read()
    sql = text.format(tablename=tablename, where=where)
    return sql


def create_df(filename, tablename, where="true") -> pd.DataFrame:
    sql = _real_sql_display(filename, tablename, where)
    df = pd.read_sql_query(sql=sql, con=engine)
    return df
