from flask import jsonify, make_response

def response(data, status_code=200):
    """ Response """
    return make_response(jsonify(data), status_code)
