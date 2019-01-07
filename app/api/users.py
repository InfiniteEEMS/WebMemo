from flask import jsonify, request
from . import api
from ..models import User


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    return jsonify(user.to_json())
