# app/services_register.py

from flask import jsonify

def inject_service_uri(app):

	#from .auth import auth as auth_blueprint
	#app.register_blueprint(auth_blueprint)

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint)

	@app.errorhandler(403)
	def forbidden(error):
	    return jsonify(code="403")

	@app.errorhandler(404)
	def page_not_found(error):
	    return jsonify(code="404")

	@app.errorhandler(500)
	def internal_server_error(error):
	    return jsonify(code="500")
