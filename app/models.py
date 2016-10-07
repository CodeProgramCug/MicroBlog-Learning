from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column( db.String(64), index = True, unique = True)
	password = db.Column( db.String(120) )
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def is_authenticated(self):
		return True;

	def is_active(self):
		return True;

	def is_anoymous(self):
		return False;

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def __repr__(self):
		return '<User %r %r>' % (self.username, self.password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column( db.String(140) )
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)