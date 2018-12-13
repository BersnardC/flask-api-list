# app/auth/views.py
import time

from flask import jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from . import auth
from .. import db
from .. models import Users
from .. cache import cache_app
from ..security_service import token_required
from flask import current_app

@auth.route('/auth/login', methods=["POST"])
def login():
	"""
	Login User
	URL: /auth/loginr -> POST
	"""
	print (request.headers)
	# Getting Data
	data = request.json
	try:
		if data['email'] == '' or data['password'] == '':
			return jsonify({'code':200, 'status':'failed', 'message':'Incompleted'})
		user = Users.query.filter_by(email = data['email']).first()
		if user is not None and user.verify_password(data['password']):
			login_user(user)
			out = {}
			out['token']= current_user.token
			out['user_id']= current_user.id
			out['email']= current_user.email
			out['username']= current_user.username
			out['date']= time.strftime("%Y/%m/%d %H:%M:%S")
			return jsonify({'code':200,'status':'success','message' : 'User Logged', 'data':out})
		else :
  			return jsonify({'code':200,'status':'failed','message' : 'Incorrect username or password.'})
	except Exception as e:
		print (e)
		return jsonify({'code':200, 'status':'error', 'message': 'Invalid Data'})

# ============= LOGOUT -> GET =================
@auth.route('/auth/logout', methods=["GET"])
@token_required
@login_required
def logout():
	"""
	Login User
	URL: /auth/logout -> GET
	"""
	print ('Logout')
	print (request.headers['token'])
	try:
		logout_user()
		return jsonify({'code':200,'status':'success','message' : 'User Logout'})
	except Exception as e:
		return jsonify({'code':200,'status':'failed','message' : 'ERROR', 'error':e})
