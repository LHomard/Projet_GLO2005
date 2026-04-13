from passlib.hash import sha256_crypt
from datetime import date

from app.db_connexion import get_db


def hash_password(password):
    return sha256_crypt.hash(password)

def verify_password(plain_password, hashed_password):
    return sha256_crypt.verify(plain_password, hashed_password)

def insert_user(username, email, password):
    hashed_password = hash_password(password)
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            request = """INSERT INTO Players (register_date, username, email, password_hash) VALUES ('{}', '{}', '{}', '{}')""".format(
                date.today(), username, email, hashed_password)
            cursor.execute(request)
    finally:
        connection.close()

def check_user_password(email, password):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            request = """SELECT id_player, username, email, password_hash FROM Players WHERE email = '{}'""".format(email)
            cursor.execute(request)
            result = cursor.fetchone()

            user_id, username, email, hashed_password = result
            if verify_password(password, hashed_password):
                return {'id': user_id,
                        'username': username,
                        'email': email,
                        }
            else:
                return None
    finally:
        connection.close()

