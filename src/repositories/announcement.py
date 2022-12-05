from models import Announcement, db


class AnnouncementRepository():

    @staticmethod
    def get_all():
        return Announcement.query.all()

    @staticmethod
    def get_by(**kwargs):
        return Announcement.query.filter_by(**kwargs)

    @staticmethod
    def create(title, content):
        announcement = Announcement(title=title, content=content)
        return announcement.save()

    @staticmethod
    def delete(id):
        announcement = Announcement.query.get(id)
        announcement.deleted_at = db.func.now()
        announcement.commit()

    @staticmethod
    def update(id, **kwargs):
        announcement = AnnouncementRepository.get_by(id=id).one()
        for key, value in kwargs.items():
            setattr(announcement, key, value)
        announcement.commit()
        return announcement
