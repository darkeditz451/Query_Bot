from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ==============================
# Gemini Setup
# ==============================
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# ==============================
# Text Normalization
# ==============================
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # Remove punctuation
    text = re.sub(r"\s+", " ", text)      # Remove extra spaces
    return text.strip()


# ==============================
# Custom Questions
# ==============================
CUSTOM_PHRASES = {
    "what is your name":
        "My name is QueryBot.",

    "who are you":
        "I'm QueryBot, an AI assistant built for the Skill Expo.",

    "introduce yourself":
        "Hello! I'm QueryBot, an AI assistant created to answer questions and demonstrate the power of artificial intelligence.",

    "which school made you":
        "I was built by KG International School",

    "which school created you":
        "I was built by KG International School.",

    "who created you":
        "I was built by KG International School's Computer Science Team.",

    "who made you":
        "I was built by KG International School's Computer Science Team.",

    "where is kg international school":
        "KG International School is located in Annur, Coimbatore.",

    "where is kg school":
        "KG International School is located in Annur, Coimbatore.",

    "who is the principal of kg international school":
        "The Principal of KG International School is Mrs. Kaleshwari Srilatha.",

    "principal of kg international school":
        "The Principal of KG International School is Mrs. Kaleshwari Srilatha.",

    "where is skill expo held":
        "The Skill Expo is held at Thangam International School, Salem.",

    "Who is the chief minister of tamilnadu":
        "The Chief Minister of Tamilnadu is C.Joseph Vijay.",

    "Who is the cm of tamilnadu":
        "The Chief Minister of Tamilnadu is C.Joseph Vijay.",

    "who is the Chief minister of tamilnadu":
        "The Chief Minister of Tamilnadu is C.Joseph Vijay.",

    "who is the cm of tamilnadu":
        "The Chief Minister of Tamilnadu is C.Joseph Vijay."
    
}


# ==============================
# Routes
# ==============================
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

        question = normalize(user_message)

        # ==============================
        # Custom Responses
        # ==============================
        for phrase, answer in CUSTOM_PHRASES.items():
            if question == phrase or phrase in question:
                return jsonify({"reply": answer})

        # ==============================
        # Gemini AI
        # ==============================
        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ==============================
# Run
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
