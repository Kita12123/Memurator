SELECT
    DYMD as purchase_date,
    DKBN as purchase_category,
    HOYOKB as supplement_category,
    SIR as supplier_code,
    SIRNM as supplier_kana,
    BUCD as goods_factory_code,
    BUHNM as goods_factory_kana,
    KIS as parent_goods_code,
    KISNM as parent_goods_kana,
    SUR as quantity,
    TANKA + TANKA2 as unit_price,
    KIN + KIN2 as price
FROM
    MOLIB.NSFILEP
WHERE
    DYMD >= {first_date} AND DYMD <= {last_date}
UNION ALL
SELECT
    日付 as purchase_date,
    データ区分 as purchase_category,
    区分 as supplement_category,
    仕入先コード as supplier_code,
    '' as supplier_kana,
    品目コード as goods_factory_code,
    品名 as goods_factory_kana,
    0 as parent_goods_code,
    '' as parent_goods_kana,
    数量 as quantity,
    単価１ + 単価２ as unit_price,
    金額１ + 金額２ as price
FROM
    FLIB.RIPPGA
WHERE
    日付 >= {first_now_month} AND 日付 <= {last_date}
