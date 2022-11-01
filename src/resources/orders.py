from flask_restful import Resource
from models import order
from utils import parse_params, response
from flask_restful.reqparse import Argument

from utils import parse_params, response, token_required, get_shipping_fee
from repositories import OrderRepository, CartRepository, UserRepository


class OrdersResource(Resource):
    """Orders Resource"""

    @parse_params(
        Argument("shipping_method", location="json", required=True,
                 help="Shipping method is required"),
        Argument("shipping_address", location="json", required=True,
                 help="Shipping address is required"),
    )
    @token_required
    def post(self, shipping_method, shipping_address, user_id):
        """Create an order"""
        user_carts = CartRepository.get_by(user_id=user_id).all()

        if not user_carts:
            return response({"message": "Cart is empty"}, 400)

        total_price = 0
        for cart in user_carts:
            total_price += cart.price

        # user = UserRepository.get_by_id(user_id)
        # if user.balance < total_price:
        #     return response({"message": "Insufficient balance"}, 400)

        shipping_fee = get_shipping_fee(total_price, shipping_method)

        order = OrderRepository.create(user_id, total_price, shipping_fee , shipping_method)

        OrderRepository.create_order_item(user_carts, order.id)

        CartRepository.delete_all(user_carts)

        return response({"message": "Order Created"}, 201)


class OrderResource(Resource):
    @token_required
    def get(self, user_id):
        orders = OrderRepository.get_by(user_id=user_id).all()

        res = [
            {
                "id": order.id,
                "created_at": order.created_at,
                "shipping_method": order.shipping_method,
                "status": order.status,
                "products": [{
                    "id": item.product.id,
                    "details": {
                        "quantity": item.quantity,
                        "size": item.size,
                    },
                    "price": item.price,
                    "image": item.product.product_images[0].image,
                    "name":item.product.title,
                } for item in order.order_items],
            } for order in orders
        ]

        return response({"data": res}, 200)
