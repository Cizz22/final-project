import click
from flask.cli import with_appcontext
from .user import userSeeder
from .category import categorySeeder
from .banner import bannerSeeder
from models import db

@click.command(name='seeder')
@with_appcontext
def mainSeeder():
    db.drop_all()
    db.create_all()
    
    userSeeder()
    categorySeeder()
    bannerSeeder()  