SELECT
    s.id_set
    s.set_code,
    s.set_name,
    s.release_date,
    s.icon_url
FROM Sets s
ORDER BY release_date DESC;