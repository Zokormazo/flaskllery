from flask import render_template, flash, redirect, url_for, g, send_file, abort, Response
from flask.ext.user import login_required
from app.gallery.models import Album, Directory, Photo
from app.gallery.forms import NewAlbumForm, EditAlbumForm, AddDirectoryForm
from app import app, db
from config import FLASKLLERY_ALBUMS_PER_PAGE
from PIL import Image
import StringIO

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
def index(page=1):
	albums = Album.query.paginate(page, FLASKLLERY_ALBUMS_PER_PAGE, False)
	return render_template('index.html', albums=albums)

@app.route('/album/new', methods=['GET', 'POST'])
@login_required
def new_album():
	form = NewAlbumForm()
	if form.validate_on_submit():
		album = Album(title=form.title.data, description=form.description.data, author=g.user)
		db.session.add(album)
		db.session.commit()
		flash('New album \'' + album.title + '\' added')
		return redirect(url_for('index'))
	return render_template('new_album.html', form=form)

@app.route('/album/view/<int:id>')
@login_required
def album(id):
	album = Album.query.get(id)
	return render_template('album.html', album=album)

@app.route('/album/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_album(id):
	form = EditAlbumForm(prefix='form1')
	directory_form = AddDirectoryForm(prefix='form2')
	album = Album.query.get(id)
	if form.validate_on_submit() and form.submit.data:
		album.title = form.title.data
		album.description = form.description.data
		db.session.add(album)
		db.session.commit()
		flash('Album \'' + album.title + '\' edited')
		return redirect(url_for('album', id=album.id))
	if directory_form.validate_on_submit() and directory_form.submit.data:
		directory = Directory(album=album, path=directory_form.path.data)
		db.session.add(directory)
		db.session.commit()
		flash('\'' + directory.path + '\' directory added to \'' + album.title + '\'')
		return redirect(url_for('edit_album', id=album.id))

	form.title.data = album.title
	form.description.data = album.description
	return render_template('edit_album.html', album=album, form=form, directory_form = directory_form)

@app.route('/album/delete/<int:id>')
@login_required
def delete_album(id):
	album = Album.query.get(id)
	db.session.delete(album)
	db.session.commit()
	flash('\'' + album.title + '\' album deleted')
	return redirect(url_for('index'))

@app.route('/album/refresh/<int:id>')
@login_required
def refresh_album(id):
	album = Album.query.get(id)
	album.refresh()
	flash('\'' + album.title + '\' album refreshed')
	return redirect(url_for('album', id=album.id))

@app.route('/directory/refresh/<int:id>')
@login_required
def refresh_directory(id):
	directory = Directory.query.get(id)
	directory.refresh()
	flash('Directory \'' + directory.path + '\' refreshed')
	return redirect(url_for('edit_album', id=directory.album_id))

@app.route('/directory/delete/<int:id>')
@login_required
def delete_directory(id):
	directory = Directory.query.get(id)
	album = directory.album
	db.session.delete(directory)
	db.session.commit()
	flash('\'' + directory.path + '\' directory deleted from \'' + album.title + '\'')
	return redirect(url_for('edit_album', id=album.id))

@app.route('/photo/raw/<int:id>')
def photo_file(id):
	photo = Photo.query.get(id)
	return send_file(photo.path)

@app.route('/photo/thumb/<int:id>/<int:width>x<int:height>')
@login_required
def photo(id, width, height):
	photo = Photo.query.get(id)
	return photo.thumb(width,height)
