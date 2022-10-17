"""Define User Address Model"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserAddress(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The User Address model """

    __tablename__ = "user_addresses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(300), nullable=True)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)

    user = db.relationship('User', back_populates='user_addresses')

    def __init__(self, user_id, address, city, name, phone_number):
        """ Create a new User """
        self.user_id = user_id
        self.address = address
        self.city = city
        self.name = name
        self.phone_number = phone_number
