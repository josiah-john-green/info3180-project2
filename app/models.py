from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False) 
    location = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.String(700), nullable=False)
    profile_photo = db.Column(db.String(255), nullable=False)
    joined_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo, joined_on):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = joined_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    caption = db.Column(db.String(700))
    photo = db.Column(db.String(255))
    user_id = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, caption, photo, user_id, created_on):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id
        self.created_on = created_on


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id


class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    follower_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id