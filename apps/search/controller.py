from pathlib import Path

import pandas as pd

from apps.app import db

SALES_COLUMNS_DIC = {
    "伝票日付": "伝票日付",
    "伝票区分名": "伝区"
}


def _real_sql(filename: str, /) -> str:
    sql_dir = Path(__file__).parent / "static" / "sql"
    sql_file = sql_dir / f"{filename}.sql"
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_fstring = f.read()
    return sql_fstring


def create_df_sales(tablename, where="true", /) -> tuple[pd.DataFrame, list]:
    sql = _real_sql("sales").format(
        tablename=tablename,
        where=where
    )
    df = pd.read_sql_query(sql=sql, con=db.engine)
    messages = (
        f"件数: {len(df)}",
        f"合計数量: {df['数量'].sum():,}",
        f"合計金額: {df['金額'].sum():,}"

    )
    df.loc[:, ("数量", "単価", "金額")] = (
        df[["数量", "単価", "金額"]].applymap("{:,}".format)
    )
    return df, messages
