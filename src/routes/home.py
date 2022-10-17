"""
Defines the blueprint for the home
"""
from flask import Blueprint
from flask_restful import Api

from resources import BannerResource, CategoryResource

HOME_BLUEPRINT = Blueprint("home", __name__)
Api(HOME_BLUEPRINT).add_resource(
    BannerResource, "/home/banner"
)

Api(HOME_BLUEPRINT).add_resource(
    CategoryResource, "/home/category"
)
