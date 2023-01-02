SELECT
    TOKCD1 as customer_code1,
    TOKCD2 as customer_code2,
    TOKA1 as customer_kana,
    TOKJ1 as customer_name,
    LESS as customer_less_rate,
    SIMEBI as closing_date,
    TANCD as customer_manager_code,
    KENCD as prefecture_code,
    YUBIA1 as post_code1,
    YUBIA2 as post_code2,
    ADLJ1 || ADLJ2 as address,
    TELNO as phone_number,
    SAKUSE as create_date
FROM
    FLIB.TOKMPF
