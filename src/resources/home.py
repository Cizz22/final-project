from flask_restful import Resource
from utils import parse_params, response
from flask_restful.reqparse import Argument


from repositories import BannerRepository, CategoryRepository


class BannerResource(Resource):
    """ Banner resource """

    def get(self):
        """ Get all banners """
        banners = BannerRepository.get_all()
        return response({"data": [banner.json for banner in banners]})


class CategoryResource(Resource):
    """ Category resource """

    def get(self):
        """ Get all categories """
        categories = CategoryRepository.get_all()
        res = {
            "data": [{
                "id": category.id,
                "title": category.title,
               
            }] for category in categories
        }

        return response(res)
