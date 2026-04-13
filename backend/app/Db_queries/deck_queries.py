from datetime import datetime

from app.db_connexion import get_db


def get_deck_by_id_logic(deck_id):
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_deck, deck_name, id_format, id_user, date_creation
                FROM Decks
                WHERE id_deck = %s
            """, (deck_id,))

            d = cursor.fetchone()

            if d is None:
                return None

            return {
                "id": d[0],
                "name": d[1],
                "format": d[2],
                "user_id": d[3],
                "created_at": d[4].isoformat() if d[4] else None
            }

    finally:
        conn.close()


def create_deck_logic(deck_name, format_name, id_user_current=1):
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            #Get id_format from format_name
            id_format_request = """ 
                SELECT id_format
                FROM Formats
                WHERE TRIM(format_name) = %s
            """
            cursor.execute(id_format_request, (format_name,))
            result = cursor.fetchone()

            if not result:
                return None

            id_format = result[0]

            #Insert deck
            insert_deck_request = """ 
                INSERT INTO Decks (id_user, id_format, deck_name, date_creation)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_deck_request, (
                id_user_current,
                id_format,
                deck_name,
                datetime.now()
            ))

            conn.commit()

            #Get inserted id
            deck_id = cursor.lastrowid

            return {
                'id_deck': deck_id,
                'deck_name': deck_name,
                'id_format': id_format,
                'id_user': id_user_current,
                'date_creation': datetime.now().isoformat()
            }

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


def delete_deck_logic(deck_id):
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            delete_deck_request = """DELETE FROM Decks WHERE id_deck = %s """

            cursor.execute(delete_deck_request, (deck_id,))
            conn.commit()

        return {'message': 'Deck deleted'}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()