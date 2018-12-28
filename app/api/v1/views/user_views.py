from flask import Blueprint, request, jsonify, make_response
import jwt, uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
from app.api.v1.utils.validations import ValidateUser, token_required
from app.api.v1.models.models import Users
from app import create_app

user_mod = Blueprint('api',__name__)

@user_mod.route('/signup', methods=['POST'])
def user_signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data found"}), 400

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

@user_mod.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data found"}), 400
    all_names = []
    all_passwords = []

    for user in Users:
        all_names.append(user["username"])
        all_passwords.append(user['password'])

    if data['username'] in all_names:
        login_user = {}
        for user in Users:
            if user["username"] == data["username"]:
                login_user = user
                break

        if login_user["username"] != "admin":        
            if check_password_hash(login_user["password"], data['password']):
                token = jwt.encode({"public_id": login_user['public_id'], 'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)}, create_app.config["SECRET_KEY"])
                return jsonify({"token": token.decode('UTF-8')}), 200
            return jsonify({"message": "Invalid password"}), 401

        else: 
            if login_user['password'] == data['password']:
                token = jwt.encode({"public_id": login_user['public_id'], 'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)}, create_app.config["SECRET_KEY"])
                return jsonify({"token": token.decode('UTF-8')}), 200
        return jsonify({"message": "Invalid password"}), 401

    return jsonify({"message": "username not found"}), 401 

@user_mod.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    admin_user = {}
    for user in Users:
        if user['public_id'] == current_user:
            admin_user = user
            break
            
    if not admin_user['admin']:
        return jsonify({"message" : "You cannot perform this action"}), 403
    
    return jsonify({"Users" : Users})