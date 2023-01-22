SELECT
    T.code AS 得意先コード,
    T.kana AS 得意先カナ,
    T.name AS 得意先名,
    T.manager_code AS 担当者コード,
    ifnull(担当.name,'') AS 担当者名,
    T.post_code AS 郵便番号,
    T.address AS 住所,
    T.phone_number AS 電話番号,
    T.closing_date AS 締め日,
    T.less_rate AS ＬＥＳＳ率,
    CASE T.create_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             T.create_date + 19500000
    END AS 作成日
FROM 得意先コードマスタ AS T
LEFT OUTER JOIN 得意先担当者コードマスタ 担当 ON 担当.code=T.manager_code
WHERE
    {where}
ORDER BY T.code ASC
