"""
Sync with HOST
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from pathlib import Path
import pyodbc
from sqlalchemy import and_
from werkzeug.exceptions import BadRequest

from flaskr.common.model import Base
from flaskr.common.model import engine
from flaskr.common.model import Session


CONNECT_STRING = "DSN=HOST;UID=MINORU1;PWD=;SCH=;CNV=K"

sql_host_dir = Path(__file__).parent / "sql_sync"
sql_host_files = list(sql_host_dir.glob("*.sql"))


def _real_sql_code(filename: str, /) -> str:
    sql_file = sql_host_dir / (filename + ".sql")
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()
    # ホストのODBCは改行が入っているとエラーになる
    #    文字列またはバッファーの長さが無効です
    return sql.replace("\n", " ").replace("  ", "")


def sync_host(tablename, /, **kwargs):
    """ホストとデータベースを同期する"""
    # テーブルモデル取得
    table_model = Base.metadata.tables[tablename]
    if getattr(table_model, "ctime", "") == "更新中":
        raise BadRequest
    setattr(table_model, "ctime", "更新中")
    # 日付取得
    today = datetime.today()
    now_yyyymm = int(today.strftime(r"%Y%m"))
    last_yyyymm = int((today - relativedelta(months=1)).strftime(r"%Y%m"))
    first_now_month = int(str(now_yyyymm - 195000) + "00")
    first_last_month = int(str(last_yyyymm - 195000) + "00")
    last_last_month = int(str(last_yyyymm - 195000) + "99")
    # ホストODBC接続SQL作成
    first_date = kwargs.get(
        "first_date", first_last_month
    )
    last_date = kwargs.get(
        "last_date", last_last_month
    )
    if first_now_month < first_date:
        # 開始日付が月始めより新しい時
        first_now_month = first_date
    if last_date < first_now_month:
        # 終了日付が月始めより古い時
        last_date = first_now_month
    sql = _real_sql_code(tablename).format(
        first_now_month=first_now_month,
        first_date=first_date,
        last_date=last_date
    )
    # ホストよりDataFrame作成
    with pyodbc.connect(CONNECT_STRING) as conn:
        df =  pd.read_sql_query(sql, conn)

    with Session() as session, session.begin():
        # 同等データを削除
        if hasattr(table_model, "sync_column"):
            # 日付で一部削除
            query = and_(
                table_model.sync_column >= first_date,
                table_model.sync_column <= last_date
            )
            session.query(table_model).filter(query).delete()
        else:
            # テーブルを削除
            session.query(table_model).delete()
        session.commit()
    print(df)
    df.to_sql(tablename, engine, if_exists="append", index=False)
    setattr(
        table_model,
        "ctime",
        datetime.today().strftime(r"%Y/%m/%d %H:%M:%S")
    )


def sync_host_all(**kwargs):
    for tablename in Base.metadata.tables:
        sync_host(tablename, **kwargs)
