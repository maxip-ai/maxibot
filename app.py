from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="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")

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
    app.run(debug=True)