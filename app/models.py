#imports db from our app.py
from app.api import db
#import hashing library
import bcrypt


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(80), nullable = False)
	email = db.Column(db.String(30), nullable = False)
	password_hash = db.Column(db.String(128), nullable = False)

	def __init__(self, name, email, password_hash):
		# self.id = id
		self.name = name
		self.email = email
		self.password_hash = password_hash

	def password_hashing(self, password):
		''' password hashing method'''
		return bcrypt.hashpw(password, bcrypt.gensalt())

	def verify_password(self, password, password_hash):
		'''verifies that hash for password entered matches stored hash, returns True or False'''
		if bcrypt.hashpw(password, password_hash) == password_hash:
			return True
		else:
			return False 

	# def post(self, email, password, name):
	# 	hashpass = password_hashing(password)
	# 	user = User(name, email, hashpass)
	# 	db.session.add(user)
	# 	db.session.commit()

	# def auth_user(self, username, password):
	# 	""""""

	# def __repr__(self):
		# return '()'.format(self.title)


class Bucketlist(db.Model):
	__tablename__ = 'bucketlists'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(80), nullable = False)
	description = db.Column(db.String(254), nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship(User)

	def __init__(self, title, description, user_id):
		# self.id = id
		self.title = title
		self.description = description
		self.user_id = user_id

	@staticmethod
	def get_all():
		''' to return all bucketlists '''
		return Bucketlist.query.all()

	def delete(self, id):
		''' deletes a bucketlist given a user '''
		query1 = db.session.delete(self)
		res = db.session.commit()
		if res and query1:
			return True
		else:
			return False

	def update(self, title, desc):
		''' updates a db bucketlist '''
		self.title = title
		self.description = desc
		query1 = db.session.add(self)
		res = db.session.commit()
		if res and query1:
			return True
		else:
			return False

	def __repr__(self):
		return "<Bucketlist: {}>".format(self.title)
		
class Activities(db.Model):
	__tablename__ = 'activities'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(80), nullable = False)
	description = db.Column(db.String(254), nullable = False)
	place = db.Column(db.String(50))
	people = db.Column(db.String(254))
	bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

	bucketlist = db.relationship(Bucketlist)

	def __init__(self, title, description, bucketlist_id, place="", people=""):
		self.title = title
		self.description = description
		self.place = place
		self.people = people
		self.bucketlist_id = bucketlist_id
	
	@staticmethod
	def get_all():
		''' to return all activities '''
		return Activities.query.all()

	def delete(self, id):
		''' deletes an activity given an activity id '''
		db.session.delete(self)
		db.session.commit()

	def update(self, title, desc):
		''' updates an activity '''
		self.title = title
		self.description = desc
		db.session.add(self)
		db.session.commit()
	
	def __repr__(self):
		return "<Activity: {}>".format(self.title)
