import pymysql
import json

from app.db_connexion import get_db


def get_discussion_history(id_player):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
                SELECT chats
                FROM Ai_chats
                WHERE id_player = %s
                """

        cursor.execute(query, (id_player,))
        chat = cursor.fetchone()

        return chat['chats'] if chat else "[]"

    finally:
        cursor.close()
        conn.close()



def save_discussion_history(id_player, history, id_chat=None):
    conn = get_db()
    cursor = conn.cursor()
    history_json = json.dumps(history)

    title = history[0]['text'][:30] if len(history) > 0 else "New Conversation"

    try:
        if id_chat:
            query = """
                    UPDATE Ai_chats
                    SET
                    chats = %s,
                    title = %s
                    WHERE id_chat = %s
                    """
            cursor.execute(query, (history_json, title, id_chat))
            conn.commit()
        else:
            query = """
                    INSERT INTO Ai_chats (id_player, chats, title)
                    VALUES (%s, %s, %s)
                    """
            cursor.execute(query, (id_player, history_json, title))
            conn.commit()

            return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()


