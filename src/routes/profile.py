"""
Defines the blueprint for the profile page
"""
from flask import Blueprint
from flask_restful import Api

from resources import UserResource, ShippingAddressResource

PROFILE_BLUEPRINT = Blueprint("profile", __name__)

Api(PROFILE_BLUEPRINT).add_resource(
    UserResource, "/user"
)

Api(PROFILE_BLUEPRINT).add_resource(
    ShippingAddressResource, "/user/shipping_address"
)
