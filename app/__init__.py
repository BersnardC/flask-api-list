# app/__init__.py

import os
import logging

# third-party imports
from flask import session
from flask import Flask, abort, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from flask_cors import CORS

from datetime import timedelta
db = SQLAlchemy()
login_manager = LoginManager()

from flask_restful import Api
# local imports
from config import app_config
from app.cache import cache_app
from flask_cors import CORS

def create_app(config_name):

    if config_name == "production":
        app = Flask(__name__)
        CORS(app)
        app.config.from_object(app_config[config_name])
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
        session.permanent = True
        SECRET_KEY = os.getenv('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
        PICTURES_DIR = os.getenv('PICTURES_DIR')

        app.config.update(
            SECRET_KEY=SECRET_KEY,
            SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
            PICTURES_DIR=PICTURES_DIR
        )

    else:
        UPLOAD_FOLDER = os.getcwd()
        app = Flask(__name__, instance_relative_config=True)
        CORS(app)
        app.config.from_object(app_config[config_name])
        app.secret_key = 'my_secret_key'
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
        SECRET_KEY = os.getenv('SECRET_KEY')
        
    role_admin = ""; # Global variable for admin Menu Role
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    cors = CORS(app, resources={r"/auth/*": {"origins": "*"}})
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)
    #cache_app.init_app(app)

    api = Api(app)

    from app import models

    # Register Service Blueprint for ULR's API | and response HTTP Server
    from .services_register import inject_service_uri
    inject_service_uri(app)

    return app
