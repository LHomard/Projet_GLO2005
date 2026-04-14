import requests


def load_comprehensive_rules():
    url = "https://media.wizards.com/2025/downloads/MagicCompRules_20250207.txt"
    response = requests.get(url)
    return response.text

print(load_comprehensive_rules())