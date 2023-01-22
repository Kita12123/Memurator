SELECT
    code AS 県コード,
    name AS 県名
FROM
    県コードマスタ
WHERE
    {where}
ORDER BY code ASC
