from models import Product
from models import ProductImage
from models import db



class ProductRepository:
    """The Repository for products modol"""

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def create(title, price, category_id, condition, product_detail):
        product = Product(title, price, category_id, condition, product_detail)
        return product.save()

    def create_image(*images_url, product_id):
        for image_url in images_url:
            images = ProductImage(image_url, product_id)
            images.save()

    @staticmethod
    def get_by_id(id):
        return Product.query.filter_by(id=id).one_or_none()

    @staticmethod
    def get_query_results(*filters, page, page_size, sort, order):
        sort_by = f"{sort} asc" if order == "a_z" else f"{sort} desc"
        res = Product.query
        for i, filt in enumerate(filters, 1):
            if filt is not None:
                d = {'filter{}'.format(i): filt}
                res = res.filter(**d)
        return res.order_by(db.text(sort_by)).paginate(page=page, per_page=page_size, error_out=False)
