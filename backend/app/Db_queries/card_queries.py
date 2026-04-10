import pymysql

from app.db_connexion import get_db


def get_cards_paginated(page=1, cards_per_page=168, search=""):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    offset = (page - 1) * cards_per_page
    try:
        query = """
            SELECT
                co.id_oracle,
                co.name,
                co.type_line,
                MAX(cp.image_url) AS image,
                GROUP_CONCAT(c.color_symbol ORDER BY c.id_color SEPARATOR '') AS colors
            FROM Card_oracle co
            JOIN Card_printing cp
                ON co.id_oracle = cp.id_oracle
            LEFT JOIN Card_colors cc
                ON co.id_oracle = cc.id_oracle
            LEFT JOIN Colors c
                ON cc.id_color = c.id_color
            WHERE
                co.name NOT LIKE 'A-%%' -- Afin d'éviter les doubles faces
                AND co.type_line NOT LIKE '%%Token%%' 
                AND co.type_line NOT LIKE '%%Emblem%%'
                AND co.type_line NOT LIKE '%%Card%%'
                AND co.name NOT LIKE '%%//%%' -- Afin d'éviter les doubles faces
                AND cp.image_url IS NOT NULL 
                AND co.name LIKE %s
            GROUP BY
                co.id_oracle,
                co.name,
                co.type_line,
                cp.image_url
            ORDER BY co.name
            LIMIT %s OFFSET %s;
        """
        search_param = f"{search}%" if search else "%"
        cursor.execute(query, (search_param, cards_per_page, offset))
        cards = cursor.fetchall()
        print(cards)

        count_query = """SELECT COUNT(*) AS total_cards FROM Card_oracle;"""
        cursor.execute(count_query)
        total = cursor.fetchone()["total_cards"]

        has_more = (page * cards_per_page) < total

    finally:
        cursor.close()
        conn.close()

    return {
        "cards": cards,
        "has_more": has_more,
    }



def get_random_card_image():
        conn = get_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            query = """
                SELECT cp.image_url AS image
                FROM Card_printing cp
                JOIN Card_oracle co ON cp.id_oracle = co.id_oracle
                WHERE cp.image_url IS NOT NULL
                AND co.name NOT LIKE 'A-%%'
                AND co.name NOT LIKE '%%//%%'
                AND co.type_line NOT LIKE '%%Token%%'
                AND co.type_line NOT LIKE '%%Emblem%%'
                ORDER BY RAND() LIMIT 1; 
            """

            cursor.execute(query)
            card = cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

        return {
            'image': card['image']
        }


def get_card_oracle_text(card_name):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
            SELECT 
                co.name,
                co.oracle_text,
                co.type_line,
                co.mana_cost,
                co.power,
                co.toughness,
                cp.image_url
            FROM Card_oracle co
            JOIN Card_printing cp ON cp.id_oracle = co.id_oracle
            WHERE co.name LIKE %s AND
                cp.image_url IS NOT NULL
            LIMIT 3;
        """
        cursor.execute(query, (f"%{card_name}%",))
        results = cursor.fetchall()

        # CAS 1 : Match Exact
        exact_match = next((r for r in results if r['name'].lower() == card_name.lower()), None)
        if exact_match:
            return {"status": "exact", "card": exact_match}

        # CAS 2 : Une seule carte trouvée
        if len(results) == 1:
            return {"status": "exact", "card": results[0]}

        # CAS 3 : Plusieurs carte
        if len(results) > 1:
            return {"status": "ambiguous", "names": [r['name'] for r in results]}

        return {"status": "not_found"}

    finally:
        cursor.close()
        conn.close()

    return card