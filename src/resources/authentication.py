from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response, create_token
from repositories import UserRepository

class SigninResource(Resource):
    """ Signin resource """

    @parse_params(
        Argument("email", location="json", required=True, help="Email cannot be blank."),
        Argument("password", location="json", required=True, help="Password cannot be blank."),
    )

    def post(self, email, password):
        """ Signin """

        user = UserRepository.get_by_email(email)

        if user is None:
            return response({"error": "Email is not registered"}, 401)
        
        if not user.check_password(password):
            return response({"error": "Password incorrect"}, 401)
        
        token = create_token(str(user.id))
        user_information = {
            "name" : user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "type": user.type
        }

        return response({
            "user_information": user_information,
            "token": token,
            "message": "Login success"
        }, 200)
    



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
            return response({"message": "Error, user already exists"}, 409)

        UserRepository.create(name, email, phone_number, password, type)
        return response({"message": "Success, user created"}, 201)
