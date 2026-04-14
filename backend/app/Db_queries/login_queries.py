from passlib.hash import sha256_crypt
from datetime import date
from flask_login import UserMixin

from app.db_connexion import get_db

#Classe user utilisé pour le log in de flask
class User(UserMixin):
    def __init__(self, id_player, username, email):
        self.id = id_player
        self.username = username
        self.email = email


def hash_password(password):
    return sha256_crypt.hash(password)

def verify_password(plain_password, hashed_password):
    return sha256_crypt.verify(plain_password, hashed_password)

def insert_user(username, email, age, password, first_name, last_name, gender):
    hashed_password = hash_password(password)
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Players (register_date, username, email, age, password_hash, first_name, last_name, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (date.today(), username, email, age, hashed_password, first_name, last_name, gender)
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
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_player, username, email FROM Players WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            if result is None:
                return None
            return User(result[0], result[1], result[2])
    finally:
        connection.close()

def get_user_by_id(user_id):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_player, username, email FROM Players WHERE id_player = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            if result is None:
                return None
            return User(result[0], result[1], result[2])
    finally:
        connection.close()