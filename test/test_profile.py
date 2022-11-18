import json
import unittest

from models.abc import db
from repositories import UserRepository
from server import server

class TestUser(unittest.TestCase):
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
    
    def test_get(self):

        user_data = {
            "name": "test",
            "email": "test@email.com",
            "phone_number": "081234567890",
            "password": "password",
            "type": "buyer"
        }

        data = {
            "name": user_data["name"],
            "email": user_data["email"],
            "phone_number": user_data["phone_number"]
        }
        
        UserRepository.create(user_data["name"], user_data["email"], user_data["phone_number"], user_data["password"], user_data["type"])

        login_user = self.client.post(
            "/sign-in",
            data = json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type = "application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        response = self.client.get(
            "/user",
            headers = {
                "Authentication": self.token
            }
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": data
            }
        )

class TestShippingAddress(unittest.TestCase):
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

        address_data = {
            "name": "address name",
            "phone_number": "087654321098",
            "address": "address detail",
            "city": "Birnin Zana"
        }

        UserRepository.create(user_data["name"], user_data["email"], user_data["phone_number"], user_data["password"], user_data["type"])

        login_user = self.client.post(
            "/sign-in",
            data = json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type = "application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        response = self.client.post(
            "/user/shipping_address",
            headers = {
                "Authentication": self.token
            },
            data = json.dumps({
                "name": address_data["name"],
                "phone_number": address_data["phone_number"],
                "address": address_data["address"],
                "city": address_data["city"]
            }),
            content_type = "application/json"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": address_data
            }
        )

    def test_get(self):

        user_data = {
            "name": "test",
            "email": "test@email.com",
            "phone_number": "081234567890",
            "password": "password",
            "type": "buyer"
        }

        address_data = {
            "name": "address name",
            "phone_number": "087654321098",
            "address": "address detail",
            "city": "Birnin Zana"
        }

        UserRepository.create(user_data["name"], user_data["email"], user_data["phone_number"], user_data["password"], user_data["type"])

        login_user = self.client.post(
            "/sign-in",
            data = json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type = "application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        user_id = UserRepository.get_by_email(user_data["email"]).id

        data = {
            "id": str(user_id),
            "name":address_data["name"],
            "phone_number": address_data["phone_number"],
            "address": address_data["address"],
            "city": address_data["city"]
        }

        self.client.post(
            "/user/shipping_address",
            headers = {
                "Authentication": self.token
            },
            data = json.dumps({
                "name": address_data["name"],
                "phone_number": address_data["phone_number"],
                "address": address_data["address"],
                "city": address_data["city"]
            }),
            content_type = "application/json"
        )

        response = self.client.get(
            "/user/shipping_address",
            headers = {
                "Authentication": self.token
            }
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": data
            }
        )
