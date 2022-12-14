from models import Product
from models import ProductImage
from models import db

from sqlalchemy import and_, desc


class ProductRepository:
    """The Repository for products model"""

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by(**kwargs):
        return Product.query.filter_by(**kwargs)

    @staticmethod
    def create(title, price, category_id, condition, product_detail):
        product = Product(title, price, category_id, condition, product_detail)
        return product.save()

    @staticmethod
    def create_image(images_url, product_id):
        for image_url in images_url:
            url = "image/" + image_url
            product_image = ProductImage(image=url, product_id=product_id)
            product_image.save()

    @staticmethod
    def get_query_results(page, page_size, sort_by , **filters):
        res = Product.query.filter(Product.deleted_at == None)

        for key, value in filters.items():
            if value:
                if key == "price" :
                    res = res.filter(and_(Product.price >= value[0], Product.price <= value[1]))
                elif key == "categories":
                    res = res.filter(Product.category_id.in_(value))
                elif key == "title" :
                    res = res.filter(Product.title.ilike(f"%{value}%"))
                else:
                    res = res.filter_by(**{key: value})
        if sort_by:
            res = res.order_by(getattr(Product, sort_by[0].lower())) if sort_by[1] == "a_z" else res.order_by(
                desc(getattr(Product, sort_by[0].lower())))

        return {"data": res.paginate(page=page, per_page=page_size) , "total" : res.count()}

    @staticmethod
    def update(id, **kwargs):
        product = Product.query.get(id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(product, key, value)
        product.commit()
        return product

    @staticmethod
    def update_image(images_url, product_id):
        [image.delete() for image in ProductImage.query.filter_by(product_id=product_id).all()]

        for image_url in images_url:
            url = image_url
            product_image = ProductImage(image=url, product_id=product_id)
            product_image.save()

    @staticmethod
    def delete(id):
        product = Product.query.get(id)
        product.deleted_at = db.func.now()
        product.commit()
