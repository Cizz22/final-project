import json
import unittest

from models.abc import db
from repositories import ProductRepository, UserRepository, CartRepository, OrderAddressRepository, OrderRepository, CategoryRepository
from server import server
from flask.json import jsonify
from utils import get_shipping_fee


class TestShippingPrice(unittest.TestCase):
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
        UserRepository.update(user.id, balance=100000)

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
            "/shipping_price",
            headers={"Authentication": self.token["token"]},
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "data": [{
                    "name": "regular",
                    "price": get_shipping_fee(1000, "regular")
                },
                    {
                    "name": "next day",
                    "price": get_shipping_fee(1000, "next day")
                }]
            }
        )
