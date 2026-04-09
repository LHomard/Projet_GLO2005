import json, requests

from flask import request, jsonify

headers = {
    "User-Agent": "MTGExampleApp/1.0",
    "Accept": "application/json"
}


API_URL = "https://api.scryfall.com/bulk-data"
scryfall = requests.get(API_URL, headers=headers).json()

print(scryfall)
def getCards() -> dict:
    try:
        items = next(
            item for item in scryfall['data']
            if item['type'] == 'default_cards'
        )
    except StopIteration:
        raise ValueError("default_cards  n'a pas été trouvé")

    print(items)

    try:
        response = requests.get(items['download_uri'], headers=headers)
        response.raise_for_status()
        cards = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ValueError('Aucun JSON valide') from e

    return cards

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
def getRules() -> dict:
    try:
        items = next(
            item for item in scryfall['data']
            if item['type'] == 'rules'
        )
    except StopIteration:
        raise ValueError("rules  n'a pas été trouvé")

    try:
        response = requests.get(items['download_uri'], headers=headers)
        response.raise_for_status()
        rules = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ValueError('Aucun JSON valide') from e

    return rules

print(getCards())
