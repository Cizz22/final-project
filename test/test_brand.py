import json
import unittest

from models.abc import db
from repositories import BrandRepository, UserRepository
from server import server

class TestBrand(unittest.TestCase):

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

        BrandRepository.create("Brand A")
        BrandRepository.create("Brand B")

        brands = BrandRepository.get_all()

        data = [
            {
                "id": str(brand.id),
                "title": brand.title
            } for brand in brands
        ]

        response = self.client.get(
            "/brands"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "data": data
            }
        )

    def test_post(self):

        token = self.get_token()

        response = self.client.post(
            "/brands",
            headers = {
                "Authentication": token
            },
            data = json.dumps({
                "brand_name": "Brand A"
            }),
            content_type = "application/json"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        brand = BrandRepository.get_by(title="Brand A").one_or_none()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json,
            {
                "message": "Brand added"
            }
        )
        self.assertEqual(brand.title, "Brand A")

    def test_put(self):

        BrandRepository.create("Brand A")
        brand = BrandRepository.get_by(title="Brand A").one_or_none()
        brand_id = str(brand.id)

        token = self.get_token()

        response = self.client.put(
            f"/brands/{brand_id}",
            headers = {
                "Authentication": token
            },
            data = json.dumps({
                "brand_name": "Brand B"
            }),
            content_type = "application/json"
        )

        response_json = json.loads(response.data.decode("utf-8"))

        new_brand = BrandRepository.get_by(id=brand_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "message": "Brand updated"
            }
        )
        self.assertEqual(new_brand.title, "Brand B")

    def test_delete(self):

        BrandRepository.create("Brand A")
        brand = BrandRepository.get_by(title="Brand A").one_or_none()
        brand_id = str(brand.id)

        token = self.get_token()

        response = self.client.delete(
            f"/brands/{brand_id}",
            headers = {
                "Authentication": token
            }
        )

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "message": "Brand deleted"
            }
        )
        self.assertNotEqual(brand.deleted_at, None)