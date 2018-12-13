# app/admin/__init__.py

from flask import Blueprint
from flask_cors import CORS

admin = Blueprint('admin', __name__)

from . import users, tasks

CORS(admin)
