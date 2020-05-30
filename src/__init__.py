from datetime import timedelta
import os
from flask import Flask
from flask_mongoengine import MongoEngine
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/authentication")
SECRET_KEY = os.getenv("SECRET_KEY", '9OLWxND4o83j4K4iuopO')


# init mongoenggine, login manager and login_serializer
db = MongoEngine()
login_manager = LoginManager()
login_serializer = URLSafeTimedSerializer(SECRET_KEY)


def create_app():
    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {
    "db": "user",
    "host": MONGODB_URL
    }
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=1)
    
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

