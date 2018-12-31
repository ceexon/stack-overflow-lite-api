import unittest
import os
from app import create_app
import json
import pytest


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

        self.data1 = {}

        self.data2 = {
            "username": "trevor",
            "email": "trevbk@gmail.com",
            "password": "$$22BBkk"
        }

        self.question = {
            "title": "A good question",
            "text": "Can I ask It now?"
        }

    def tearDown(self):
        pass


class TestQuestion(BaseTest):
    def login(self):
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.data2), content_type="application/json")
        self.token = json.loads(login.data.decode('utf-8'))
        self.token = self.token["token"]
        return self.token

    def test_question_asked_not_loged_in(self):
        response = self.client.post(
            'api/v1/question', data=json.dumps(self.question), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Token is missing")
        self.assertEqual(response.status_code, 401)

    def test_asked_succesfully(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.question), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_missing_title(self):
        pass
