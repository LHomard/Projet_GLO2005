from datetime import datetime

import pymysql

from app.db_connexion import get_db


def get_deck_by_user_id_logic(user_id):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_deck, deck_name, id_format, date_creation
                FROM Decks
                WHERE id_user = %s
            """, (user_id,))

            decks = cursor.fetchall()

            return [
                {
                    "id": d[0],
                    "name": d[1],
                    "format": d[2],
                    "created_at": d[3].isoformat() if d[3] else None
                }
                for d in decks
            ]
    finally:
        conn.close()


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


def add_card_to_deck_logic(id_deck, id_printing, quantity=1):
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            add_card_to_deck_request = """                
               INSERT INTO Deck_composition (id_deck, id_printing, quantity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity) 
           """
            cursor.execute(add_card_to_deck_request, (id_deck, id_printing, quantity))
            conn.commit()

    except pymysql.err.OperationalError as e:
        return {'error': e.args[1]}

    finally:
        conn.close()


def get_deck_cards_logic(id_deck):
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            get_deck_cards_request = """
                SELECT 
                    cp.id_printing,
                    co.card_name,
                    cp.image_url,
                    cp.price,
                    cp.rarity,
                    cp.artist,
                    dc.quantity,
                    dc.pillar_cost
                FROM Deck_composition dc
                JOIN Card_printing cp ON dc.id_printing = cp.id_printing
                JOIN Card_oracle co ON cp.id_oracle = co.id_oracle
                WHERE dc.id_deck = %s
            """

            cursor.execute(get_deck_cards_request, (id_deck,))

            cards = cursor.fetchall()

            return [
                {
                    "id_printing": c[0],
                    "name": c[1],
                    "image_url": c[2],
                    "price": float(c[3]) if c[3] else None,
                    "rarity": c[4],
                    "artist": c[5],
                    "quantity": c[6],
                    "pillar_cost": c[7],
                }
                for c in cards
            ]

    finally:
        conn.close()


def remove_card_from_deck_logic(id_deck, id_printing):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Récupère la quantité actuelle
            cursor.execute("""
                SELECT quantity FROM Deck_composition
                WHERE id_deck = %s AND id_printing = %s
            """, (id_deck, id_printing))

            result = cursor.fetchone()

            if result is None:
                return {'error': 'Carte introuvable dans ce deck'}

            #If deck's card quantity is greater than 0, decrease its card quantity of 1
            if result[0] <= 1:
                cursor.execute("""
                    DELETE FROM Deck_composition
                    WHERE id_deck = %s AND id_printing = %s
                """, (id_deck, id_printing))
            else:
                cursor.execute("""
                    UPDATE Deck_composition
                    SET quantity = quantity - 1
                    WHERE id_deck = %s AND id_printing = %s
                """, (id_deck, id_printing))

            conn.commit()
    except pymysql.err.OperationalError as e:
        return {'error': e.args[1]}
    finally:
        conn.close()