"""
Define the User model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The User model """

    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(300), nullable=True)
    type = db.Column(db.String(300), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)
    
    orders = db.relationship('Order', back_populates='user', lazy=True)
    carts = db.relationship('Cart', back_populates='user', lazy=True)
    user_addresses = db.relationship('UserAddress', back_populates = 'user', lazy=True)

    def __init__(self, name, email, phone_number, type):
        """ Create a new User """
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.type = type
    
    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

