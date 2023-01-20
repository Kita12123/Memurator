SELECT
    CASE purchase_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             purchase_date+19500000
    END AS purchase_date,
    supplier_code AS 仕入先コード,
    supplier_kana AS 仕入先カナ,
    sc.name AS 仕入先名,
    CASE supplement_category
        WHEN 'H' THEN '補用'
        WHEN 'P' THEN '単発'
        WHEN 'T' THEN '単発'
        ELSE          ''
    END AS 発注区分,
    goods_factory_code AS 品目コード,
    goods_factory_kana AS 品目カナ,
    gfc.specification AS 品目仕様＊,
    gfc.diagram AS 品目図番＊,
    quantity AS 数量,
    unit_price AS 単価,
    price AS 金額,
    parent_goods_code AS 機種コード,
    parent_goods_kana AS 機種カナ,
    purchase_slip_number AS 伝票番号
FROM purchases
LEFT OUTER JOIN goods_factory_codes gfc ON gfc.code=goods_factory_code
LEFT OUTER JOIN supplier_codes sc ON sc.code=supplier_code
WHERE
    {where}
ORDER BY purchase_date supplier_code ASC
