import pymysql
import pymysql.cursors
from flask import g
import os

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def load_sql(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
