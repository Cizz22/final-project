"""Define blueprint for orders"""

from flask_restful import Api
from flask import Blueprint

from resources import OrdersResource, OrderResource

ORDERS_BLUEPRINT = Blueprint("orders", __name__)

Api(ORDERS_BLUEPRINT).add_resource(
    OrderResource, "/order"
)
Api(ORDERS_BLUEPRINT).add_resource(
    OrdersResource, "/orders"
)

