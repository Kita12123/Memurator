"""
製品部品マスタ用 Module
"""

def Create_SQL_dsp(
    where: str=""
    ) -> str:
    if where:
        where = "WHERE\n" + where
    sql =  f"""
    SELECT
        製品コード＊ || '' AS 製品部品コード,
        製品カナ＊ AS カナ名,
        'ｾｲﾋﾝ' AS 部番,
        '' AS 単価,
        '' AS 原価,
        CASE
            WHEN 廃止区分＊ = 2 THEN '廃止機種'
            WHEN 廃止区分＊ = 1 THEN '廃止コード'
            ELSE ''
        END AS 廃止区分,
        作成日＊ + 19500000 AS 作成日
    FROM SEIMPF
{where}
    UNION ALL
    SELECT
        部品コード＊ || '' AS 製品部品コード,
        部品カナ＊ AS カナ名,
        部番＊ AS 部番,
        単価＊ AS 単価,
        原価＊ AS 原価,
        '' AS 廃止区分,
        作成日＊ + 19500000 AS 作成日
    FROM BUHMPF
{where}
    ORDER BY 製品部品コード ASC
    """
    return sql

def Create_SQL_download(
    where: str=""
    ) -> str:
    if where:
        where = "WHERE\n" + where
    sql =  f"""
    SELECT
        製品コード＊ AS 製品部品コード,
        製品カナ＊ AS カナ名,
        'ｾｲﾋﾝ' AS 部番,
        '' AS 単価,
        '' AS 原価,
        CASE
            WHEN 廃止区分＊ = 2 THEN '廃止機種'
            WHEN 廃止区分＊ = 1 THEN '廃止コード'
            ELSE ''
        END AS 廃止区分,
        作成日＊ + 19500000 AS 作成日
    FROM SEIMPF
{where}
    UNION ALL
    SELECT
        部品コード＊ || '' AS 製品部品コード,
        部品カナ＊ AS カナ名,
        部番＊ AS 部番,
        単価＊ AS 単価,
        原価＊ AS 原価,
        '' AS 廃止区分,
        作成日＊ + 19500000 AS 作成日
    FROM BUHMPF
{where}
    ORDER BY 製品部品コード ASC
    """
    return sql