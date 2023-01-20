from datetime import datetime
from pathlib import Path

import pandas as pd
import pyodbc
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_

from apps.app import db

CONNECT_STRING = "DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"
SQL_DIR = Path(__file__).parent / "static" / "sql"


def _real_sql_syncing(filename: str, /) -> str:
    sql_file = SQL_DIR / "syncing" / f"{filename}.sql"
    with open(sql_file, "r", encoding="utf-8") as f:
        text = f.read()
    # ホストのODBCは改行が入っているとエラーになる
    #    文字列またはバッファーの長さが無効です
    sql = text.replace("\n", " ").replace("  ", "")
    return sql


def _real_sql_display(filename, where, /) -> str:
    sql_file = SQL_DIR / "display" / f"{filename}.sql"
    with open(sql_file, "r", encoding="utf-8") as f:
        text = f.read()
    sql = text.format(where=where)
    return sql


def sync_host(tablename, /, **kwargs):
    """ホストと同期する

    Args:
        tablename (str): テーブル名
        first_date(str): 開始日付
        last_date(str): 終了日付
    """
    # テーブルモデル取得
    table_model = db.metadata.tables[tablename]
    if getattr(table_model, "ctime", "") == "更新中":
        return False
    setattr(table_model, "ctime", "更新中")
    # 日付取得
    today = datetime.today()
    now_yyyymm = int(today.strftime(r"%Y%m"))
    last_yyyymm = int((today - relativedelta(months=1)).strftime(r"%Y%m"))
    first_now_month = int(str(now_yyyymm - 195000) + "00")
    first_last_month = int(str(last_yyyymm - 195000) + "00")
    last_date = 999999
    # ホストODBC接続SQL作成
    first_date = kwargs.get(
        "first_date", first_last_month
    )
    last_date = kwargs.get(
        "last_date", last_date
    )
    if first_now_month < first_date:
        # 開始日付が月始めより新しい時
        first_now_month = first_date
    if last_date < first_now_month:
        # 終了日付が月始めより古い時
        last_date = first_now_month
    sql = _real_sql_syncing(tablename).format(
        first_now_month=first_now_month,
        first_date=first_date,
        last_date=last_date
    )
    # ホストよりDataFrame作成
    with pyodbc.connect(CONNECT_STRING) as conn:
        df = pd.read_sql_query(sql, conn)
    # 同等データを削除
    if hasattr(table_model, "sync_column"):
        # 日付で一部削除
        query = and_(
            table_model.sync_column >= first_date,
            table_model.sync_column <= last_date
        )
        db.session.query(table_model).filter(query).delete()
    else:
        # テーブルを削除
        db.session.query(table_model).delete()
        db.session.commit()
    df.to_sql(tablename, db.engine, if_exists="append", index=False)
    setattr(
        table_model,
        "ctime",
        datetime.today().strftime(r"%Y/%m/%d %H:%M:%S")
    )


def sync_host_all(**kwargs):
    """ホストとすべて同期する

    Args:
        first_date(str): 開始日付
        last_date(str): 終了日付
    """
    for tablename in db.metadata.tables:
        if tablename == "users":
            continue
        sync_host(tablename, **kwargs)


def create_df(tablename, where="true") -> pd.DataFrame:
    """データ取得

    Args:
        tablename (str): テーブル名
        where (str, optional): WHERE句. Defaults to "true".

    Returns:
        pd.DataFrame: SQL実行後のデータ
    """
    sql = _real_sql_display(tablename, where)
    df = pd.read_sql_query(sql=sql, con=db.engine)
    return df
