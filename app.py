from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# Custom keyword-based answers
CUSTOM_KEYWORDS = [
    (["what","is","your","name"], "My name is QueryBot."),
    (["who","are","you"], "I'm QueryBot, an AI assistant built for the Skill Expo."),
    (["introduce","yourself"], "Hello! I'm QueryBot, an AI assistant created to answer questions and demonstrate the power of artificial intelligence."),
    (["which","school","made","you"], "I was built by KG International School's Computer Science Team."),
    (["which","school","created","you"], "I was built by KG International School's Computer Science Team."),
    (["who","created","you"], "I was built by KG International School's Computer Science Team."),
    (["who","made","you"], "I was built at KG International School's Computer Science Team.."),
    (["where","school","kg"], "KG International School is located in Annur, Coimbatore."),
    (["principal","kg","school"], "The Principal of KG International School is Mrs. Kaleshwari Srilatha."),
    (["chief","minister","tamil", "nadu"], "The Chief Minister of Tamil Nadu is C. Joseph Vijay."),
    (["where","is","skill", "expo","held"], "The Skill Expo is Held at Thangam International School, Salem."),
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        question = user_message.lower()

        # ===== Smart Keyword Matching =====
        best_match = None
        best_score = 0

        for keywords, answer in CUSTOM_KEYWORDS:
            score = sum(1 for word in keywords if word in question)
            required = max(1, (len(keywords) + 1) // 2)

            if score >= required and score > best_score:
                best_score = score
                best_match = answer

        if best_match:
            return jsonify({"reply": best_match})

        # ===== Gemini =====
        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
