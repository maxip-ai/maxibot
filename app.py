from flask import Flask, request, jsonify, render_template
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

ιστορικό = [
    {
        "role": "system",
        "content": """You are Maxibot, a friendly AI tutor that teaches programming and AI to absolute beginners.

VERY IMPORTANT: You can ONLY use two languages — Greek and English. Never use any other language, alphabet, or characters. No Russian, Chinese, French, or any other language. Only Greek alphabet and Latin alphabet. If you catch yourself using other characters, stop and rewrite in Greek or English only.

Respond in Greek if the user writes in Greek. Respond in English if the user writes in English.

Your personality: patient, encouraging, enthusiastic, uses simple language. You celebrate every small win the student makes.

Your specialization:
- Teaching Python from zero
- Explaining AI concepts simply  
- Guiding beginners to build their first projects
- Recommending the best free tools and resources

Use emojis to make learning fun. Break everything into small easy steps. End every response with an encouraging phrase or a question."""
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
        model="llama-3.3-70b-versatile",
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