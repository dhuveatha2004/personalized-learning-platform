from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import chardet
import os

project_path = "D:/xampp/htdocs/Project"
app = Flask(__name__, template_folder=project_path)
CORS(app)

csv_path = os.path.join(project_path, "Datasets.csv")
unanswered_csv = os.path.join(project_path, "Unanswered.csv")

def load_dataset():
    try:
        with open(csv_path, "rb") as f:
            result = chardet.detect(f.read())
            df = pd.read_csv(csv_path, encoding=result["encoding"], on_bad_lines="skip")
            df["Question"] = df["Question"].astype(str).str.lower().str.strip()
            return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=["Question", "Answer"])

df = load_dataset()

def load_unanswered():
    if os.path.exists(unanswered_csv):
        return pd.read_csv(unanswered_csv, encoding="utf-8")["Question"].tolist()
    return []

unanswered_questions = set(load_unanswered())
harmful_words = ["kill", "harm", "attack", "hate", "terror", "bomb", "violence", "abuse", "threat"]

def contains_harmful_words(text):
    return any(word in text for word in harmful_words)

@app.route("/")
def home():
    return "<h1>Chatbot API is running!</h1>"

@app.route("/chatbot", methods=["POST"])
def chatbot():
    global df, unanswered_questions
    data = request.json
    user_question = data.get("question", "").strip().lower()
    if not user_question:
        return jsonify({"answer": "Please enter a valid question."})
    if contains_harmful_words(user_question):
        return jsonify({"answer": "Sorry, I cannot process harmful or inappropriate content."})
    
    response = df[df["Question"] == user_question]["Answer"].values
    if len(response) > 0:
        return jsonify({"answer": response[0]})
    
    if user_question not in unanswered_questions:
        unanswered_questions.add(user_question)
        pd.DataFrame({"Question": list(unanswered_questions)}).to_csv(unanswered_csv, index=False, encoding="utf-8")
    
    return jsonify({"answer": "I don't understand. Can you teach me the answer?", "teach": True, "question": user_question})

@app.route("/teach", methods=["POST"])
def teach():
    global df, unanswered_questions
    data = request.json
    user_question = data.get("question", "").strip().lower()
    user_answer = data.get("answer", "").strip()

    if not user_question or not user_answer:
        return jsonify({"message": "Invalid input. Provide both question and answer."})
    if contains_harmful_words(user_question) or contains_harmful_words(user_answer):
        return jsonify({"message": "Cannot learn harmful or inappropriate content."})

    if user_question in df["Question"].values:
        df.loc[df["Question"] == user_question, "Answer"] = user_answer
        message = f"Updated answer for: '{user_question}'"
    elif user_question in unanswered_questions:
        df = pd.concat([df, pd.DataFrame([[user_question, user_answer]], columns=["Question", "Answer"])], ignore_index=True)
        unanswered_questions.remove(user_question)
        message = f"Thank you! I've learned the answer for: '{user_question}'."
    else:
        return jsonify({"message": "This question was not previously asked, so I cannot attach an answer."})
    
    df.to_csv(csv_path, index=False, encoding="utf-8")
    pd.DataFrame({"Question": list(unanswered_questions)}).to_csv(unanswered_csv, index=False, encoding="utf-8")
    return jsonify({"message": message})

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
