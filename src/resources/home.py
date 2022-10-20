from urllib import response
from flask.json import jsonify
from flask_restful import Resource
from utils import parse_params
from flask_restful.reqparse import Argument

from repositories import BannerRepository, CategoryRepository


class BannerResource(Resource):
    """ Banner resource """
    def get(self):
        """ Get all banners """
        banners = BannerRepository.get_all()
        response = jsonify({"data":[banner.json for banner in banners]})
        response.status_code = 200
        return response


class CategoryResource(Resource):
    """ Category resource """

    def get(self):
        """ Get all categories """
        categories = CategoryRepository.get_all()
        return jsonify({"data": [category.json for category in categories]})
