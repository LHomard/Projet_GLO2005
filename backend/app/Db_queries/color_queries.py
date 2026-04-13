from app.db_connexion import get_db


def get_all_colors_logic():
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT color_name FROM Colors")
            formats = cursor.fetchall()

            return [f[0] for f in formats]

    finally:
        conn.close()