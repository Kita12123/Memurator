SELECT
    category AS 伝票区分,
    name AS 伝票区分名
FROM 伝票区分マスタ
WHERE
    {where}
ORDER BY category ASC
