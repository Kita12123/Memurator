SELECT
    code AS 運送会社コード,
    name AS 運送会社名
FROM 運送会社コードマスタ
WHERE
    {where}
ORDER BY code ASC
