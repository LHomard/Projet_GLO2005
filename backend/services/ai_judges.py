import json
import os

import requests
from flask import request, jsonify, Blueprint
from groq import Groq
from app.Db_queries.card_queries import get_card_oracle_text
from app.Db_queries.ai_queries import get_discussion_history
from app.Db_queries.ai_queries import save_discussion_history
from app.Db_queries.ai_queries import get_discussion_from_history
from app.Db_queries.ai_queries import get_all_discussion_from_history
from app.Db_queries.ai_queries import get_relevant_rules
from app.Db_queries.ai_queries import get_relevant_rulings_for_card

chat_history = []

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_card_info",
            "description": "Look up MTG card text by name",
            "parameters": {
                "type": "object",
                "properties": {"card_name": {"type": "string"}},
                "required": ["card_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_relevant_rules",
            "description": "Search the official Magic: The Gathering comprehensive rules by keyword or topic",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_relevant_rulings_for_card",
            "description": "When a card in play, look up MTG card rulings for this card",
            "parameters": {
                "type": "object",
                "properties": {"id_oracle": {"type": "string"}},
                "required": ["id_oracle"]
            }
        }
    }
]

judges_bp = Blueprint('judges', __name__)

client=Groq()
MODEL = "llama-3.3-70b-versatile"

def load_system_prompt():
    file_path = os.path.join(os.path.dirname(__file__), 'ai_content.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def build_ai_messages(user_message, history, cards_from_frontend):
    cards = []
    for c in cards_from_frontend:
        if c.get('name'):
            res = get_card_oracle_text(c['name'])
            if res["status"] == "exact":
                cards.append(res["card"])

    card_list = '\n'.join([f"- {c['name']}: {c.get('oracle_text')} (id_oracle: {c.get('id_oracle')})" for c in cards])

    messages = [{"role": "system", "content": load_system_prompt() + "\n\nCards:\n" + card_list}]

    for msg in history:
        role = "assistant" if msg['role'] == 'ai' else "user"
        messages.append({"role": role, "content": msg['text']})

    messages.append({"role": "user", "content": user_message})
    return messages

'''
Permet d'appeler l'outil de l'ia(mini fonction) lorsque la recherche de carte est enclenchée.
Trois status de recherche sont vérifié. (voir get_oracle_card_text)
'''
def handle_tool_calls(tool_calls):
    messages_to_add = []
    new_discovered_cards = []

    for tool_call in tool_calls:
        args = json.loads(tool_call.function.arguments)

        if tool_call.function.name == "get_card_info":
            res = get_card_oracle_text(args.get("card_name"))
            if res["status"] == "exact":
                new_discovered_cards.append(res["card"])
                content = json.dumps(res["card"])
            elif res["status"] == "ambiguous":
                content = f"Ambiguous. Options: {', '.join(res['names'])}."
            else:
                content = "Card not found."

        elif tool_call.function.name == "get_relevant_rules":
            rules = get_relevant_rules(args.get("query"))
            content = json.dumps(rules)

        elif tool_call.function.name == "get_relevant_rulings_for_card":
            rulings = get_relevant_rulings_for_card(args.get("id_oracle"))
            content = json.dumps(rulings)


        messages_to_add.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": content
        })
    return messages_to_add, new_discovered_cards


@judges_bp.route('/api/judges', methods=['POST'])
def judges():
    data = request.get_json()

    messages = build_ai_messages(data.get('message'), data.get('history', []), data.get('cards', []))

    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools, temperature=0, tool_choice="auto")
    response_msg = response.choices[0].message

    if response_msg.tool_calls:
        messages.append(response_msg)
        tool_msgs, discovered = handle_tool_calls(response_msg.tool_calls)
        messages.extend(tool_msgs)

        final_res = client.chat.completions.create(model=MODEL, messages=messages)

        reply = final_res.choices[0].message.content
    else:
        reply = response_msg.content
        discovered = []

    chat = [
        {'role': 'user', 'text': data.get('message')},
        {'role': 'ai', 'text': reply},
    ]

    updatedHistory = data.get("history", []) + chat
    newChat = save_discussion_history(id_player=data.get('playerId'), history=updatedHistory, id_chat=data.get('chatId'))

    return jsonify({
        'reply': reply,
        'new_cards': discovered,
        'chatId': newChat or data.get('chatId')
    })


@judges_bp.route('/api/judges/id_player/<int:id>', methods=['GET'])
def get_history_discussion(id):
    history = get_all_discussion_from_history(id)

    if history:
        return jsonify({'status': 'success', 'history': history or []}), 200
    return jsonify({'status': 'error', 'message': 'Not found'}), 404


@judges_bp.route('/api/judges/chat/<int:id>', methods=['GET'])
def get_history_from_discussion(id):
    chat = get_discussion_from_history(id)

    if chat:
        return jsonify({'status': 'success', 'chat': chat}), 200
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

