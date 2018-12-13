# app/admin/users.py
from flask import request, jsonify
from flask_login import current_user, login_required
from app import db
from . import admin
import time
from ..models import Users
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# =========== ALL : GET REQUEST ===========
@admin.route('/users', methods=['GET'])
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
            user_data['username']          = user.username
            user_data['email']             = user.email
            user_data['create_at']         = user.created_at.strftime("%d-%m-%Y %H:%M:%S")
            user_data['updated_at']        = user.updated_at.strftime("%d-%m-%Y %H:%M:%S")
            out.append(user_data)
        return jsonify({
                        'code'                       : 200,
                        'status'                     : 'success',
                        'users'                      : out
                        })
    except Exception as e:
        return jsonify({'code':200, 'status':'error', 'message': 'An error ocurred: %s'%e, 'error':'%s'%e })

# =========== CREATE : POST REQUEST ==============
@admin.route('/users', methods=["POST"])
def create_user():
    """
        Create an user on DB
        Url: /users | -> POST
    """
    data = request.json
    try:        
        if not data:
            return jsonify({'code':200, 'status':'warning', 'message':'Data required.'})
        if data['email'] == '' or data['username'] == '' or data['password'] == '':
            return jsonify({'code':200, 'status':'warning', 'message':'Data incompleted'})
        # Validate User of current data in not registered on DB
        user = Users.query.filter_by(email = data['email']).first()
        if not user:
            new_user = Users(
                email         = data['email'],
                username      = data['username'],
                password_hash = generate_password_hash(data['password']),
                token         = gen_user_uuid(),
                created_at = time.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
            )
            db.session.add(new_user)
            db.session.commit()
            out = {}
            out['user_id'] = new_user.id
            return jsonify({'code':200, 'status':'success', 'message':'New User has been created.', 'data':out})
        return jsonify({'code':200, 'status': 'warning', 'message': 'User already exist'})
    except Exception as e:
        print (e)
        return jsonify({'code':200, 'status':'error', 'message': 'Invalid Data'})


# ============= UTILS FUNCT TOOLS ==============
def gen_user_uuid():

    u = uuid.uuid4()

    return str(u)