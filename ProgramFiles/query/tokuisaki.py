"""
得意先マスタ用 Module
"""

def Create_SQL_dsp(
    where: str="",
    sort_column: str="得意先コード１＊, 得意先コード２＊",
    sort_type: str="昇順"
    ) -> str:
    if where == "":
        where = "得意先コード２＊<>0"
    else:
        where += " AND 得意先コード２＊<>0"
    sql =  f"""
    SELECT
        得意先コード１＊
            || SUBSTR('000' || 得意先コード２＊,-2,2)
            AS 得意先コード,
        得意先カナ＊ AS カナ名,
        得意先名＊ AS 名称,
        担当者コード＊ AS 担当者コード,
        ifnull(ET1.名称＊,'') AS 担当者名,
        SUBSTR('0000' || 郵便番号１＊,-4,4)
            || '-' ||
            SUBSTR('000' || 郵便番号２＊,-3,3)
            AS 郵便番号,
        住所１＊ || 住所２＊ AS 住所,
        電話番号＊ AS 電話番号,
        締め日＊ AS 締め日,
        ＬＥＳＳ率＊ AS ＬＥＳＳ率,
        作成日＊ + 19500000 AS 作成日
    FROM TOKMPF
    LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分＊=22 AND ET1.コード＊=担当者コード＊
    WHERE 
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
    sort_column: str="得意先コード１＊, 得意先コード２＊",
    sort_type: str="昇順"
    ) -> str:
    if where == "":
        where = "得意先コード２＊<>0"
    else:
        where += " AND 得意先コード２＊<>0"
    sql =  f"""
    SELECT
        得意先コード１＊
            || SUBSTR('000' || 得意先コード２＊,-2,2)
            AS 得意先コード,
        得意先カナ＊ AS カナ名,
        得意先名＊ AS 名称,
        担当者コード＊ AS 担当者コード,
        ifnull(ET1.名称＊,'') AS 担当者名,
        SUBSTR('0000' || 郵便番号１＊,-4,4)
            || '-' ||
            SUBSTR('000' || 郵便番号２＊,-3,3)
            AS 郵便番号,
        住所１＊ || 住所２＊ AS 住所,
        電話番号＊ AS 電話番号,
        締め日＊ AS 締め日,
        ＬＥＳＳ率＊ AS ＬＥＳＳ率,
        作成日＊ + 19500000 AS 作成日
    FROM TOKMPF
    LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分＊=22 AND ET1.コード＊=担当者コード＊
    WHERE 
{where}
    """
    if sort_column:
        if sort_type == "昇順":
            sql += f"\nORDER BY {sort_column} ASC"
        else:
            sql += f"\nORDER BY {sort_column} DESC"
    return sql