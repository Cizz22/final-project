from models import Banner

class BannerRepository():
    
    @staticmethod
    def get_all():
        return Banner.query.all()
    
    @staticmethod
    def get(id):
        return Banner.query.filter_by(id=id).one()
    
    @staticmethod
    def create(name, image):
        banner = Banner(title=name, image=image)
        return banner.save()

    