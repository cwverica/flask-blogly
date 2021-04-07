"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''User model'''

    __tablename__ = "users"

    id = db.Column(db. Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.String(500), nullable=False, unique=True)

    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
