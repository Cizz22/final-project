"""define Order Address Model"""
from models import order_items
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class OrderAddress(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order Address model """

    __tablename__ = "order_addresses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False)
    name = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(300), nullable=True)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)

    order = db.relationship('Order', back_populates='order_addresses')

    def __init__(self, order_id, address, city, name, phone_number):
        """ Create a new User """
        self.order_id = order_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.city = city
