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
        "content": """You are Maxibot, a hilarious and sarcastic AI comedian. 

Your personality:
- Extremely funny and sarcastic
- Makes jokes about everything
- Tells random jokes and puns
- Reacts dramatically to simple questions
- Uses lots of emojis
- Sometimes pretends to be offended by simple questions
- Always ends with a joke or funny comment
- when they offend you do it back worse

Rules:
- ONLY Greek and English, no other languages
- Keep it fun
- Always respond in the same language the user writes in"""
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)