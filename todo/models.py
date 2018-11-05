from run import db

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	public_id = db.Column(db.String(50),unique=True)
	name = db.Column(db.String(50))
	password = db.Column(db.String(50))
	admin = db.Column(db.Boolean)

	def __repr__(self):
		return f'Name ={self.name}, admin={self.admin}'

class Todo(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String)
	complete = db.Column(db.Boolean)
	user_id = db.Column(db.Integer)

	def __repr__(self):
		return f'Descr ={self.text}, Complete Status={self.complete}'