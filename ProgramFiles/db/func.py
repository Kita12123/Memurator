"""
Main Fuction
"""
import pandas as pd
import sqlite3
from ProgramData import DATABASE

#
# Sub Funciton
#
def craft_sql(
    sql_where_sqlite3: str,
    sort_column: str,
    sort_type: str
    ) -> str:
    """Create Code of SQL for Database on sqlite3

    Args:
        sql_where_sqlite3 (str, optional): WHERE句(WHETEは不要). Defaults to "".

    Returns:
        str: 売上データ用に加工したSQLコード
    """
    def func(file: str) -> str:
        return f"""
        SELECT
            伝票日付+19500000 AS 伝票日付,
            伝票区分,
            ifnull(ET1.名称,'') AS 伝票区分名,
            委託区分,
            ifnull(ET2.名称,'') AS 委託区分名,
            担当者コード,
            ifnull(ET3.名称,'') AS 担当者名,
            得意先コード,
            得意先カナ,
            雑コード,
            送荷先コード,
            送荷先カナ,
            製品部品コード,
            製品部品カナ,
            級区分,
            CASE
                /* 返品,値引き*/
                WHEN 伝票区分=30 THEN 数量*-1
                WHEN 伝票区分=90 THEN 数量*-1
                ELSE 数量
            END AS 数量,
            単価,
            CASE
                /* 返品,値引き*/
                WHEN 伝票区分=30 THEN 数量*-1*単価
                WHEN 伝票区分=90 THEN 数量*-1*単価
                ELSE 数量*単価
            END AS 金額,
            備考
        FROM {file}
        LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分=10 AND ET1.コード=伝票区分
        LEFT OUTER JOIN ETCMPF ET2 ON ET2.レコード区分=20 AND ET2.コード=委託区分
        LEFT OUTER JOIN ETCMPF ET3 ON ET3.レコード区分=22 AND ET3.コード=担当者コード
        WHERE 
{sql_where_sqlite3}
        AND   数量<>0
        /* 
        伝票区分抽出なし
        AND   伝票区分<>20
        AND   伝票区分<>22
        AND   伝票区分<>50
        AND   伝票区分<>70
        AND   伝票区分<>80
        AND   伝票区分<>95
        AND   伝票区分<>96
        AND   伝票区分<>99
        */
        """
    sql_sqlite3 = ""
    sql_sqlite3 += func(file="MUJNRPF")
    sql_sqlite3 += "\nUNION ALL\n"
    sql_sqlite3 += func(file="UJNRPFW")
    sql_sqlite3 += "\nUNION ALL\n"
    sql_sqlite3 += func(file="UJNRPF")
    if sort_column:
        if sort_type == "昇順":
            sql_sqlite3 += f"\nORDER BY {sort_column} ASC"
        else:
            sql_sqlite3 += f"\nORDER BY {sort_column} DESC"
    return sql_sqlite3

def create_df_sqlite3(sql: str) -> pd.DataFrame:
    with sqlite3.connect(DATABASE) as conn:
        df = pd.read_sql(sql=sql, con=conn)
    return df