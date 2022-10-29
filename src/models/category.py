"""Define Category Model"""

from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Category(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Category model """

    __tablename__ = "categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)

    products = db.relationship('Product', back_populates='category')

    def __init__(self, title, image):
        """ Create a new User """
        self.title = title
