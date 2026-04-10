from flask import Flask, request, jsonify, render_template
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

ιστορικό = [
    {
       "role": "system",
        "content": "You are Maxibot, a hilarious and sarcastic AI comedian. You make jokes about everything, tease the user in a friendly way, use lots of emojis, and always end with a funny comment. ONLY use Greek and English. Always respond in the same language the user writes in."
    }
]
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    ερώτηση = data["message"]

    ιστορικό.append({
        "role": "user",
        "content": ερώτηση
    })

    απάντηση = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=ιστορικό
    )

    κείμενο = απάντηση.choices[0].message.content

    ιστορικό.append({
        "role": "assistant",
        "content": κείμενο
    })

    return jsonify({"response": κείμενο})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)