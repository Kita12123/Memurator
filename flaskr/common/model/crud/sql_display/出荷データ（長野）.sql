SELECT
    CASE shipping_date
        WHEN 0 THEN 0
        WHEN 999999 THEN 99999999
        ELSE shipping_date+19500000
    END AS 伝票日付,
    ifnull(shipping_categories.name, '') AS 伝票区分名＊,
    ifnull(consign_categories.name, '') AS 委託区分名＊,
    ifnull(fare_categories.name, '') AS 扱い区分名＊,
    ifnull(shipping_campany_codes.name, '') AS 運送会社名＊,
    ifnull(customer_manager_codes.name, '') AS 担当者名＊,
    customer_code AS 得意先コード,
    customer_kana AS 得意先カナ,
    CASE
        WHEN ( customer_code>=500000 AND customer_code< 600000 )
        OR   ( customer_code>=333800 AND customer_code<=333899 ) THEN buyer_code
        ELSE ''
    END AS 雑コード,
    CASE
        WHEN ( customer_code>=500000 AND customer_code< 600000 )
        OR   ( customer_code>=333800 AND customer_code<=333899 ) THEN destination_codes.kana
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
FROM shippings_nagano
LEFT OUTER JOIN shipping_categories ON shipping_categories.category=shipping_category
LEFT OUTER JOIN consign_categories ON consign_categories.category=consign_category
LEFT OUTER JOIN customer_manager_codes ON customer_manager_codes.code=customer_manager_code
LEFT OUTER JOIN shipping_campany_codes ON shipping_campany_codes.code=shipping_campany_code
LEFT OUTER JOIN fare_categories ON fare_categories.category=fare_category
LEFT OUTER JOIN destination_codes ON destination_codes.code=destination_code
WHERE 
    {where}
AND   quantity<>0
