from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response

from repositories import UserRepository


class SigninResource(Resource):
    """ Signin resource """
    @parse_params(
        Argument("email", location="json", required=True, help="Email user"),
        Argument("password", location="json", required=True, help="password user")
    )
    def post(self, email, password):
        """ Signin """
        return response({"data": [email, password]})


class SignupResource(Resource):
    """ Signup resource """

    def post(self):
        """ Signup """
        return response({"data": "Signup"})
