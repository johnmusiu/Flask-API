#imports db from our app.py
from app import db


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(Integer, primary_key = True)
	name = db.Column(String(80), nullable = False)
	email = db.Column(String(30), nullable = False)
	password = db.Column(String(30), nullable = False)

	def __init__(self, id, name, username, email, password):
		self.id = id
		self.name =name
		self.email = email
		self.password = password

	# def __repr__(self):
		# return '()'.format(self.title)



class Bucketlist(db.Model):
	__tablename__ = 'bucketlists'
	id = db.Column(Integer, primary_key = True)
	title = db.Column(String(80), nullable = False)
	description = db.Column(String(254), nullable = False)
	user_id = db.Column(Integer, ForeignKey('users.id'))

	user = relationship(User)

	def __init__(self, id, title, description, user_id):
		self.id = id
		self.title = title
		self.description = description
		self.user_id = user_id


class Activities(db.Model):
	__tablename__ = 'activities'
	id = db.Column(Integer, primary_key = True)
	title = db.Column(String(80), nullable = False)
	description = db.Column(String(254), nullable = False)
	place = db.Column(String(50))
	people = db.Column(String(254))
	bucketlist_id = db.Column(Integer, ForeignKey('bucketlists.id'))

	bucketlist = relationship(Bucketlist)

	def __init__(self, id, title, description, place, people, bucketlist_id):
		self.id = id
		self.title = title
		self.description = description
		self.place = place
		self.people = people
		self.bucketlist_id = bucketlist_id

#add to bottom
#adds classes as tables to database
Base.metadata.create_all(engine)