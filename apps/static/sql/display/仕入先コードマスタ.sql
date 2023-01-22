SELECT
    code AS 仕入先コード,
    name AS 仕入先名
FROM 仕入先コードマスタ
WHERE
    {where}
ORDER BY code ASC
