from app import db
from flask.ext.user import UserMixin
import os
from datetime import datetime
from config import basedir
from flask import current_app
from PIL import Image
from util import sizeof_fmt
import json

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
	roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
	albums = db.relationship('Album', backref='author', lazy='dynamic', cascade='save-update, merge, delete, delete-orphan')
	photos = db.relationship('Photo', backref='author', lazy='dynamic', cascade='save-update, merge, delete, delete-orphan')

	def can_edit(self,element):
		''' return wether can edit element or not '''
		if self.has_roles('admin'):
			return True
		if self.has_roles('poweruser') and self == element.author:
			return True

# Role data model
class Role(db.Model):
	id = db.Column(db.Integer(), primary_key = True)

	name = db.Column(db.String(50), unique=True)

# UserRole data model
class UserRoles(db.Model):
	id = db.Column(db.Integer(), primary_key = True)

	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

class Album(db.Model):
	id = db.Column(db.Integer, primary_key = True)

	# Album information
	title = db.Column(db.String(64))
	description = db.Column(db.String(255))
	author_id = db.Column('author', db.Integer, db.ForeignKey('user.id'), nullable = False)

	# Timestamp information
	created_at = db.Column(db.DateTime, default=db.func.now(), nullable = False)
	timestamp_from = db.Column(db.DateTime)
	timestamp_to = db.Column(db.DateTime)

	# Relationships
	directories = db.relationship('Directory', backref='album', lazy='dynamic', cascade='merge, save-update, delete, delete-orphan')

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

	# Relationships
	photos = db.relationship('Photo', backref='directory', lazy='dynamic', cascade='merge, save-update, delete, delete-orphan')

	def refresh(self):
		''' Refresh Directory
		'''
		for file in os.listdir(self.path):
			file_path = os.path.join(self.path,file)
			if os.path.isfile(file_path):
				try:
					im = Image.open(file_path)
					photo = Photo.query.filter_by(path = file_path).first()
					if photo is None:
						photo = Photo( path = file_path, updated_at = datetime.utcnow(), directory_id = self.id, author_id = self.album.author.id )
					photo.update()

				except IOError:
					pass

		self.refreshed_at = datetime.utcnow()
		db.session.add(self)
		db.session.commit()

