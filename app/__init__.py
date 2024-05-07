
import jwt
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from app.config import Config

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Instantiate CSRF-Protect library here
csrf = CSRFProtect(app)

#Initialize JWT
jwt = JWTManager(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import views
