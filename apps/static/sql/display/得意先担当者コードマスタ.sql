SELECT
    code AS 担当者コード,
    name AS 担当者名
FROM 得意先担当者コードマスタ
WHERE
    {where}
ORDER BY code ASC
