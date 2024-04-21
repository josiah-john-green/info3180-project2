from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

# Model for Users
class User(db.Model):
    __tablename__ = 'users'  # Specify the table name here

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    location = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text, nullable=False)

    profile_photo = db.Column(db.String(255), nullable=False)
    joined_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location 
        self.biography = biography
        self.profile_photo = profile_photo

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
        return f"User('{self.username}', '{self.profile_photo}')"


# Model for Posts
class Post(db.Model):
    __tablename__ = 'posts'  # Specify the table name here


    id = db.Column(db.Integer, primary_key=True)
    
    caption = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define a method to associate each post with its user
    def set_user(self, user):
        self.user_id = user.id

    def __repr__(self):
        return f"Post(id={self.id}, caption='{self.caption}', user_id={self.user_id}, created_on='{self.created_on}')"