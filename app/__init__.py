from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.user import UserManager, SQLAlchemyAdapter
from flask.ext.bootstrap import Bootstrap
from config import config

import os

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
from app.models import User
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter)

def create_app(config_name):
	# Setup Flask app and load config.py
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	mail.init_app(app)
	bootstrap.init_app(app)
	user_manager.init_app(app)

	from app.main import blueprint as main_blueprint
	app.register_blueprint(main_blueprint)

	from app.users import blueprint as users_blueprint
	app.register_blueprint(users_blueprint)

	from app.gallery import blueprint as gallery_blueprint
	app.register_blueprint(gallery_blueprint, url_prefix='/gallery')

	return app