class Photo(db.Model):
	id = db.Column(db.Integer, primary_key = True)

	# Photo information
	path = db.Column(db.String(255), nullable = False, index = True)
	directory_id = db.Column('directory', db.Integer, db.ForeignKey('directory.id'), nullable = False)
	author_id = db.Column('author', db.Integer, db.ForeignKey('user.id'), nullable = False)
	title = db.Column(db.String(64))
	caption = db.Column(db.String(255))
	size = db.Column(db.Integer)
	width = db.Column(db.Integer)
	height = db.Column(db.Integer)
	format = db.Column(db.String(5))
	mode = db.Column(db.String(5))

	# Timestamp information
	added_at = db.Column(db.DateTime, default=db.func.now(), nullable = False)
	updated_at = db.Column(db.DateTime)

	# Relationships
	exif_data = db.relationship('ExifData', backref='photo', lazy='joined', cascade='merge, save-update, delete, delete-orphan', uselist=False)

	def update(self):
		''' Update image info from file
		'''
		im = Image.open(self.path)
		self.width = im.size[0]
		self.height = im.size[1]
		self.format = im.format
		self.mode = im.mode
		self.size = os.path.getsize(self.path)
		self.updated_at = datetime.utcnow()
		db.session.add(self)

		# get exifdata if exists
		if hasattr( im, '_getexif' ):
			exif_data = im._getexif()
			if exif_data != None:
				write = False
				if self.exif_data:
					exif = self.exif_data
				else:
					exif = ExifData(photo = self)
				try:
					exif.taken_at = datetime.strptime(exif_data[36867], '%Y:%m:%d %H:%M:%S')
					write = True
				except:
					pass
				try:
					exif.camera_make = exif_data[271]
					write = True
				except:
					pass
				try:
					exif.camera_model = exif_data[272]
					write = True
				except:
					pass
				try:
					exif.orientation = exif_data[274]
					write = True
				except:
					pass
				try:
					exif.focal_length = '[' + str(exif_data[37386][0]) + ',' + str(exif_data[37378][1]) + ']'
					write = True
				except:
					pass
				try:
					exif.aperture = '[' + str(exif_data[37378][0]) + ',' + str(exif_data[37378][1]) + ']'
					write = True
				except:
					pass
				try:
					if exif_data[34855].isdigit():
						exif.iso = exif_data[34855]
						write = True
				except:
					pass
				if write:
					db.session.add(exif)


	def thumbnail_path(self, width, height):
		''' Return thumbnail's path
		Generates thumbnail if needed
		'''
		cache_dir = os.path.join(current_app.config['FLASKLLERY_CACHE_DIR'] + '/' + str(width) + 'x' + str(height))
		thumb_path = os.path.join(cache_dir, str(self.id) + '.jpg')
		if not os.path.exists(thumb_path):
			self._generate_thumb(width,height)
		return thumb_path

	def _generate_thumb(self, width, height):
		''' Generate specified size thumbnail
		'''
		cache_dir = os.path.join(current_app.config['FLASKLLERY_CACHE_DIR'], str(width) + 'x' + str(height))
		if not os.path.isdir(cache_dir):
                        os.mkdir(cache_dir)
		target = os.path.join(cache_dir, str(self.id) + '.jpg')
		im = Image.open(self.path)
		im.thumbnail((width, height), Image.ANTIALIAS)
		im.save(target, "JPEG")

	def filename(self):
		''' return filename without directory
		'''
		return os.path.basename(self.path)

	def json(self):
		''' Return photo info in json
		'''
		json_photo = {
			'id' : self.id,
			'path' : self.path,
			'title' : self.title,
			'caption' : self.caption,
			'size' : sizeof_fmt(self.size),
			'width' : self.width,
			'height' : self.height,
			'format' : self.format,
			'mode' : self.mode,
			'added_at' : self.added_at,
			'updated_at' : self.updated_at,
			'filename' : self.filename()
		}
		return json_photo

class ExifData(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	photo_id = db.Column('photo', db.Integer, db.ForeignKey('photo.id'), nullable = False)

	# exif information
	taken_at = db.Column(db.DateTime)	# exif tag 36867
	camera_make = db.Column(db.String(50))	# exit tag 271
	camera_model = db.Column(db.String(50))	# exif tag 272
	orientarion = db.Column(db.Integer)	# exif tag 274
	focal_length = db.Column(db.String(20))	# exif tag 37386
	aperture = db.Column(db.String(20))	# exif tag 37378
	iso = db.Column(db.Integer)		# exif tag 34855
	latitude = db.Column(db.String(255))	# exif tag 34853.2
	longitude = db.Column(db.String(255))	# exif tag 34853.4

	def json(self):
		''' Return exif data in json
		'''
		json_exif = {
			'id' : self.id,
			'photo_id' : self.photo_id
		}
		if hasattr(self, 'taken_at') and self.taken_at is not None:
			json_exif['taken_at'] = self.taken_at
		if hasattr(self, 'camera_make') and self.camera_make is not None:
			json_exif['camera_make'] = self.camera_make
		if hasattr(self, 'camera_model') and self.camera_model is not None:
			json_exif['camera_model'] = self.camera_model
		if hasattr(self, 'orientation') and self.orientation is not None:
			json_exif['orientation'] = self.orientation
		if hasattr(self, 'focal_length') and self.focal_length is not None:
			focal_length = json.loads(self.focal_length)
			json_exif['focal_length'] = focal_length
		if hasattr(self, 'aperture') and self.aperture is not None:
			aperture = json.loads(self.aperture)
			json_exif['aperture'] = aperture
		if hasattr(self, 'iso') and self.iso is not None:
			json_exif['iso'] = self.iso
		if hasattr(self, 'latitude') and self.latitude is not None:
			json_exif['latitude'] = self.latitude
		if hasattr(self, 'longitude') and self.longitude is not None:
			json_exif['longitude'] = self.longitude
		return json_exif
