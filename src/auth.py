import logging
from flask import Blueprint, render_template, redirect, url_for, request, current_app as app, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, login_manager, login_serializer, jwt
from flask_jwt_extended import (create_access_token, 
create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, set_access_cookies,
set_refresh_cookies, unset_jwt_cookies)

auth = Blueprint('auth', __name__)


def set_cookies(token_identity, token_types=["access", "refresh"]):
    """
    Helper function to set cookies 
    """
    logging.warning("Setting cookies")
    token_types.sort()
    if token_types == ["access", "refresh"]:
        access_token = create_access_token(identity = token_identity)
        refresh_token = create_refresh_token(identity = token_identity)
        resp = jsonify({"access_token": access_token, "refresh_token": refresh_token})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp 
    elif token_types == ["access"]:
        access_token = create_access_token(identity = token_identity)
        resp = jsonify({"access_token": access_token})
        set_access_cookies(resp, access_token)
        return resp 
    elif token_types == ["refresh"]:
        refresh_token = create_refresh_token(identity = token_identity)
        resp = jsonify({"refresh_token": refresh_token})
        set_refresh_cookies(resp, refresh_token)
        return resp 
    else:
        raise ValueError("Wrong Call to this function")


@login_manager.user_loader
def load_user(username):
    u = User.objects(email=email).first()
    if not u:
        return None
    return u


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout', methods=['GET'])
@jwt_refresh_token_required
@jwt_required
@login_required
def logout():
    logout_user()
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return redirect(url_for('src.routes.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.objects(email=email) 
    if user:  # Email already exist.  
        return redirect(url_for('auth.signup')), 409
    logging.warning("User not existing")
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user.save()
    set_cookies(email, ["access", "refresh"])
    return redirect(url_for('auth.login')), 200


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if not email or not password:
        return "Missing fields", 400
    user = User.objects(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('src.routes.index'))  # if user doesn't exist or password is wrong, reload the page
    set_cookies(email, ["access", "refresh"])
    return redirect(url_for('src.routes.profile')), 200


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
        resp = set_cookies(obj["email"], ["access", "refresh"])
        return resp, 200    


@auth.route('/token', methods=['GET'])
@jwt_refresh_token_required
@jwt_required
def token_check():
    """
    Check if a token is valid
    """
    return "OK", 200


@auth.route('/token/remove', methods=['GET'])
@jwt_refresh_token_required
@jwt_required
def token_drop():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
