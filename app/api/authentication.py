from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    if email == "" or password == "":
        return False
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if g.current_user.confirmed is False:
        return forbidden('Unconfirmed account')

