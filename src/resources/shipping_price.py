from flask_restful import Resource
from utils import parse_params, response
from flask_restful.reqparse import Argument


from repositories import CartRepository
from utils.jwt_verif import token_required
from utils.shipping_fee import get_shipping_fee


class ShippingPriceResource(Resource):
    """ Shipping price resource """

    @token_required
    def get(self, user_id):
        """ Get shipping price """
        carts = CartRepository.get_by(user_id=user_id).all()

        if not carts:
            return response({"message": "Cart is empty"}, 400)

        total_price = 0
        for cart in carts:
            total_price += cart.price

        res = [{
            "name": "regular",
            "price": get_shipping_fee(total_price, "regular")
        },
            {
            "name": "next day",
            "price": get_shipping_fee(total_price, "next day")
        }]

        return response({"data": res})
