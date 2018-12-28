import unittest
import os
from app import create_app
import json

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

        self.data1 = {
            "username":"trevor",
            "email":"trevbk@gmail.com",
            "password":"$$22BBkk"
        }

        self.data2 = {}

        self.data3 = {
            "name":"",
            "password" :"",
            "email":""
        }

        self.data4 = {
            "username":"",
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
        response = self.client.post('api/v1/auth/signup')
        result = json.loads(response.data)
        self.assertEqual(result["message"],"No data found")
        self.assertEqual(response.status_code, 400)



if __name__ == "__main__":
    unittest.main()