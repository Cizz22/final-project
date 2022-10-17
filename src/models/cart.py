"""define Cart Model"""

from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Cart(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Cart model """

    __tablename__ = "carts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)
    
    user = db.relationship('User',back_populates='carts')
    product = db.relationship('Product', back_populates='carts')

    def __init__(self, user_id, product_id, quantity, size, price):
        """ Create a new User """
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.size = size
        self.price - price