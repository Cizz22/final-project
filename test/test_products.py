import json
import unittest
from models.abc import db
from server import server
from flask.json import jsonify

from repositories import ProductRepository, CategoryRepository, UserRepository


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
        self.category = CategoryRepository.create("test2")
        product = ProductRepository.create("test", 1, self.category.id, "new", "Product Details")
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
                    "image": "image/test1",
                }],
                "total_rows": 1,
            }
        )

    def test_post(self):
        self.category = CategoryRepository.create("test2")
        UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "seller")
        login_users = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email" : "test@gmail.com",
                "password" : "12345678",
            }),
            content_type="application/json"
        )
        self.token = json.loads(login_users.data.decode("utf-8"))

        response = self.client.post(
            "/products",
            headers={"Authentication": self.token['token']},
            data=json.dumps({
                "product_name": "test",
                "description": "Product Details",
                "price": 1,
                "condition": "new",
                "category": str(self.category.id),
                "images": ["data:image/png;base64,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"],
            }),
            content_type="application/json",
        )
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Product added",
            }
        )
        self.assertEqual(ProductRepository.get_by().count(), 1)

    def test_put(self):
        category = CategoryRepository.create("test2")
        UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "seller")

        login_users = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email" : "test@gmail.com",
                "password" : "12345678",
            }),
            content_type="application/json"
        )
        self.token = json.loads(login_users.data.decode("utf-8"))

        product = ProductRepository.create("test", 10000, category.id, "new", "test")
        images = ProductRepository.create_image(["test1.jpg", "test2.jpg"], product.id)

        response = self.client.put(
            "/products",
            headers={"Authentication": self.token['token']},
            data=json.dumps({
                "product_id": str(product.id),
                "title": "testedit",
                "images": ["data:image/png;base64,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"],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Product updated",
            }
        )


class TestProduct(unittest.TestCase):
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
        product = ProductRepository.create("test", 100, category.id , "new", "test")
        images = ProductRepository.create_image(["test1.jpg", "test2.jpg"], product.id)

        response = self.client.get(f"/products/{str(product.id)}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {"data": {
                "id": str(product.json['id']),
                "title": product.json['title'],
                "size": ["S", "M", "L"],
                "product_detail": product.json['product_detail'],
                "price": product.json['price'],
                "images_url": [product_image.json['image'] for product_image in product.product_images],
            }
            }
        )

    def test_delete(self):
        category = CategoryRepository.create("test2")
        UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "seller")

        login_users = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email" : "test@gmail.com",
                "password" : "12345678",
            }),
            content_type="application/json"
        )
        self.token = json.loads(login_users.data.decode("utf-8"))

        product = ProductRepository.create("test", 10000, category.id, "new", "test")
        images = ProductRepository.create_image(["test1.jpg", "test2.jpg"], product.id)

        response = self.client.delete(
            f"/products/{str(product.id)}", headers={"Authentication": self.token["token"]})

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Product deleted",
            }
        )

class TestProductImageSearch(unittest.TestCase):
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
        category = CategoryRepository.create("Hat")
        
        response = self.client.post(
            "/products/search_image",
            data=json.dumps({
                "image": "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"
            }),
            content_type="application/json"
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "category_id": str(category.id),
            }
        )
