import csv
from datetime import date

from app.Db_queries.login_queries import hash_password

from app.db_connexion import get_db


def import_players_from_csv(csv_file):
    connection = get_db()

    try:
        with connection.cursor() as cursor:
            with open(csv_file, newline='') as file:
                render = csv.DictReader(file)

                for row in render:
                    username = row['username']
                    email = row['email']
                    password = row['password']
                    register_date = row['register_date']

                    hashed_password = hash_password(password)

                    request = """INSERT IGNORE INTO Players (register_date, username, email, password_hash) VALUES ('{}', '{}', '{}', '{}')""".format(
                    register_date, username, email, hashed_password)

                    cursor.execute(request)

        print("All players inserted successfully!")

    finally:
        connection.close()

import_players_from_csv('/app/app/Db_queries/players.csv')