SELECT
    substr('0000' || to_char(TOKCD1), 5, 4)
    ||
    substr('00' || to_char(TOKCD2), 3, 2) as code,
    TOKA1 as kana,
    TOKJ1 as name,
    LESS as less_rate,
    SIMEBI as closing_date,
    TANCD as manager_code,
    KENCD as prefecture_code,
    substr('000' || to_char(YUBIA1), 4, 3)
    || '-' ||
    substr('0000' || to_char(YUBIA2), 3s, 2) as post_code,
    ADLJ1 || ADLJ2 as address,
    TELNO as phone_number,
    SAKUSE as create_date
FROM
    FLIB.TOKMPF
