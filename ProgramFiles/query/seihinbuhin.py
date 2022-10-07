"""
製品部品マスタ用 Module
"""

def Create_SQL_dsp(
    where: str="",
    sort_column: str="製品部品コード",
    sort_type: str="昇順"
    ) -> str:
    if where:
        where = "WHERE\n" + where
    sql =  f"""
    SELECT
        製品コード＊ AS 製品部品コード,
        製品カナ＊ AS カナ名,
        送荷先名＊ AS 名称,
        '' AS 部番,
        '' AS 単価,
        作成日＊ AS 作成日
    FROM SEIMPF
    WHERE
        SUBSTR(製品コード＊,-2,2) <> 0
    UNION ALL
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
    sort_column: str="送荷先コード＊",
    sort_type: str="昇順"
    ) -> str:
    if where:
        where = "WHERE\n" + where
    sql =  f"""
    SELECT
        送荷先コード＊ AS 送荷先コード,
        送荷先カナ＊ AS カナ名,
        送荷先名＊ AS 名称,
        SUBSTR('0000' || 郵便番号１＊,-4,4)
            || '-' ||
            SUBSTR('000' || 郵便番号２＊,-3,3)
            AS 郵便番号,
        住所１＊ || 住所２＊ AS 住所,
        電話番号＊ AS 電話番号
    FROM NIHONPF
{where}
    """
    if sort_column:
        if sort_type == "昇順":
            sql += f"\nORDER BY {sort_column} ASC"
        else:
            sql += f"\nORDER BY {sort_column} DESC"
    return sql