import time

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.ai_judges import judges_bp

from .Db_queries.card_queries import get_cards_paginated, get_random_card_image, get_card_details_logic
from .Db_queries.set_queries import get_sets_logic
from .db_connexion import close_db

print("INIT LOADED")

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    app.register_blueprint(judges_bp)
    app.teardown_appcontext(close_db)

    _sets_cache = {"data": None, "time": 0}
    CACHE_TTL = 3600

    @app.route('/api/cards/random')
    def random_card():
        data = get_random_card_image()

        return jsonify(data)

    @app.route('/api/cards')
    def get_cards():
        page = request.args.get("page", default=1, type=int)
        sort_by = request.args.get("sort_by", default="name", type=str)
        order = request.args.get("order", default="asc", type=str)
        rarity = request.args.get("rarity", default=None, type=str)
        min_price = request.args.get("min_price", default=None, type=float)
        max_price = request.args.get("max_price", default=None, type=float)

        data = get_cards_paginated(page, sort_by=sort_by, order=order, rarity=rarity, min_price=min_price,
                                   max_price=max_price)
        return jsonify(data)


    @app.route('/api/sets')
    def get_sets():
        data = get_sets_logic()

        return jsonify(data)

    @app.route('/api/cards/<int:id>')
    def get_card_details(id):
        data = get_card_details_logic(id)

        return jsonify(data['cardDetail'])

    return app