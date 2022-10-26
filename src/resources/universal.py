from flask_restful import Resource
from flask import send_from_directory, current_app


class ImageResource(Resource):
    """ Image resource """

    def get(self, filename):
        """ Get image by filename """
        return send_from_directory(current_app.config["IMAGE_URL"], filename)
