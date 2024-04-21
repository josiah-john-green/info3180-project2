from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect 
from app.config import Config
from app.logger import logger  # Import the logger
from flask_login import LoginManager

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Use the logger
logger.info("Flask application initialized.")

# Instantiate CSRF-Protect library here
csrf = CSRFProtect(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import views
