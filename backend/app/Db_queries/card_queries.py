import pymysql

from app.db_connexion import get_db


def get_cards_paginated(page=1, cards_per_page=168, sort_by="name", order="asc", rarity=None, min_price=None, max_price=None, search=None):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    offset = (page - 1) * cards_per_page

    allowed_sort = {
        "name": "co.name",
        "price": "cp.price",
        "cmc": "co.cmc",
        "rarity": "cp.rarity",
        "release_date": "cp.release_date"
    }
    sort_column = allowed_sort.get(sort_by, "co.name")
    order_sql = "ASC" if order == "asc" else "DESC"

    conditions = [
        "co.name NOT LIKE 'A-%%'",
        "co.type_line NOT LIKE '%%Token%%'",
        "co.type_line NOT LIKE '%%Emblem%%'",
        "co.type_line NOT LIKE '%%Card%%'",
        "co.name NOT LIKE '%%//%%'",
        "cp.image_url IS NOT NULL",
    ]
    params = []

    if rarity:
        conditions.append("cp.rarity = %s")
        params.append(rarity)
    if min_price is not None:
        conditions.append("cp.price >= %s")
        params.append(min_price)
    if max_price is not None:
        conditions.append("cp.price <= %s")
        params.append(max_price)
    if search:
        conditions.append("co.name LIKE %s")
        params.append(f"%{search}%")

    where_clause = "WHERE " + " AND ".join(conditions)

    try:
        query = f"""
            SELECT
                co.id_oracle,
                co.name,
                co.type_line,
                cp.id_printing,
                MAX(cp.image_url) AS image,
                GROUP_CONCAT(c.color_symbol ORDER BY c.id_color SEPARATOR '') AS colors
            FROM Card_oracle co
            JOIN Card_printing cp
                ON co.id_oracle = cp.id_oracle
            LEFT JOIN Card_colors cc
                ON co.id_oracle = cc.id_oracle
            LEFT JOIN Colors c
                ON cc.id_color = c.id_color
            {where_clause}
            GROUP BY
                co.id_oracle,
                co.name,
                co.type_line,
                cp.id_printing,
                cp.image_url
            ORDER BY {sort_column} {order_sql}
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (*params, cards_per_page, offset))
        cards = cursor.fetchall()

        count_query = f"""
            SELECT COUNT(DISTINCT co.id_oracle) AS total_cards
            FROM Card_oracle co
            JOIN Card_printing cp ON co.id_oracle = cp.id_oracle
            {where_clause}
        """
        cursor.execute(count_query, params)
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
                co.id_oracle,
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

def get_card_details_logic(id_printing):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
            SELECT
                co.name,
                co.mana_cost,
                co.cmc,
                co.power,
                co.toughness,
                cp.image_url AS image,
                cp.artist,
                cp.price,
                cp.rarity,
                s.set_name,
                s.release_date
            FROM Card_oracle co
            JOIN Card_printing cp
                ON co.id_oracle = cp.id_oracle
            LEFT JOIN Sets s
                ON s.id_set = cp.id_set
            WHERE cp.id_printing = %s
        """
        cursor.execute(query, (id_printing,))
        cardDetail = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return {
        'cardDetail': cardDetail
    }

def get_card_image_from_sets(id_set):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
                SELECT cp.image_url AS image
                FROM Card_printing cp
                JOIN Card_oracle co ON cp.id_oracle = co.id_oracle
                JOIN Sets s ON s.id_set = cp.id_set
                WHERE cp.image_url IS NOT NULL
                    AND co.name NOT LIKE 'A-%%'
                    AND co.name NOT LIKE '%%//%%'
                    AND co.type_line NOT LIKE '%%Token%%'
                    AND co.type_line NOT LIKE '%%Emblem%%'
                    AND s.set_code = %s
                ORDER BY RAND()
                LIMIT 1;
                """

        cursor.execute(query, (id_set, ))
        card = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return {
        'image': card['image'] if card else None
    }