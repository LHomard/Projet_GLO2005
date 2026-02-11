import json, requests

headers = {
    "User-Agent": "MTGExampleApp/1.0",
    "Accept": "application/json"
}


API_URL = "https://api.scryfall.com/bulk-data"
scryfall = requests.get(API_URL, headers=headers).json()

print(scryfall)
def getCards() -> dict:
    print('1')
    try:
        items = next(
            item for item in scryfall['data']
            if item['type'] == 'all_cards'
        )
    except StopIteration:
        raise ValueError("all_cards  n'a pas été trouvé")

    print(items)

    try:
        response = requests.get(items['download_uri'], headers=headers)
        response.raise_for_status()
        cards = response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise ValueError('Aucun JSON valide') from e

    return cards[0]

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
