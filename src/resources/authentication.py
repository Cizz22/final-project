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

    @parse_params(
        Argument("email", location="json", required=True, help="Email cannot be blank."),
        Argument("password", location="json", required=True, help="Password cannot be blank."),
        Argument("name", location="json", required=True, help="Name cannot be blank"),
        Argument("phone_number", location="json", required=True, help="Phone Number cannot be blank"),
        Argument("type", location="json", required=True, help="Type cannot be blank"),
    )

    def post(self, email, password, name, phone_number, type):
        """ Signup """

        if UserRepository.get_by_email(email) is not None:
            return response({"error": "Email is already registered"})

        UserRepository.create(name, email, phone_number, password, type)
        return response({"message": "Success, user created"})
