from pathlib import Path

import pandas as pd

from apps.app import db

MAX_ROWS = 500

SALES_COLUMNS_DIC = {
    "伝票日付": "伝票日付",
    "伝票区分名": "伝区",
    "委託区分名": "委託",
    "扱い区分名": "扱い",
    "運送会社名": "運送会社",
    "担当者名": "担当",
    "得意先コード": "得意先CD",
    "得意先名": "得意先名",
    "雑コード": "雑CD",
    "雑名": "雑名",
    "送荷先コード": "送荷先CD",
    "送荷先名": "送荷先名",
    "製品部品コード": "製品部品CD",
    "製品部品カナ": "製品部品カナ",
    "級区分": "等級",
    "数量": "数量",
    "単価": "単価",
    "金額": "金額",
    "出荷伝票番号": "伝票NO",
    "備考": "備考",
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
    row_count = len(df)
    if row_count > MAX_ROWS:
        count_message = f"件数: {row_count}(表示件数: {MAX_ROWS})"
    else:
        count_message = f"件数: {row_count}"
    messages = [
        count_message,
        f"合計数量: {df['数量'].sum():,}",
        f"合計金額: ¥{df['金額'].sum():,}"

    ]
    df.loc[:, ("数量", "単価", "金額")] = (
        df[["数量", "単価", "金額"]].applymap("{:,}".format)
    )
    return df, messages
