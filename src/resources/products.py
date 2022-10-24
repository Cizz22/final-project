from utils import response
from flask_restful import Resource
from utils import parse_params
from flask_restful.reqparse import Argument

from repositories import ProductRepository


class ProductsResource(Resource):
    """ Products resource """

    @parse_params(
        Argument("page", location="args", type=int, required=False, default=1),
        Argument("page_size", location="args", type=int, required=False, default=10),
        Argument("sort_by", location="args", type=str, required=False, default="created_at"),
        Argument("price", location="args", type=str, required=False, default=None),
        Argument("category", location="args", type=int,
                 required=False, default=None, dest="category_id"),
        Argument("condition", location="args", type=str, required=False, default=None),
        Argument("product_name", location="args", type=str,
                 required=False, default=None, dest='title'),
    )
    def get(self, page, page_size, sort_by, price, category_id, condition, title):
        """ Get all products """
        [sort, order] = sort_by.split()

        products = ProductRepository.get_query_results(
            filters=[category_id, condition, title], page=page, page_size=page_size, sort_by=sort, order=order)

        return response({"data" : [product.json for product in products]}, 200)


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
        product = ProductRepository.get_by_id(id)

        return response(product.json, 200)
