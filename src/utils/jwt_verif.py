from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, make_response
import jwt
from flask import current_app

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authentication' in request.headers:
            token = request.headers['Authentication']

        if not token:
            return make_response(jsonify({'message': 'a valid token is missing'}), 401)
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return make_response(jsonify({'message': 'token is invalid'}), 401)

        return f(*args, **kwargs)
    return decorator


def create_token(user_id):
    return jwt.encode({'user_id': user_id, 'exp' : datetime.utcnow() + timedelta(minutes=60)}, current_app.config['SECRET_KEY'])
