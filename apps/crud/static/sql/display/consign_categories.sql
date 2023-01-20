SELECT
    category AS 委託区分,
    name AS 委託区分名
FROM consign_categories
WHERE
    {where}
ORDER BY category ASC
