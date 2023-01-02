SELECT
    ET.CODE as consign_category,
    ET.NAME as consign_name
FROM
    FLIB.ETCMPF ET
WHERE
    ET.RKBN = 20
