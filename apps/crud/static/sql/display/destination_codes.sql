SELECT
    code AS 送荷先コード,
    kana AS 送荷先カナ,
    name AS 送荷先名,
    post_code AS 郵便番号,
    address AS 住所,
    phone_number AS 電話番号,
    flg AS 社員フラグ
FROM destination_codes
WHERE
    {where}
ORDER BY code ASC
