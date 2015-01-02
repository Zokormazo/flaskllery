from app import db
import os
from datetime import datetime

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

	# Relationships
	directories = db.relationship('Directory', backref='album', lazy='dynamic')
	photos = db.relationship('Photo', backref='album', lazy='dynamic')

	# Refresh directories
	def refresh(self):
		for directory in self.directories:
			directory.refresh()

class Directory(db.Model):
	id = db.Column(db.Integer, primary_key = True)

	# Directory information
	path = db.Column(db.String(255), nullable = False)
	album_id = db.Column('album', db.Integer, db.ForeignKey('album.id'), nullable = False)

	# Timestamp information
	added_at = db.Column(db.DateTime, default=db.func.now(), nullable = False)
	refreshed_at = db.Column(db.DateTime)

	# Refresh directory
	def refresh(self):
		for file in os.listdir(self.path):
			if file.endswith(".jpg") or file.endswith(".JPG"):
				path = os.path.join(self.path,file)
				if Photo.query.filter_by(path = path).first() is None:
					photo = Photo( path = path, updated_at = datetime.utcnow(), album = self.album )
					db.session.add(photo)
		db.session.commit()

class Photo(db.Model):
	id = db.Column(db.Integer, primary_key = True)

	# Photo information
	path = db.Column(db.String(255), nullable = False, index = True)
	album_id = db.Column('album', db.Integer, db.ForeignKey('album.id'), nullable = False)
	title = db.Column(db.String(64))
	caption = db.Column(db.String(255))

	# Timestamp information
	added_at = db.Column(db.DateTime, default=db.func.now(), nullable = False)
	updated_at = db.Column(db.DateTime)
