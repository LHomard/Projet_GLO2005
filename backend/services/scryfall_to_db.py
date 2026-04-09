import requests
import os
import pymysql
from dotenv import load_dotenv
import cryptography
import time

load_dotenv()
print("HOST =", os.getenv("DB_HOST"))
print("PORT=", os.getenv("DB_PORT"))
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

def fetch_scryfall_data (data_type):
    print(f"Retrieving Bulk scryfall's URl for ({data_type})...")
    bulk_meta = requests.get("https://api.scryfall.com/bulk-data").json()
    download_url = next(d['download_uri'] for d in bulk_meta['data'] if d['type'] == data_type)
    return requests.get(download_url).json()


def populate_card_oracle(cards):
    print("Populating Card_oracle table...")

    to_insert = []
    for card in cards:
        to_insert.append((
            card.get('name'),
            card.get('mana_cost'),
            card.get('cmc', 0),
            card.get('oracle_text'),
            card.get('power'),
            card.get('toughness'),
            card.get('type_line')
        ))

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Card_oracle")
            if cursor.fetchone()[0] == 0:
                print(f"Insertion of {len(to_insert)} cards...")
                sql = """INSERT INTO Card_oracle (name, mana_cost, cmc, oracle_text, power, toughness, type_line)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                # Separate in chunks of 1000 elements to not overcharge the buffer
                for i in range(0, len(to_insert), 1000):
                    cursor.executemany(sql, to_insert[i:i + 1000])

                connection.commit()
                print("Table card_oracle populated !")
            else:
                print("Table card_oracle already has data !")
    finally:
        connection.close()


def populate_sets():
    print("Retrieving sets from Scryfall...")
    response = requests.get("https://api.scryfall.com/sets").json()
    sets_data = response.get('data', [])

    to_insert = [
        (s.get('code').upper(), s.get('name'), s.get('released_at'), s.get('icon_svg_uri'), s.get('card_count'))
        for s in sets_data
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Sets")
            if cursor.fetchone()[0] == 0:
                print(f"Insertion de {len(to_insert)} extensions...")
                sql = "INSERT INTO Sets (set_code, set_name, release_date, icon_url, card_count) VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(sql, to_insert)
                conn.commit()
                print("Table sets populated !")
            else:
                print("Table sets already has data !")
    finally:
        conn.close()


def populate_card_printing(cards):
    print("Populating Card_printing table...")

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_oracle, name FROM Card_oracle")
            oracle_map = {name: id_o for id_o, name in cursor.fetchall()}

            cursor.execute("SELECT id_set, set_code FROM Sets")
            set_map = {code.upper(): id_s for id_s, code in cursor.fetchall()}

            to_insert = []
            for c in cards:
                set_code = c.get('set', '').upper()
                if c.get('name') in oracle_map and set_code in set_map:
                    to_insert.append((
                        oracle_map[c.get('name')],
                        set_map[set_code],
                        c.get('rarity'),
                        c.get('artist'),
                        c.get('image_uris', {}).get('normal'),
                        c.get('prices', {}).get('usd')
                    ))

            sql = "INSERT INTO Card_printing (id_oracle, id_set, rarity, artist, image_url, price) VALUES (%s, %s, %s, %s, %s, %s)"
            for i in range(0, len(to_insert), 1000):
                cursor.executemany(sql, to_insert[i:i + 1000])
            connection.commit()
    finally:
        connection.close()


def populate_colors():
    print("Populating Card_printing table...")

    colors = [
        ('White', 'W'),
        ('Blue', 'U'),
        ('Black', 'B'),
        ('Red', 'R'),
        ('Green', 'G'),
        ('Colorless', 'C'),
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Colors")
            if cursor.fetchone()[0] == 0:
                sql = "INSERT INTO Colors (color_name, color_symbol) VALUES (%s, %s)"
                cursor.executemany(sql, colors)
                conn.commit()
                print("Table sets populated !")
            else:
                print("Table colors already has data !")
    finally:
        conn.close()


def populate_card_colors(cards):
    print("Population Card_colors table...")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_oracle, name FROM Card_oracle")
            oracle_map = {name: id_o for id_o, name in cursor.fetchall()}

            cursor.execute("SELECT id_color, color_symbol FROM Colors")
            color_map = {symbol: id_c for id_c, symbol in cursor.fetchall()}

            card_colors_to_insert = []

            for c in cards:
                card_name = c.get('name')
                scryfall_colors = c.get('colors', [])

                if not scryfall_colors:
                    scryfall_colors = ['C']

                if card_name in oracle_map:
                    id_oracle = oracle_map[card_name]
                    for symbol in scryfall_colors:
                        if symbol in color_map:
                            card_colors_to_insert.append((id_oracle, color_map[symbol]))

            if card_colors_to_insert:
                sql = "INSERT IGNORE INTO Card_colors (id_oracle, id_color) VALUES (%s, %s)"
                for i in range(0, len(card_colors_to_insert), 1000):
                    cursor.executemany(sql, card_colors_to_insert[i:i + 1000])

                conn.commit()
                print("Table Card_colors populated !")

    finally:
        conn.close()


def populate_formats(cards):
    print("Populate Formats table...")

    sample_legalities = cards[0].get('legalities', {})
    format_names = list(sample_legalities.keys())

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            formats_to_insert = []
            for name in format_names:
                max_qty = 1 if 'commander' in name or 'brawl' in name else 4
                formats_to_insert.append((name, max_qty))

            sql = "INSERT IGNORE INTO Formats (format_name, max_card_quantity) VALUES (%s,%s )"
            cursor.executemany(sql, formats_to_insert)
            conn.commit()

            print(f"Table Formats has been populated !")

    finally:
        conn.close()


def populate_legalities(cards):
    print("Populating Legalities table...")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_oracle, name FROM Card_oracle")
            oracle_map = {name: id_o for id_o, name in cursor.fetchall()}

            cursor.execute("SELECT id_format, format_name FROM Formats")
            format_map = {name: id_f for id_f, name in cursor.fetchall()}

            legalities_to_insert = []
            for c in cards:
                card_name = c.get('name')
                if card_name in oracle_map:
                    id_oracle = oracle_map[card_name]
                    card_legalities = c.get('legalities', {})

                    for f_name, status in card_legalities.items():
                        if f_name in format_map and status != 'not_legal':
                            legalities_to_insert.append((
                                id_oracle,
                                format_map[f_name],
                                status.capitalize()
                            ))

            sql = "INSERT IGNORE INTO Legality (id_oracle, id_format, status) VALUES (%s, %s, %s)"
            for i in range(0, len(legalities_to_insert), 5000):
                cursor.executemany(sql, legalities_to_insert[i:i + 5000])

            conn.commit()
            print(f"Table Legalities has been populated !")
    finally:
        conn.close()


def run_full_population():
    populate_sets()
    populate_colors()

    oracle_data = fetch_scryfall_data("oracle_cards")
    populate_card_oracle(oracle_data)

    populate_card_colors(oracle_data)
    populate_card_colors(oracle_data)
    populate_legalities(oracle_data)

    default_data = fetch_scryfall_data("default_cards")
    populate_card_printing(default_data)

if __name__ == "__main__":
    run_full_population()