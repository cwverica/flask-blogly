from models import *
from app import app

connect_db(app)

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
PostTag.query.delete()
Post.query.delete()
Tag.query.delete()


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

# Do the same with some posts!
johnp1 = Post(title="This is my first post!", content="This is the post that never ends, it goes on and on my friends", user_id=1)
johnp2 = Post(title="I've matured for my next post", content="Not really, blahblahblah \nblahblahblah blahblahblah blahblahblah", user_id=1)
jacobp1 = Post(title="I like dogs", content="I know it's not shocking. I mean who DOESN'T like dogs? I don't trust thos people", user_id=2)
jinglep1 = Post(title="I'm a girl.", content="So I like girly things, like being incredibly intelligent, independent, and powerful.", user_id=3)
jinglep2 = Post(title="Rocking out", content="As a geologist, I like rocks. I collect them, but mostly I just study them", user_id=3)
jinglep3 = Post(title="I grow weary", content="Weary is the name of my favorite ficus. I also grow orchids, tomatos, mint, peppers, and violets", user_id=3)

db.session.add_all([johnp1, johnp2, jacobp1, jinglep1, jinglep2, jinglep3])
db.session.commit()

# Do the same with tags!
tag1 = Tag(name="Fun!")
tag2 = Tag(name="Interesting...")
tag3 = Tag(name="Shocking")

db.session.add_all([tag1, tag2, tag3])
db.session.commit()

# And a couple PostTags!
pt1 = PostTag(post_id=2, tag_id=2)
pt2 = PostTag(post_id=3, tag_id=3)
pt3 = PostTag(post_id=6, tag_id=1)

db.session.add_all([pt1, pt2, pt3])
db.session.commit()