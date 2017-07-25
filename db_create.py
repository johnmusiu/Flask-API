mod app import db
from models import *

#Create the database and the database tables
db.create_all()

#insert data
#db.session.add(User(1, "John Musiu", "jmusiu", "jmusiu@a.com", "passs"))

#commit changes
#db.session.commit()