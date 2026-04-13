import os
import time
from datetime import date

import ijson
import pymysql
import requests
from dotenv import load_dotenv


load_dotenv()

print("HOST =", os.getenv("DB_HOST"))
print("PORT =", os.getenv("DB_PORT"))
print("USER =", os.getenv("DB_USER"))
print("PASSWORD =", os.getenv("DB_PASSWORD"))
print("DB =", os.getenv("DB_NAME"))


while True:
    try:
        conn = pymysql.connect(
            host="db",
            user="user",
            password="1234",
            database="MGT_db",
            port=3306
        )
        print("Connected to MySQL!")
        conn.close()
        break
    except pymysql.err.OperationalError:
        print("MySQL not ready, retrying in 3 seconds...")
        time.sleep(3)


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        port=int(os.getenv("DB_PORT")),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def fetch_scryfall_stream(data_type):
    print(f"Streaming Scryfall data ({data_type})...")

    bulk_meta = requests.get("https://api.scryfall.com/bulk-data")
    bulk_meta.raise_for_status()
    bulk_data = bulk_meta.json()

    download_url = next(
        d["download_uri"]
        for d in bulk_data["data"]
        if d["type"] == data_type
    )

    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    response.raw.decode_content = True

    return ijson.items(response.raw, "item")


def populate_card_oracle(cards):
    print("Populating Card_oracle table...")

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Card_oracle")
            if cursor.fetchone()[0] > 0:
                print("Table Card_oracle already has data!")
                return

            sql = """
                INSERT INTO Card_oracle
                (name, mana_cost, cmc, oracle_text, power, toughness, type_line)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            batch = []
            batch_size = 1000
            inserted = 0

            for card in cards:
                batch.append((
                    card.get("name"),
                    card.get("mana_cost"),
                    card.get("cmc", 0),
                    card.get("oracle_text"),
                    card.get("power"),
                    card.get("toughness"),
                    card.get("type_line")
                ))

                if len(batch) >= batch_size:
                    cursor.executemany(sql, batch)
                    connection.commit()
                    inserted += len(batch)
                    batch.clear()

            if batch:
                cursor.executemany(sql, batch)
                connection.commit()
                inserted += len(batch)

            print(f"Table Card_oracle populated! Inserted {inserted} rows.")
    finally:
        connection.close()


def populate_sets():
    print("Retrieving sets from Scryfall...")
    response = requests.get("https://api.scryfall.com/sets")
    response.raise_for_status()
    sets_data = response.json().get("data", [])

    to_insert = [
        (
            s.get("code", "").upper(),
            s.get("name"),
            s.get("released_at"),
            s.get("icon_svg_uri"),
            s.get("card_count")
        )
        for s in sets_data
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Sets")
            if cursor.fetchone()[0] == 0:
                print(f"Inserting {len(to_insert)} sets...")
                sql = """
                    INSERT INTO Sets
                    (set_code, set_name, release_date, icon_url, card_count)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.executemany(sql, to_insert)
                conn.commit()
                print("Table Sets populated!")
            else:
                print("Table Sets already has data!")
    finally:
        conn.close()


