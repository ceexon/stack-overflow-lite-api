from app.api.v1.models.models import Users
from flask import jsonify, request
import re
import jwt
from functools import wraps
from app import create_app

EMAIL_REGEX = re.compile(r'(\w+[.|\w])*@(\w+[.])*\w+')
# PASSWORD_REGEX = re.compile(r'[A-Za-z0-9@#$]{6,}')

class ValidateUser():
    """ This class validates data input by a user for creating an account"""
    def __init__(self, user_data):
        self.user_data = user_data

    def username_taken(self):
        available_users = []
        for user in Users:
            available_users.append(user['username'])
        
        if self.user_data['username'] in available_users:
            return False
        
        return True

    def valid_email(self):
        email = self.user_data["email"]
        if not EMAIL_REGEX.match(email):
            return False
        
        return True

    def valid_password(self):
       p = self.user_data['password']
       while True:
            if (len(p)<6 or len(p)>50):
                return False
            elif not re.search("[a-z]",p):
                return False
            elif not re.search("[0-9]",p):
                return False
            elif not re.search("[A-Z]",p):
                return False
            elif not re.search("[$#@]",p):
                return False
            else:
                return True

            
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, create_app.config["SECRET_KEY"])
            current_user = data["public_id"]

        except:
            return jsonify({"message" : "Token is invalid or expired"}), 401

        return f(current_user, *args, **kwargs)
    return decorated