from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

# Define career options based on score ranges
def calculate_recommendation(data):
    # Initialize scores for different career paths
    scores = {
        "Data Scientist": 0,
        "Software Engineer": 0,
        "Marketing Specialist": 0,
        "Graphic Designer": 0
    }

    # Define scoring based on answers
    scoring = {
        "q1": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q2": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q3": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q4": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q5": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q6": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q7": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q8": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q9": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q10": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        }
    }

    # Calculate scores based on user answers
    for question, answer in data.items():
        if question in scoring:
            career = scoring[question].get(answer)
            if career:
                scores[career] += 1

    # Determine the highest scoring career
    recommendation = max(scores, key=scores.get)

    return recommendation


@app.route('/submit', methods=['POST'])
def submit_quiz():
    data = request.json
    # Process the data to determine recommendation
    recommendation = calculate_recommendation(data)
    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True)
