"""Define Banner Model"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Banner(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Banner model """

    __tablename__ = "banners"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)

    def __init__(self, title, image):
        """ Create a new User """
        self.title = title
        self.image = image

