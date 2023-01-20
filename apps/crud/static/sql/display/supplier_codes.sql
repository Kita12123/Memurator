SELECT
    code AS 仕入先コード,
    name AS 仕入先名
FROM supplier_codes
WHERE
    {where}
ORDER BY code ASC
