from flask import Blueprint
from flask_restful import Api

from resources import ImageResource

UNIVERSAL_BLUEPRINT = Blueprint("universal", __name__)
Api(UNIVERSAL_BLUEPRINT).add_resource(
    ImageResource, "/image/<path:filename>"
)
