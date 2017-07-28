from app.api import db
from app.models import User, Bucketlist, Activities

#Create the database and the database tables
db.create_all()
