"""
Defines the blueprint for the profile page
"""
from flask import Blueprint
from flask_restful import Api

from resources import CategoriesResource, CategoryResource

CATEGORY_BLUEPRINT = Blueprint("category", __name__)

Api(CATEGORY_BLUEPRINT).add_resource(
    CategoriesResource, "/categories"
)

Api(CATEGORY_BLUEPRINT).add_resource(
    CategoryResource, "/categories/<string:id>"
)