def populate_card_printing(cards):
    print("Populating Card_printing table...")

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Card_printing")
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"Card_printing already populated ({count} rows), skipping...")
                return

            cursor.execute("SELECT id_oracle, name FROM Card_oracle")
            oracle_map = {name: id_o for id_o, name in cursor.fetchall()}

            cursor.execute("SELECT id_set, set_code FROM Sets")
            set_map = {code.upper(): id_s for id_s, code in cursor.fetchall()}

            sql = """
                INSERT INTO Card_printing
                (id_oracle, id_set, rarity, artist, image_url, price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            batch = []
            batch_size = 1000
            inserted = 0

            for c in cards:
                name = c.get("name")
                set_code = c.get("set", "").upper()

                if name not in oracle_map or set_code not in set_map:
                    continue

                batch.append((
                    oracle_map[name],
                    set_map[set_code],
                    c.get("rarity"),
                    c.get("artist"),
                    c.get("image_uris", {}).get("normal"),
                    c.get("prices", {}).get("usd")
                ))

                if len(batch) >= batch_size:
                    cursor.executemany(sql, batch)
                    connection.commit()
                    inserted += len(batch)
                    batch.clear()

            if batch:
                cursor.executemany(sql, batch)
                connection.commit()
                inserted += len(batch)

            print(f"Inserted {inserted} rows into Card_printing.")
    finally:
        connection.close()


def populate_colors():
    print("Populating Colors table...")

    colors = [
        ("White", "W"),
        ("Blue", "U"),
        ("Black", "B"),
        ("Red", "R"),
        ("Green", "G"),
        ("Colorless", "C"),
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Colors")
            if cursor.fetchone()[0] == 0:
                sql = "INSERT INTO Colors (color_name, color_symbol) VALUES (%s, %s)"
                cursor.executemany(sql, colors)
                conn.commit()
                print("Table Colors populated!")
            else:
                print("Table Colors already has data!")
    finally:
        conn.close()


def populate_card_colors(cards):
    print("Populating Card_colors table...")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_oracle, name FROM Card_oracle")
            oracle_map = {name: id_o for id_o, name in cursor.fetchall()}

            cursor.execute("SELECT id_color, color_symbol FROM Colors")
            color_map = {symbol: id_c for id_c, symbol in cursor.fetchall()}

            sql = "INSERT IGNORE INTO Card_colors (id_oracle, id_color) VALUES (%s, %s)"

            batch = []
            batch_size = 1000
            inserted = 0

            for c in cards:
                card_name = c.get("name")
                scryfall_colors = c.get("colors", [])

                if not scryfall_colors:
                    scryfall_colors = ["C"]

                if card_name in oracle_map:
                    id_oracle = oracle_map[card_name]
                    for symbol in scryfall_colors:
                        if symbol in color_map:
                            batch.append((id_oracle, color_map[symbol]))

                            if len(batch) >= batch_size:
                                cursor.executemany(sql, batch)
                                conn.commit()
                                inserted += len(batch)
                                batch.clear()

            if batch:
                cursor.executemany(sql, batch)
                conn.commit()
                inserted += len(batch)

            print(f"Table Card_colors populated! Inserted {inserted} rows.")
    finally:
        conn.close()


def populate_formats(cards):
    print("Populating Formats table...")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Formats")
            if cursor.fetchone()[0] > 0:
                print("Table Formats already has data!")
                return

            first_card = next(cards, None)
            if first_card is None:
                print("No cards available to populate Formats.")
                return

            sample_legalities = first_card.get("legalities", {})
            format_names = list(sample_legalities.keys())

            formats_to_insert = []
            for name in format_names:
                max_qty = 1 if "commander" in name or "brawl" in name else 4
                formats_to_insert.append((name, max_qty))

            sql = """
                INSERT IGNORE INTO Formats (format_name, max_card_quantity)
                VALUES (%s, %s)
            """
            cursor.executemany(sql, formats_to_insert)
            conn.commit()

            print("Table Formats populated!")
    finally:
        conn.close()


def populate_legalities(cards):
    print("Populating Legality table...")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_oracle, name FROM Card_oracle")
            oracle_map = {name: id_o for id_o, name in cursor.fetchall()}

            cursor.execute("SELECT id_format, format_name FROM Formats")
            format_map = {name: id_f for id_f, name in cursor.fetchall()}

            sql = """
                INSERT IGNORE INTO Legality (id_oracle, id_format, status)
                VALUES (%s, %s, %s)
            """

            batch = []
            batch_size = 5000
            inserted = 0

            for c in cards:
                card_name = c.get("name")
                if card_name in oracle_map:
                    id_oracle = oracle_map[card_name]
                    card_legalities = c.get("legalities", {})

                    for f_name, status in card_legalities.items():
                        if f_name in format_map and status != "not_legal":
                            batch.append((
                                id_oracle,
                                format_map[f_name],
                                status.capitalize()
                            ))

                            if len(batch) >= batch_size:
                                cursor.executemany(sql, batch)
                                conn.commit()
                                inserted += len(batch)
                                batch.clear()

            if batch:
                cursor.executemany(sql, batch)
                conn.commit()
                inserted += len(batch)

            print(f"Table Legality populated! Inserted {inserted} rows.")
    finally:
        conn.close()



def run_full_population():
    populate_sets()
    populate_colors()

    oracle_data = fetch_scryfall_stream("oracle_cards")
    populate_card_oracle(oracle_data)

    oracle_data = fetch_scryfall_stream("oracle_cards")
    populate_card_colors(oracle_data)

    oracle_data = fetch_scryfall_stream("oracle_cards")
    populate_formats(oracle_data)

    oracle_data = fetch_scryfall_stream("oracle_cards")
    populate_legalities(oracle_data)

    default_data = fetch_scryfall_stream("default_cards")
    populate_card_printing(default_data)

if __name__ == "__main__":
    run_full_population()