from app.db_connexion import get_db, load_sql


def get_cards_paginated(page=1, cards_per_page=168):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    offset = (page - 1) * cards_per_page
    try:
        query = load_sql("Queries/cards/get_cards.sql")
        cursor.execute(query, (page, offset))
        cards = cursor.fetchall()

        count_query = load_sql("Queries/cards/count_cards.sql")
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