import pymysql

from app.db_connexion import get_db
import time

_sets_cache = {"data": None, "time": 0}
CACHE_TTL = 3600

def get_sets_logic():

    if _sets_cache["data"] and (time.time() - _sets_cache["time"]) < CACHE_TTL:
        return _sets_cache["data"]
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
            SELECT
                s.id_set,
                s.set_code,
                s.set_name AS name,
                s.release_date,
                s.icon_url AS icon,
                s.card_count, 
                (
                    SELECT REPLACE(cp.image_url, '/normal/', '/art_crop/')
                    FROM Card_printing cp
                    JOIN Card_oracle co ON cp.id_oracle = co.id_oracle
                    WHERE cp.id_set = s.id_set
                        AND cp.image_url IS NOT NULL
                        AND co.name NOT LIKE 'A-%%'
                        AND co.name NOT LIKE '%%//%%'
                        AND co.type_line NOT LIKE '%%Token%%'
                        AND co.type_line NOT LIKE '%%Emblem%%'
                    LIMIT 1
                ) AS image
            FROM Sets s
            ORDER BY release_date DESC;
        """
        cursor.execute(query)
        sets = cursor.fetchall()

        _sets_cache["data"] = sets
        _sets_cache["time"] = time.time()

    finally:
        cursor.close()
        conn.close()

    return sets