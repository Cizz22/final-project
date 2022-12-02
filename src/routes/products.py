"""
Defines the blueprint for the products
"""
from flask import Blueprint
from flask_restful import Api

from resources import ProductsResource, ProductResource, ProductImageSearchResource

PRODUCTS_BLUEPRINT = Blueprint("products", __name__)
Api(PRODUCTS_BLUEPRINT).add_resource(
    ProductsResource, "/products"
)
Api(PRODUCTS_BLUEPRINT).add_resource(
    ProductImageSearchResource, "/products/search_image"
)
Api(PRODUCTS_BLUEPRINT).add_resource(
    ProductResource, "/products/<string:id>"
)
