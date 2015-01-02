from app import db

class Album(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	
	# Album information
	title = db.Column(db.String(64), nullable = False)
	description = db.Column(db.String(255))
	author_id = db.Column('author', db.Integer, db.ForeignKey('user.id'), nullable = False)

	# Timestamp information
	created_at = db.Column(db.DateTime, default=db.func.now(), nullable = False)
	timestamp_from = db.Column(db.DateTime)
	timestamp_to = db.Column(db.DateTime)
