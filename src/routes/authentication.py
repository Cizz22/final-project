"""
Defines the blueprint for the authentication
"""
from flask import Blueprint
from flask_restful import Api

from resources import SigninResource, SignupResource

AUTHENTICATION_BLUEPRINT = Blueprint("authentication", __name__)
Api(AUTHENTICATION_BLUEPRINT).add_resource(
    SigninResource, "/sign-in"
)

Api(AUTHENTICATION_BLUEPRINT).add_resource(
    SignupResource, "/sign-up"
)
