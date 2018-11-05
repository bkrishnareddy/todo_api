from todo import app,db
from flask import Flask, request, jsonify
from bcrypt import hashpw
import uuid

@app.route("/")
@app.route("/home")
def home():
	return "<h1>Welcome todo</h1>"

@app.route('/user',methods=['GET'])
def get_all_user():
	return ''

@app.route('/user/<user_id>',methods=['GET'])
def get_one_user():
	return ''

@app.route('/user',methods=['POST'])
def create_user():
	data = request.get_json()
	

	password_hash = bcrypt.hashpw(data['password'],bcrypt.gensalt(14))
	user = User(public_id=str(uuid.uuid4()), name=data['name'], password = password_hash, admin = False)
	db.session.add(user)
	db.session.commit()
	return ''		

@app.route('/user/<user_id>',methods=['PUT'])
def promote_user():
	return ''	

@app.route('/user/<user_id>',methods=['DELTE'])
def delete_user():
	return ''		