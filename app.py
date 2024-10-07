# app.py (Backend using Flask)
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"

# Store the user's answers for dynamic question generation
game_state = {
    "questions": [],
    "answers": []
}

# Route to generate the next question
@app.route('/generate_question', methods=['POST'])
def generate_question():
    # Get the user's previous answers
    data = request.get_json()
    question_history = data.get("history", "")

    prompt = f"Based on the following answers, generate the next best question for guessing the entity:\n{question_history}\nNext question:"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=50
    )

    question = response.choices[0].text.strip()
    return jsonify({"question": question})

# Route to guess the entity based on the answers
@app.route('/guess_entity', methods=['POST'])
def guess_entity():
    data = request.get_json()
    answers = data.get("answers", "")
    
    prompt = f"Based on the following answers, guess the entity:\n{answers}\nGuess:"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100
    )

    guess = response.choices[0].text.strip()
    return jsonify({"guess": guess})

# Route to learn a new entity (when incorrect)
@app.route('/learn_new_entity', methods=['POST'])
def learn_new_entity():
    data = request.get_json()
    entity_description = data.get("entity_description", "")

    prompt = f"Add the following entity to the database:\n{entity_description}\nCreate an entry with its main traits."
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )

    learning_output = response.choices[0].text.strip()
    return jsonify({"learning_output": learning_output})

if __name__ == '__main__':
    app.run(debug=True)
