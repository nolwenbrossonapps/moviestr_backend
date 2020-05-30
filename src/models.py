from mongoengine import *
from . import db
from flask_login import UserMixin
from flask import Flask
from flask_login import LoginManager
from flask_login import current_user, login_user, logout_user, login_required


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class User(db.Document):
    email = db.StringField(required=True)
    name = db.StringField(required=True)
    password = db.StringField(required=True)


    