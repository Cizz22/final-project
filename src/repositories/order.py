"""Order Repository"""
from models import Order, db, OrderItem
from repositories import CartRepository
from utils import celery_app


class OrderRepository():

    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def create(user_id, subtotal, shipping_fee, shipping_method):
        total_price = subtotal + shipping_fee
        order = Order(user_id=user_id, subtotal=subtotal, shipping_fee=shipping_fee,
                      shipping_method=shipping_method, total_price=total_price)
        return order.save()

    @staticmethod
    def get_by(**kwargs):
        return Order.query.filter_by(**kwargs)

    @staticmethod
    def create_order_item(carts, order_id):
        for cart in carts:
            order_item = OrderItem(order_id=order_id, product_id=cart.product_id,
                                   quantity=cart.quantity, size=cart.size, price=cart.price)
            order_item.save()
