import json
import unittest

from models.abc import db
from repositories import ProductRepository, UserRepository, CartRepository, OrderAddressRepository, OrderRepository, CategoryRepository
from server import server
from flask.json import jsonify


class TestOrders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.config['SERVER_NAME'] = 'localhost:5053'
        cls.client = server.test_client()

    def setUp(self):
        self.app_context = server.app_context()
        self.app_context.push()
        self.maxDiff = None
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get(self):
        category = CategoryRepository.create("test2")
        product = ProductRepository.create("test", 1, category.id, "new", "Product Details")
        ProductRepository.create_image(["test1", "test2"], product.id)

        user = UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "seller")
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

        self.client.post(
            "/order",
            headers={"Authentication": self.token["token"]},
            data=json.dumps({
                "shipping_method" : "regular",
                "shipping_address": {
                    "name": "auli",
                    "phone_number": "12345678",
                    "address": "Jalan1234",
                    "city": "malang"
                }
            }),
            content_type="application/json"
        )

        order = OrderRepository.get_by(user_id=user.id).first()
        item = order.order_items[0]

        response = self.client.get(
            "/orders",
            headers={"Authentication": self.token["token"]},
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "data": [{
                    "id": str(order.id),
                    "created_at": f"{order.created_at:%a, %d %b %Y %H:%M:%S} GMT",
                    "shipping_method": order.shipping_method,
                    "status": order.status,
                    "user_id": str(order.user_id),
                    "email": order.user.email,
                    "total": order.total_price,
                    "products": [{
                        "id": str(item.product.id),
                        "details": {
                            "quantity": item.quantity,
                            "size": item.size,
                        },
                        "price": item.price,
                        "image": [image.image for image in item.product.product_images],
                        "name":item.product.title,
                    }]
                }],
            }
        )


class TestOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.config['SERVER_NAME'] = 'localhost:5053'
        cls.client = server.test_client()

    def setUp(self):
        self.app_context = server.app_context()
        self.app_context.push()
        self.maxDiff = None
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

        self.client.post(
            "/order",
            headers={"Authentication": self.token["token"]},
            data=json.dumps({
                "shipping_method" : "regular",
                "shipping_address": {
                    "name": "auli",
                    "phone_number": "12345678",
                    "address": "Jalan1234",
                    "city": "malang"
                }
            }),
            content_type="application/json"
        )

        order = OrderRepository.get_by(user_id=user.id).first()
        item = order.order_items[0]

        response = self.client.get(
            "/order",
            headers={"Authentication": self.token["token"]},
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "data": [{
                    "id": str(order.id),
                    "created_at": f"{order.created_at:%a, %d %b %Y %H:%M:%S} GMT",
                    "shipping_method": order.shipping_method,
                    "status": order.status,
                    "products": [{
                        "id": str(item.product.id),
                        "details": {
                            "quantity": item.quantity,
                            "size": item.size,
                        },
                        "price": item.price,
                        "image": item.product.product_images[0].image,
                        "name":item.product.title,
                    }]
                }],
            }
        )

    def test_post(self):
        category = CategoryRepository.create("test2")
        product = ProductRepository.create("test", 1, category.id, "new", "Product Details")
        ProductRepository.create_image(["test1", "test2"], product.id)

        user = UserRepository.create("test", "test@gmail.com", "12345678", "12345678", "buyer")
        UserRepository.create("test2", "test2@gmail.com", "12345678", "12345678", "seller")
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

        response = self.client.post(
            "/order",
            headers={"Authentication": self.token["token"]},
            data=json.dumps({
                "shipping_method" : "regular",
                "shipping_address": {
                    "name": "auli",
                    "phone_number": "12345678",
                    "address": "Jalan1234",
                    "city": "malang"
                }
            }),
            content_type="application/json"
        )

        self.assertEqual(
            json.loads(response.data.decode("utf-8")),
            {
                "message": "Order Created",
            }
        )
