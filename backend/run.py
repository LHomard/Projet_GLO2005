import os
import pymysql
from app import create_app

app = create_app()
#
#def get_db_connection():
#    return pymysql.connect(
 #       host=os.getenv("DB_HOST"),
 #       user=os.getenv("DB_USER"),
 #       password=os.getenv("DB_PASSWORD"),
  #      database=os.getenv("DB_NAME")
  #  )

#@app.route('/')
#def home():
#    conn = get_db_connection()
 #   cursor = conn.cursor()
   # cursor.execute("SELECT DATABASE();")
  #  conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)