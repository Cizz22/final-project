import logging
import os

DEBUG = os.getenv("ENVIRONEMENT") == "DEV"
APPLICATION_ROOT = os.getenv("APPLICATION_APPLICATION_ROOT", "/")
HOST = os.getenv("APPLICATION_HOST")
PORT = int(os.getenv("APPLICATION_PORT", "3000"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("APPLICATION_SECRET_KEY")

DB_CONTAINER = os.getenv("APPLICATION_DB_CONTAINER", "db")
POSTGRES = {
    "user": os.getenv("APPLICATION_POSTGRES_USER", "user"),
    "pw": os.getenv("APPLICATION_POSTGRES_PW", "pass"),
    "host": os.getenv("APPLICATION_POSTGRES_HOST", DB_CONTAINER),
    "port": os.getenv("APPLICATION_POSTGRES_PORT", 5432),
    "db": os.getenv("APPLICATION_POSTGRES_DB", "db"),
}
DB_URI = "postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES

logging.basicConfig(
    filename=os.getenv("SERVICE_LOG", "server.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
