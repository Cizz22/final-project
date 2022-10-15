"""
Define the User model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The User model """

    __tablename__ = "user"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(300), nullable=True)

    def __init__(self, name, email, password, phone):
        """ Create a new User """
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
