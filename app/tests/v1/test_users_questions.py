import unittest
import os
from app import create_app
import json
import pytest


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

        self.empty_question = {}

        self.data2 = {
            "username": "trevor",
            "email": "trevbk@gmail.com",
            "password": "$$22BBkk"
        }

        self.question = {
            "title": "A good question",
            "text": "Can I ask It now?"
        }

        self.no_title = {
            "text": "No title found"
        }

        self.no_title_or_text_keys = {
            "": ""
        }

        self.no_desc_text = {
            "title": "No title found"
        }

        self.empty_title_and_text = {
            "title": "",
            "text": ""
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

    def test_no_question_content(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.empty_question), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn(result["message"], "Cannot be empty")

    def test_no_question_title(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.no_title), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn(result["message"],
                      "Either title and text data fields are missing")

    def test_no_question_description_test(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.no_desc_text), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn(result["message"],
                      "Either title and text data fields are missing")

    def test_no_title_or_question_description_text(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.no_title_or_text_keys), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn(result["message"],
                      "Both title and text description are required")

    def test_empty_title_and_text(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.empty_title_and_text), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertIn(result["message"],
                      "Both title and text fields must be filled")

    def test_asked_succesfully(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.question), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_missing_title(self):
        pass
