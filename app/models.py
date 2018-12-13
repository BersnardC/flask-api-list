# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

class AlembicVersion (db.Model):
    __tablename__ = "alembic_version"
    version_num = db.Column('version_num', db.String, primary_key = True)

class Users (UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column('email', db.String)
    username = db.Column('username', db.String)
    password_hash = db.Column('password_hash', db.String)
    token = db.Column('token', db.String)
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)

    @property
    def password(self):

        """
        Prevents password from being accessed
        """

        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):

        """
        Sets a password to a hashed password
        """

        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):

        """
        Checks if hashed password matches actual password
        """

        return check_password_hash(self.password_hash, password)

    def __repr__(self):

        return '<Users: {0}>'.format(self.username)
# Set up user_loader
@login_manager.user_loader
def load_user(user_id):

    return Users.query.get(int(user_id))

class Tasks (db.Model):
    __tablename__ = "tasks"
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column('title', db.String)
    description = db.Column('description', db.String)
    status_id = db.Column('status_id', db.Integer)
    created_at = db.Column('created_at', db.DateTime)
    updated_at = db.Column('updated_at', db.DateTime)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', foreign_keys=user_id)
# end
