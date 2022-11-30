
from models import Brand, db


class BrandRepository():

    @staticmethod
    def get_all():
        return Brand.query.filter(Brand.deleted_at == None).all()

    @staticmethod
    def get_by(**kwargs):
        return Brand.query.filter_by(**kwargs)

    @staticmethod
    def create(title):
        brand = Brand(title=title)
        return brand.save()

    @staticmethod
    def delete(id):
        brand = Brand.query.get(id)
        brand.deleted_at = db.func.now()
        brand.commit()

    @staticmethod
    def update(id, **kwargs):
        brand = BrandRepository.get_by(id=id).one()
        for key, value in kwargs.items():
            setattr(brand, key, value)
        brand.commit()
        return brand
