from models import OrderAddress


class OrderAddressRepository():
    """ OrderAddress repository """

    @staticmethod
    def get_by(**kwargs):
        return OrderAddress.query.filter_by(**kwargs)

    @staticmethod
    def create(order_id, shipping_address):
        order_address = OrderAddress(
            order_id, shipping_address['address'], shipping_address['city'], shipping_address['name'], shipping_address['phone_number'])

        return order_address.save()
