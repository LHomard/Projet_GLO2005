import csv
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from login_queries import get_connection, hash_password


def import_players_from_csv(csv_file):
    connection = get_connection()

    try:
        with open(csv_file, newline='') as file:
            render = csv.DictReader(file)

            for row in render:
                username = row['username']
                email = row['email']
                password = row['password']

                hashed_password = hash_password(password)

                request = """INSERT IGNORE INTO Players (register_date, username, email, password_hash) VALUES ('{}', '{}', '{}', '{}')""".format(
                date.today(), username, email, hashed_password)

                with connection.cursor() as cursor:
                    cursor.execute(request)

        print("All players insert successfully!")

    finally:
        connection.close()

import_players_from_csv(os.path.join(os.path.dirname(__file__), 'players.csv'))