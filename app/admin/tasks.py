# app/admin/tasks.py
from flask import request, jsonify
from flask_login import current_user, login_required
from app import db
from . import admin
import time
from ..models import Users, Tasks
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from ..security_service import *
# =========== ALL : GET REQUEST ===========
@admin.route('/tasks', methods=['GET'])
@token_required
@login_required
def tasks():
    """
    Get all tasks on DB
    Url: /tasks | /tasks/ -> GET
    """
    try:
        tasks = Tasks.query.filter_by(user_id = current_user.id).all()
        out = []
        for task in tasks :
            task_data = {}
            status_name = 'Pending'
            if task.status_id == 1:
                status_name = 'Finish'
                pass
            task_data['id']                = task.id
            task_data['title']             = task.title
            task_data['email']             = task.description
            task_data['status_id'] 		   = task.status_id
            task_data['status_name']       = status_name
            task_data['user_id'] 		   = task.user_id 
            task_data['create_at']         = task.created_at.strftime("%d-%m-%Y %H:%M:%S")
            task_data['updated_at']        = task.updated_at.strftime("%d-%m-%Y %H:%M:%S")
            out.append(task_data)
        return jsonify({
                        'code'                       : 200,
                        'status'                     : 'success',
                        'tasks'                      : out
                        })
    except Exception as e:
        return jsonify({'code':200, 'status':'error', 'message': 'An error ocurred: %s'%e, 'error':'%s'%e })

# =========== CREATE : POST REQUEST ==============
@admin.route('/tasks', methods=["POST"])
@token_required
@login_required
def create_task():
    """
        Create an task on DB
        Url: /tasks | -> POST
    """
    data = request.json
    try:        
        if not data:
            return jsonify({'code':200, 'status':'warning', 'message':'Data required.'})
        if data['title'] == '' or data['description'] == '':
            return jsonify({'code':200, 'status':'warning', 'message':'Data incompleted'})
        new_task = Tasks(
            title         = data['title'],
            description   = data['description'],
            status_id 	  = 0,
            user_id       = current_user.id,
            created_at = time.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(new_task)
        db.session.commit()
        out = {}
        out['task_id'] = new_task.id
        return jsonify({'code':200, 'status':'success', 'message':'New Task has been created.', 'data':out})
    except Exception as e:
        print (e)
        return jsonify({'code':200, 'status':'error', 'message': 'Invalid Data'})

# =========== UPDATE : PUT REQUEST ==============
@admin.route('/tasks/<int:id>', methods=["PUT"])
@token_required
@login_required
def update_task(id):
    task = Tasks.query.filter_by(user_id = current_user.id, id = id).first()
    if task:
        task.status_id = 1
        db.session.commit()
        return jsonify({'code':200, 'status':'success','message':'Updated successfull'})
    else:
        return jsonify({'code':200, 'status':'warning','message':'Task not foud'})