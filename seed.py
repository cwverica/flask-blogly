from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
john = User(first_name="John", last_name="Smith", img_url="https://images.unsplash.com/photo-1489980557514-251d61e3eeb6?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80")
jacob = User(first_name="Jacob", last_name="Radford", img_url="https://images.unsplash.com/photo-1566492031773-4f4e44671857?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80")
jingleheimerschmit = User(first_name="Lana", last_name="Relday", img_url="https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80")

# Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(jacob)
db.session.add(jingleheimerschmit)

# Commit--otherwise, this never gets saved!
db.session.commit()