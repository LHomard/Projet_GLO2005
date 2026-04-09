import time

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from .db_connexion import close_db
from .routes.cards import get_cards_paginated
from .routes.sets import get_sets_logic

print("INIT LOADED")

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    app.teardown_appcontext(close_db)

    _sets_cache = {"data": None, "time": 0}
    CACHE_TTL = 3600

    @app.route('/api/test-db')
    def test_db():
        from .db_connexion import get_db
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute('SELECT 1')
        return {'status': 'DB connected!'}

    @app.route('/api/cards/random')
    def random_card():
        res = requests.get('https://api.scryfall.com/cards/random')
        card = res.json()
        return jsonify({
            'image': card['image_uris']['normal'],
        })

    @app.route('/api/cards')
    def get_cards():
        page = request.args.get("page", default=1, type=int)

        data = get_cards_paginated(page)

        return jsonify(data)


    @app.route('/api/sets')
    def get_sets():
        data = get_sets_logic()

        return jsonify(data)

    return app