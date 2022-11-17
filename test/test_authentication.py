import json
import unittest
from urllib import response

from models import Category, Banner
from models.abc import db
from repositories import UserRepository
from server import server
from flask.json import jsonify


class TestSignIn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.config['SERVER_NAME'] = 'localhost:5053'
        cls.client = server.test_client()

    def setUp(self):
        self.app_context = server.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post(self):
        
        user_data = {
            "name": "test",
            "email": "test@email.com",
            "phone_number": "081234567890",
            "password": "password",
            "type": "buyer"
        }
        
        UserRepository.create(user_data["name"], user_data["email"], user_data["phone_number"], user_data["password"], user_data["type"])

        response = self.client.post(
            "/sign-in",
            data = json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type = "application/json"
        )

        response_json = json.loads(response.data.decode("utf-8"))
        token = response_json['token']

        user_information = {
            "name": user_data["name"],
            "email": user_data["email"],
            "phone_number": user_data["phone_number"],
            "type": user_data["type"]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "user_information": user_information,
                "token": token,
                "message": "Login success"
            }
        )


class TestSignUp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.config['SERVER_NAME'] = 'localhost:5053'
        cls.client = server.test_client()

    def setUp(self):
        self.app_context = server.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post(self):
        
        user_data = {
            "name": "test",
            "email": "test@email.com",
            "phone_number": "081234567890",
            "password": "password",
            "type": "buyer"
        }

        response = self.client.post(
            "/sign-up",
            data = json.dumps({
                "email": user_data["email"],
                "password": user_data["password"],
                "name": user_data["name"],
                "phone_number": user_data["phone_number"],
                "type": user_data["type"]
            }),
            content_type = "application/json"
        )

        user = UserRepository.get_by_email(user_data["email"])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Success, user created",
            }
        )
        self.assertEqual(user.name, user_data["name"])
