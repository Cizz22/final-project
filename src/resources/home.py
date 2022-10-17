from flask.json import jsonify
from flask_restful import Resource
from utils import parse_params
from flask_restful.reqparse import Argument

from repositories import BannerRepository, CategoryRepository


class BannerResource(Resource):
    """ Banner resource """
    def get():
        """ Get all banners """
        banners = BannerRepository.get_all()
        return jsonify([banner.json for banner in banners])


class CategoryResource(Resource):
    """ Category resource """

    def get(self):
        """ Get all categories """
        categories = CategoryRepository.get_all()
        return jsonify({"data": [category.json for category in categories]})
