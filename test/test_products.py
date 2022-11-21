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
                    "image": ["image/test1", "image/test2"],
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
                "title": "test",
                "description": "Product Details",
                "price": 1,
                "condition": "new",
                "category": str(self.category.id),
                "images": ["data:image/png;base64,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"],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
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
            {
                "id": str(product.json['id']),
                "title": product.json['title'],
                "size": product.json['size'],
                "product_detail": product.json['product_detail'],
                "price": product.json['price'],
                "images_url": [product_image.json['image'] for product_image in product.product_images],
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
