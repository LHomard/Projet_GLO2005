import csv
import os
import pymysql

def import_rules():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True,
    )

    cursor = conn.cursor()

    csv_path = os.path.join(os.path.dirname(__file__), 'magic_rules.csv')

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO rules (rule_number, parent_rule, keyword, text, example)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                row['rule_number'],
                row['parent_rule'],
                row['keyword'],
                row['text'],
                row['example']
            ))

    cursor.close()
    conn.close()
    print("Done!")

import_rules()