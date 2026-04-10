import os
from flask import request, jsonify, Blueprint
from groq import Groq

judges_bp = Blueprint('judges', __name__)

client=Groq()
MODEL = "llama-3.3-70b-versatile"

def load_system_prompt():
    file_path = os.path.join(os.path.dirname(__file__), 'ai_content.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

@judges_bp.route('/api/judges', methods=['POST'])
def judges():
    data = request.get_json()
    user_prompt = data.get('message', '')
    cards = data.get('cards', [])

    card_context = ''
    if cards:
        card_list = '\n'.join([f"- {c['name']} ({c['type']}) ({c['oracle_text']})" for c in cards])
        card_context = f"\n\nCards currently in play:\n{card_list}\n"

    messages=[
        {
            "role": "system",
            "content": load_system_prompt() + card_context,
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    response_message = response.choices[0].message.content
    return jsonify({'reply' : response_message})
