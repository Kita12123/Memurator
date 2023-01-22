SELECT
    category AS 委託区分,
    name AS 委託区分名
FROM 委託区分マスタ
WHERE
    {where}
ORDER BY category ASC
