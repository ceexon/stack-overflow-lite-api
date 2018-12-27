from flask import Blueprint, request, jsonify
from app.api.v1.models.models import Users, Questions
from app.api.v1.utils.validations import token_required

v1_mod = Blueprint('QA', __name__)

@v1_mod.route('/question', methods=['POST'])
@token_required
def post_question(current_user):
    data = request.get_json()
    if data["title"] == "" or data["text"] == "":
        return jsonify({"message" : "Both title and text description are required"}), 400
    for user in Users:
        if user['public_id'] == current_user:
            data["user-id"] = user["id"]
            break

    data["accept"] = False
    latest_quiz = Questions[-1]
    latest_quiz_id = latest_quiz["q_id"]
    latest_quiz_id = latest_quiz_id[len('quiz-00'):]
    latest_quiz_id = int(latest_quiz_id) + 1
    latest_quiz_id = 'quiz-00' + str(latest_quiz_id)
    data["q_id"] = latest_quiz_id
    
    Questions.append(data)

    return jsonify({"New Question" : data})

@v1_mod.route('/question', methods=['GET'])
def get_all_questions():
    return jsonify({"Questions": Questions})

