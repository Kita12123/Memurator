SELECT
    CASE purchase_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             purchase_date+19500000
    END AS purchase_date,
    supplier_code AS 仕入先コード,
    supplier_kana AS 仕入先カナ,
    仕入.name AS 仕入先名,
    CASE supplement_category
        WHEN 'H' THEN '補用'
        WHEN 'P' THEN '単発'
        WHEN 'T' THEN '単発'
        ELSE          ''
    END AS 発注区分,
    goods_factory_code AS 品目コード,
    goods_factory_kana AS 品目カナ,
    品目.specification AS 品目仕様＊,
    品目.diagram AS 品目図番＊,
    quantity AS 数量,
    unit_price AS 単価,
    price AS 金額,
    parent_goods_code AS 機種コード,
    parent_goods_kana AS 機種カナ,
    purchase_slip_number AS 伝票番号
FROM 仕入れデータ
LEFT OUTER JOIN 品目コードマスタ（工場） 品目 ON 品目.code=goods_factory_code
LEFT OUTER JOIN 仕入先コードマスタ 仕入 ON 仕入.code=supplier_code
WHERE
    {where}
ORDER BY purchase_date supplier_code ASC
