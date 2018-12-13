# app/admin/__init__.py

from flask import Blueprint
from flask_cors import CORS

auth = Blueprint('auth', __name__)

from . import auth_services
print ("aki")
CORS(auth)
