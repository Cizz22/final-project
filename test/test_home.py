import json
import unittest

from models.abc import db
from repositories import BannerRepository, CategoryRepository
from server import server
from flask.json import jsonify


class TestBanner(unittest.TestCase):
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
        banner = BannerRepository.create("test", "test")
        response = self.client.get("/home/banner")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {"data" : [{"id": str(banner.json['id']), "image": "test", "title":"test"}, ]}
        )
class TestCategory(unittest.TestCase):

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