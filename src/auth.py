import logging
from flask import Blueprint, request, current_app as app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, login_serializer, jwt
from .endpoint_utils import set_response_cookies
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, unset_jwt_cookies)

auth = Blueprint('auth', __name__)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    """
    Allow to identify the token with the username
    """
    return {
        'username': identity
    }


@auth.route('/logout', methods=['POST'])
@jwt_refresh_token_required
@jwt_required
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return "Logged out", 200


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.objects(email=email) 
    if user:  # Email already exist.  
        return "User already exist", 409
    logging.warning("User not existing")
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user.save()
    set_response_cookies(email, None, ["access", "refresh"])
    return "User created", 200


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return "Missing fields", 400
    user = User.objects(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return "Wrong login informations", 400 
    set_response_cookies(email, None, ["access", "refresh"])
    return "User logged in", 200


@auth.route('/token', methods=['POST'])
def token_post():
    """
    {"email": "email", "password": password} => Tokens 
    """
    obj = request.get_json()
    user = User.objects(email=obj["email"]).first()
    if not user or not check_password_hash(user.password, str(obj["password"])):
        return "Wrong login informations", 400
    else:
        resp = set_response_cookies(obj["email"], None, ["access", "refresh"])
        return resp, 200    


@auth.route('/token', methods=['GET'])
@jwt_refresh_token_required
@jwt_required
def token_check():
    """
    Check if a token is valid
    To access a jwt_required protected view, all we have to do is send in the JWT
    with the request. By default, this is done with an authorization header that looks like:
    Authorization: Bearer <access_token>
    """
    return "OK", 200


@auth.route('/token/remove', methods=['POST'])
@jwt_refresh_token_required
@jwt_required
def token_drop():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
