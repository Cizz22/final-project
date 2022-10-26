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
        Argument("sort_by", location="args", type=str, required=False, default="Created_at a_z"),
        Argument("price", location="args", type=str, required=False, default=None),
        Argument("category", location="args", type=int,
                 required=False, default=None, dest="category_id"),
        Argument("condition", location="args", type=str, required=False, default=None),
        Argument("product_name", location="args", type=str,
                 required=False, default=None, dest='title'),
    )
    def get(self, page, page_size, sort_by, price, category_id, condition, title):
        """ Get all products """
        sort_order = sort_by.split()

        products = ProductRepository.get_query_results(
            price, category_id, condition, title, page=page, page_size=page_size, sort=sort_order[
                0], order=sort_order[1]
        )

        res = {
            "data": [{
                "id": product.json['id'],
                "image": product.product_images[0].json['image'],
                "title": product.json['title'],
                "price": product.json['price'],
            } for product in products]
        }

        return response(res, 200)


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

        res = {
            "id": product.json['id'],
            "title": product.json['title'],
            "size": product.json['size'],
            "product_detail": product.json['product_detail'],
            "price": product.json['price'],
            "images_url": [product_image.json['image'] for product_image in product.product_images],
        }

        return response(res, 200)
