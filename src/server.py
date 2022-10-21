from flask import Flask
from flask.blueprints import Blueprint
from flask_migrate import Migrate

import config
import routes
from models import db

server = Flask(__name__)

server.debug = config.DEBUG
server.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
server.config["SECRET_KEY"] = config.SECRET_KEY
migrate = Migrate(server, db)
db.init_app(server) 
db.app = server

@server.route("/")
def main():
    return "Hello!! check database diagram here https://dbdiagram.io/d/60b86e8bb29a09603d17c2d6"


for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.APPLICATION_ROOT)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT)
