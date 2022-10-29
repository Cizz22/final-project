from models import Product
from models import ProductImage
from models import db

from sqlalchemy import and_, desc


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
    def get_query_results(page, page_size, sort_by , **filters):
        res = Product.query

        for key, value in filters.items():
            if value:
                if key == "price" :
                    res = res.filter(and_(Product.price >= value[0], Product.price <= value[1]))
                elif key == "categories":
                    res = res.filter(Product.category_id.in_(value))
                elif key == "title" :
                    res = res.filter(Product.title.like(f"%{value}%"))
                else:
                    res = res.filter_by(**{key: value})
        if sort_by:
            res = res.order_by(getattr(Product, sort_by[0])) if sort_by[1] == "a_z" else res.order_by(
                desc(getattr(Product, sort_by[0])))

        return {"data": res.paginate(page=page, per_page=page_size) , "total" : res.count()}

    @staticmethod
    def update(id, title, price, category_id, condition, product_detail):
        product = Product.query.get(id)
        product.title = title
        product.price = price
        product.category_id = category_id
        product.condition = condition
        product.product_detail = product_detail
        product.commit()
        return product

    @staticmethod
    def update_image(id, *images_url):
        product = Product.query.get(id)
        ProductImage.query.filter_by(product_id=id).delete()

        for image_url in images_url:
            product_image = ProductImage(image=image_url, product_id=id)
            product_image.save()

    def delete(id):
        product = Product.query.get(id)
        product.delete()

    @staticmethod
    def rollback():
        db.session.rollback()
