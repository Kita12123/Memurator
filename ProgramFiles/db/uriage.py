"""
売上データ用 Module
"""

DSP_COLUMNS = [
    "伝票日付",
    "伝票区分",
    "伝票区分名＊",
    "委託区分",
    "委託区分名＊",
    "担当者名＊",
    "得意先コード",
    "得意先カナ",
    "雑コード",
    "雑カナ＊",
    "送荷先コード",
    "送荷先カナ",
    "製品部品コード",
    "製品部品カナ",
    "級区分",
    "数量",
    "単価",
    "金額",
    "備考",
    "出荷伝票番号"
    ]

def Create_SQL_dsp(
    where: str,
    sort_column: str,
    sort_type: str
    ) -> str:
    def func(file: str) -> str:
        return f"""
        SELECT
            伝票日付+19500000 AS 伝票日付,
            伝票区分,
            ifnull(ET1.名称＊,'') AS 伝票区分名＊,
            委託区分,
            ifnull(ET2.名称＊,'') AS 委託区分名＊,
            ifnull(ET3.名称＊,'') AS 担当者名＊,
            得意先コード,
            得意先カナ,
            CASE
                WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN 雑コード
                ELSE ''
            END AS 雑コード,
            CASE
                WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN ifnull(NI2.送荷先カナ＊,'')
                ELSE ''
            END AS 雑カナ＊,
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
            出荷伝票番号,
            備考
        FROM {file}
        LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分＊=10 AND ET1.コード＊=伝票区分
        LEFT OUTER JOIN ETCMPF ET2 ON ET2.レコード区分＊=20 AND ET2.コード＊=委託区分
        LEFT OUTER JOIN ETCMPF ET3 ON ET3.レコード区分＊=22 AND ET3.コード＊=担当者コード
        LEFT OUTER JOIN NIHONPF NI2 ON NI2.送荷先コード＊=雑コード
        WHERE 
{where}
        AND   数量<>0
        """
    sql = (
        func(file="MUJNRPF")
    +   "\nUNION ALL\n"
    +   func(file="UJNRPFW")
    +   "\nUNION ALL\n"
    +   func(file="UJNRPF")
    )
    if sort_column:
        if sort_type == "昇順":
            sql += f"\nORDER BY {sort_column} ASC"
        else:
            sql += f"\nORDER BY {sort_column} DESC"
    return sql

def Create_SQL_download(
    where: str,
    sort_column: str,
    sort_type: str
    ) -> str:
    def func(file: str) -> str:
        return f"""
        SELECT
            伝票日付+19500000 AS 伝票日付,
            伝票区分,
            ifnull(ET1.名称＊,'') AS 伝票区分名＊,
            委託区分,
            ifnull(ET2.名称＊,'') AS 委託区分名＊,
            ifnull(ET3.名称＊,'') AS 担当者名＊,
            得意先コード,
            得意先カナ,
            /*
            ifnull(TOK.得意先名＊,'') AS 得意先名＊,
            TOK.郵便番号１＊ || '-' || TOK.郵便番号２＊ AS 得意先郵便番号＊,
            ifnull(TOK.住所１＊ || TOK.住所２＊,'') AS 得意先住所＊,
            ifnull(TOK.電話番号＊,'') AS 得意先電話番号＊,
            */
            CASE
                WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN 雑コード
                ELSE ''
            END AS 雑コード,
            CASE
                WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN ifnull(NI2.送荷先カナ＊,'')
                ELSE ''
            END AS 雑カナ＊,
            送荷先コード,
            送荷先カナ,
            ifnull(NI.送荷先名＊,'') AS 送荷先名＊,
            SUBSTR('0000' || NI.郵便番号１＊,-4,4)
             || '-' ||
            SUBSTR('000' || NI.郵便番号２＊,-3,3) AS 送荷先郵便番号＊,
            ifnull(NI.住所１＊ || NI.住所２＊,'') AS 送荷先住所＊,
            CASE
                WHEN ifnull(NI.電話番号＊,'') = '' THEN ''
                WHEN ifnull(NI.電話番号＊,'') = ' ' THEN ''
                ELSE ifnull(NI.電話番号＊,'') || ','
            END AS 送荷先電話番号＊,
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
            出荷伝票番号,
            備考,
            オーダー番号
        FROM {file}
        LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分＊=10 AND ET1.コード＊=伝票区分
        LEFT OUTER JOIN ETCMPF ET2 ON ET2.レコード区分＊=20 AND ET2.コード＊=委託区分
        LEFT OUTER JOIN ETCMPF ET3 ON ET3.レコード区分＊=22 AND ET3.コード＊=担当者コード
        LEFT OUTER JOIN NIHONPF NI ON NI.送荷先コード＊=送荷先コード
        LEFT OUTER JOIN NIHONPF NI2 ON NI2.送荷先コード＊=雑コード
        /* 得意先はコードが二つに分かれているからめんどくさい
        LEFT OUTER JOIN TOKMPF TOK ON TOK.得意先コード＊=得意先コード
        */
        WHERE 
{where}
        AND   数量<>0
        """
    sql = (
        func(file="MUJNRPF")
    +   "\nUNION ALL\n"
    +   func(file="UJNRPFW")
    +   "\nUNION ALL\n"
    +   func(file="UJNRPF")
    )
    if sort_column:
        if sort_type == "昇順":
            sql += f"\nORDER BY {sort_column} ASC"
        else:
            sql += f"\nORDER BY {sort_column} DESC"
    return sql