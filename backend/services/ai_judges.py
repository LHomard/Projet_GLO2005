import json
import os

import requests
from flask import request, jsonify, Blueprint
from groq import Groq
from app.Db_queries.card_queries import get_card_oracle_text

CARD_TOOL = [{
    "type": "function",
    "function": {
        "name": "get_card_info",
        "description": "Look up MTG card text and rulings by name",
        "parameters": {
            "type": "object",
            "properties": {"card_name": {"type": "string"}},
            "required": ["card_name"]
        }
    }
}]

judges_bp = Blueprint('judges', __name__)

client=Groq()
MODEL = "llama-3.3-70b-versatile"

def load_system_prompt():
    file_path = os.path.join(os.path.dirname(__file__), 'ai_content.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def build_ai_messages(user_message, history, cards_from_frontend):
    # Logique pour extraire les cartes du terrain
    cards = []
    for c in cards_from_frontend:
        if c.get('name'):
            res = get_card_oracle_text(c['name'])
            if res["status"] == "exact":
                cards.append(res["card"])

    card_list = '\n'.join([f"- {c['name']}: {c.get('oracle_text')}" for c in cards])

    messages = [{"role": "system", "content": load_system_prompt() + "\n\nCards:\n" + card_list}]

    # Intégration de la mémoire
    for msg in history:
        role = "assistant" if msg['role'] == 'ai' else "user"
        messages.append({"role": role, "content": msg['text']})

    messages.append({"role": "user", "content": user_message})
    return messages


def handle_tool_calls(tool_calls):
    messages_to_add = []
    new_discovered_cards = []

    for tool_call in tool_calls:
        args = json.loads(tool_call.function.arguments)
        res = get_card_oracle_text(args.get("card_name"))

        if res["status"] == "exact":
            new_discovered_cards.append(res["card"])
            content = json.dumps(res["card"])
        elif res["status"] == "ambiguous":
            content = f"Ambiguous. Options: {', '.join(res['names'])}."
        else:
            content = "Card not found."

        messages_to_add.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": "get_card_info",
            "content": content
        })
    return messages_to_add, new_discovered_cards


@judges_bp.route('/api/judges', methods=['POST'])
def judges():
    data = request.get_json()

    messages = build_ai_messages(data.get('message'), data.get('history', []), data.get('cards', []))

    response = client.chat.completions.create(model=MODEL, messages=messages, tools=CARD_TOOL, temperature=0)
    response_msg = response.choices[0].message

    if response_msg.tool_calls:
        messages.append(response_msg)
        tool_msgs, discovered = handle_tool_calls(response_msg.tool_calls)
        messages.extend(tool_msgs)

        final_res = client.chat.completions.create(model=MODEL, messages=messages)
        return jsonify({
            'reply': final_res.choices[0].message.content,
            'new_cards': discovered
        })

    return jsonify({'reply': response_msg.content, 'new_cards': []})


