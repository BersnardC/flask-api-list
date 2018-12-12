# app/admin/users.py
from flask import request, jsonify
from flask_login import current_user, login_required
from app import db
from . import admin
import time
from ..models import Users

# =========== ALL : GET REQUEST ===========
@admin.route('/users/', methods=['GET'])
def users():
    """
    Get all users on DB
    Url: /users | /users/ -> GET
    """
    try:
        users = Users.query.all()
        out = []
        for user in users :
            user_data = {}
            user_data['id']                = user.id
            user_data['create_at']         = user.created_at.strftime("%d-%m-%Y %H:%M:%S")
            user_data['updated_at']        = user.updated_at.strftime("%d-%m-%Y %H:%M:%S")
            out.append(truck_data)
        return jsonify({
                        'code'                       : 200,
                        'status'                     : 'success',
                        'users'                      : out
                        })
    except Exception as e:
        return jsonify({'code':200, 'status':'error', 'message': 'An error ocurred: %s'%e, 'error':'%s'%e })
