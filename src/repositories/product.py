from models import Product
from models import ProductImage
from models import db
import uuid


class ProductRepository:
    """The Repository for products modol"""

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def create(title, price, category_id, condition, product_detail):
        product = Product(title, price, category_id, condition, product_detail)
        return product.save()

    @staticmethod
    def create_image(*images_url, product_id):
        for image_url in images_url:
            product_image = ProductImage(image=image_url, product_id=product_id)
            product_image.save()

    @staticmethod
    def get_by_id(id):
        return Product.query.filter_by(id=id).one_or_none()

    @staticmethod
    def get_query_results(*filters, page, page_size, sort, order):
        sort_by = f"{sort} asc" if order == "a_z" else f"{sort} desc"
        NAMES = "price category_id condition title".split()
        res = Product.query

        for name, filt in zip(NAMES, filters):
            if filt is not None:
                print(name, filt)
                res = res.filter_by(**{name: filt})
        return {"data": res.order_by(db.text(sort_by)).paginate(page=page, per_page=page_size) , "total" : res.count()}
