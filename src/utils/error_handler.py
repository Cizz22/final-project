from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from utils import response


def handle_exception(e):
    if isinstance(e, HTTPException):
        return response({"message": e.description}, e.code)

    if isinstance(e, SQLAlchemyError):
        error = str(e.__dict__['orig'])
        return response({"message": error}, 500)

    return response({"message": e}, 500) if current_app.debug else response({"message": "Internal Server Error"}, 500)
