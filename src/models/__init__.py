from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .product import Product
from .cart import Cart
from .product_images import ProductImage
from .category import Category
from .order import Order
from .banner import Banner
from .order_items import OrderItem
from .order_addresses import OrderAddress
from .brand import Brand
from .announcement import Announcement
