from flask.json import jsonify
from flask_restful import Resource
from utils import parse_params
from flask_restful.reqparse import Argument

class ProductsResource(Resource):
    """ Products resource """

    @parse_params(
        Argument("page", location="args", type=int, required=False, default=1),
        Argument("page_size", location="args", type=int, required=False),
        Argument("sort_by", location="args", type=str, required=False),
        Argument("price", location="args", type=str, required=False),
        Argument("category", location="args", type=int, required=False),
        Argument("condition", location="args", type=str, required=False),
        Argument("product_name", location="args", type=str, required=False),
    )
    def get(self, page, page_size, sort_by, price, category, condition, product_name):
        """ Get all products """
        

class ProductImageSearchResource(Resource):
    """ ProductImageSearch resource """

    @parse_params(
        Argument("image", location="json")
    )
    def post(self, image):
        """ Search product image """

class ProductResource(Resource):
    """ Product resource """

    def get(self, id):
        """ Get product by id """

    def put(self, id):
        """ Update product by id """

    def delete(self, id):
        """ Delete product by id """