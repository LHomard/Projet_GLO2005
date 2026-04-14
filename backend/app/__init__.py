import pymysql
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from services.ai_judges import judges_bp
from flask_login import LoginManager, login_user, current_user, login_required

from .Db_queries.ai_queries import get_all_discussion_from_history, delete_chat, get_discussion_from_history
from .Db_queries.login_queries import check_user_password
from .Db_queries.card_queries import get_cards_paginated, get_random_card_image, get_card_details_logic, \
    get_card_image_from_sets
from .Db_queries.color_queries import get_all_colors_logic
from .Db_queries.deck_queries import create_deck_logic, delete_deck_logic, get_deck_by_id_logic, \
    get_deck_by_user_id_logic, get_deck_cards_logic, add_card_to_deck_logic
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
    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)


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
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }), 200

        return jsonify({'error': 'Invalid email or password'}), 403


    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json(silent=True) or {}

        username = (data.get('username') or '').strip()
        email = (data.get('email') or '').strip()
        password = data.get('password') or ''
        age = data.get('age')

        if not username or not email or not password or not age:
            return jsonify({'error': 'All fields are required.'}), 400

        if get_user_by_email(email):
            return jsonify({'error': 'Email already in use.'}), 409

        try:
            insert_user(username, email, age, password)
        except pymysql.err.OperationalError as e:
            return jsonify({'error': e.args[1]}), 400

        return jsonify({
            'message': 'Account created successfully.'
        }), 201


    @app.route('/api/decks')
    def get_user_decks():
        data = get_deck_by_user_id_logic(current_user.id)
        return jsonify(data), 200


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

    @app.route('/api/colors')
    def get_all_colors():
        data = get_all_colors_logic()

        return jsonify(data)


    @app.route('/api/decks/<int:deck_id>/cards', methods=['GET'])
    @login_required
    def get_deck_cards(deck_id):
        deck = get_deck_by_id_logic(deck_id)

        if deck is None:
            return jsonify({'error': 'Deck not found'}), 404

        if deck['user_id'] != current_user.id:
            return jsonify({'error': 'Denied access'}), 403

        data = get_deck_cards_logic(deck_id)

        return jsonify(data), 200


    @app.route('/api/decks/<int:deck_id>/cards', methods=['POST'])
    @login_required
    def add_card_to_deck(deck_id):
        deck = get_deck_by_id_logic(deck_id)

        if deck is None:
            return jsonify({'error': 'Deck not found'}), 404

        if deck['user_id'] != current_user.id:
            return jsonify({'error': 'Denied access'}), 403

        data = request.get_json(silent=True) or {}
        id_printing = data.get('id_printing')
        quantity = data.get('quantity', 1)

        if not id_printing:
            return jsonify({'error': 'id_printing is required'}), 400

        result = add_card_to_deck_logic(deck_id, id_printing, quantity)

        if result and 'error' in result:
            return jsonify(result), 400

        return jsonify({'message': 'Card added successfully'}), 201


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



