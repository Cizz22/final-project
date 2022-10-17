from models import Category

class CategoryRepository():
    
    @staticmethod
    def get_all():
        return Category.query.all()
    
    @staticmethod
    def get(id):
        return Category.query.filter_by(id=id).one()
    
    @staticmethod
    def create(name, image):
        category = Category(title=name, image=image)
        return category.save()

    