"""
雑マスタ用 Module
"""

def Create_SQL_dsp(
    where: str=""
    ) -> str:
    if where:
        where = "WHERE\n" + where
    sql =  f"""
    SELECT
        送荷先コード＊ || '' AS 雑コード,
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
    ORDER BY 送荷先コード＊ ASC
    """
    return sql

def Create_SQL_download(
    where: str=""
    ) -> str:
    if where:
        where = "WHERE\n" + where
    sql =  f"""
    SELECT
        送荷先コード＊ AS 雑コード,
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
    ORDER BY 送荷先コード＊ ASC
    """
    return sql