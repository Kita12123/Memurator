"""
出荷データ用 Module
"""

def Create_SQL_dsp(
    where: str
    ) -> str:
    return  f"""
    SELECT
        伝票日付+19500000 AS 伝票日付,
        ifnull(ET1.名称＊,'') AS 伝票区分名＊,
        ifnull(ET2.名称＊,'') AS 委託区分名＊,
        ifnull(ET4.名称＊,'') AS 扱い区分名＊,
        CASE
            WHEN ifnull(ET6.名称＊,'') <> '' THEN ifnull(ET6.名称＊,'')
            ELSE ifnull(ET5.名称＊,'')
        END AS 運送会社名＊,
        ifnull(ET3.名称＊,'') AS 担当者名＊,
        得意先コード,
        得意先カナ,
        CASE
            WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN 雑コード
            WHEN 得意先コード=333840                         THEN 雑コード
            ELSE ''
        END AS 雑コード,
        CASE
            WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN ifnull(NI2.送荷先カナ＊,'')
            WHEN 得意先コード=333840                         THEN ifnull(NI2.送荷先カナ＊,'')
            ELSE ''
        END AS 雑カナ＊,
        送荷先コード,
        送荷先カナ,
        製品部品コード,
        製品部品カナ,
        級区分,
        CASE
            /* 返品,値引き*/
            WHEN 伝票区分=30 THEN 出荷数*-1
            WHEN 伝票区分=90 THEN 出荷数*-1
            ELSE 出荷数
        END AS 数量,
        単価,
        CASE
            /* 返品,値引き*/
            WHEN 伝票区分=30 THEN 金額*-1
            WHEN 伝票区分=90 THEN 金額*-1
            ELSE 金額
        END AS 金額,
        出荷伝票番号 || 出荷行番号 AS 出荷伝票番号,
        備考
    FROM SYUKAPF
    LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分＊=10 AND ET1.コード＊=伝票区分
    LEFT OUTER JOIN ETCMPF ET2 ON ET2.レコード区分＊=20 AND ET2.コード＊=委託区分
    LEFT OUTER JOIN ETCMPF ET3 ON ET3.レコード区分＊=22 AND ET3.コード＊=担当者コード
    LEFT OUTER JOIN ETCMPF ET4 ON ET4.レコード区分＊=30 AND ET4.コード＊=substr(扱い運送,1,1)
    LEFT OUTER JOIN ETCMPF ET5 ON ET5.レコード区分＊=40 AND ET5.コード＊=substr(扱い運送,2,2)
    LEFT OUTER JOIN ETCMPF ET6 ON ET6.レコード区分＊=40 AND ET6.コード＊=扱い運送
    LEFT OUTER JOIN NIHONPF NI2 ON NI2.送荷先コード＊=雑コード
    WHERE 
{where}
    AND   出荷数<>0
    ORDER BY 伝票日付 ASC
    """

def Create_SQL_download(
    where: str
    ) -> str:
    return  f"""
    SELECT
        伝票日付+19500000 AS 伝票日付,
        伝票区分,
        ifnull(ET1.名称＊,'') AS 伝票区分名＊,
        委託区分,
        ifnull(ET2.名称＊,'') AS 委託区分名＊,
        扱い運送 AS 扱い運送区分,
        ifnull(ET4.名称＊,'') AS 扱い区分名＊,
        CASE
            WHEN ifnull(ET6.名称＊,'') <> '' THEN ifnull(ET6.名称＊,'')
            ELSE ifnull(ET5.名称＊,'')
        END AS 運送会社名＊,
        担当者コード,
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
            WHEN 得意先コード=333840                         THEN 雑コード
            ELSE ''
        END AS 雑コード,
        CASE
            WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN ifnull(NI2.送荷先カナ＊,'')
            WHEN 得意先コード=333840                         THEN ifnull(NI2.送荷先カナ＊,'')
            ELSE ''
        END AS 雑カナ＊,
        CASE
            WHEN 得意先コード>=500000 AND 得意先コード<600000 THEN ifnull(NI2.送荷先名＊,'')
            WHEN 得意先コード=333840                         THEN ifnull(NI2.送荷先名＊,'')
            ELSE ''
        END AS 雑名＊,
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
            WHEN 伝票区分=30 THEN 受注数*-1
            WHEN 伝票区分=90 THEN 受注数*-1
            ELSE 受注数
        END AS 受注数,
        CASE
            /* 返品,値引き*/
            WHEN 伝票区分=30 THEN 出荷数*-1
            WHEN 伝票区分=90 THEN 出荷数*-1
            ELSE 出荷数
        END AS 出荷数,
        ＢＯ区分,
        単価,
        CASE
            /* 返品,値引き*/
            WHEN 伝票区分=30 THEN 金額*-1
            WHEN 伝票区分=90 THEN 金額*-1
            ELSE 金額
        END AS 金額,
        出荷伝票番号,
        備考,
        オーダー番号,
        入力日 || '日' || 入力時 || '時' || 入力分 || '分' AS 入力時間
    FROM SYUKAPF
    LEFT OUTER JOIN ETCMPF ET1 ON ET1.レコード区分＊=10 AND ET1.コード＊=伝票区分
    LEFT OUTER JOIN ETCMPF ET2 ON ET2.レコード区分＊=20 AND ET2.コード＊=委託区分
    LEFT OUTER JOIN ETCMPF ET3 ON ET3.レコード区分＊=22 AND ET3.コード＊=担当者コード
    LEFT OUTER JOIN ETCMPF ET4 ON ET4.レコード区分＊=30 AND ET4.コード＊=substr(扱い運送,1,1)
    LEFT OUTER JOIN ETCMPF ET5 ON ET5.レコード区分＊=40 AND ET5.コード＊=substr(扱い運送,2,2)
    LEFT OUTER JOIN ETCMPF ET6 ON ET6.レコード区分＊=40 AND ET6.コード＊=扱い運送
    LEFT OUTER JOIN NIHONPF NI ON NI.送荷先コード＊=送荷先コード
    LEFT OUTER JOIN NIHONPF NI2 ON NI2.送荷先コード＊=雑コード
    /* 得意先はコードが二つに分かれているからめんどくさい
    LEFT OUTER JOIN TOKMPF TOK ON TOK.得意先コード＊=得意先コード
    */
    WHERE 
{where}
    AND   出荷数<>0
    ORDER BY 伝票日付 ASC
    """