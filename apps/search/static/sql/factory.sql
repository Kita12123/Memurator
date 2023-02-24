SELECT
    CASE T.purchase_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             T.purchase_date+19500000
    END AS 伝票日付,
    T.supplier_code AS 仕入先コード,
    T.supplier_kana AS 仕入先カナ,
    仕入.name AS 仕入先名,
    CASE T.supplement_category
        WHEN 'H' THEN '補用'
        WHEN 'P' THEN '単発'
        WHEN 'T' THEN '単発'
        ELSE          ''
    END AS 発注区分,
    T.goods_factory_code AS 品目コード,
    T.goods_factory_kana AS 品目カナ,
    品目.name AS 品目名,
    品目.specification AS 品目仕様,
    品目.diagram AS 品目図番,
    T.quantity AS 数量,
    T.unit_price AS 単価,
    T.price AS 金額,
    T.parent_goods_code AS 機種コード,
    T.parent_goods_kana AS 機種カナ
FROM 仕入れデータ T
LEFT OUTER JOIN 品目コードマスタ（工場） 品目 ON 品目.code=T.goods_factory_code
LEFT OUTER JOIN 仕入先コードマスタ 仕入 ON 仕入.code=T.supplier_code
WHERE
    {where}
ORDER BY T.purchase_date, T.supplier_code ASC
