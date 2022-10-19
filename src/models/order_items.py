"""Define Order Item Model"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class OrderItem(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order Item model """

    __tablename__ = "order_items"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    size  = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)
    
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')

    def __init__(self, order_id, product_id, quantity, price):
        """ Create a new Order Item """
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price