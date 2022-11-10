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

    # @parse_params(
    #     Argument("category_name", location="json", required=True, help="Category name is required")
    # )
    # @token_required
    # def post(self, user_id):
    #     """ Create Category """

    #     user = UserRepository.get_by_id(user_id)

    #     if user.type != "seller":
    #         return response({
    #             "error": "User is not a seller"
    #         }, 400)
        
