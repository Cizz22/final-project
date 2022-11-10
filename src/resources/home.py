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
