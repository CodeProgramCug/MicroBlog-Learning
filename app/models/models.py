from app import db
from flask import jsonify

class User(db.Document):
	username = db.StringField(unique = True)
	password = db.StringField()

	def is_authenticated(self):
		#if self.objects().first():
		return True

	def is_active(self):
		return True

	def is_anoymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def to_json(self):
		return {"name" : self.username,
				"email": self.password}


class BlogPost(db.Document):
	title = db.StringField(unique = True)
	timestamp = db.DateTimeField()
	author = db.StringField() # user_id 
	body = db.StringField()
	tags = db.StringField()

	def to_json(self):
		print self.id
		return {'id'	: str(self.id),
				'title' : self.title,
				'author': self.author,
				'body'	: self.body,
				'timestamp' : self.timestamp}

	def __repr__(self):
		return '<Post %r>' % (self.body)

