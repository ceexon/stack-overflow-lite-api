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

        self.ask_user = {
            "username": "trevor",
            "email": "trevbk@gmail.com",
            "password": "$$22BBkk"
        }

        self.fake_user = {
            "username": "trev",
            "email": "trev@gmail.com",
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

        self.empty_title = {
            "title": "",
            "text": "Title is empty"
        }

        self.empty_text = {
            "title": "Text description is empty",
            "text": ""
        }

        self.change_data = {
            "text": "this answer content was changed"
        }

    def tearDown(self):
        pass


class TestPostQuestion(BaseTest):
    def login(self):
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.ask_user), content_type="application/json")
        self.token = json.loads(login.data.decode('utf-8'))
        self.token = self.token["token"]
        return self.token

    def login_1(self):
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.fake_user), content_type="application/json")
        login1 = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.fake_user), content_type="application/json")
        self.token1 = json.loads(login1.data.decode('utf-8'))
        self.token1 = self.token1["token"]
        return self.token1

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

    def test_empty_question_title_and_text(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.empty_title_and_text), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"],
                         "Both title and text fields must be filled")

    def test_empty_question_title(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.empty_title), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"],
                         "Question Title is required")

    def test_empty_question_text_desc(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.empty_text), content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        print(result)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"],
                         "Question text description is required")

    def test_asked_succesfully(self):
        self.token = self.login()
        response = self.client.post(
            'api/v1/question', headers={'x-access-token': self.token}, data=json.dumps(self.question), content_type="application/json")
        self.assertEqual(response.status_code, 201)


class TestGetQuestion(BaseTest):
    def test_get_all_questions(self):
        response = self.client.get('api/v1/question')
        self.assertEqual(response.status_code, 200)

    def test_get_question_by_id_fail(self):
        response = self.client.get('api/v1/question/10')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['Invalid Question Id'], "Question not found")
        self.assertEqual(response.status_code, 404)

    def test_get_question_by_id_success(self):
        response = self.client.get('api/v1/question/0')
        self.assertEqual(response.status_code, 200)


class TestDeleteQuestion(TestPostQuestion):
    def test_delete_question_no_token(self):
        response = self.client.delete('api/v1/question/10')
        result = json.loads(response.data.decode('utf-8'))
        print(result)
        self.assertEqual(result['message'], "Token is missing")
        self.assertEqual(response.status_code, 401)

    def test_delete_question_invalid_user(self):
        self.token = self.login_1()
        response = self.client.delete(
            'api/v1/question/1', headers={'x-access-token': self.token})
        result = json.loads(response.data.decode('utf-8'))
        print(result)
        self.assertEqual(result["message"],
                         "You cannot delete a question you did not ask")
        self.assertEqual(response.status_code, 401)

    def test_delete_question_successful(self):
        self.token = self.login()
        response = self.client.delete(
            'api/v1/question/1', headers={'x-access-token': self.token})
        result = json.loads(response.data.decode('utf-8'))
        print(result)
        self.assertEqual(result["message"],
                         "Question has been deleted")
        self.assertEqual(response.status_code, 200)
