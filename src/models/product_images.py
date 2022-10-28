"""Define Product Image Model"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ProductImage(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Product Image model """

    __tablename__ = "product_images"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    image = db.Column(db.String(300), nullable=False)

    product = db.relationship('Product', back_populates='product_images')

    def __init__(self, product_id, image):
        """ Create a new User """
        self.product_id = product_id
        self.image = image