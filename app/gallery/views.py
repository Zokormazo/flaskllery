from flask import render_template, flash, redirect, url_for, send_file, abort, Response, jsonify, current_app
from flask.ext.user import login_required, roles_required, current_user
from flask.ext.babel import gettext
from app.models import Album, Directory, Photo
from app.decorators import can_edit
from app.gallery.forms import NewAlbumForm, EditAlbumForm, AddDirectoryForm, EditPhotoForm
from app import db
from PIL import Image
from . import blueprint
import json
import StringIO

@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/index/<int:page>')
@login_required
def index(page=1):
	'''
	Show gallery main page: album list
	'''
	albums = Album.query.paginate(page, current_app.config['FLASKLLERY_ALBUMS_PER_PAGE'], False)
	return render_template('index.html', albums=albums)

@blueprint.route('/album/new', methods=['GET', 'POST'])
@roles_required(['admin','poweruser'])
def new_album():
	'''
	New album
	'''
	form = NewAlbumForm()
	if form.validate_on_submit():
		album = Album(title=form.title.data, description=form.description.data, author=current_user)
		db.session.add(album)
		db.session.commit()
		flash(gettext('New album \'%(album)s\' added', album=album.title))
		return redirect(url_for('.index'))
	return render_template('new_album.html', form=form)

@blueprint.route('/album/view/<int:id>')
@blueprint.route('/album/view/<int:id>/<int:page>')
@login_required
def album(id, page=1):
	'''
	View album
	'''
	album = Album.query.get_or_404(id)
	photos = Photo.query.join(Directory).filter(Directory.album_id == album.id).paginate(page, current_app.config['FLASKLLERY_PHOTOS_PER_PAGE'], False)
	return render_template('album.html', album=album, photos=photos)

@blueprint.route('/album/edit/<int:id>', methods=['GET', 'POST'])
@can_edit(Album)
def edit_album(id):
	'''
	Edit album
	'''
	form = EditAlbumForm(prefix='form1')
	directory_form = AddDirectoryForm(prefix='form2')
	album = Album.query.get_or_404(id)
	if form.validate_on_submit() and form.submit.data:
		album.title = form.title.data
		album.description = form.description.data
		db.session.add(album)
		db.session.commit()
		flash(gettext('\'%(album)s\' album edited', album=album.title))
		return redirect(url_for('.album', id=album.id))
	if directory_form.validate_on_submit() and directory_form.submit.data:
		directory = Directory(album=album, path=directory_form.path.data)
		db.session.add(directory)
		db.session.commit()
		flash(gettext('\%(directory)s\' directory added to \'%(album)s\'', directory=directory.path, album=album.title))
		return redirect(url_for('.edit_album', id=album.id))

	form.title.data = album.title
	form.description.data = album.description
	return render_template('edit_album.html', album=album, form=form, directory_form = directory_form)

@blueprint.route('/album/delete/<int:id>')
@can_edit(Album)
def delete_album(id):
	'''
	Delete album
	'''
	album = Album.query.get_or_404(id)
	db.session.delete(album)
	db.session.commit()
	flash(gettext('\'%(album)s\' album deleted', album=album.title))
	return redirect(url_for('.index'))

@blueprint.route('/album/refresh/<int:id>')
@can_edit(Album)
def refresh_album(id):
	'''
	Refresh album: check all directories tracked by album for new photos & changes
	'''
	album = Album.query.get_or_404(id)
	album.refresh()
	flash(gettext('\'%(album)s\' album refreshed', album=album.title))
	return redirect(url_for('.album', id=album.id))

@blueprint.route('/directory/refresh/<int:id>')
@can_edit(Directory)
def refresh_directory(id):
	'''
	Refresh directory: check directory for new photos & changes
	'''
	directory = Directory.query.get_or_404(id)
	directory.refresh()
	flash(gettext('Directory \'%(directory)s\' refreshed', directory=directory.path))
	return redirect(url_for('.edit_album', id=directory.album_id))

@blueprint.route('/directory/delete/<int:id>')
@can_edit(Directory)
def delete_directory(id):
	'''
	Delete directory
	'''
	directory = Directory.query.get_or_404(id)
	album = directory.album
	db.session.delete(directory)
	db.session.commit()
	flash(gettext('\'%(directory)s\' directory deleted from \'%(album)s\'', directory=directory.path, album=album.title))
	return redirect(url_for('.edit_album', id=album.id))

@blueprint.route('/photo/view/<int:id>')
@login_required
def photo(id):
	'''
	Show photo
	'''
	photo = Photo.query.get_or_404(id)
	return render_template('photo.html', photo=photo)

@blueprint.route('/photo/update/<int:id>')
@can_edit(Photo)
def update_photo(id):
	'''
	Update photo information
	'''
	photo = Photo.query.get_or_404(id)
	photo.update()
	db.session.commit()
	flash(gettext('\'%(photo)s\' updated on \'%(album)s\'', photo=photo.path, album=photo.directory.album.title))
	return redirect(url_for('.photo', id=photo.id))

@blueprint.route('/photo/edit/<int:id>', methods=['GET', 'POST'])
@can_edit(Photo)
def edit_photo(id):
	''' Edit photo title & caption '''
	form = EditPhotoForm()
	photo = Photo.query.get_or_404(id)
	if form.validate_on_submit():
		photo.title = form.title.data
		photo.caption = form.caption.data
		db.session.add(photo)
		db.session.commit()
		flash(gettext('Photo \'%(photo)s\' edited', photo=photo.path))
		return redirect(url_for('.photo', id=photo.id))
	form.title.data = photo.title
	form.caption.data = photo.caption
	return render_template('edit_photo.html', photo=photo, form=form)

@blueprint.route('/photo/delete/<int:id>')
@can_edit(Photo)
def delete_photo(id):
	'''
	Delete photo
	'''
	photo = Photo.query.get_or_404(id)
	db.session.delete(photo)
	db.session.commit()
	return redirect(url_for('.album', id=photo.album_id))

@blueprint.route('/photo/raw/<int:id>')
@login_required
def photo_file(id):
	'''
	Return raw photo file
	'''
	photo = Photo.query.get_or_404(id)
	return send_file(photo.path)

@blueprint.route('/photo/thumb/<int:id>/<int:width>x<int:height>')
@login_required
def photo_thumbnail(id, width, height):
	'''
	Return photo thumbnail of given dimension
	'''
	photo = Photo.query.get_or_404(id)
	return send_file(photo.thumbnail_path(width,height))

@blueprint.route('/json/album/<int:id>/photos')
@login_required
def json_album_photos(id):
	'''
	Returns an array of photo ids that belongs to Album
	'''
	photos = Photo.query.with_entities(Photo.id).join(Directory).filter(Directory.album_id == id).all()
	if photos:
		return json.dumps(zip(*photos))[1:-1]
	else:
		Abort(404)

@blueprint.route('/json/photo/<int:id>')
@login_required
def json_photo(id):
	'''
	Returns photo info in json format
	'''
	photo = Photo.query.get_or_404(id)
	return jsonify(photo.json())

@blueprint.route('/json/photo/<int:id>/exif')
@login_required
def json_photo_exif(id):
	'''
	Returns exif info in json format
	'''
	photo = Photo.query.get_or_404(id)
	if photo.exif_data:
		return jsonify(photo.exif_data.json())
	else:
		abort(404)
