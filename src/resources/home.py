from flask_restful import Resource
from utils import parse_params, response
from flask_restful.reqparse import Argument


from repositories import BannerRepository, CategoryRepository


class HomeBannerResource(Resource):
    """ Banner resource """

    def get(self):
        """ Get all banners """
        banners = BannerRepository.get_all()

        return response(
            {"data": [{
                "id": banner.json['id'],
                "title": banner.json['title'],
            } for banner in banners]
            })


class HomeCategoryResource(Resource):
    """ Home category resource """

    def get(self):
        """ Get all categories """
        categories = CategoryRepository.get_all()
        return response({"data": [{
            "id": category.json['id'],
            "title": category.json['title'],
        } for category in categories]})
