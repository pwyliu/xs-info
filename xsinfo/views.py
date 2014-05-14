from xsinfo import app
from flask import abort, make_response, jsonify


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({'error': 'not found'}), 404)


@app.errorhandler(500)
def app_error(err):
    return make_response(jsonify({'error': 'app error'}), 500)


@app.route('/')
def index():
    return "home"