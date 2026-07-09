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
    (["creator"], "I was created by Mukundan and Pranit."),
    (["made", "you"], "I was developed by Mukundan and Pranit using Flask and Google's Gemini AI."),
    (["your", "name"], "I'm QueryBot, your smart AI assistant!"),
    (["school", "created"], "I was built in KG International School."),
    (["how", "old"], "I'm a newly created AI assistant."),
    (["chief", "minister", "tamil"], "The Chief Minister of Tamil Nadu is C. Joseph Vijay."),
    (["cm", "tamil"], "The Chief Minister of Tamil Nadu is C. Joseph Vijay.")
    (["school", "made"], "I was built in KG International School."),
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

        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Convert to lowercase
        question = user_message.lower().strip()

        # Check keyword-based custom answers
        for keywords, answer in CUSTOM_KEYWORDS:
            if all(word in question for word in keywords):
                return jsonify({
                    "reply": answer
                })

        # Otherwise ask Gemini
        response = model.generate_content(user_message)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
