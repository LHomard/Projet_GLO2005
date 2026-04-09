import os
import pymysql.cursors
from passlib.hash import sha256_crypt
from datetime import date


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        autocommit=True,
    )

def hash_password(password):
    return sha256_crypt.hash(password)

def verify_password(plain_password, hashed_password):
    return sha256_crypt.verify(plain_password, hashed_password)

def insert_user(username, email, password):
    hashed_password = hash_password(password)
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            request = """INSERT INTO User (date_inscription, username, email, password) VALUES ('{}', '{}', '{}', '{}')""".format(
                date.today(), username, email, hashed_password)
            cursor.execute(request)
    finally:
        connection.close()

def check_user_password(email, password):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            request = """SELECT password FROM User WHERE email = '{}'""".format(email)
            cursor.execute(request)
            result = cursor.fetchone()

            if result is None:
                return False

            hashed_password = result[0]
            return verify_password(password, hashed_password)
    finally:
        connection.close()

# Ajout d'un test user
if __name__ == "__main__":
    insert_user('username', 'test@email.com', 'password')
