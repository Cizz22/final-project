import json
import unittest

from models.abc import db
from repositories import CartRepository, UserRepository, CategoryRepository, ProductRepository
from server import server
from flask.json import jsonify


class TestCarts(unittest.TestCase):
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
        category = CategoryRepository.create("test2")
        product = ProductRepository.create("test", 1, category.id, "new", "Product Details")
        ProductRepository.create_image(["test1", "test2"], product.id)

        user = UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "buyer")

        login_users = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email" : "test@gmail.com",
                "password" : "12345678",
            }),
            content_type="application/json"
        )
        self.token = json.loads(login_users.data.decode("utf-8"))

        cart = CartRepository.create(user.id, product.id, "S", 1, 1000)

        response = self.client.get("/cart", headers={"Authentication": self.token["token"]})
        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "data": [
                    {
                        "id": str(cart.id),
                        "details": {
                            "quantity": cart.quantity,
                            "size": cart.size,
                        },
                        "price": cart.price,
                        "image": cart.product.product_images[0].image,
                        "name": cart.product.title,
                    }
                ]
            }
        )

    def test_post(self):
        category = CategoryRepository.create("test2")
        product = ProductRepository.create("test", 1, category.id, "new", "Product Details")
        ProductRepository.create_image(["test1", "test2"], product.id)

        user = UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "buyer")

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
            "/cart",
            headers={"Authentication": self.token['token']},
            data=json.dumps({
                "id": str(product.id),
                "quantity": 1,
                "size": "S"
            }),
            content_type="application/json"
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Item success added to cart",
            }
        )
        self.assertEqual(CartRepository.get_by().count(), 1)


class TestCart(unittest.TestCase):
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
        category = CategoryRepository.create("test2")
        product = ProductRepository.create("test", 1, category.id, "new", "Product Details")
        ProductRepository.create_image(["test1", "test2"], product.id)

        user = UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "buyer")

        login_users = self.client.post(
            "/sign-in",
            data=json.dumps({
                "email" : "test@gmail.com",
                "password" : "12345678",
            }),
            content_type="application/json"
        )
        self.token = json.loads(login_users.data.decode("utf-8"))

        cart = CartRepository.create(user.id, product.id, "S", 1, 1000)

        response = self.client.get(
            f"/cart/{str(cart.id)}",
            headers={"Authentication": self.token['token']}
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Cart deleted",
            }
        )
