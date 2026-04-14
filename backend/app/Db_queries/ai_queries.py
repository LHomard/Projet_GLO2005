

import pymysql
import json

import requests
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


def get_all_discussion_from_history(id_player):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
                SELECT id_chat, title
                FROM Ai_chats
                WHERE id_player = %s
                """
        cursor.execute(query, (id_player,))
        conn.commit()
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_discussion_from_history(id_chat):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
        SELECT chats, title
        FROM Ai_chats
        WHERE id_chat = %s
          AND chats IS NOT NULL
        """
        cursor.execute(query, (id_chat,))
        conn.commit()
        chat = cursor.fetchone()

        if chat:
            chat['chats'] = json.loads(chat['chats'])
        return chat

    finally:
        cursor.close()
        conn.close()


def delete_chat(id_chat):
    conn = get_db()
    cursor = conn.cursor()

    try:
        query = """
        DELETE FROM Ai_chats
        WHERE id_chat = %s
        """
        cursor.execute(query, (id_chat,))
        conn.commit()
        return cursor.rowcount

    finally:
        cursor.close()
        conn.close()

def get_relevant_rules(prompt):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
            SELECT rule_number, text, example 
            FROM rules 
            WHERE text LIKE %s OR keyword LIKE %s OR rule_number LIKE %s
            LIMIT 20
        """
        cursor.execute(query, (prompt, prompt, prompt))
        conn.commit()

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

def get_relevant_rulings_for_card(id_oracle):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = """
            SELECT rulings_uri 
            FROM Card_oracle 
            WHERE id_oracle = %s
            LIMIT 20
        """
        cursor.execute(query, (id_oracle,))
        rulings = cursor.fetchone()

        #REquest the ruling URI and then fetch the rulings on the api
        if not rulings or not rulings[0]:
            return []

        response = requests.get(rulings[0])
        data = response.json()
        #Store each rulinggs of the card
        return data.get("data", [])

    finally:
        cursor.close()
        conn.close()