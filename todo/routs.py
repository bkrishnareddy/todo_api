from todo import app, db, bcrypt
from todo.models import User,Todo
from flask import Flask, request, jsonify, make_response
from flask.json import dumps
import uuid
from jwt import encode, decode
import datetime
from functools import wraps


def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		if not token:
			return jsonify({'message':'token is missing'})
		try:
			data = decode(token,app.config['SECRET_KEY'])
			current_user = User.query.filter_by(public_id=data['public_id']).first()
		except:
			return jsonify({'message':'token is invalid'}), 401			

		return f(current_user,*args, **kwargs)
	return decorated	

@app.route("/")
@app.route("/home")
def home():
	return "<h1>Welcome todo</h1>"

@app.route('/user',methods=['GET'])
@token_required
def get_all_user(current_user):
		users = User.query.all()
		output=[]
		for user in users:
			user_data={}
			user_data['public_id'] = str(user.public_id)
			user_data['name'] = user.name
			user_data['password'] =str(user.password)
			user_data['admin'] = user.admin
			output.append(user_data)
	
		#print(output)				
		return jsonify({"users":output})

@app.route('/user/<public_id>',methods=['GET'])
@token_required
def get_one_user(current_user,public_id):
	user = User.query.filter_by(public_id=public_id).first()
	user_data = {'public_id': str(user.public_id), 'name':user.name, 'password':str(user.password),'admin':user.admin}
	print(user_data)
	return jsonify(user_data)


@app.route('/user',methods=['POST'])
@token_required
def create_user(current_user):
	data = request.get_json()
	password_hash = bcrypt.generate_password_hash(data['password'])
	user = User(public_id=str(uuid.uuid4()), name=data['name'], password = password_hash, admin = False)
	db.session.add(user)
	db.session.commit()
	return jsonify({'message':'New user created'})		

@app.route('/user/<public_id>',methods=['PUT'])
@token_required
def promote_user(current_user,public_id):
	user = User.query.filter_by(public_id=public_id).first() 
	if not user:
		return jsonify({"message":"No user found"})
	else:
		user.admin = True
		db.session.commit()
		return jsonify({"message":"User has been promoted"})	

@app.route('/user/<public_id>',methods=['DELTE'])
@token_required
def delete_user(current_user,public_id):
	user = User.query.filter_by(public_id=public_id).first() 
	if not user:
		return jsonify({"message":"No user found"})
	else:
		db.session.delete(user)
		db.session.commit()
		return jsonify({"message":"User has been Deleted"})

@app.route('/login')
def login():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm-"Login Requeird"'})

	user = User.query.filter_by(name=auth.username).first()
	if not user:
		return make_response('Loggedin User Not found',401,{'WWW-Authenticate':'Basic realm-"No User Exist"'})
	if bcrypt.check_password_hash(user.password,auth.password):
		token = encode({'public_id':user.public_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])	
		return jsonify({'token':token.decode('utf-8')})	
	print(user.password)
	return make_response('Other Errors',401,{'WWW-Authenticate':'Basic realm-"password Missmatch"'})
