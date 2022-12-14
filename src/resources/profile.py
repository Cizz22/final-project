from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response, token_required, admin_required
from repositories import UserRepository


class UserResource(Resource):
    """ Profile Resource """

    @token_required
    def get(self, user_id):
        """ Get User Details """

        user = UserRepository.get_by_id(user_id)

        data = {
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        }

        res = {
            "data": data
        }

        return response(res, 200)


class ShippingAddressResource(Resource):
    """ Shipping Address Resource """

    @parse_params(
        Argument("name", location="json", required=True,
                 help="Name cannot be blank.", dest="address_name"),
        Argument("phone_number", location="json", required=True,
                 help="Phone number cannot be blank."),
        Argument("address", location="json", required=True, help="Address cannot be blank."),
        Argument("city", location="json", required=True, help="City cannot be blank.")
    )
    @token_required
    def post(self, user_id, address_name, phone_number, address, city):
        """ Change shipping address """

        UserRepository.update(user_id, address_name=address_name,
                              phone_number=phone_number, address=address, city=city)

        user = UserRepository.get_by_id(user_id)

        data = {
            "name": user.address_name,
            "phone_number": user.phone_number,
            "address": user.address,
            "city": user.city
        }

        res = {
            "data": data,
            "message":"Update shipping address success"
        }

        return response(res, 200)

    @token_required
    def get(self, user_id):
        """ Get User Shipping Address """

        user = UserRepository.get_by_id(user_id)

        data = {
            "id": user.id,
            "name": user.address_name,
            "phone_number": user.phone_number,
            "address": user.address,
            "city": user.city
        }

        res = {
            "data": data
        }

        return response(res, 200)


class BalanceResource(Resource):
    """ Balance Resource """

    @parse_params(
        Argument("amount", location="json", required=True,
                 help="Amount cannot be blank.", type=int)
    )
    @token_required
    def post(self, user_id, amount):
        """ Top up Balance """

        user = UserRepository.get_by_id(user_id)

        if user.type != "buyer":
            res = {
                "error": "User is not a buyer"
            }
            return response(res, 400)

        balance = user.balance + amount

        UserRepository.update(user_id, balance=balance)

        res = {
            "message": "Top up balance success"
        }

        return response(res, 200)

    @token_required
    def get(self, user_id):
        """ Get User Balance """

        user = UserRepository.get_by_id(user_id)

        if user.type != "buyer":
            res = {
                "error": "User is not a buyer"
            }
            return response(res, 400)

        data = {
            "balance": user.balance
        }

        res = {
            "data": data
        }

        return response(res, 200)


class SalesResource(Resource):
    """ Sales Resource """

    @admin_required
    def get(self, user_id):
        """ Get Total Sales """

        user = UserRepository.get_by_id(user_id)

        if user.type != "seller":
            res = {
                "error": "User is not a seller"
            }
            return response(res, 400)

        data = {
            "total": user.balance
        }

        res = {
            "data": data
        }

        return response(res, 200)
