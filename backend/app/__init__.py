import pymysql
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from services.ai_judges import judges_bp
from flask_login import LoginManager, login_user, current_user, login_required

from .Db_queries.color_queries import get_all_colors_logic
from .Db_queries.deck_queries import create_deck_logic, delete_deck_logic, get_deck_by_id_logic
from .Db_queries.format_queries import get_all_formats_logic
from .Db_queries.login_queries import check_user_password, get_user_by_id, get_user_by_email, insert_user

from .Db_queries.card_queries import get_cards_paginated, get_random_card_image, get_card_details_logic
from .Db_queries.set_queries import get_sets_logic
from .db_connexion import close_db

print("INIT LOADED")

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    app.register_blueprint(judges_bp)
    app.teardown_appcontext(close_db)
    app.secret_key = 'dev_secret_key'

    login_manager = LoginManager()
    login_manager.init_app(app)

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

        if check_user_password(email, password):
            user = get_user_by_email(email)
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200

        return jsonify({'error': 'Invalid email or password'}), 403


    @app.route('/api/decks/<int:id>')
    def get_deck_by_user_id(user_id):
        data = get_deck_by_id_logic(user_id)

        return jsonify(data)


    @app.route('/api/decks', methods=['POST'])
    @login_required
    def create_deck():
        data = request.get_json(silent=True) or {}

        deck_name = data.get('deck_name')
        format_name = data.get('format_name')
        format_name = format_name.strip()


        if not deck_name or not format_name:
           return jsonify({'error': 'deck_name or format_name are required.'}), 400

        result = create_deck_logic(deck_name, format_name, current_user.id)


        if result is None:
            return jsonify({'error': 'Format introuvable'}), 404

        return jsonify({
            'id_deck': result['id_deck'],
            'nom': result['deck_name'],
            'id_format': result['id_format']
        }), 201


    @app.route('/api/decks/<int:deck_id>', methods=['DELETE'])
    @login_required
    def delete_deck(deck_id):
        deck = get_deck_by_id_logic(deck_id)

        if deck is None:
            return jsonify({'error': 'Deck introuvable'}), 404

        if deck['user_id'] != current_user.id:
            return jsonify({'error': 'Accès refusé'}), 403

        data = delete_deck_logic(deck_id)

        return jsonify(data), 200

    @app.route('/api/formats')
    def get_all_formats():
        data = get_all_formats_logic()

        return jsonify(data)


    @app.route('/api/Colors')
    def get_all_colors():
        data = get_all_colors_logic()

        return jsonify(data)


    return app

