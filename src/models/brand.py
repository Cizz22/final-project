"""Define Brand Model"""

from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Brand(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Brand model """

    __tablename__ = "brands"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(300), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)

    products = db.relationship('Product', back_populates='brand')

    def __init__(self, title):
        """ Create a new Brand """
        self.title = title
