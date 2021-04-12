"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User model'''

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.String(500), nullable=False, unique=True)

    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    '''Post model'''

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', cascade="all", backref='posts')

class Tag(db.Model):
    '''Tag Model'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='PostTag', backref='tags')

class PostTag(db.Model):
    '''Post to Tag relation model'''

    __tablename__ = 'post_tags'

    post_id = db.Column(db.ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
    tag_id = db.Column(db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)

    posts = db.relationship('Post', backref='post_tags')
    tags = db.relationship('Tag', backref='post_tags')