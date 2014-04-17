from flask import request
from auth_server.db import models

@app.route('/authenticate', methods=['POST'])
def authenticate():
	email = request.form['email']
	password = request.form['password']

	if models.User.objects(email=email, password=password):
		return True

	return False