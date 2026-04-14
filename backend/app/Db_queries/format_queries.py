from app.db_connexion import get_db


def get_all_formats_logic():
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT format_name FROM Formats")
            formats = cursor.fetchall()

            return [f[0] for f in formats]

    finally:
        conn.close()