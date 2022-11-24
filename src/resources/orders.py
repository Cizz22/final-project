from flask_restful import Resource
from utils import parse_params, response
from flask_restful.reqparse import Argument

from utils import parse_params, response, token_required, get_shipping_fee, admin_required
from repositories import OrderRepository, CartRepository, UserRepository, OrderAddressRepository


class OrdersResource(Resource):
    """Orders Resource"""
    @parse_params(
        Argument("sort_by", location="args", required=False),
        Argument("page", location="args", required=False, default=1),
        Argument("page_size", location="args", required=False, default=10),
    )
    @admin_required
    def get(self, sort_by, page, page_size, user_id):
        """Get all orders"""

        orders = OrderRepository.get_query(sort_by, page, page_size)

        res = {
            "data": [
                {
                    "id": order.id,
                    "created_at": order.created_at,
                    "shipping_method": order.shipping_method,
                    "status": order.status,
                    "user_id": order.user_id,
                    "email": order.user.email,
                    "total": order.total_price,
                    "products": [{
                        "id": item.product.id,
                        "details": {
                            "quantity": item.quantity,
                            "size": item.size,
                        },
                        "price": item.price,
                        "image": [image.image for image in item.product.product_images],
                        "name":item.product.title,
                    } for item in order.order_items],
                } for order in orders['data']
            ]}

        return response(res, 200)


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

    @parse_params(
        Argument("shipping_method", location="json", required=True,
                 help="Shipping method is required"),
        Argument("shipping_address", location="json", required=True,
                 help="Shipping address is required", type=dict),
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

        user = UserRepository.get_by_id(user_id)
        if user.balance < total_price:
            return response({"message": "Insufficient balance"}, 400)

        shipping_fee = get_shipping_fee(total_price, shipping_method)

        order = OrderRepository.create(user_id, total_price, shipping_fee , shipping_method)

        OrderRepository.create_order_item(user_carts, order.id)

        OrderAddressRepository.create(order.id, shipping_address)

        CartRepository.delete_all(user_carts)

        return response({"message": "Order Created"}, 201)
