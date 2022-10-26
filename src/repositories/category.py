from models import Category

class CategoryRepository():
    
    @staticmethod
    def get_all():
        return Category.query.all()
    
    @staticmethod
    def get(id):
        return Category.query.filter_by(id=id).one()
    
    @staticmethod
    def create(title, image):
        category = Category(title=title, image=image)
        return category.save()

    