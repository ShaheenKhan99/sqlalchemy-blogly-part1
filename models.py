"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect this database to Flask app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(25),
                            nullable=False)

    last_name = db.Column(db.String(25),
                          nullable=False)

    image_url = db.Column(db.String, 
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)



