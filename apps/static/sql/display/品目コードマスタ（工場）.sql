SELECT
    code AS 品目コード,
    kana AS 品目カナ,
    name AS 品目名,
    specification AS 仕様,
    diagrm AS 図番,
    parts_number AS 部番,
    material_unit_price AS 資材単価,
    processing_unit_price AS 加工単価,
    scan_category AS 検査区分,
    supplier_code AS 手配先コード,
    include_code AS 納入先コード,
    CASE change_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             change_date + 19500000
    END AS 変更日,
    CASE create_date
        WHEN      0 THEN        0
        WHEN 999999 THEN 99999999
        ELSE             create_date + 19500000
    END AS 作成日
FROM 品目マスタ（工場）
WHERE
    {where}
ORDER BY code ASC