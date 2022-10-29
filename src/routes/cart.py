"""
Defines the blueprint for the cart
"""

from flask import Blueprint
from flask_restful import Api

from resources import CartsResource, CartResource


CART_BLUEPRINT = Blueprint("cart", __name__)
Api(CART_BLUEPRINT).add_resource(
    CartsResource , "/cart"
)

Api(CART_BLUEPRINT).add_resource(
    CartResource , "/cart/<int:id>"
)
