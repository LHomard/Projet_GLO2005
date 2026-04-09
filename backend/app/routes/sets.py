from app.db_connexion import get_db, load_sql
import time

_sets_cache = {"data": None, "time": 0}
CACHE_TTL = 3600

def get_sets_logic():

    if _sets_cache["data"] and (time.time() - _sets_cache["time"]) < CACHE_TTL:
        return _sets_cache["data"]
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        query = ("Queries/Sets/get_sets.sql")
        cursor.execute(query)
        sets = cursor.fetchall()

        _sets_cache["data"] = sets
        _sets_cache["time"] = time.time()

    finally:
        cursor.close()
        conn.close()

    return sets
