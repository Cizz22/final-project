from models import Product


class ProductRepository:
    """The Repository for products modol"""

    def get_all():
        return Product.query.all()

    def create(title, size, price, category_id, condition, product_detail):
        product = Product(title, size, price, category_id, condition, product_detail)
        product.save()

    def get_by_id(id):
        return Product.query.filter_by(id=id).one_or_none()

    def get_query_results(*filters, page, page_size, sort, order):
        res = Product.query
        for i, filt in enumerate(filters, 1):
            if filt is not None:
                d = {'filter{}'.format(i): filt}
                res = res.filter(**d)
        return res.paginate(page=page, per_page=page_size, error_out=False).order_by(sort)
