import time

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.ai_judges import judges_bp

from .Db_queries.ai_queries import get_all_discussion_from_history, delete_chat, get_discussion_from_history
from .Db_queries.login_queries import check_user_password
from .Db_queries.card_queries import get_cards_paginated, get_random_card_image, get_card_details_logic, \
    get_card_image_from_sets
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
        search = request.args.get('search')

        data = get_cards_paginated(page, sort_by=sort_by, order=order, rarity=rarity, min_price=min_price,
                                   max_price=max_price, search=search)
        return jsonify(data)

    @app.route('/api/cards/<int:id>')
    def get_card_details(id):
        data = get_card_details_logic(id)

        return jsonify(data['cardDetail'])

    @app.route('/api/sets')
    def get_sets():
        data = get_sets_logic()

        return jsonify(data)

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json(silent=True) or {}

        email = (data.get('email') or '').strip()
        password = data.get('password') or ''

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400

        user = check_user_password(email, password)

        if user:
            return jsonify({
                'message': 'Login successful.',
                'user': user
            }), 200

        return jsonify({'error': 'Invalid email or password'}), 403


    @app.route('/api/chat/<int:id>', methods=['GET', 'DELETE'])
    def get_chat_history(id):
        if request.method == 'GET':
            data = get_all_discussion_from_history(id)
            return jsonify(data)

        if request.method == 'DELETE':
            data = delete_chat(id)
            return jsonify(data)
        return None



    return app



