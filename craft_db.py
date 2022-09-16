"""
データベース作成
引数
    1: 開始日付 (デフォルト - 2000)
    2: 終了日付（デフォルト - 現在)
注意
    MUJNRPFの別のクエリを実行中だと
    pyodbc.Error: ('HY000', 'The driver did not supply an error!')
    が出力されて、エラーになる可能性がある。
"""

import pandas as pd
import sqlite3
import pyodbc
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys

from ProgramData import DATABASE
from ProgramFiles.db import file_ins
from ProgramFiles.log import LOGGER, dsp_except

URI = file_ins.TOTAL_URI
def func(
    yyyy :int
    ):
    """Syncing from HOST to sqlite3

    Args:
        where (str, optional): WHERE of SQL("WHERE ~~"). Defaults to "".
    """
    sql_where_host    = f" WHERE DYMD>={yyyy - 1950}0000 AND DYMD<={yyyy - 1950}9999"
    sql_where_sqlite3 = f" WHERE 伝票日付>={yyyy}0000 AND 伝票日付<={yyyy}9999"
    # host -> df (pyodbc)
    sql_select_host = ",".join([f"{v[0]} AS {k}" for k, v in URI.columns_dic.items()])
    sql_host = f"SELECT {sql_select_host} FROM {URI.lib_name}.{URI.file_name} {sql_where_host}"
    print("ODBC Conecting...\n" + sql_host)
    con = pyodbc.connect("DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K")
    cur = con.cursor()
    df = pd.read_sql(
        sql=sql_host,
        con=con)
    cur.close()
    con.close()
    # df -> sqlite3 (to_sql)
    print("Syncing database.db")
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM {URI.file_name} {sql_where_sqlite3}")
        df.to_sql(
            name=URI.file_name,
            con=con, 
            if_exists="append",
            index=False)
        con.commit()
        cur.close()

def main(
    first_yyyy:str,
    last_yyyy :str
    ):
    if first_yyyy == "":
        first_yyyy = "2000"
    if last_yyyy  == "":
        last_yyyy  = datetime.today().strftime(r"%Y")
    first_yyyy = int(first_yyyy)
    last_yyyy  = int(last_yyyy)
    while True:
        func(first_yyyy)
        if first_yyyy == last_yyyy:
            break
        else:
            first_yyyy += 1

if __name__=="__main__":
    try:
        first_yyyy = sys.argv[1]
    except(IndexError):
        first_yyyy = ""
    try:
        last_yyyy = sys.argv[2]
    except(IndexError):
        last_yyyy = ""
    LOGGER.info(f"*************** Connect HOST and SQL ({first_yyyy} - {last_yyyy}) ***************")
    if first_yyyy == "auto":
        try:
            last_month = datetime.today() - relativedelta(months=1)
            file_ins.TOTAL_URI.refresh(first_date=last_month.strftime(r"%Y%m"+"00"))
            file_ins.TEMP_URI1.refresh()
            file_ins.TEMP_URI2.refresh()
            file_ins.ETC_MASTER.refresh()
        except:
            dsp_except()
    else:
        try:
            main(
                first_yyyy=first_yyyy,
                last_yyyy =last_yyyy
            )
        except:
            dsp_except()