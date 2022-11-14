from models import Cart

class CartRepository():
    @staticmethod
    def get_by(**kwargs):
        return Cart.query.filter_by(**kwargs)

    @staticmethod
    def create(user_id, product_id, size, quantity, price):
        cart = Cart(user_id=user_id, product_id=product_id,
                    size=size, quantity=quantity, price=price)
        return cart.save()

    @staticmethod
    def update(id, **columns):
        cart = CartRepository.get_by(id=id).one()
        for key, value in columns.items():
            setattr(cart, key, value)
        cart.commit()
        return cart

    @staticmethod
    def delete(id):
        cart = CartRepository.get_by(id=id).one()
        return cart.delete()

    @staticmethod
    def get_all():
        return Cart.query.all()

    @staticmethod
    def delete_all(carts):
        for cart in carts:
            cart.delete()
