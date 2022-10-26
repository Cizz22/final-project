from models import Banner
from sqlalchemy.orm import load_only

class BannerRepository():
    
    @staticmethod
    def get_all():
        return Banner.query.all()
    
    @staticmethod
    def get(id):
        return Banner.query.filter_by(id=id).one()
    
    @staticmethod
    def create(title, image):
        banner = Banner(title=title, image=image)
        return banner.save()

    