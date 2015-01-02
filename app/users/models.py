from app import db
from flask.ext.user import UserMixin

# User data model
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)

	# User authentication information
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')
	reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

	# User email information
	email = db.Column(db.String(255), nullable=False, unique=True)
	confirmed_at = db.Column(db.DateTime())

	# User activity information
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
	registered_at = db.Column(db.DateTime, default=db.func.now())
	last_seen = db.Column(db.DateTime)

	# Relationships
	albums = db.relationship('Album', backref='author', lazy='dynamic')
