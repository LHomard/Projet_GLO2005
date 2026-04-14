from app.db_connexion import get_db


def get_all_colors_logic():
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT color_name, color_symbol FROM Colors")
            colors = cursor.fetchall()
            return [{'name': c[0], 'symbol': c[1]} for c in colors]

    finally:
        conn.close()