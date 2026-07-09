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
    (["hello"], "Hello! Welcome to our Skill Expo. I'm QueryBot. Feel free to ask me anything."),
    (["hi"], "Hi! Welcome to our project."),
    (["good", "morning"], "Good morning! Welcome to our Skill Expo."),
    (["good", "afternoon"], "Good afternoon! Welcome to our Skill Expo."),
    (["good", "evening"], "Good evening! Welcome to our Skill Expo."),
    (["how", "are", "you"], "I'm doing great! Thanks for asking."),
    (["thank"], "You're welcome!"),
    (["bye"], "Goodbye! Thank you for visiting our project."),

    # ===== Identity =====
    (["your", "name"], "My name is QueryBot."),
    (["who", "are", "you"], "I'm QueryBot, an AI assistant built for the Skill Expo."),
    (["introduce"], "Hello! I'm QueryBot, an AI assistant created to answer questions and demonstrate the power of artificial intelligence."),

    # ===== Creators =====
    (["which", "school", "made", "you"], "I was built at KG International School by Mukundan and Pranit."),
    (["school", "created", "you"], "I was built at KG International School by Mukundan and Pranit."),
    (["school", "made"], "I was built at KG International School by Mukundan and Pranit."),
    (["who", "created", "you"], "I was created by Mukundan and Pranit."),
    (["creator"], "My creators are Mukundan and Pranit."),
    (["who", "made", "you"], "I was developed by Mukundan and Pranit."),
    (["made", "you"], "I was developed by Mukundan and Pranit."),
    (["developers"], "Mukundan and Pranit developed me."),
    (["team"], "I was built by Mukundan and Pranit."),
    (["student"], "Yes! I was built by students of KG International School."),

    # ===== School =====
    (["school", "name"], "The name of my school is KG International School."),
    (["where", "school"], "KG International School is located in Annur, Coimbatore."),
    (["kg", "international"], "KG International School is located in Annur, Coimbatore."),
    (["principal"], "The Principal of KG International School is Mrs. Kaleshwari Srilatha."),
     (["expo", "where"], "The Skill Expo is being held at Thangam International School, Salem.")
    


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
