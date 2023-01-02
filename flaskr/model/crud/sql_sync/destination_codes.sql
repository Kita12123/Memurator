SELECT
    コード as code,
    日本語１カナ as kana,
    日本語１漢字 as name,
    県コード as prefecture_code,
    to_char(郵便番号１, 'FM000')
    || '-' ||
    to_char(郵便番号２, 'FM0000') as post_code,
    日本語２漢字 || 日本語３漢字 as address,
    電話番号 as phone_number,
    読み as flg
FROM
    FLIB.NIHONPF