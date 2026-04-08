import os
from flask import Flask, request, jsonify
from openai import OpenAI

from backend.run import app

BASE_URL = "https://api.groq.com/openai/v1"

client = OpenAI(
    base_url=BASE_URL,
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route('/api/judge', methods=['POST'])
def ai_judge():
    try:
        data = request.get_json()
        user_input = data.get("user_input")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                "role": "system",
                "content": "You are a professional Magic: The Gathering Judge. Provide clear, rules-based rulings. Be concise."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        return jsonify({
            "verdict": response.choices[0].message.content
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"error" : "The judge is currently unavailable"}), 500
