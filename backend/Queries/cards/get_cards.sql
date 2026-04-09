SELECT
    co.id_oracle,
    co.name,
    co.type_line,
    cp.image_url,
    GROUP_CONCAT(c.color_symbol ORDER BY c.id_color SEPARATOR '') AS colors
FROM Card_oracle co
JOIN Card_printing cp
    ON co.id_oracle = cp.id_printing
LEFT JOIN Card_colors cc
    ON co.id_oracle = cc.id_oracle
LEFT JOIN Colors c
    ON cc.id_color = c.id_color
GROUP BY
    co.id_oracle,
    co.name,
    co.type_line,
    cp.image_url
ORDER BY co.name
LIMIT %s OFFSET %s;
