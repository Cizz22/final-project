"""
Defines the blueprint for the profile page
"""
from flask import Blueprint
from flask_restful import Api

from resources import BrandResource, BrandsResource

BRAND_BLUEPRINT = Blueprint("brand", __name__)

Api(BRAND_BLUEPRINT).add_resource(
    BrandsResource, "/brands"
)

Api(BRAND_BLUEPRINT).add_resource(
    BrandResource, "/brands/<string:id>"
)