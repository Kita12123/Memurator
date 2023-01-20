SELECT
    category AS 伝票区分,
    name AS 伝票区分名
FROM shipping_categories
WHERE
    {where}
ORDER BY category ASC
