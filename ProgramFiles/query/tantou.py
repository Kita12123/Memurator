"""
担当者マスタ用 Module
"""

def Create_SQL_dsp(
    where: str=""
    ) -> str:
    if where:
        where = "AND " + where
    sql =  f"""
    SELECT
        コード＊ || '' AS 担当者コード,
        名称＊ AS 名称,
        カナ＊ AS カナ名
    FROM ETCMPF
    WHERE
        レコード区分＊ = 22
{where}
    ORDER BY コード＊ ASC
    """
    return sql

def Create_SQL_download(
    where: str=""
    ) -> str:
    if where:
        where = "AND " + where
    sql =  f"""
    SELECT
        コード＊ AS 担当者コード,
        名称＊ AS 名称,
        カナ＊ AS カナ名
    FROM ETCMPF
    WHERE
        レコード区分＊ = 22
{where}
    ORDER BY コード＊ ASC
    """
    return sql