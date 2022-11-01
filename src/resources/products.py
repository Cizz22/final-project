from utils import response
from flask_restful import Resource
from utils import parse_params
from flask_restful.reqparse import Argument
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import UUID

from repositories import ProductRepository
from utils import token_required, decodeImage


class ProductsResource(Resource):
    """ Products resource """

    @parse_params(
        Argument("page", location="args", type=int, required=False, default=1),
        Argument("page_size", location="args", type=int, required=False, default=10),
        Argument("sort_by", location="args", type=str, required=False, default="created_at z_a"),
        Argument("price", location="args", type=str, required=False, default=None),
        Argument("category", location="args", type=str,
                 required=False, default=None, dest="category_id"),
        Argument("condition", location="args", type=str, required=False, default=None),
        Argument("product_name", location="args", type=str,
                 required=False, default=None, dest='title'),
    )
    def get(self, page, page_size, sort_by, price, category_id, condition, title):
        """ Get all products """
        sort_by = sort_by.split(" ")
        category_id = category_id.split(',') if category_id else None
        price = price.split(',') if price else None

        products = ProductRepository.get_query_results(
            page, page_size, sort_by, price=price, categories=category_id, condition=condition, title=title
        )

        res = {
            "data": [{
                "id": product.json['id'],
                "title": product.json['title'],
                "price": product.json['price'],
                "image": [image.json['image'] for image in product.product_images],
            } for product in products['data']],
            "total_rows": products['total']
        }

        return response(res, 200)

    @parse_params(
        Argument("title", location="json", required=True, help="Title is required"),
        Argument("description", location="json", required=True,
                 dest='product_detail', help="Description is required"),
        Argument("price", location="json", required=True, help="Price is required"),
        Argument("condition", location="json", required=True, help="Condition is required"),
        Argument("category", location="json", required=True,
                 dest='category_id', help="Category is required"),
        Argument("images", location="json", required=True, type=list,
                 dest='product_images', help="Images is required"),

    )
    @token_required
    def post(self, title, product_detail, condition, category_id, price, product_images, user_id):
        """ Create a new product """

        product = ProductRepository.get_by(title=title, condition=condition).one_or_one()

        if product and product.deleted_at is None:
            return response({"message": "Product already exist"}, 409)

        if product.deleted_at is not None:
            ProductRepository.update(product.id, title=title, product_detail=product_detail, condition=condition,
                                     category_id=category_id, price=price, product_images=product_images, deleted_at=None)
        else:
            product = ProductRepository.create(
                title, price, category_id, condition, product_detail)

        images = {}

        for i, image in enumerate(product_images, 1):
            images.update({f"{product.title}_{product.id}_{i}.jpg": image})

        decodeImage(images)

        ProductRepository.create_image(images.keys(), product_id=product.id)

        return response({"message": "Product added"}, 201)

    @parse_params(
        Argument("title", location="json", required=True, help="Title is required"),
        Argument("description", location="json", required=True,
                 dest='product_detail', help="Description is required"),
        Argument("price", location="json", required=True, help="Price is required"),
        Argument("condition", location="json", required=True, help="Condition is required"),
        Argument("category", location="json", required=True,
                 dest='category_id', help="Category is required"),
        Argument("images", location="json", required=True, type=list,
                 dest='product_images', help="Images is required"),
        Argument("product_id", location="json", required=True,
                 dest='id', help="Product_id is required"),
    )
    def put(self, id, title, product_detail, condition, category_id, price, product_images):
        ProductRepository.update(
            id, title=title, price=price, category_id=category_id, condition=condition, product_detail=product_detail)
        ProductRepository.update_image(*product_images, product_id=id)

        return response({"message": "Product updated"}, 201)


class ProductImageSearchResource(Resource):
    """ ProductImageSearch resource """

    @parse_params(
        Argument("image", location="json")
    )
    def post(self, image):
        """ Search product image """

        return response({"message": "Product image search"}, 201)

class ProductResource(Resource):
    """ Product resource """

    def get(self, id):
        """ Get product by id """
        product = ProductRepository.get_by(id=id).one_or_none()

        if product is None:
            return response({"message": "Product not found"}, 404)

        res = {
            "id": product.json['id'],
            "title": product.json['title'],
            "size": product.json['size'],
            "product_detail": product.json['product_detail'],
            "price": product.json['price'],
            "images_url": [product_image.json['image'] for product_image in product.product_images],
        }

        return response(res, 200)

    @token_required
    def delete(self, id, user_id):
        ProductRepository.delete(id)
        return response({"message": "Product deleted"}, 201)
