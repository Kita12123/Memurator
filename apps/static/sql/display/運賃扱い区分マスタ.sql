SELECT
    category AS 運賃扱い区分,
    name AS 運賃扱い区分名
FROM 運賃扱い区分マスタ
WHERE
    {where}
ORDER BY category ASC
