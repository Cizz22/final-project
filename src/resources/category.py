from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response, token_required
from repositories import CategoryRepository, UserRepository

class CategoriesResource(Resource):
    """ Categories Resource """

    def get(self):
        """ Get all categories """
 
        categories = CategoryRepository.get_all()

        data = [
            {
                "id": category.id,
                "title": category.title
            } for category in categories
        ]

        res = {
            "data": data
        }

        return response(res, 200)

    @parse_params(
        Argument("category_name", location="json", required=True, help="Category name is required")
    )
    @token_required
    def post(self, user_id, category_name):
        """ Create Category """

        user = UserRepository.get_by_id(user_id)

        if user.type != "seller":
            return response({
                "error": "User is not a seller"
            }, 400)

        category = CategoryRepository.get_by(title=category_name).one_or_none()

        if category is not None:
            return response({
                "error": "Category is already exists"
            }, 400)
        
        CategoryRepository.create(category_name)

        res = {
            "message": "Category added"
        }

        return response(res, 201)