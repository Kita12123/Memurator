SELECT
    SE.機種コード as code,
    SE.製品名 as kana,
    '' as parts_number,
    SE.重量㎏ as wight,
    SE.１級売単価 as unit_price,
    SE.２級売単価 as unit_price_grade2,
    0 as unit_price_past,
    SE.１級原価 as cost,
    SE.２級原価 as cost_grade2,
    SE.重点品目区分 as abolition_category,
    0 as alternative_code,
    SE.作成日 as create_date
FROM
    FLIB.SEIMPF SE
UNION ALL
SELECT
    BU.RKEY as code,
    BU.NAME as kana,
    BU.BAN as parts_number,
    BU.JURYO as wight,
    BU.TANK1 as unit_price,
    0 as unit_price_grade2,
    BU.TANKS as unit_price_past,
    BU.TANK2 as cost,
    0 as cost_grade2,
    to_char(BU.HAISIF) as abolition_category,
    BU.DAIC as alternative_code,
    BU.CRTYMD as create_date
FROM
    FLIB.BUHMPF BU
