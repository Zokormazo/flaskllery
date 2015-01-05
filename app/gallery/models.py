from app import db
import os
from datetime import datetime
from config import FLASKLLERY_CACHE_DIR
from flask import send_file
from PIL import Image

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
	photos = db.relationship('Photo', backref='photos', lazy='dynamic')

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
		self.refreshed_at = datetime.utcnow()
		db.session.add(self)
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

	# Get specified size thumbnail
	def thumb(self, width, height):
		cache_dir = os.path.join(FLASKLLERY_CACHE_DIR, str(width) + 'x' + str(height))
		thumb_path = os.path.join(cache_dir, str(self.id) + '.jpg')
		if not os.path.exists(thumb_path):
			self._generate_thumb(width,height)
		return send_file(thumb_path)

	# Generate specified size thumb
	def _generate_thumb(self, width, height):
		cache_dir = os.path.join(FLASKLLERY_CACHE_DIR, str(width) + 'x' + str(height))
		if not os.path.isdir(cache_dir):
                        os.mkdir(cache_dir)
		target = os.path.join(cache_dir, str(self.id) + '.jpg')
		im = Image.open(self.path)
		im.thumbnail((width, height), Image.ANTIALIAS)
		im.save(target, "JPEG")
