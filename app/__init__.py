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

# Setup logging
import logging
from logging.handlers import RotatingFileHandler

# Log INFO to a file
file_handler = RotatingFileHandler('log/flaskllery.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Log ERROR to mail in production environments
if not app.debug:
	from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
	from logging.handlers import SMTPHandler
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials = (MAIL_USERNAME, MAIL_PASSWORD)
	mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), MAIL_DEFAULT_SENDER, ADMINS, 'Flaskllery failure', credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flaskllery startup')

# import error views
from app import errors

# import user views
from app.users import views

# import gallery views
from app.gallery import views



