"""define Order Model"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Order(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order model """

    __tablename__ = "orders"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    shipping_method =db.Column(db.String(300), nullable=False)
    shipping_fee = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(300), nullable=False, server_default="pending")
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __init__(self, user_id, shipping_method, shipping_fee, subtotal, total_price):
        """ Create a new User """
        self.user_id = user_id
        self.shipping_fee = shipping_fee
        self.shipping_method = shipping_method
        self.subtotal = subtotal
        self.total_price = total_price
        