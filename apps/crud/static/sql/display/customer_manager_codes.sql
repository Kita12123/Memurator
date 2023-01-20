SELECT
    code AS 担当者コード,
    name AS 担当者名
FROM customer_manager_codes
WHERE
    {where}
ORDER BY code ASC
