from models import Cart


class CartRepository():
    @staticmethod
    def get_by_id(id):
        return Cart.query.filter_by(id=id).one_or_none()

    def get_by_product_id(id):
        return Cart.query.filter_by(product_id=id).one_or_none()

    def get_by_id_size(id, size):
        return Cart.query.filter_by(product_id=id, size=size).one_or_none()

    @staticmethod
    def get_by_user_id(user_id):
        return Cart.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(user_id, product_id, size, quantity, price):
        cart = Cart(user_id=user_id, product_id=product_id,
                    size=size, quantity=quantity, price=price)
        return cart.save()

    @staticmethod
    def update(id, **columns):
        cart = CartRepository.get_by_id(id)
        for key, value in columns.items():
            setattr(cart, key, value)
        cart.commit()
        return cart

    @staticmethod
    def delete(id):
        cart = CartRepository.get_by_id(id)
        return cart.delete()

    @staticmethod
    def get_all():
        return Cart.query.all()
