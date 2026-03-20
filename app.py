from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load dataset
with open("dataset.json") as f:
    data = json.load(f)

def get_response(user_input):
    user_input = user_input.lower()

    # Emergency check
    if "chest pain" in user_input or "severe" in user_input:
        return "This may be serious. Please seek medical help immediately."

    for item in data:
        for keyword in item["keywords"]:
            if keyword in user_input:
                return item["response"]

    return "I'm not sure. Please consult a doctor."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    response = get_response(user_msg)
    return jsonify({"reply": response})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)