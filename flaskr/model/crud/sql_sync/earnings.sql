SELECT
    BLK as block_number,
    GYO as block_row,
    SDENNO as shipping_slip_number,
    DYMD as shipping_date,
    DENK as shipping_category,
    substr('000' || to_char(ATU),-2,2) as shipping_campany_code,
    substr('000' || to_char(ATU),-3,1) as fare_category,
    TOKCD as customer_code,
    TOKNM as customer_kana,
    TANCD as customer_manager_code,
    ZATUCD as buyer_code,
    ATUNM as destination_code,
    SOK as destination_kana,
    CODE as goods_sales_code,
    HINNM as goods_sales_kana,
    KKBN as goods_sales_grade,
    SUR as quantity,
    TANKA as unit_price,
    KIN as price,
    TANATA as cost,
    ODER as order_number,
    BIKO as note
FROM
    MOLIB.MUJNRPF
WHERE
    DYMD >= {first_date} AND DYMD <= {last_date}
UNION ALL
SELECT
    BLKNO as block_number,
    GYONO as block_row,
    SYUDEN as shipping_slip_number,
    DENYMD as shipping_date,
    DENKBN as shipping_category,
    to_char(UNSOCD) as shipping_campany_code,
    to_char(ATUKAI) as fare_category,
    TOKCD as customer_code,
    TOKMEK as customer_kana,
    TANCD as customer_manager_code,
    ZATUCD as buyer_code,
    ATUMEI as destination_code,
    SOKMEI as destination_kana,
    SEIBUC as goods_sales_code,
    HINMEI as goods_sales_kana,
    KYUKBN as goods_sales_grade,
    SURYO as quantity,
    TANKA as unit_price,
    SURYO * TANKA as price,
    0 as cost,
    ODER as order_number,
    BIKO as note
FROM
    FLIB1.UJNRPF
WHERE
    DENYMD >= {first_now_month} AND DENYMD <= {last_date}
UNION ALL
SELECT
    BLKNO as block_number,
    GYONO as block_row,
    SYUDEN as shipping_slip_number,
    DENYMD as shipping_date,
    DENKBN as shipping_category,
    to_char(UNSOCD) as shipping_campany_code,
    to_char(ATUKAI) as fare_category,
    TOKCD as customer_code,
    TOKMEK as customer_kana,
    TANCD as customer_manager_code,
    ZATUCD as buyer_code,
    ATUMEI as destination_code,
    SOKMEI as destination_kana,
    SEIBUC as goods_sales_code,
    HINMEI as goods_sales_kana,
    KYUKBN as goods_sales_grade,
    SURYO as quantity,
    TANKA as unit_price,
    SURYO * TANKA as price,
    0 as cost,
    ODER as order_number,
    BIKO as note
FROM
    FLIB1.UJNRPFW
WHERE
    DENYMD >= {first_now_month} AND DENYMD <= {last_date}
