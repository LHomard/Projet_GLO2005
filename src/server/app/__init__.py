from flask import Flask
from flask_cors import CORS
from .extensions import close_db

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    app.teardown_appcontext(close_db)

    @app.route("/api/test-db")
    def test_db():
        from .extensions import get_db
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
        return {"status": "DB connected!"}

    return app

