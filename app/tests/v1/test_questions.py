import unittest
import os
from app import create_app
import json
import pytest


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

        self.data1 = {
            "title": "The question",
            "text": "This is the question description"
        }

    def tearDown(self):
        pass


class TestQuestion(BaseTest):
    def test_question_asked_successfully(self):
        pass
