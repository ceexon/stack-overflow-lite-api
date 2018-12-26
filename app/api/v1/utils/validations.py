from app.api.v1.models.models import Users
from flask import jsonify
import re

EMAIL_REGEX = re.compile(r'(\w+[.|\w])*@(\w+[.])*\w+')
PASSWORD_REGEX = re.compile(r'[A-Za-z0-9@#$%^&+=]{6,}')

class ValidateUser():
    """ This class validates data input by a user for creating an account"""
    def __init__(self, user_data):
        self.user_data = user_data

    def no_empty_field(self):
        for key in self.user_data:
            if self.user_data[key] == "" or self.user_data[key].strip() == "":
                return False
        return True

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
        if not re.match(PASSWORD_REGEX, self.user_data["password"]):
            return False
        
        return True

            