SELECT
    ltrim(rtrim(to_char(TOKCD1, '0000'))
    || ltrim(to_char(TOKCD2, '00'))) as customer_code,
    TOKA1 as kana,
    TOKJ1 as name,
    LESS as less_rate,
    SIMEBI as closing_date,
    TANCD as customer_manager_code,
    KENCD as prefecture_code,
    ltrim(rtrim(to_char(YUBIA1, '0000'))
    || '-'
    || ltrim(to_char(YUBIA2, '000'))) as post_code,
    ADLJ1 || ADLJ2 as address,
    TELNO as phone_number,
    SAKUSE as create_date
FROM
    FLIB.TOKMPF
