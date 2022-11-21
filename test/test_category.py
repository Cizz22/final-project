import json
import unittest

from models.abc import db
from repositories import CategoryRepository, UserRepository
from server import server

class TestCategory(unittest.TestCase):

    user_data = {
            "name": "test",
            "email": "test@email.com",
            "phone_number": "081234567890",
            "password": "password",
            "type": "seller"
        }

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

    def get_token(self):
        UserRepository.create(self.user_data["name"], self.user_data["email"], self.user_data["phone_number"], self.user_data["password"], self.user_data["type"])

        login_admin = self.client.post(
            "/sign-in",
            data = json.dumps({
                "email": self.user_data["email"],
                "password": self.user_data["password"]
            }),
            content_type = "application/json"
        )

        token = json.loads(login_admin.data.decode("utf-8"))["token"]

        return token

    def test_get(self):

        CategoryRepository.create("Category A")
        CategoryRepository.create("Category B")

        categories = CategoryRepository.get_all()

        data = [
            {
                "id": str(category.id),
                "title": category.title
            } for category in categories
        ]

        response = self.client.get(
            "/categories"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": data
            }
        )