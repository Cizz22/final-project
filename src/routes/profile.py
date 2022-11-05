"""
Defines the blueprint for the profile page
"""
from flask import Blueprint
from flask_restful import Api

from resources import UserResource

PROFILE_BLUEPRINT = Blueprint("profile", __name__)

Api(PROFILE_BLUEPRINT).add_resource(
    UserResource, "/user"
)
