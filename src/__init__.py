from datetime import timedelta
import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/authentication")
SERIALIZER_SECRET_KEY = os.getenv("SERIALIZER_SECRET_KEY", '9OLWxND4o83j4K4iuopO')
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'local-secret')


# init mongoenggine, login manager and login_serializer
db = MongoEngine()
login_manager = LoginManager()
login_serializer = URLSafeTimedSerializer(SERIALIZER_SECRET_KEY)
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {
    "host": MONGODB_URL
    }
    app.config["SECRET_KEY"] = SERIALIZER_SECRET_KEY
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    jwt.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

