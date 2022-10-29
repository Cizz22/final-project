from flask import Flask
from flask.blueprints import Blueprint
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

from utils import handle_exception, make_celery

import config
import routes
from models import db


"""Create an application."""
server = Flask(__name__)

"""Server Configuration"""
server.debug = config.DEBUG
server.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
server.config["SECRET_KEY"] = config.SECRET_KEY
server.config["IMAGE_URL"] = config.IMAGE_URL
server.config["CELERY_CONFIG"] = config.CELERY_CONFIG


"""Database Configuration"""
db.init_app(server)
db.app = server

"""Migration Configuration"""
migrate = Migrate(server, db)

@server.route("/")
def main():
    return "oke"


@server.errorhandler(Exception)
def handle_error(e):
    return handle_exception(e)


for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.APPLICATION_ROOT)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT)
