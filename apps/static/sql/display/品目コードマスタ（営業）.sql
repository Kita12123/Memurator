SELECT
    code AS 製品部品コード,
    kana AS 製品部品カナ,
    parts_number AS 部番,
    wight AS 重量,
    unit_price_past AS 旧小売単価,
    unit_price AS 小売単価,
    cost AS 原価,
    CASE abolition_category
        WHEN 2 THEN '廃止'
        WHEN 1 THEN '廃止'
        ELSE        ''
    END AS 廃止区分,
    alternative_code AS 代替部品,
    CASE create_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             create_date + 19500000
    END AS 作成日
FROM 品目コードマスタ（営業）
WHERE
    {where}
ORDER BY code ASC
