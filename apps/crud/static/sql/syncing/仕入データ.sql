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
    TANKA as unit_price1,
    TANKA2 as unit_price2,
    KIN as price1,
    KIN2 as price2,
    KCODE1 as payment_code1,
    KCODE2 as payment_code2
FROM
    MOLIB.NSFILEP
WHERE
    DYMD >= {first_date} AND DYMD <= {last_date}
