"""
Defines the blueprint for the home
"""
from flask import Blueprint
from flask_restful import Api

from resources import HomeCategoryResource, HomeBannerResource

HOME_BLUEPRINT = Blueprint("home", __name__)
Api(HOME_BLUEPRINT).add_resource(
    HomeBannerResource, "/home/banner"
)

Api(HOME_BLUEPRINT).add_resource(
    HomeCategoryResource, "/home/category"
)
