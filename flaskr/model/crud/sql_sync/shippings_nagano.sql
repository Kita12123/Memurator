SELECT
    S04 as shipping_slip_number,
    S05 as shipping_slip_row,
    S08 as shipping_date,
    S09 as shipping_category,
    substr('000' || to_char(S21),-2,2) as shipping_campany_code,
    substr('000' || to_char(S21),-3,1) as fare_category,
    S07 as instruction_date,
    S12 as customer_code,
    S13 as customer_kana,
    S199 as customer_manager_code,
    ZATUCD as buyer_code,
    S20 as destination_code,
    S36 as destination_kana,
    S25 as goods_sales_code,
    S27 as goods_sales_kana,
    S24 as goods_sales_grade,
    S26 as parts_number,
    S28 as order_number,
    S29 as order_quantity,
    S365 as back_order_category,
    S31 as back_order_quantity,
    S30 as shipping_quantity,
    S33 as unit_price,
    S34 as price,
    S35 as note,
    HONJIT as input_day,
    HH as input_hour,
    MM as input_minute
FROM
    FLIBN.SYUKAPF
WHERE
    S08 >= {first_date} AND S08 <= {last_date}
