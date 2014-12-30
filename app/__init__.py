from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.user import UserManager, SQLAlchemyAdapter
from flask.ext.bootstrap import Bootstrap

# Setup Flask app and load config.py
app = Flask(__name__)
app.config.from_object('config')

# Initialize Flask extensiones
db = SQLAlchemy(app)				# Initialize Flask-SQLAlchemy
mail = Mail(app)				# Initialize Flask-Mail
bootstrap = Bootstrap(app)			# Initialize Flask-Bootstrap

# Setup Flask-User
from app.users.models import User
db_adapter = SQLAlchemyAdapter(db, User)	# Register the user model
user_manager = UserManager(db_adapter, app)	# Initialize Flask-User

# import main views
from app import views



