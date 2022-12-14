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

        UserRepository.create(user_data["name"], user_data["email"],
                              user_data["phone_number"], user_data["password"], user_data["type"])

        login_user = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type="application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        response = self.client.get(
            "/user",
            headers={
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

        UserRepository.create(user_data["name"], user_data["email"],
                              user_data["phone_number"], user_data["password"], user_data["type"])

        login_user = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type="application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        response = self.client.post(
            "/user/shipping_address",
            headers={
                "Authentication": self.token
            },
            data=json.dumps({
                "name": address_data["name"],
                "phone_number": address_data["phone_number"],
                "address": address_data["address"],
                "city": address_data["city"]
            }),
            content_type="application/json"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": address_data,
                'message': 'Update shipping address success'
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

        UserRepository.create(user_data["name"], user_data["email"],
                              user_data["phone_number"], user_data["password"], user_data["type"])

        login_user = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type="application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        user_id = UserRepository.get_by_email(user_data["email"]).id

        data = {
            "id": str(user_id),
            "name": address_data["name"],
            "phone_number": address_data["phone_number"],
            "address": address_data["address"],
            "city": address_data["city"]
        }

        self.client.post(
            "/user/shipping_address",
            headers={
                "Authentication": self.token
            },
            data=json.dumps({
                "name": address_data["name"],
                "phone_number": address_data["phone_number"],
                "address": address_data["address"],
                "city": address_data["city"]
            }),
            content_type="application/json"
        )

        response = self.client.get(
            "/user/shipping_address",
            headers={
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


class TestBalance(unittest.TestCase):
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

        UserRepository.create(user_data["name"], user_data["email"],
                              user_data["phone_number"], user_data["password"], user_data["type"])
        user = UserRepository.get_by_email(user_data["email"])

        self.assertEqual(user.balance, 0)

        login_user = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type="application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        response = self.client.post(
            "/user/balance",
            headers={
                "Authentication": self.token
            },
            data=json.dumps({
                "amount": 10000
            }),
            content_type="application/json"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "message": "Top up balance success"
            }
        )

        self.assertEqual(user.balance, 10000)

    def assert_get(self):

        response = self.client.get(
            "/user/balance",
            headers={
                "Authentication": self.token
            }
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": self.data
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

        UserRepository.create(user_data["name"], user_data["email"],
                              user_data["phone_number"], user_data["password"], user_data["type"])

        self.data = {
            "balance": 0
        }

        login_user = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email": user_data["email"],
                "password": user_data["password"]
            }),
            content_type="application/json"
        )

        self.token = json.loads(login_user.data.decode("utf-8"))["token"]

        self.assert_get()

        self.client.post(
            "/user/balance",
            headers={
                "Authentication": self.token
            },
            data=json.dumps({
                "amount": 10000
            }),
            content_type="application/json"
        )

        self.data["balance"] += 10000

        self.assert_get()


class TestSales(unittest.TestCase):
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

    def assert_get(self):

        response = self.client.get(
            "/sales",
            headers={
                "Authentication": self.token
            }
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": self.data
            }
        )

    def test_get(self):

        admin_data = {
            "name": "test",
            "email": "test@email.com",
            "phone_number": "081234567890",
            "password": "password",
            "type": "seller"
        }

        UserRepository.create(admin_data["name"], admin_data["email"],
                              admin_data["phone_number"], admin_data["password"], admin_data["type"])
        admin = UserRepository.get_by_email(admin_data["email"])

        self.data = {
            "total": 0
        }

        login_admin = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email": admin_data["email"],
                "password": admin_data["password"]
            }),
            content_type="application/json"
        )

        self.token = json.loads(login_admin.data.decode("utf-8"))["token"]

        self.assert_get()

        self.data["total"] += 10000
        UserRepository.update(admin.id, balance=self.data["total"])

        self.assert_get()
