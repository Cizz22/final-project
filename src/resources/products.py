from utils import response
from flask_restful import Resource
from utils import parse_params, search_img
from flask_restful.reqparse import Argument
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


from repositories import ProductRepository, CategoryRepository
from utils import token_required, decodeImage, admin_required


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
                "image": product.product_images[0].json['image'],
            } for product in products['data']],
            "total_rows": products['total']
        }

        return response(res, 200)

    @parse_params(
        Argument("product_name", location="json", required=True,
                 help="Product name is required" , dest="title"),
        Argument("description", location="json", required=True,
                 dest='product_detail', help="Description is required"),
        Argument("price", location="json", required=True, help="Price is required"),
        Argument("condition", location="json", required=True, help="Condition is required"),
        Argument("category", location="json", required=True,
                 dest='category_id', help="Category is required"),
        Argument("images", location="json", required=True, type=list,
                 dest='product_images', help="Images is required"),

    )
    @admin_required
    def post(self, title, product_detail, condition, category_id, price, product_images, user_id):
        """ Create a new product """

        product = ProductRepository.get_by(title=title, condition=condition).first()

        if product is not None:
            if product.deleted_at is None:
                return response({"message": "Product already exist"}, 409)
            else:
                product = ProductRepository.update(product.id, title=title, product_detail=product_detail, condition=condition,
                                                   category_id=category_id, price=price, product_images=product_images, deleted_at=None)

        else:
            product = ProductRepository.create(
                title, price, category_id, condition, product_detail)

        images = {}

        for i, image in enumerate(product_images, 1):
            base = image.split(",")[1]
            type = image.split(",")[0].split("/")[1].split(";")[0]
            images.update(
                {f"{product.title}_{product.id}_{i}_{int(datetime.now().timestamp())}.{type}": base})

        decodeImage(images)

        ProductRepository.create_image(images.keys(), product_id=product.id)

        return response({"message": "Product added"}, 201)

    @parse_params(
        Argument("product_name", location="json", default=None, dest="title"),
        Argument("description", location="json",
                 dest='product_detail', default=None),
        Argument("price", location="json", default=None),
        Argument("condition", location="json", default=None),
        Argument("category", location="json",
                 dest='category_id', default=None),
        Argument("images", location="json", type=list,
                 dest='product_images', default=[]),
        Argument("product_id", location="json", required=True,
                 dest='id', help="product_id is required"),
    )
    @admin_required
    def put(self, id, title, product_detail, condition, category_id, price, product_images, user_id):
        product = ProductRepository.get_by(id=id).first()

        if product is None:
            return response({"message": "Product not found"}, 404)

        ProductRepository.update(
            id, title=title, price=price, category_id=category_id, condition=condition, product_detail=product_detail)

        images_base = {}
        images_url = []

        
        for i, image in enumerate(product_images, 1):
            if image.startswith("data:image"):
                base = image.split(",")[1]
                type = image.split(",")[0].split("/")[1].split(";")[0]
                images_base.update(
                    {f"image/{product.title}_{product.id}_{i}_{int(datetime.now().timestamp())}.{type}": base})
            else:
                images_url.append(image)
                
        decodeImage(images_base)
        
        images_url.extend(images_base.keys())

        ProductRepository.update_image(images_url, product_id=product.id)

        return response({"message": "Product updated"}, 201)


class ProductImageSearchResource(Resource):
    """ ProductImageSearch resource """

    @parse_params(
        Argument("image", location="json")
    )
    def post(self, image):
        """ Search product image """

        base = image.split(",")[1]
        title_result = search_img(base)
        category = CategoryRepository.get_by(title=title_result).one_or_none()

        return response({"category_id": category.id}, 200)


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
            "size": ["S", "M", "L"],
            "product_detail": product.json['product_detail'],
            "price": product.json['price'],
            "images_url": [product_image.json['image'] for product_image in product.product_images],
        }

        return response({"data": res}, 200)

    @admin_required
    def delete(self, id, user_id):
        ProductRepository.delete(id)
        return response({"message": "Product deleted"}, 201)
