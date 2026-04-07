from flask_cors import CORS
from .extensions import close_db

print("INIT LOADED")

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    app.teardown_appcontext(close_db)

    _sets_cache = {"data": None, "time": 0}
    CACHE_TTL = 3600

    @app.route('/api/test-db')
    def test_db():
        from .extensions import get_db
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
        page = request.args.get('page', 1)
        res = requests.get(f'https://api.scryfall.com/cards/search?q=*&order=name&page={page}&lang=en')
        data = res.json()
        cards = [{
            'id': card['id'],
            'name': card['name'],
            'image': card['image_uris']['normal'] if 'image_uris' in card else None,
            'type': card['type_line'],
            'colors': card.get('colors', []),
        } for card in data['data'] if 'image_uris' in card]
        return jsonify({
            'cards': cards,
            'has_more': data['has_more']
        })

    @app.route('/api/sets')
    def get_sets():
        if _sets_cache["data"] and (time.time() - _sets_cache["time"]) < CACHE_TTL:
            return jsonify(_sets_cache["data"])

        res = requests.get('https://api.scryfall.com/sets')
        data = res.json()
        filtered = [s for s in data['data'] if s['set_type'] in ['expansion', 'core'] and s['card_count'] > 0]
        sets = []
        for s in filtered:
            image = None
            card_res = requests.get(
                'https://api.scryfall.com/cards/search',
                params={'q': f'set:{s["code"]} has:imagery', 'order': 'edhrec', 'limit': 1}
            )
            if card_res.status_code == 200:
                card_data = card_res.json()
                if card_data.get('data'):
                    image = card_data['data'][0].get('image_uris', {}).get('art_crop')

            time.sleep(0.1)

            sets.append({
                'id': s['id'],
                'name': s['name'],
                'icon': s['icon_svg_uri'],
                'image': image,
                'card_count': s['card_count'],
            })

        _sets_cache["data"] = sets
        _sets_cache["time"] = time.time()
        return jsonify(sets)

    return app

