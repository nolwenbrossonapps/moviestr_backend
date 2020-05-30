from flask import Blueprint, render_template, redirect, url_for, request, current_app as app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, login_manager, login_serializer


auth = Blueprint('auth', __name__)


def get_auth_token(user_obj):
    """
    Encode a secure token for cookie
    """
    data = [user_obj.id, user_obj.password]
    return login_serializer.dumps(data)


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


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('src.routes.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.objects(email=email) 
    if user:  # Email already exist.  
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user.save()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.objects(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    return redirect(url_for('src.routes.profile'))