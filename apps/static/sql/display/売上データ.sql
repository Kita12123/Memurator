SELECT
    CASE shipping_date
        WHEN 0 THEN 0
        WHEN 999999 THEN 99999999
        ELSE shipping_date+19500000
    END AS 伝票日付,
    ifnull(伝票区分マスタ.name, '') AS 伝票区分名＊,
    ifnull(委託区分マスタ.name, '') AS 委託区分名＊,
    ifnull(運賃扱い区分マスタ.name, '') AS 扱い区分名＊,
    ifnull(運送会社コードマスタ.name, '') AS 運送会社名＊,
    ifnull(得意先担当者コードマスタ.name, '') AS 担当者名＊,
    customer_code AS 得意先コード,
    customer_kana AS 得意先カナ,
    CASE
        WHEN ( customer_code>=500000 AND customer_code< 600000 )
        OR   ( customer_code>=333800 AND customer_code<=333899 ) THEN buyer_code
        ELSE ''
    END AS 雑コード,
    CASE
        WHEN ( customer_code>=500000 AND customer_code< 600000 )
        OR   ( customer_code>=333800 AND customer_code<=333899 ) THEN 送荷先コードマスタ.kana
        ELSE ''
    END AS 雑カナ＊,
    destination_code AS 送荷先コード,
    destination_kana AS 送荷先カナ,
    goods_sales_code AS 製品部品コード,
    goods_sales_kana AS 製品部品カナ,
    goods_sales_grade AS 級区分,
    CASE shipping_category
        /* 返品,値引き*/
        WHEN 30 OR 90 THEN quantity*-1
        ELSE quantity
    END AS 数量,
    unit_price AS 単価,
    CASE shipping_category
        /* 返品,値引き*/
        WHEN 30 OR 90 THEN quantity * unit_price * -1
        ELSE quantity * unit_price
    END AS 金額,
    shipping_slip_number AS 出荷伝票番号,
    note AS 備考
FROM 売上データ
LEFT OUTER JOIN 伝票区分マスタ ON 伝票区分マスタ.category=shipping_category
LEFT OUTER JOIN 委託区分マスタ ON 委託区分マスタ.category=consign_category
LEFT OUTER JOIN 得意先担当者コードマスタ ON 得意先担当者コードマスタ.code=customer_manager_code
LEFT OUTER JOIN 運送会社コードマスタ ON 運送会社コードマスタ.code=shipping_campany_code
LEFT OUTER JOIN 運賃扱い区分マスタ ON 運賃扱い区分マスタ.category=fare_category
LEFT OUTER JOIN 送荷先コードマスタ ON 送荷先コードマスタ.code=destination_code
WHERE 
    {where}
AND   quantity<>0
ORDER BY shipping_date, customer_code ASC
