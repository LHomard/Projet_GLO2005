import os
import pymysql.cursors
import csv
from passlib.hash import sha256_crypt
from datetime import date
from app.db_connexion import get_db


def hash_password(password):
    return sha256_crypt.hash(password)

def verify_password(plain_password, hashed_password):
    return sha256_crypt.verify(plain_password, hashed_password)

def insert_user(username, email, age, password):
    hashed_password = hash_password(password)
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Players (register_date, username, email, age, password_hash) VALUES (%s, %s, %s, %s, %s)",
                (date.today(), username, email, age, hashed_password)
            )
            connection.commit()
    finally:
        connection.close()

def check_user_password(email, password):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT password_hash FROM Players WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()

            if result is None:
                return False

            return verify_password(password, result[0])
    finally:
        connection.close()


def get_user_by_email(email):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id_player, email, username FROM Players WHERE email = %s",
            (email,)
        )
        row = cur.fetchone()

        if row is None:
            return None

        return {
            'id_player': row[0],
            'email': row[1],
            'username': row[2]
        }

    finally:
        cur.close()
        conn.close()


def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id_player, email, username FROM Players WHERE id_player = %s",
            (user_id,)
        )
        row = cur.fetchone()

        if row is None:
            return None

        return {
            'id_player': row[0],
            'email': row[1],
            'username': row[2]
        }

    finally:
        cur.close()
        conn.close()