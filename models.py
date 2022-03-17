"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect this database to Flask app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.Text,
                            nullable=False)

    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.Text, 
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user """

        return f"{self.first_name}  {self.last_name}"


class Post(db.Model):
    """ Model for post """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text, 
                      nullable=False,
                      unique=True)

    content = db.Column(db.Text,
                         nullable=False)

    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Show friendly looking version of date"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    

    def __repr__(self):
        return f"<Post {self.id}  {self.title}  {self.content} {self.created_at} {self.user_id} >"



