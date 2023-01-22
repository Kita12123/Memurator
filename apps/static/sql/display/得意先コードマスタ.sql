SELECT
    code AS 得意先コード,
    kana AS 得意先カナ,
    name AS 得意先名,
    manager_code AS 担当者コード,
    ifnull(cmc.name,'') AS 担当者名,
    post_code AS 郵便番号,
    address AS 住所,
    phone_number AS 電話番号,
    closing_date AS 締め日,
    less_rate AS ＬＥＳＳ率,
    CASE create_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             create_date + 19500000
    END AS 作成日
FROM 得意先コードマスタ
LEFT OUTER JOIN customer_manager_codes cmc ON cmc.code=manager_code
WHERE
    {where}
ORDER BY code ASC
