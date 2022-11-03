"""
Defines the blueprint for the shipping price
"""
from flask import Blueprint
from flask_restful import Api

from resources import ShippingPriceResource

SHIPPING_BLUEPRINT = Blueprint("shipping", __name__)
Api(SHIPPING_BLUEPRINT).add_resource(
    ShippingPriceResource, "/shipping_price"
)
