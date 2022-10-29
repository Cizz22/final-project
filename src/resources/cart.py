from flask_restful import Resource
from utils import parse_params, response
from flask_restful.reqparse import Argument

from utils.jwt_verif import token_required

from repositories import ProductRepository, CartRepository


class CartsResource(Resource):
    """Carts Resource"""

    @token_required
    def get(self, user_id):
        """Get cart"""
        items = CartRepository.get_by_user_id(user_id)

        res = [
            {
                "id": item.id,
                "details": {
                    "quantity": item.quantity,
                    "size": item.size,
                },
                "price": item.price,
                "image": item.product.product_images[0].image,
                "name": item.product.title,

            } for item in items
        ]
        
        return response(res, 200)

    @parse_params(
        Argument("id", location="json", required=True,
                 help="Product ID cannot be blank.", dest="product_id"),
        Argument("quantity", location="json", required=True, help="Quantity cannot be blank."),
        Argument("size", location="json", required=True, help="Size cannot be blank."),
    )
    @token_required
    def post(self, product_id, quantity, size, user_id):
        cartItem = CartRepository.get_by_id_size(product_id, size)

        if cartItem:
            data = {
                "quantity" : cartItem.quantity + quantity
            }
            CartRepository.update(cartItem.id, data)

            return response({"message": "Item added to cart"}, 200)

        product = ProductRepository.get_by_id(product_id)
        CartRepository.create(user_id, product_id, size, quantity, product.price * quantity)

        return response({"message": "Item added to cart"}, 200)


class CartResource(Resource):
    """Cart Resource"""

    def get(id):
        pass

    def put(id):
        pass

    def delete(id):
        pass
