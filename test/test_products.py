import json
import unittest
from models.abc import db
from server import server
from flask.json import jsonify

from repositories import ProductRepository, CategoryRepository


class TestProducts(unittest.TestCase):
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
        category = CategoryRepository.create("test")
        product = ProductRepository.create("test", 1, category.id, "new", "Product Details")
        images = ProductRepository.create_image(["test1", "test2"], product.id)

        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "data": [{
                    "id": str(product.json['id']),
                    "title":"test",
                    "price": 1,
                    "image": ["image/test1", "image/test2"],
                }],
                "total_rows": 1,
            }
        )
    
