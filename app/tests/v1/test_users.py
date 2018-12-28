import unittest
import os
from app import create_app
import json
import pytest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

        self.data2 = {
            "username":"trevor",
            "email":"trevbk@gmail.com",
            "password":"$$22BBkk"
        }

        self.data1 = {}

        self.data3 = {
            "name":"",
            "password" :"",
            "emal":""
        }

        self.data4 = {
            "username":"nnskks",
            "password" :"",
            "email":""
        }

        self.data5 = {
            "username":"bkzone",
            "password" :"233gsis",
            "email":"trev@burudi.com"
        }
        
        self.data6 = {
            "username":"bkzone",
            "password" :"233gsisBB#$",
            "email":"trevburudi.com"
        }

    def tearDown(self):
        pass

class TestUser(BaseTest):
    def test_no_signup_info(self):
        response = self.client.post('api/v1/auth/signup', data=json.dumps(self.data1),content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"],"No data found")
        self.assertEqual(response.status_code, 400)

    def test_missing_signup_fields(self):
        response = self.client.post('api/v1/auth/signup', data=json.dumps(self.data3),content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"],"Missing either the username, password or email fields")
        self.assertEqual(response.status_code, 400)

    def test_empty_signup_fieldvalues(self):
        response = self.client.post('api/v1/auth/signup', data=json.dumps(self.data4),content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"],"All fields must be filled")
        self.assertEqual(response.status_code, 400)

    def test_signup_invalid_password(self):
        response = self.client.post('api/v1/auth/signup', data=json.dumps(self.data5),content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"],"Password should have a lowercase and uppercase letter, a number and a character(@#$)")
        self.assertEqual(response.status_code, 400)

    def test_signup_invalid_email(self):
        response = self.client.post('api/v1/auth/signup', data=json.dumps(self.data6),content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["message"],"Invalid email format")
        self.assertEqual(response.status_code, 400)

    def test_signup_successful(self):
        response = self.client.post('api/v1/auth/signup', data=json.dumps(self.data2),content_type="application/json")
        self.assertEqual(response.status_code, 201)



if __name__ == "__main__":
    unittest.main()