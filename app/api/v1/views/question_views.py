from flask import Blueprint, request, jsonify
from app.api.v1.models.models import Users, Questions, Answers
from app.api.v1.utils.validations import token_required
import time

v1_mod = Blueprint('QA', __name__)

@v1_mod.route('/question', methods=['POST'])
@token_required
def post_question(current_user):
    data = request.get_json()
    try:
        if not data:
            return jsonify({"message" : "Cannot be empt"}), 400

        if data["title"] == "" or data["text"] == "":
            return jsonify({"message" : "Both title and text description are required"}), 400
    except:
        return jsonify({"message": "Either title and text data fields are missing"}), 400

    logged_user = {}
    for user in Users:
        if user["public_id"] == current_user:
            logged_user = user
            
    if not logged_user:
        return jsonify({"message" : "user not found"}), 401

    data["username"] = logged_user["username"]
    latest_quiz = Questions[-1]
    latest_quiz_id = latest_quiz["q_id"]
    latest_quiz_id = latest_quiz_id[len('quiz-00'):]
    latest_quiz_id = int(latest_quiz_id) + 1
    latest_quiz_id = 'quiz-00' + str(latest_quiz_id)
    data["q_id"] = latest_quiz_id
    data["time"] = time.strftime("%d/%m/%Y, %H:%M")
    
    Questions.append(data)

    return jsonify({"New Question" : data})

@v1_mod.route('/question', methods=['GET'])
def get_all_questions():
    return jsonify({"Questions": Questions})

@v1_mod.route('/question/<question_id>', methods=['GET'])
def get_specific_question(question_id):
    for question in Questions:
        q_id = question['q_id']
        q_id = q_id[len('quiz-00'):]
        if q_id == question_id:
            return jsonify({"Question " + question_id : question}), 200

    return jsonify({"Invalid Question Id" : "Question not found"}), 404

@v1_mod.route('/question/<question_id>/answer', methods=['POST'])
@token_required
def answer_question(current_user, question_id):
    data = request.get_json()
    try:
        if not data:
            return jsonify({"message" : "Cannot be empt"}), 400

        if data["text"] == "":
            return jsonify({"message" : "Answer text description is required"}), 400
    except:
        return jsonify({"message": "Answer text data field is missing"}), 400

    logged_user = {}
    for user in Users:
        if user["public_id"] == current_user:
            logged_user = user
    
    if not logged_user:
        return jsonify({"message" : "user not found"}), 401

    data["username"] = logged_user["username"]

    the_question = {}
    q_ids = []
    for question in Questions:
        q_ids.append(question["q_id"])
        if question["q_id"][len("quiz-00"):] == question_id:
            the_question = question
            break

    q_id = "quiz-00" + question_id
    if q_id in q_ids:
        pass
    else:
        return jsonify({"Invalid Question Id" : "Question not found"}), 404

    for user in Users:
        if user['public_id'] == current_user:
            data["username"] = user["username"]
            break

    latest_ans = Answers[-1]
    latest_ans_id = latest_ans["ans_id"]
    latest_ans_id = latest_ans_id[len('ans-00'):]
    latest_ans_id = int(latest_ans_id) + 1
    latest_ans_id = 'ans-00' + str(latest_ans_id)
    data["ans_id"] = latest_ans_id
    data["q_id"] = the_question["q_id"]
    data["accepted"] = False

    Answers.append(data)

    return jsonify({the_question["text"]: data})

