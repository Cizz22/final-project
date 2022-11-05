from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response, token_required
from repositories import UserRepository

class UserResource(Resource):
    """ Profile Resource """
    
    @token_required
    def get(self, user_id):
        """ Get User Details """

        user = UserRepository.get_by_id(user_id)

        data = {
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        }

        res = {
            "data": data
        }

        return response(res, 200)