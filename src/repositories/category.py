
from models import Category, db


class CategoryRepository():

    @staticmethod
    def get_all():
        return Category.query.filter(Category.deleted_at == None).all()

    @staticmethod
    def get_by(**kwargs):
        return Category.query.filter_by(**kwargs)

    @staticmethod
    def create(title):
        category = Category(title=title)
        return category.save()

    @staticmethod
    def delete(id):
        category = Category.query.get(id)
        category.deleted_at = db.func.now()
        category.commit()

    @staticmethod
    def update(id, **kwargs):
        category = CategoryRepository.get_by(id=id).one()
        for key, value in kwargs.items():
            setattr(category, key, value)
        category.commit()
        return category
