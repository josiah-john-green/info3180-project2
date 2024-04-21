from app import db
from datetime import datetime, timezone

# Model for Users
class User(db.Model):
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

    def __repr__(self):
        return f"User('{self.username}', '{self.profile_photo}')"

