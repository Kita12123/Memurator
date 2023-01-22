SELECT
    DBCTRL as code,
    HINMEI as kana,
    HSMALL as category,
    SIYOU as specification,
    ZUBAN as diagram,
    BUBAN as parts_number,
    TEHAI as supplier_code,
    NOUNYU as include_code,
    ASHI as material_unit_price,
    AKAK as processing_unit_price,
    KENKBN as scan_category,
    UPDYMD as change_date,
    CRTYMD as create_date
FROM
    FLIB.PMDBPF