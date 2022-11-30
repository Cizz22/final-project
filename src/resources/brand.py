from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response, admin_required
from repositories import BrandRepository

class BrandsResource(Resource):
    """ Brands Resource """

    def get(self):
        """ Get all brands """
 
        brands = BrandRepository.get_all()

        data = [
            {
                "id": brand.id,
                "title": brand.title
            } for brand in brands
        ]

        res = {
            "data": data
        }

        return response(res, 200)

    @parse_params(
        Argument("brand_name", location="json", required=True, help="Brand name is required")
    )
    @admin_required
    def post(self, brand_name, user_id):
        """ Create Brand """

        brand = BrandRepository.get_by(title=brand_name).one_or_none()

        if brand is not None:
            return response({
                "error": "Brand is already exists"
            }, 400)
        
        BrandRepository.create(brand_name)

        res = {
            "message": "Brand added"
        }

        return response(res, 201)

class BrandResource(Resource):
    """ Brand Resource """

    @parse_params(
        Argument("brand_name", location="json", required=True, help="Brand name is required")
    )
    @admin_required
    def put(self, id, brand_name, user_id):
        """ Update Brand """
        
        brand = BrandRepository.get_by(title=brand_name).one_or_none()

        if brand is not None:
            return response({
                "error": "Brand is already exists"
            }, 400)

        
        BrandRepository.update(id, title=brand_name)

        res = {
            "message": "Brand updated"
        }

        return response(res, 200)

    @admin_required
    def delete(self, id, user_id):
        """" Delete Brand """

        BrandRepository.delete(id)

        res = {
            "message": "Category deleted"
        }

        return response(res, 200)



