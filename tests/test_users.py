import unittest
from app import create_app
import json

class Basetest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

        self.data1 = {
            "username":"trevor",
            "email":"trevbk@gmail.com",
            "password":"$$22BBkk"
        }



if __name__ == "__main__":
    unittest.main()