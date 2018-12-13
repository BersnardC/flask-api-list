from functools import wraps
from flask import request, jsonify
from flask_login import current_user, logout_user, login_user
from .models import Users
from app import db

def token_required(fn):
    @wraps(fn)
    def required_token(*args, **kwargs):
        access_token = ''
        try:
            access_token = request.headers['token']
        except Exception as e:
            return jsonify({'code':401, 'status':'error', 'message':'Denegated request'})
        try:
            if request.headers['token'] is not None:
                try:
                    if current_user.token == request.headers['token'] :
                        r = fn(*args, **kwargs)
                        return r
                except Exception as e:
                    user = Users.query.filter_by(token=access_token).first()
                    if user:
                        login_user(user)
                        r = fn(*args, **kwargs)
                        return r
                    else:
                        return jsonify({'code':401, 'status':'warning', 'message':'Denegated request'}),401
                else:
                    logout_user()
                    return jsonify({'code':401, 'status':'warning', 'message':'User logout'}), 401
            return ({'code':401, 'status':'error', 'message':'Denegated request'}),401
        except Exception as e:
            return ({'code':401, 'status':'error', 'message':'Denegated request'}),401
    return required_token