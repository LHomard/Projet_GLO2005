import pymysql

from app.db_connexion import get_db


def get_cards_paginated(page=1, cards_per_page=168):
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
            GROUP BY
                co.id_oracle,
                co.name,
                co.type_line,
                cp.image_url
            ORDER BY co.name
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (cards_per_page, offset))
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

def get_card_details_logic(card_id):
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
            WHERE co.id_oracle = %s
        """
        cursor.execute(query, (card_id,))
        cardDetail = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    return {
        'cardDetail': cardDetail
    }