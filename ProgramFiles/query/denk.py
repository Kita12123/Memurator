"""
伝票区分マスタ用 Module
"""

def Create_SQL_dsp(
    where: str="",
    sort_column: str="コード＊",
    sort_type: str="昇順"
    ) -> str:
    if where:
        where = "AND " + where
    sql =  f"""
    SELECT
        コード＊ || '' AS 伝票区分,
        名称＊ AS 名称,
        カナ＊ AS カナ名
    FROM ETCMPF
    WHERE
        レコード区分＊ = 10
{where}
    """
    if sort_column:
        if sort_type == "昇順":
            sql += f"\nORDER BY {sort_column} ASC"
        else:
            sql += f"\nORDER BY {sort_column} DESC"
    return sql

def Create_SQL_download(
    where: str="",
    sort_column: str="コード＊",
    sort_type: str="昇順"
    ) -> str:
    if where:
        where = "AND " + where
    sql =  f"""
    SELECT
        コード＊ AS 伝票区分,
        名称＊ AS 名称,
        カナ＊ AS カナ名
    FROM ETCMPF
    WHERE
        レコード区分＊ = 10
{where}
    """
    if sort_column:
        if sort_type == "昇順":
            sql += f"\nORDER BY {sort_column} ASC"
        else:
            sql += f"\nORDER BY {sort_column} DESC"
    return sql