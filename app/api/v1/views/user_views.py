from flask import Blueprint, request, jsonify, make_response
import jwt, uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
from app.api.v1.utils.validations import ValidateUser
from app.api.v1.models.models import Users

user_mod = Blueprint('api',__name__)

@user_mod.route('/signup', methods=['POST'])
def user_signup():
    data = request.get_json()
    val = ValidateUser(data)
    empty = val.no_empty_field()
    name = val.username_taken()
    password = val.valid_password()
    email = val.valid_email()

    if not empty:
        return jsonify({"message" : "Please fill all the fields"}), 400

    if not name:
        return jsonify({"message" : "Username is already taken"}), 403

    if not password:
        return jsonify({"message" : "Password should have a lowercase and uppercase letter, a number and a character(@#$)"}), 400
    hashed_pass = generate_password_hash(data['password'], method="sha256")

    if not email:
        return jsonify({"message" : "Invalid email format"}), 400

    new_user = {}
    for key in data:
        new_user[key] = data[key]
    new_user["password"] = hashed_pass
    new_user['public_id'] = str(uuid.uuid4())
    new_user['admin'] = False

    latest_user = Users[-1]
    latest_user_id = latest_user['id'][len('user-00'):]
    new_user_id = int(latest_user_id) + 1

    new_user['id'] = 'user-00' + str(new_user_id)

    Users.append(new_user)
    return jsonify({"New User" : new_user})




