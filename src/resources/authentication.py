from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response
from utils import create_token

from repositories import UserRepository
from utils.jwt_verif import token_required


class SigninResource(Resource):
    """ Signin resource """

    @parse_params(
        Argument("email", location="json", required=True, help="Email cannot be blank."),
        Argument("password", location="json", required=True, help="Password cannot be blank."),
    )
    def post(self, email, password):
        """ Signin """
        return response({"data": "Signin"})
    



class SignupResource(Resource):
    """ Signup resource """

    def post(self):
        """ Signup """
        return response({"data": "Signup"})
