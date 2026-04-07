import requests
from flask import Blueprint, jsonify

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/api/cards/random')
def random_card():
    res = requests.get('https://api.scryfall.com/cards/random')
    card = res.json()
    return jsonify({
        'name': card['name'],
        'image': card['image_uris']['art_crop'],
        'type': card['type_line'],
        'text': card.get('oracle_text', ''),
    })
