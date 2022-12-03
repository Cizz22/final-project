from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Announcement(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Announcement model """

    __tablename__ = "announcements"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __init__(self, title, content):
        """ Create a new User """
        self.title = title
        self.content = content