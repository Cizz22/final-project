"""
Define the Product model
"""

from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Product(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The User model """

    __tablename__ = "products"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(300), nullable=False, unique=True)
    brand_name = db.Column(db.String(300), nullable=False)
    size = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'), nullable=False)
    product_detail = db.Column(db.Text(), nullable=False)
    condition = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True, server_default=None)
    
    category = db.relationship('Category', back_populates='products')
    product_images = db.relationship('ProductImage', back_populates='product')
    carts = db.relationship('Cart', back_populates='product')
    order_items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    
    def __init__(self, title, brand_name, size, price, category_id, condition, product_detail):
        """ Create a new User """
        self.title = title
        self.brand_name = brand_name
        self.size = size
        self.price = price
        self.category_id = category_id
        self.condition = condition
        self.product_detail = product_detail
